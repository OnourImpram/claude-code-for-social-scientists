"""Analyse the fully synthetic self-efficacy teaching fixture."""

from __future__ import annotations

import csv
import json
import math
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Final

VALID_GROUPS: Final = {"comparison", "guided"}
ID_PATTERN: Final = re.compile(r"^SYN-\d{3}$")


class DataValidationError(ValueError):
    """Raised when the synthetic fixture violates its declared schema."""


@dataclass(frozen=True)
class Record:
    """One validated synthetic record."""

    participant_id: str
    group: str
    baseline: float
    followup: float | None
    completed_plan: int | None
    missing_reason: str

    @property
    def change(self) -> float | None:
        """Return the observed change score when follow-up exists."""

        if self.followup is None:
            return None
        return self.followup - self.baseline


def _parse_float(value: str, *, field: str, participant_id: str) -> float:
    try:
        parsed = float(value)
    except ValueError as exc:
        raise DataValidationError(
            f"{participant_id}: {field} must be numeric, found {value!r}"
        ) from exc
    if not 0 <= parsed <= 100:
        raise DataValidationError(
            f"{participant_id}: {field} must be between 0 and 100"
        )
    return parsed


def _parse_completed(value: str, *, participant_id: str) -> int | None:
    if value == "":
        return None
    if value not in {"0", "1"}:
        raise DataValidationError(
            f"{participant_id}: completed_plan must be 0, 1, or missing"
        )
    return int(value)


def load_records(path: Path) -> list[Record]:
    """Load and validate the synthetic CSV file."""

    required = {
        "participant_id",
        "group",
        "baseline_self_efficacy",
        "followup_self_efficacy",
        "completed_plan",
        "missing_reason",
    }
    records: list[Record] = []
    seen: set[str] = set()

    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or set(reader.fieldnames) != required:
            raise DataValidationError(
                f"CSV columns must be exactly {sorted(required)}, found {reader.fieldnames}"
            )

        for row_number, row in enumerate(reader, start=2):
            participant_id = row["participant_id"]
            if not ID_PATTERN.fullmatch(participant_id):
                raise DataValidationError(
                    f"row {row_number}: unsafe nonsynthetic participant identifier "
                    f"{participant_id!r}"
                )
            if participant_id in seen:
                raise DataValidationError(
                    f"row {row_number}: duplicate participant identifier {participant_id}"
                )
            seen.add(participant_id)

            group = row["group"]
            if group not in VALID_GROUPS:
                raise DataValidationError(
                    f"{participant_id}: group must be one of {sorted(VALID_GROUPS)}"
                )

            baseline = _parse_float(
                row["baseline_self_efficacy"],
                field="baseline_self_efficacy",
                participant_id=participant_id,
            )
            followup_raw = row["followup_self_efficacy"]
            followup = (
                None
                if followup_raw == ""
                else _parse_float(
                    followup_raw,
                    field="followup_self_efficacy",
                    participant_id=participant_id,
                )
            )
            completed = _parse_completed(
                row["completed_plan"], participant_id=participant_id
            )
            missing_reason = row["missing_reason"]

            if followup is None:
                if completed is not None or not missing_reason:
                    raise DataValidationError(
                        f"{participant_id}: missing follow-up requires a missing reason "
                        "and missing completed_plan"
                    )
            elif missing_reason:
                raise DataValidationError(
                    f"{participant_id}: observed follow-up must not have a missing reason"
                )

            records.append(
                Record(
                    participant_id=participant_id,
                    group=group,
                    baseline=baseline,
                    followup=followup,
                    completed_plan=completed,
                    missing_reason=missing_reason,
                )
            )

    if not records:
        raise DataValidationError("synthetic dataset is empty")
    return records


def _round(value: float) -> float:
    return round(value, 6)


def analyse(records: list[Record]) -> dict[str, object]:
    """Compute the preregistered illustrative summary."""

    changes: dict[str, list[float]] = {group: [] for group in VALID_GROUPS}
    baselines: dict[str, list[float]] = {group: [] for group in VALID_GROUPS}
    missing: dict[str, int] = {group: 0 for group in VALID_GROUPS}
    completed: dict[str, list[int]] = {group: [] for group in VALID_GROUPS}

    for record in records:
        baselines[record.group].append(record.baseline)
        if record.change is None:
            missing[record.group] += 1
            continue
        changes[record.group].append(record.change)
        if record.completed_plan is not None:
            completed[record.group].append(record.completed_plan)

    group_summary: dict[str, dict[str, float | int]] = {}
    for group in sorted(VALID_GROUPS):
        values = changes[group]
        if len(values) < 2:
            raise DataValidationError(
                f"{group}: at least two complete pairs are required"
            )
        standard_deviation = statistics.stdev(values)
        group_summary[group] = {
            "n_total": len(baselines[group]),
            "n_complete": len(values),
            "n_missing_followup": missing[group],
            "missing_followup_proportion": _round(
                missing[group] / len(baselines[group])
            ),
            "baseline_mean": _round(statistics.mean(baselines[group])),
            "mean_change": _round(statistics.mean(values)),
            "sd_change": _round(standard_deviation),
            "se_change": _round(standard_deviation / math.sqrt(len(values))),
            "completed_plan_proportion_observed": _round(
                statistics.mean(completed[group])
            ),
        }

    guided = changes["guided"]
    comparison = changes["comparison"]
    guided_mean = statistics.mean(guided)
    comparison_mean = statistics.mean(comparison)
    difference = guided_mean - comparison_mean
    standard_error = math.sqrt(
        statistics.variance(guided) / len(guided)
        + statistics.variance(comparison) / len(comparison)
    )
    lower = difference - 1.96 * standard_error
    upper = difference + 1.96 * standard_error

    return {
        "fixture_status": "fully_synthetic_not_empirical_evidence",
        "python_version": sys.version.split()[0],
        "total_rows": len(records),
        "complete_pairs": len(guided) + len(comparison),
        "groups": group_summary,
        "primary_estimand": {
            "name": "guided_minus_comparison_mean_change",
            "estimate": _round(difference),
            "normal_approximation_95_interval": [_round(lower), _round(upper)],
        },
        "interpretation": (
            "The generated guided group has a larger mean change in this fixture. "
            "This independently calculated result is not evidence of real-world efficacy, "
            "causality, external validity, or instrument validity."
        ),
        "human_decisions_required": [
            "real study design and allocation",
            "construct and instrument validity",
            "sample size and power",
            "missing data strategy",
            "estimand and uncertainty method",
            "ethics and data governance",
            "substantive interpretation",
        ],
    }


def main() -> int:
    """Run the analysis and write a deterministic JSON artifact."""

    project_root = Path(__file__).resolve().parents[1]
    data_path = project_root / "data" / "synthetic_self_efficacy.csv"
    output_path = project_root / "outputs" / "analysis-summary.json"

    try:
        result = analyse(load_records(data_path))
    except (OSError, DataValidationError) as exc:
        print(f"analysis failed: {exc}", file=sys.stderr)
        return 1

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
