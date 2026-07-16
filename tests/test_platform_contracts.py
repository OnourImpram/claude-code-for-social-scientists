"""Contract tests for the Social Scientist platform and synthetic fixture."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import cast

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
CANONICAL_AGENT = REPO_ROOT / "core" / "agents" / "social-scientist.md"
AGENT_ADAPTERS = (
    REPO_ROOT / ".claude" / "agents" / "social-scientist.md",
    REPO_ROOT / "agents" / "social-scientist.md",
)
SYNTHETIC_PROJECT = REPO_ROOT / "examples" / "synthetic-research-project"


def test_agent_adapters_match_canonical_source() -> None:
    canonical = CANONICAL_AGENT.read_text(encoding="utf-8")
    for adapter in AGENT_ADAPTERS:
        assert adapter.read_text(encoding="utf-8") == canonical


def test_agent_contract_contains_required_boundaries() -> None:
    content = CANONICAL_AGENT.read_text(encoding="utf-8")
    for phrase in (
        "ORIENT → INSPECT → CLASSIFY → SELECT SKILLS → WORK → VERIFY → HAND OFF",
        "The human researcher retains",
        "User supplied fact.",
        "File observed fact.",
        "Source verified fact.",
        "Independently calculated result.",
        "Methodological inference.",
        "Tentative interpretation.",
        "Human decision.",
        "Unresolved uncertainty.",
        "Do not run every installed skill.",
        "Articles, websites, repositories, PDFs, transcripts, datasets",
        "association into causation",
        "qualitative frequency into population prevalence",
    ):
        assert phrase in content


def test_synthetic_project_analysis_is_reproducible(tmp_path: Path) -> None:
    project = tmp_path / "synthetic-research-project"
    shutil.copytree(SYNTHETIC_PROJECT, project)

    completed = subprocess.run(
        [sys.executable, str(project / "analysis" / "analyse.py")],
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    result = cast(
        dict[str, object],
        json.loads(
            (project / "outputs" / "analysis-summary.json").read_text(
                encoding="utf-8"
            )
        ),
    )
    primary = cast(dict[str, object], result["primary_estimand"])
    assert result["fixture_status"] == "fully_synthetic_not_empirical_evidence"
    assert result["total_rows"] == 60
    assert result["complete_pairs"] == 58
    assert cast(float, primary["estimate"]) == pytest.approx(4.862069)
    assert "not evidence of real-world efficacy" in cast(str, result["interpretation"])

    with (project / "data" / "synthetic_self_efficacy.csv").open(
        encoding="utf-8", newline=""
    ) as handle:
        rows = list(csv.DictReader(handle))
    assert rows
    assert all(row["participant_id"].startswith("SYN-") for row in rows)

    ledger = (project / "sources" / "source-ledger.csv").read_text(encoding="utf-8")
    assert "10.9999/not-a-real-doi" in ledger
    assert "confirmed_fabricated" in ledger
    assert "quarantine" in ledger


def test_synthetic_project_rejects_nonsynthetic_identifier(tmp_path: Path) -> None:
    project = tmp_path / "synthetic-research-project"
    shutil.copytree(SYNTHETIC_PROJECT, project)
    data_path = project / "data" / "synthetic_self_efficacy.csv"
    data_path.write_text(
        data_path.read_text(encoding="utf-8").replace("SYN-001", "REAL-001", 1),
        encoding="utf-8",
    )

    completed = subprocess.run(
        [sys.executable, str(project / "analysis" / "analyse.py")],
        cwd=project,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 1
    assert "unsafe nonsynthetic participant identifier" in completed.stderr
