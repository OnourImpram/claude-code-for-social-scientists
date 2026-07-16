# Synthetic Project Release Checklist

## Identity and scope

- [x] Project is labelled fully synthetic.
- [x] No claim describes the fixture as an empirical study.
- [x] The research question, design, outcome, and estimand are documented.
- [x] Human decision boundaries are explicit.

## Data and privacy

- [x] Every identifier begins with `SYN-`.
- [x] No real participant, patient, student, reviewer, credential, or institutional information is present.
- [x] Missing values and reasons are synthetic and documented.
- [x] The analysis rejects nonsynthetic identifiers.

## Analysis

- [x] The preregistration is committed before the expected output.
- [x] Inclusion, exclusion, missing data, and analysis rules are explicit.
- [x] The script uses only the Python standard library.
- [x] The primary estimand and uncertainty calculation are reproducible.
- [x] Exploratory outputs remain labelled.
- [x] The interpretation prohibits real world efficacy, causality, external validity, and instrument validity claims.

## Sources and citations

- [x] Internal fixture records are marked not citable.
- [x] The fabricated DOI is labelled and quarantined.
- [x] Prompt injection text is labelled untrusted content.
- [x] No unverified source enters a bibliography.

## AI assistance

- [x] AI contribution is described.
- [x] Human review responsibilities are recorded.
- [x] No model identifier is invented.
- [x] The suggested disclosure states that the fixture is synthetic and nonempirical.

## Open science package

- [x] README and project map are present.
- [x] Protocol and preregistration are present.
- [x] Data and analysis code are present.
- [x] Expected machine readable output is present.
- [x] Source ledger and adversarial fixture are present.
- [x] Disclosure and release checklist are present.
- [x] Repository level code and content licenses govern the fixture.

## Final human boundary

A maintainer must rerun the analysis, inspect the diff, confirm the privacy classification, and review the interpretation before a tagged release. This checklist does not certify a real study or authorize adaptation to human participant research.
