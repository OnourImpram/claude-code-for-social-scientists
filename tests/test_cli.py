"""Tests for the safe dual-client social-cc installer."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

import social_cc_plugin
from social_cc_plugin import cli


def _make_source(tmp_path: Path, names: tuple[str, ...] = ("alpha-skill", "beta-skill")) -> Path:
    source = tmp_path / "skills"
    for name in names:
        skill_dir = source / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(
            f"---\nname: {name}\ndescription: test\n---\n\n# {name}\n",
            encoding="utf-8",
        )
    return source


def _manifest_path(target: Path) -> Path:
    return target.parent / ".social-cc" / "manifest.json"


def _backup_matches(target: Path, name: str) -> list[Path]:
    return list((target.parent / ".social-cc" / "backups").glob(f"*/{name}"))


def test_list_skill_names_sorted(tmp_path: Path) -> None:
    source = _make_source(tmp_path)
    assert cli.list_skill_names(source) == ["alpha-skill", "beta-skill"]


def test_install_copies_all_and_writes_manifest(tmp_path: Path) -> None:
    source = _make_source(tmp_path)
    target = tmp_path / "out"
    changed, skipped = cli.install_skills(source, target, force=False, dry_run=False)
    assert (changed, skipped) == (2, 0)
    assert (target / "alpha-skill" / "SKILL.md").is_file()
    manifest = json.loads(_manifest_path(target).read_text(encoding="utf-8"))
    assert manifest["client"] == "claude-code"
    assert manifest["scope"] == "user"
    assert sorted(manifest["skills"]) == ["alpha-skill", "beta-skill"]


def test_second_install_reports_current_without_backup(tmp_path: Path) -> None:
    source = _make_source(tmp_path)
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    changed, skipped = cli.install_skills(source, target, force=False, dry_run=False)
    assert (changed, skipped) == (0, 2)
    assert _backup_matches(target, "alpha-skill") == []


def test_unmanaged_existing_skill_is_protected(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    existing = target / "alpha-skill"
    existing.mkdir(parents=True)
    (existing / "SKILL.md").write_text("# user skill\n", encoding="utf-8")

    changed, skipped = cli.install_skills(source, target, force=False, dry_run=False)

    assert (changed, skipped) == (0, 1)
    assert (existing / "SKILL.md").read_text(encoding="utf-8") == "# user skill\n"
    assert not _manifest_path(target).exists()


def test_force_preserves_unmanaged_skill_in_backup_before_replace(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    existing = target / "alpha-skill"
    existing.mkdir(parents=True)
    (existing / "SKILL.md").write_text("# user skill\n", encoding="utf-8")

    changed, skipped = cli.install_skills(source, target, force=True, dry_run=False)

    assert (changed, skipped) == (1, 0)
    backups = _backup_matches(target, "alpha-skill")
    assert len(backups) == 1
    assert (backups[0] / "SKILL.md").read_text(encoding="utf-8") == "# user skill\n"
    assert "# alpha-skill" in (existing / "SKILL.md").read_text(encoding="utf-8")


def test_modified_owned_skill_is_protected_without_force(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    installed = target / "alpha-skill" / "SKILL.md"
    installed.write_text("# local edit\n", encoding="utf-8")

    changed, skipped = cli.install_skills(source, target, force=False, dry_run=False)

    assert (changed, skipped) == (0, 1)
    assert installed.read_text(encoding="utf-8") == "# local edit\n"
    assert _backup_matches(target, "alpha-skill") == []


def test_force_preserves_modified_owned_skill_in_backup(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    installed = target / "alpha-skill" / "SKILL.md"
    installed.write_text("# local edit\n", encoding="utf-8")

    changed, skipped = cli.install_skills(source, target, force=True, dry_run=False)

    assert (changed, skipped) == (1, 0)
    backups = _backup_matches(target, "alpha-skill")
    assert len(backups) == 1
    assert (backups[0] / "SKILL.md").read_text(encoding="utf-8") == "# local edit\n"
    assert "# alpha-skill" in installed.read_text(encoding="utf-8")


def test_upgrade_of_unmodified_owned_skill_is_backed_up(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    old_text = (target / "alpha-skill" / "SKILL.md").read_text(encoding="utf-8")
    (source / "alpha-skill" / "SKILL.md").write_text(
        "---\nname: alpha-skill\ndescription: changed\n---\n\n# version two\n",
        encoding="utf-8",
    )

    changed, skipped = cli.install_skills(source, target, force=False, dry_run=False)

    assert (changed, skipped) == (1, 0)
    backups = _backup_matches(target, "alpha-skill")
    assert len(backups) == 1
    assert (backups[0] / "SKILL.md").read_text(encoding="utf-8") == old_text
    assert "# version two" in (target / "alpha-skill" / "SKILL.md").read_text(
        encoding="utf-8"
    )


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    source = _make_source(tmp_path)
    target = tmp_path / "out"
    changed, skipped = cli.install_skills(source, target, force=False, dry_run=True)
    assert (changed, skipped) == (2, 0)
    assert not target.exists()
    assert not _manifest_path(target).exists()


def test_uninstall_removes_only_manifest_owned_skills_and_keeps_backup(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    unrelated = target / "user-skill"
    unrelated.mkdir()
    (unrelated / "SKILL.md").write_text("# user\n", encoding="utf-8")

    removed, skipped = cli.uninstall_skills(target, force=False, dry_run=False)

    assert (removed, skipped) == (1, 0)
    assert not (target / "alpha-skill").exists()
    assert unrelated.exists()
    assert len(_backup_matches(target, "alpha-skill")) == 1
    assert not _manifest_path(target).exists()


def test_uninstall_protects_modified_owned_skill_without_force(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    installed = target / "alpha-skill" / "SKILL.md"
    installed.write_text("# local edit\n", encoding="utf-8")

    removed, skipped = cli.uninstall_skills(target, force=False, dry_run=False)

    assert (removed, skipped) == (0, 1)
    assert installed.exists()
    assert _manifest_path(target).exists()


def test_force_uninstall_preserves_modified_skill_in_backup(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    installed = target / "alpha-skill" / "SKILL.md"
    installed.write_text("# local edit\n", encoding="utf-8")

    removed, skipped = cli.uninstall_skills(target, force=True, dry_run=False)

    assert (removed, skipped) == (1, 0)
    backups = _backup_matches(target, "alpha-skill")
    assert len(backups) == 1
    assert (backups[0] / "SKILL.md").read_text(encoding="utf-8") == "# local edit\n"


def test_diff_classifies_current_modified_and_unmanaged(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill", "beta-skill"))
    target = tmp_path / "out"
    cli.install_skills(source, target, force=False, dry_run=False)
    (target / "alpha-skill" / "SKILL.md").write_text("# local edit\n", encoding="utf-8")
    unmanaged = target / "gamma-skill"
    unmanaged.mkdir()
    (unmanaged / "SKILL.md").write_text("# unmanaged\n", encoding="utf-8")

    findings = {item.name: item.status for item in cli.diff_skills(source, target)}

    assert findings == {"alpha-skill": "modified", "beta-skill": "current"}


def test_diff_reports_unmanaged_bundled_destination(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    destination = target / "alpha-skill"
    destination.mkdir(parents=True)
    (destination / "SKILL.md").write_text("# unmanaged\n", encoding="utf-8")

    findings = cli.diff_skills(source, target)

    assert [(item.name, item.status) for item in findings] == [("alpha-skill", "unmanaged")]


def test_target_specs_cover_both_clients_and_scopes(tmp_path: Path) -> None:
    home = tmp_path / "home"
    project = tmp_path / "project"
    user_targets = cli.target_specs("all", "user", home=home, cwd=project)
    project_targets = cli.target_specs("all", "project", home=home, cwd=project)

    assert [item.root for item in user_targets] == [
        home / ".claude" / "skills",
        home / ".agents" / "skills",
    ]
    assert [item.root for item in project_targets] == [
        project / ".claude" / "skills",
        project / ".agents" / "skills",
    ]


def test_install_rejects_symlinked_destination(tmp_path: Path) -> None:
    source = _make_source(tmp_path, ("alpha-skill",))
    target = tmp_path / "out"
    target.mkdir()
    external = tmp_path / "external"
    external.mkdir()
    try:
        (target / "alpha-skill").symlink_to(external, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks are unavailable in this environment")

    changed, skipped = cli.install_skills(source, target, force=True, dry_run=False)

    assert (changed, skipped) == (0, 1)
    assert not _manifest_path(target).exists()


def test_invalid_skill_name_is_rejected(tmp_path: Path) -> None:
    source = tmp_path / "skills"
    skill = source / "..unsafe"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text("# test\n", encoding="utf-8")
    with pytest.raises(cli.InstallerError):
        cli.list_skill_names(source)


def test_unicode_paths_are_supported(tmp_path: Path) -> None:
    source = _make_source(tmp_path / "kaynak", ("alpha-skill",))
    target = tmp_path / "çalışma alanı" / ".agents" / "skills"
    changed, skipped = cli.install_skills(
        source,
        target,
        force=False,
        dry_run=False,
        client="codex",
        scope="project",
    )
    assert (changed, skipped) == (1, 0)
    assert (target / "alpha-skill" / "SKILL.md").is_file()


def test_main_list_without_bundle_returns_one() -> None:
    assert cli.main(["list"]) == 1


def test_main_version_exits_zero() -> None:
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0


def test_version_matches_pyproject() -> None:
    pyproject = Path(__file__).resolve().parents[1] / "pyproject.toml"
    match = re.search(r'^version = "(.+)"$', pyproject.read_text(encoding="utf-8"), re.M)
    assert match is not None
    assert social_cc_plugin.__version__ == match.group(1)


def test_parser_preserves_project_alias_and_adds_dual_client_commands() -> None:
    args = cli.build_parser().parse_args(
        ["install", "--client", "codex", "--project", "--dry-run"]
    )
    assert args.client == "codex"
    assert args.project is True
    for command in ("upgrade", "diff", "uninstall", "doctor"):
        parsed = cli.build_parser().parse_args([command])
        assert parsed.command == command


def test_doctor_report_all_ok(tmp_path: Path) -> None:
    target = tmp_path / "skills"
    for name in ("alpha-skill", "beta-skill"):
        (target / name).mkdir(parents=True)
    tools = {
        "claude": "/usr/bin/claude",
        "git": "/usr/bin/git",
        "node": "/usr/bin/node",
    }
    lines, exit_code = cli.doctor_report(
        target,
        ["alpha-skill", "beta-skill"],
        tools,
        python_ok=True,
    )
    assert exit_code == 0
    assert "ok    all 2 bundled skills installed" in lines


def test_doctor_report_missing_skills_warns(tmp_path: Path) -> None:
    target = tmp_path / "skills"
    tools = {"claude": None, "git": "/usr/bin/git", "node": None}
    lines, exit_code = cli.doctor_report(
        target,
        ["alpha-skill", "beta-skill"],
        tools,
        python_ok=True,
    )
    assert exit_code == 0
    assert any(line.startswith("warn  2 of 2 bundled skills not installed") for line in lines)
    assert any(line.startswith("warn  claude not found") for line in lines)


def test_doctor_report_old_python_fails(tmp_path: Path) -> None:
    lines, exit_code = cli.doctor_report(tmp_path, None, {}, python_ok=False)
    assert exit_code == 1
    assert lines[0].startswith("FAIL")


def test_main_doctor_runs_from_source_checkout(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(cli.Path, "home", classmethod(lambda cls: tmp_path))
    assert cli.main(["doctor"]) == 0
