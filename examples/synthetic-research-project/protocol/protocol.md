# Protocol

## Project status

Synthetic educational fixture. No human participants, recruitment, intervention delivery, institution, or ethics approval exists.

## Research question

In the generated dataset, what is the difference between the guided and comparison groups in mean change from baseline to follow up self efficacy?

## Rationale

The fixture teaches how an agentic research workflow should distinguish design facts, calculations, interpretations, and unresolved decisions. It is deliberately simple enough to analyse with the Python standard library while retaining missing data, group comparison, preregistration, citation quarantine, and disclosure requirements.

## Design

The dataset contains sixty synthetic records. Group labels alternate between `comparison` and `guided` to make the fixture deterministic. This is not a simulation of a defensible randomization procedure for a real trial.

### Variables

| Variable | Type | Meaning |
|---|---|---|
| `participant_id` | string | Synthetic identifier beginning with `SYN-` |
| `group` | categorical | `guided` or `comparison` |
| `baseline_self_efficacy` | numeric | Illustrative baseline score from zero to one hundred |
| `followup_self_efficacy` | numeric or missing | Illustrative follow up score |
| `completed_plan` | binary or missing | Whether follow up exceeded baseline by at least one point |
| `missing_reason` | string | Synthetic reason for a missing follow up |

## Primary estimand

The difference in group mean change scores:

```text
mean(follow up minus baseline in guided)
minus
mean(follow up minus baseline in comparison)
```

This estimand is computed among records with observed baseline and follow up scores.

## Missing data

Two follow up values are missing by construction. The primary fixture analysis uses complete observed pairs and reports missingness by group. No imputation is performed. This is an instructional choice, not a recommendation for real research.

## Analysis

The analysis script reports:

1. Total rows and complete pairs.
2. Missing follow up values by group.
3. Group mean and standard deviation of change.
4. Difference in mean change.
5. A normal approximation ninety five percent uncertainty interval using the independent group standard errors.
6. A machine readable interpretation boundary.

The interval is an illustrative calculation. The fixture does not claim that normal approximation, complete case analysis, or a change score estimator is optimal for any real design.

## Data sensitivity

Classification is public synthetic. The analysis rejects participant identifiers that do not begin with `SYN-`. No personal, clinical, educational, reviewer, credential, or institutional information may be added.

## Evidence labels

- The row count and variable definitions are file observed facts.
- Summary statistics are independently calculated results.
- The statement that the guided group has a larger generated mean change is a calculation based interpretation.
- Any claim about real world efficacy is unsupported and prohibited.
- Choice of a real study design, estimator, missing data method, and substantive interpretation remains a human decision.

## Ethics boundary

This fixture requires no human participant review because it contains no human participant activity or data. That fact must not be generalized to a real study. A real project requires institution specific ethics, privacy, consent, and data governance review.

## Bilingual boundary

The self efficacy label is an instructional variable name, not a validated construct translation. A real Turkish and English instrument would require conceptual, cultural, linguistic, and psychometric evaluation.
