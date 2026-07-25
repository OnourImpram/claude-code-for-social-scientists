"""Safe cross-client installer for the Social Scientist skill library.

The Python package bundles one canonical skill source rendered from the repository's
``.claude/skills`` tree. The CLI installs that same reviewed content into the
discovery paths used by Claude Code and Codex. Installation state is recorded in a
manifest so upgrades and removals can distinguish project-owned files from user
files and protect local modifications.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
import re
import shutil
import sys
import tempfile
import uuid
from collections.abc import Iterator, Mapping
from dataclasses import dataclass, field
from datetime import datetime, timezone
from importlib import resources
from pathlib import Path
from typing import TypedDict, cast

from . import __version__

SKILLS_PACKAGE = "social_cc_plugin"
SKILLS_DIRNAME = "skills"
CONTROL_DIRNAME = ".social-cc"
MANIFEST_FILENAME = "manifest.json"
BACKUPS_DIRNAME = "backups"
MANIFEST_SCHEMA_VERSION = 1

CLIENT_PATHS: dict[str, tuple[str, str]] = {
    "claude-code": (".claude", "skills"),
    "codex": (".agents", "skills"),
}
CLIENT_TOOLS: dict[str, str] = {
    "claude-code": "claude",
    "codex": "codex",
}
SKILL_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class SkillRecord(TypedDict):
    """Manifest record for one installed skill."""

    digest: str
    installed_at: str


class InstallManifest(TypedDict):
    """On-disk ownership manifest."""

    schema_version: int
    package: str
    package_version: str
    client: str
    scope: str
    skills: dict[str, SkillRecord]


@dataclass(frozen=True)
class TargetSpec:
    """A client-specific installation target."""

    client: str
    scope: str
    root: Path


@dataclass
class OperationResult:
    """Counts produced by an installation or removal operation."""

    changed: int = 0
    skipped: int = 0
    protected: int = 0
    backups: list[Path] = field(default_factory=list)


@dataclass(frozen=True)
class SkillDiff:
    """Observed state for one skill."""

    name: str
    status: str
    detail: str


class InstallerError(RuntimeError):
    """Raised when an unsafe or invalid installation state is detected."""


def _emit(message: str) -> None:
    """Write a line of user-facing output. CLI output is part of the interface."""

    print(message)


@contextlib.contextmanager
def _bundled_source() -> Iterator[Path | None]:
    """Yield a real path to bundled skills, or ``None`` when the bundle is absent."""

    root = resources.files(SKILLS_PACKAGE).joinpath(SKILLS_DIRNAME)
    if not root.is_dir():
        yield None
        return
    with resources.as_file(root) as real:
        yield Path(real)


def _utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _validate_skill_name(name: str) -> None:
    if not SKILL_NAME_PATTERN.fullmatch(name):
        raise InstallerError(f"unsafe skill directory name: {name!r}")


def _assert_regular_tree(root: Path) -> None:
    """Reject symlinks and non-regular entries in a skill tree."""

    if root.is_symlink():
        raise InstallerError(f"skill directory must not be a symlink: {root}")
    if not root.is_dir():
        raise InstallerError(f"skill directory is missing or not a directory: {root}")
    skill_file = root / "SKILL.md"
    if skill_file.is_symlink() or not skill_file.is_file():
        raise InstallerError(f"skill directory must contain a regular SKILL.md file: {root}")
    for entry in root.rglob("*"):
        if entry.is_symlink():
            raise InstallerError(f"skill tree contains a symlink: {entry}")
        if not entry.is_dir() and not entry.is_file():
            raise InstallerError(f"skill tree contains an unsupported filesystem entry: {entry}")


def list_skill_names(source: Path) -> list[str]:
    """Return sorted, validated skill directory names under ``source``."""

    if source.is_symlink() or not source.is_dir():
        raise InstallerError(f"bundled skill source is unavailable or unsafe: {source}")
    names: list[str] = []
    for entry in source.iterdir():
        if entry.is_symlink():
            raise InstallerError(f"bundled skill entry must not be a symlink: {entry}")
        if not entry.is_dir():
            continue
        _validate_skill_name(entry.name)
        _assert_regular_tree(entry)
        names.append(entry.name)
    return sorted(names)


def _tree_digest(root: Path) -> str:
    """Return a deterministic SHA-256 digest for a regular directory tree."""

    _assert_regular_tree(root)
    digest = hashlib.sha256()
    for file_path in sorted(path for path in root.rglob("*") if path.is_file()):
        relative = file_path.relative_to(root).as_posix()
        digest.update(relative.encode("utf-8"))
        digest.update(b"\0")
        with file_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        digest.update(b"\0")
    return digest.hexdigest()


def _observed_digest(path: Path) -> str:
    """Digest an installed directory, or return a marker for an invalid type."""

    if path.is_symlink():
        raise InstallerError(f"refusing to inspect a symlinked skill path: {path}")
    if path.is_dir():
        return _tree_digest(path)
    if path.is_file():
        return "file:" + hashlib.sha256(path.read_bytes()).hexdigest()
    raise InstallerError(f"unsupported filesystem entry at skill path: {path}")


def _control_root(target_root: Path) -> Path:
    return target_root.parent / CONTROL_DIRNAME


def _manifest_path(target_root: Path) -> Path:
    return _control_root(target_root) / MANIFEST_FILENAME


def _new_manifest(client: str, scope: str) -> InstallManifest:
    return {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "package": "social-cc-plugin",
        "package_version": __version__,
        "client": client,
        "scope": scope,
        "skills": {},
    }


def _parse_skill_record(name: str, value: object) -> SkillRecord:
    if not isinstance(value, dict):
        raise InstallerError(f"manifest record for {name} is not an object")
    digest = value.get("digest")
    installed_at = value.get("installed_at")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-f]{64}", digest):
        raise InstallerError(f"manifest record for {name} has an invalid digest")
    if not isinstance(installed_at, str) or not installed_at:
        raise InstallerError(f"manifest record for {name} has no installation timestamp")
    return {"digest": digest, "installed_at": installed_at}


def _load_manifest(target_root: Path, client: str, scope: str) -> tuple[InstallManifest, bool]:
    path = _manifest_path(target_root)
    if path.is_symlink():
        raise InstallerError(f"refusing to read a symlinked installation manifest: {path}")
    if not path.exists():
        return _new_manifest(client, scope), False
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise InstallerError(f"cannot read installation manifest {path}: {exc}") from exc
    if not isinstance(raw, dict):
        raise InstallerError(f"installation manifest must be a JSON object: {path}")
    required = {
        "schema_version": int,
        "package": str,
        "package_version": str,
        "client": str,
        "scope": str,
        "skills": dict,
    }
    for key, expected_type in required.items():
        if not isinstance(raw.get(key), expected_type):
            raise InstallerError(f"installation manifest has invalid field {key}: {path}")
    if raw["schema_version"] != MANIFEST_SCHEMA_VERSION:
        raise InstallerError(
            f"unsupported installation manifest schema {raw['schema_version']}: {path}"
        )
    if raw["package"] != "social-cc-plugin":
        raise InstallerError(f"installation manifest belongs to another package: {path}")
    if raw["client"] != client or raw["scope"] != scope:
        raise InstallerError(
            f"installation manifest target mismatch, expected {client}/{scope}: {path}"
        )
    skills: dict[str, SkillRecord] = {}
    raw_skills = cast(dict[object, object], raw["skills"])
    for raw_name, value in raw_skills.items():
        if not isinstance(raw_name, str):
            raise InstallerError(f"installation manifest contains a non-string skill name: {path}")
        _validate_skill_name(raw_name)
        skills[raw_name] = _parse_skill_record(raw_name, value)
    manifest: InstallManifest = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "package": "social-cc-plugin",
        "package_version": cast(str, raw["package_version"]),
        "client": client,
        "scope": scope,
        "skills": skills,
    }
    return manifest, True


def _write_manifest(target_root: Path, manifest: InstallManifest) -> None:
    control_root = _control_root(target_root)
    if control_root.is_symlink():
        raise InstallerError(
            f"refusing to write through a symlinked control directory: {control_root}"
        )
    control_root.mkdir(parents=True, exist_ok=True)
    path = _manifest_path(target_root)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".manifest-", suffix=".json", dir=control_root
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(manifest, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def _remove_manifest(target_root: Path) -> None:
    path = _manifest_path(target_root)
    if path.is_symlink():
        raise InstallerError(f"refusing to remove a symlinked manifest: {path}")
    path.unlink(missing_ok=True)


class _BackupManager:
    """Move replaced paths into a recoverable, operation-scoped backup directory."""

    def __init__(self, target_root: Path, *, dry_run: bool) -> None:
        self.target_root = target_root
        self.dry_run = dry_run
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.batch = f"{stamp}-{uuid.uuid4().hex[:8]}"

    @property
    def root(self) -> Path:
        return _control_root(self.target_root) / BACKUPS_DIRNAME / self.batch

    def move(self, source: Path) -> Path:
        if source.is_symlink():
            raise InstallerError(f"refusing to back up a symlinked path: {source}")
        backup = self.root / source.name
        _emit(f"backup  {source.name} -> {backup}")
        if self.dry_run:
            return backup
        backup.parent.mkdir(parents=True, exist_ok=True)
        if backup.exists():
            raise InstallerError(f"backup collision at {backup}")
        source.replace(backup)
        return backup


def _ensure_safe_target(target_root: Path, *, dry_run: bool) -> None:
    if target_root.is_symlink():
        raise InstallerError(f"refusing to use a symlinked skills directory: {target_root}")
    control = _control_root(target_root)
    if control.is_symlink():
        raise InstallerError(f"refusing to use a symlinked control directory: {control}")
    if target_root.exists() and not target_root.is_dir():
        raise InstallerError(f"skills target exists but is not a directory: {target_root}")
    if not dry_run:
        target_root.parent.mkdir(parents=True, exist_ok=True)
        target_root.mkdir(parents=True, exist_ok=True)


def _replace_skill(
    source: Path,
    destination: Path,
    backup_manager: _BackupManager,
) -> Path | None:
    """Stage a skill, preserve any prior path, then atomically place the new tree."""

    _assert_regular_tree(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage_parent = Path(
        tempfile.mkdtemp(prefix=".social-cc-stage-", dir=str(destination.parent.parent))
    )
    staged = stage_parent / destination.name
    prior_backup: Path | None = None
    try:
        shutil.copytree(source, staged, copy_function=shutil.copy2)
        _assert_regular_tree(staged)
        if destination.exists():
            prior_backup = backup_manager.move(destination)
        try:
            staged.replace(destination)
        except OSError:
            if prior_backup is not None and prior_backup.exists() and not destination.exists():
                prior_backup.replace(destination)
            raise
    finally:
        shutil.rmtree(stage_parent, ignore_errors=True)
    return prior_backup


def _install_operation(
    source: Path,
    target_root: Path,
    *,
    force: bool,
    dry_run: bool,
    client: str,
    scope: str,
) -> OperationResult:
    _ensure_safe_target(target_root, dry_run=dry_run)
    manifest, manifest_exists = _load_manifest(target_root, client, scope)
    manager = _BackupManager(target_root, dry_run=dry_run)
    result = OperationResult()
    manifest_changed = manifest_exists and manifest["package_version"] != __version__

    for name in list_skill_names(source):
        source_skill = source / name
        source_digest = _tree_digest(source_skill)
        destination = target_root / name
        record = manifest["skills"].get(name)

        if destination.is_symlink():
            _emit(f"protect {name} (destination is a symlink)")
            result.skipped += 1
            result.protected += 1
            continue

        if not destination.exists():
            _emit(f"{'plan   ' if dry_run else 'install'} {name}")
            if not dry_run:
                _replace_skill(source_skill, destination, manager)
                manifest["skills"][name] = {
                    "digest": source_digest,
                    "installed_at": _utc_timestamp(),
                }
                manifest_changed = True
            result.changed += 1
            continue

        if record is None:
            if not force:
                _emit(f"protect {name} (existing directory is not owned by social-cc)")
                result.skipped += 1
                result.protected += 1
                continue
            _emit(f"{'plan   ' if dry_run else 'replace'} {name} (unmanaged, --force)")
        else:
            current_digest = _observed_digest(destination)
            if current_digest != record["digest"]:
                if not force:
                    _emit(f"protect {name} (locally modified, use --force to preserve and replace)")
                    result.skipped += 1
                    result.protected += 1
                    continue
                _emit(f"{'plan   ' if dry_run else 'replace'} {name} (modified, --force)")
            elif current_digest == source_digest:
                _emit(f"current {name}")
                result.skipped += 1
                continue
            else:
                _emit(f"{'plan   ' if dry_run else 'upgrade'} {name}")

        if dry_run:
            result.changed += 1
            continue

        backup = _replace_skill(source_skill, destination, manager)
        if backup is not None:
            result.backups.append(backup)
        manifest["skills"][name] = {
            "digest": source_digest,
            "installed_at": _utc_timestamp(),
        }
        manifest_changed = True
        result.changed += 1

    if not dry_run and manifest_changed:
        manifest["package_version"] = __version__
        _write_manifest(target_root, manifest)
    return result


def install_skills(
    source: Path,
    target_root: Path,
    *,
    force: bool,
    dry_run: bool,
    client: str = "claude-code",
    scope: str = "user",
) -> tuple[int, int]:
    """Install or upgrade skills while protecting user-owned and modified files.

    Returns a backward-compatible ``(changed, skipped)`` tuple. A manifest records
    project ownership, and every replaced path is moved to a recoverable backup.
    """

    result = _install_operation(
        source,
        target_root,
        force=force,
        dry_run=dry_run,
        client=client,
        scope=scope,
    )
    return result.changed, result.skipped


def uninstall_skills(
    target_root: Path,
    *,
    force: bool,
    dry_run: bool,
    client: str = "claude-code",
    scope: str = "user",
) -> tuple[int, int]:
    """Remove only manifest-owned skills, preserving every removed path in backup."""

    _ensure_safe_target(target_root, dry_run=dry_run)
    manifest, manifest_exists = _load_manifest(target_root, client, scope)
    if not manifest_exists:
        _emit("info    no social-cc installation manifest found")
        return 0, 0

    manager = _BackupManager(target_root, dry_run=dry_run)
    result = OperationResult()
    removed_names: list[str] = []

    for name, record in sorted(manifest["skills"].items()):
        destination = target_root / name
        if destination.is_symlink():
            _emit(f"protect {name} (destination is a symlink)")
            result.skipped += 1
            result.protected += 1
            continue
        if not destination.exists():
            _emit(f"forget  {name} (already absent)")
            removed_names.append(name)
            continue

        current_digest = _observed_digest(destination)
        if current_digest != record["digest"] and not force:
            _emit(f"protect {name} (locally modified, use --force to preserve and remove)")
            result.skipped += 1
            result.protected += 1
            continue

        reason = "modified, --force" if current_digest != record["digest"] else "owned"
        _emit(f"{'plan   ' if dry_run else 'remove '} {name} ({reason})")
        result.changed += 1
        if not dry_run:
            backup = manager.move(destination)
            result.backups.append(backup)
            removed_names.append(name)

    if not dry_run:
        for name in removed_names:
            manifest["skills"].pop(name, None)
        if manifest["skills"]:
            manifest["package_version"] = __version__
            _write_manifest(target_root, manifest)
        else:
            _remove_manifest(target_root)
    return result.changed, result.skipped


def diff_skills(
    source: Path,
    target_root: Path,
    *,
    client: str = "claude-code",
    scope: str = "user",
) -> list[SkillDiff]:
    """Compare bundled content, installed content, and the ownership manifest."""

    if target_root.is_symlink():
        raise InstallerError(f"refusing to inspect a symlinked skills directory: {target_root}")
    manifest, _ = _load_manifest(target_root, client, scope)
    source_names = set(list_skill_names(source))
    names = sorted(source_names | set(manifest["skills"]))
    findings: list[SkillDiff] = []

    for name in names:
        source_skill = source / name
        destination = target_root / name
        record = manifest["skills"].get(name)
        in_source = name in source_names

        if destination.is_symlink():
            findings.append(SkillDiff(name, "unsafe", "destination is a symlink"))
            continue
        if not destination.exists():
            status = "missing" if in_source else "stale-manifest"
            findings.append(SkillDiff(name, status, "installed path is absent"))
            continue
        if record is None:
            findings.append(SkillDiff(name, "unmanaged", "path exists without ownership record"))
            continue

        current_digest = _observed_digest(destination)
        if current_digest != record["digest"]:
            findings.append(SkillDiff(name, "modified", "installed content differs from manifest"))
            continue
        if not in_source:
            findings.append(SkillDiff(name, "orphaned", "owned skill is no longer bundled"))
            continue
        source_digest = _tree_digest(source_skill)
        if current_digest == source_digest:
            findings.append(SkillDiff(name, "current", "installed content matches bundle"))
        else:
            findings.append(SkillDiff(name, "outdated", "bundle has a newer reviewed version"))
    return findings


def target_specs(
    client: str,
    scope: str,
    *,
    home: Path | None = None,
    cwd: Path | None = None,
) -> list[TargetSpec]:
    """Resolve supported client and scope combinations to discovery paths."""

    if client not in {*CLIENT_PATHS, "all"}:
        raise InstallerError(f"unsupported client: {client}")
    if scope not in {"user", "project"}:
        raise InstallerError(f"unsupported scope: {scope}")
    base = (cwd or Path.cwd()) if scope == "project" else (home or Path.home())
    clients = list(CLIENT_PATHS) if client == "all" else [client]
    return [
        TargetSpec(item, scope, base.joinpath(*CLIENT_PATHS[item]))
        for item in clients
    ]


def _target_root(project: bool) -> Path:
    """Backward-compatible Claude Code target helper."""

    scope = "project" if project else "user"
    return target_specs("claude-code", scope)[0].root


def doctor_report(
    target_root: Path,
    bundled: list[str] | None,
    tools: Mapping[str, str | None],
    *,
    python_ok: bool,
) -> tuple[list[str], int]:
    """Build a compatibility doctor report and exit code."""

    lines: list[str] = []
    exit_code = 0
    if python_ok:
        lines.append("ok    python 3.9 or newer")
    else:
        lines.append("FAIL  python 3.9 or newer is required")
        exit_code = 1
    hints = {
        "claude": "Claude Code host",
        "codex": "Codex host",
        "git": "version control for reproducible research",
        "node": "needed only for repository validation work",
    }
    for tool, hint in hints.items():
        if tool not in tools:
            continue
        if tools.get(tool):
            lines.append(f"ok    {tool} on PATH")
        else:
            lines.append(f"warn  {tool} not found ({hint})")
    if target_root.is_dir():
        installed = sorted(
            path.name
            for path in target_root.iterdir()
            if path.is_dir() and not path.is_symlink()
        )
    else:
        installed = []
    if bundled is None:
        lines.append("warn  bundled skills not found (source checkout?)")
        lines.append(f"info  {len(installed)} skills present at the target")
    else:
        missing = [name for name in bundled if name not in installed]
        if missing:
            lines.append(
                f"warn  {len(missing)} of {len(bundled)} bundled skills not installed,"
                " run social-cc install"
            )
        else:
            lines.append(f"ok    all {len(bundled)} bundled skills installed")
    return lines, exit_code


def _effective_scope(scope: str, project: bool) -> str:
    return "project" if project else scope


def _run_install(
    *,
    client: str,
    scope: str,
    project: bool,
    force: bool,
    dry_run: bool,
) -> int:
    with _bundled_source() as source:
        if source is None:
            _emit("No bundled skills found. The package may be installed incorrectly.")
            return 1
        total_changed = 0
        total_skipped = 0
        for target in target_specs(client, _effective_scope(scope, project)):
            _emit(f"Target [{target.client}/{target.scope}]: {target.root}")
            result = _install_operation(
                source,
                target.root,
                force=force,
                dry_run=dry_run,
                client=target.client,
                scope=target.scope,
            )
            total_changed += result.changed
            total_skipped += result.skipped
        verb = "would change" if dry_run else "changed"
        _emit(f"{verb} {total_changed}, skipped {total_skipped}")
        return 0


def _run_uninstall(
    *,
    client: str,
    scope: str,
    project: bool,
    force: bool,
    dry_run: bool,
) -> int:
    total_changed = 0
    total_skipped = 0
    for target in target_specs(client, _effective_scope(scope, project)):
        _emit(f"Target [{target.client}/{target.scope}]: {target.root}")
        changed, skipped = uninstall_skills(
            target.root,
            force=force,
            dry_run=dry_run,
            client=target.client,
            scope=target.scope,
        )
        total_changed += changed
        total_skipped += skipped
    verb = "would remove" if dry_run else "removed"
    _emit(f"{verb} {total_changed}, protected or skipped {total_skipped}")
    return 0


def _run_diff(*, client: str, scope: str, project: bool) -> int:
    with _bundled_source() as source:
        if source is None:
            _emit("No bundled skills found.")
            return 1
        has_drift = False
        for target in target_specs(client, _effective_scope(scope, project)):
            _emit(f"Target [{target.client}/{target.scope}]: {target.root}")
            findings = diff_skills(
                source,
                target.root,
                client=target.client,
                scope=target.scope,
            )
            for finding in findings:
                _emit(f"{finding.status:9} {finding.name} ({finding.detail})")
                has_drift = has_drift or finding.status != "current"
        return 1 if has_drift else 0


def _run_list() -> int:
    with _bundled_source() as source:
        if source is None:
            _emit("No bundled skills found.")
            return 1
        names = list_skill_names(source)
        _emit(f"{len(names)} bundled skills:")
        for name in names:
            _emit(f"  {name}")
        return 0


def _run_doctor(*, client: str, scope: str, project: bool) -> int:
    with _bundled_source() as source:
        bundled = list_skill_names(source) if source is not None else None
    exit_code = 0
    effective_scope = _effective_scope(scope, project)
    for target in target_specs(client, effective_scope):
        tool_names = {CLIENT_TOOLS[target.client], "git", "node"}
        tools = {name: shutil.which(name) for name in sorted(tool_names)}
        lines, target_exit = doctor_report(
            target.root,
            bundled,
            tools,
            python_ok=sys.version_info >= (3, 9),
        )
        _emit(f"Target [{target.client}/{target.scope}]: {target.root}")
        for line in lines:
            _emit(line)
        manifest = _manifest_path(target.root)
        if manifest.exists() and not manifest.is_symlink():
            _emit(f"ok    ownership manifest present at {manifest}")
        else:
            _emit("warn  ownership manifest not found")
        exit_code = max(exit_code, target_exit)
    return exit_code


def _add_target_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--client",
        choices=[*CLIENT_PATHS, "all"],
        default="claude-code",
        help="Target Claude Code, Codex, or both. Default: claude-code.",
    )
    parser.add_argument(
        "--scope",
        choices=["user", "project"],
        default="user",
        help="Install for the current user or current project. Default: user.",
    )
    parser.add_argument(
        "--project",
        action="store_true",
        help="Compatibility alias for --scope project.",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="social-cc",
        description="Install and maintain the Social Scientist skills for Claude Code and Codex.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    install_parser = sub.add_parser("install", help="Install bundled skills safely.")
    _add_target_arguments(install_parser)
    install_parser.add_argument(
        "--force",
        action="store_true",
        help="Back up and replace unmanaged or locally modified skill directories.",
    )
    install_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing.",
    )

    upgrade_parser = sub.add_parser(
        "upgrade",
        help="Upgrade installed skills and add newly bundled skills.",
    )
    _add_target_arguments(upgrade_parser)
    upgrade_parser.add_argument(
        "--force",
        action="store_true",
        help="Back up and replace locally modified skill directories.",
    )
    upgrade_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing.",
    )

    diff_parser = sub.add_parser("diff", help="Report installed skill drift.")
    _add_target_arguments(diff_parser)

    uninstall_parser = sub.add_parser(
        "uninstall",
        help="Remove only manifest-owned skills and retain recoverable backups.",
    )
    _add_target_arguments(uninstall_parser)
    uninstall_parser.add_argument(
        "--force",
        action="store_true",
        help="Back up and remove locally modified manifest-owned skills.",
    )
    uninstall_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned removals without writing.",
    )

    sub.add_parser("list", help="List bundled skills.")

    doctor_parser = sub.add_parser(
        "doctor",
        help="Check host tools, target paths, installed skills, and ownership manifests.",
    )
    _add_target_arguments(doctor_parser)
    return parser


def main(argv: list[str] | None = None) -> int:
    try:
        args = build_parser().parse_args(argv)
        command = cast(str, args.command)
        if command in {"install", "upgrade"}:
            return _run_install(
                client=cast(str, args.client),
                scope=cast(str, args.scope),
                project=cast(bool, args.project),
                force=cast(bool, args.force),
                dry_run=cast(bool, args.dry_run),
            )
        if command == "uninstall":
            return _run_uninstall(
                client=cast(str, args.client),
                scope=cast(str, args.scope),
                project=cast(bool, args.project),
                force=cast(bool, args.force),
                dry_run=cast(bool, args.dry_run),
            )
        if command == "diff":
            return _run_diff(
                client=cast(str, args.client),
                scope=cast(str, args.scope),
                project=cast(bool, args.project),
            )
        if command == "doctor":
            return _run_doctor(
                client=cast(str, args.client),
                scope=cast(str, args.scope),
                project=cast(bool, args.project),
            )
        return _run_list()
    except InstallerError as exc:
        _emit(f"ERROR: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
