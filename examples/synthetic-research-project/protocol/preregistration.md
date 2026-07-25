# Preregistration and Analysis Plan

## Status

Frozen teaching fixture, version 1.0. Any change must be recorded in a deviation section before the analysis output is regenerated.

## Confirmatory teaching question

Does the synthetic guided group have a larger mean baseline to follow up change score than the synthetic comparison group?

## Primary outcome

`followup_self_efficacy - baseline_self_efficacy`

## Primary estimand

Difference between the guided and comparison group mean change scores among records with observed baseline and follow up scores.

## Inclusion rule

Include every row with:

1. A unique identifier beginning with `SYN-`.
2. A valid group label.
3. A numeric baseline score.
4. A numeric follow up score for the complete pair analysis.

Rows with missing follow up remain in the missingness report and are excluded from the primary change score calculation.

## Exclusion rule

No discretionary outlier exclusion is permitted. A row is rejected only when it violates the file schema or contains an unsafe nonsynthetic identifier.

## Missing data rule

Use complete observed baseline and follow up pairs. Report the number and proportion missing by group. Do not impute. This decision is fixed for the teaching fixture and is not a general recommendation.

## Analysis rule

For each group, calculate sample size, mean change, sample standard deviation, and standard error. Calculate the group mean difference and a normal approximation ninety five percent interval using:

```text
SE difference = sqrt(SD guided squared / n guided + SD comparison squared / n comparison)
```

```text
interval = difference plus or minus 1.96 times SE difference
```

## Confirmatory interpretation rule

The confirmatory statement is limited to the generated dataset. Report whether the observed mean change is larger in the guided group and provide the calculated difference and interval. Do not claim intervention efficacy, causality in real populations, statistical certification, or external validity.

## Exploratory outputs

- Completion proportions by group.
- Baseline group means.
- Sensitivity analysis is not included in version 1.0.

Exploratory outputs must be labelled and must not be merged into the confirmatory statement.

## Multiplicity

One confirmatory estimand is defined. Exploratory outputs are descriptive and do not receive confirmatory labels.

## Software

Python standard library only. The exact Python version used is recorded in the JSON output.

## Reproducibility

The analysis reads `data/synthetic_self_efficacy.csv` and writes `outputs/analysis-summary.json`. Output keys and decimal precision are deterministic.

## Human decisions

A human reviewer must approve any real study adaptation, including outcome validity, randomization, estimator, missing data strategy, uncertainty method, sample size, power, ethics, interpretation, and disclosure.

## Deviations

No deviations are recorded in version 1.0.
