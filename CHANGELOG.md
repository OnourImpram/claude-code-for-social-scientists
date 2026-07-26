# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Citations of this work should use the Zenodo concept DOI [10.5281/zenodo.20289687](https://doi.org/10.5281/zenodo.20289687), which always resolves to the latest version. Version-specific DOIs are listed below.

## [5.0.0] - 2026-07-26

Major release. The project becomes an installable platform. First class Claude Code and Codex installation targets at user and project scope ship together with ownership manifests, recoverable backups, a canonical Social Scientist Agent with generated adapters, and validators for release truth, agent parity, and immutable action pins.

### Added

- First class Claude Code and Codex installation targets at user and project scope, with one reviewed skill source.
- Ownership manifests, deterministic tree digests, dry runs, reviewable diffs, upgrades, recoverable backups, and safe uninstall behavior.
- A canonical Social Scientist Agent, generated Claude Code adapters, and Codex repository guidance through `AGENTS.md`.
- Release truth, generated agent parity, and immutable GitHub Action pin validators.
- Platform architecture, client integration, skill responsibility, security and privacy, learning path, and ten loop engineering documentation.
- A synthetic research project and bilingual agent and skill evaluation fixtures.

### Changed

- The README pair, catalog, roadmap, academic paper, website, package landing page, citation metadata, and security policy now describe the v4.0.0 product surface consistently.
- CI now runs Python 3.9 and 3.12 tests, Ruff, strict mypy, package builds, wheel inspection, isolated installation, release truth checks, agent drift checks, and action pin checks.
- All third party GitHub Actions are pinned to full commit SHAs.
- The installer no longer recursively deletes an existing skill directory without ownership evidence and recovery.

### Security

- Unmanaged and locally modified skill directories are protected by default.
- Forced replacement and removal preserve the prior directory under `.social-cc/backups/`.
- Symlinked skill and control paths, unsafe skill names, and malformed ownership manifests are rejected.
- Retrieved articles, websites, repositories, PDFs, transcripts, datasets, and reviewer files are explicitly treated as untrusted research content rather than instructions.

## [4.0.0] - 2026-06-22

Major release. The companion project skill library grows from twenty to thirty-two skills, completing operational coverage of the research lifecycle, and ships together with a craft-grade bilingual overhaul of the companion site copy.

### Added

- Twelve new project skills under `.claude/skills/`, each authored to the repository's bilingual skill schema. The additions are `prisma-scoping-review-pipeline`, `sensitive-data-anonymization-gate`, `open-science-release-packager`, `authorship-contribution-ledger`, `peer-review-confidentiality-protocol`, `multilingual-concept-validity-audit`, `grant-proposal-workpackage-builder`, `teaching-feedback-ai-boundaries`, `public-scholarship-ethics-adapter`, `preregistration-analysis-plan-ledger`, `agent-portability-matrix`, and `cross-agent-second-opinion`.

### Changed

- The existing twenty skills were enriched in place with explicit when-not-to-use boundaries, named cross-skill handoffs, a session-end record line, and a closing quality gate.
- The companion site copy was rewritten in Turkish and English, and the skill catalogue advanced from twenty to thirty-two across the README pair, catalog, validator, and plugin manifests.

## [3.2.0] - 2026-06-21

Minor release. Twelve continuation booklets expanded bilingually from the author's source drafts, opening two new categories and extending six existing ones.

### Added

- Twelve new booklets at `release` status. The released catalog grows from twenty-one to thirty-three booklets across fourteen categories.
- Teaching and Supervision and Tool Portability become categories 013 and 014.

### Changed

- Every citation in the twelve new booklets was verified against Crossref and doi.org before inclusion. Aggregate verified declarations rise from 354 to 566, with zero fabricated citations.
- Reading order, navigation, catalog, landing page statistics, and aggregate disclosure were updated for the new surface.

## [3.1.0] - 2026-06-21

Minor release. A full bilingual content overhaul of every booklet, shipped together with the academic journal site redesign.

### Changed

- All twenty-one booklets were rebuilt from the author's hand-revised Turkish sources. English was natively re-authored rather than literally translated.
- Every reference was re-audited. Bibliographic and documentation defects were corrected, and two fabricated grey-literature citations were replaced with verified sources supporting the intended claims.
- Booklet titles were reconciled across frontmatter, headings, navigation, footers, and catalog.

### Added

- Archive and Maps of Content diagrams with bilingual alternative text and captions.
- Restored body tables in seven booklet pairs.

## [3.0.2] - 2026-06-20

Patch release. Provenance and licensing accuracy. An unfiled United States copyright registration claim was removed. Copyright was restated as automatic under the Berne Convention, with provenance evidenced through Zenodo, OpenTimestamps, and public Git history.

### Added

- A `provenance/` directory with a release timestamp record and OpenTimestamps proof.

### Archived

- Zenodo version DOI [10.5281/zenodo.20774182](https://doi.org/10.5281/zenodo.20774182).

## [3.0.1] - 2026-06-20

Patch release. A repository-wide audit corrected confirmed bibliographic, overclaiming, bilingual, and prose defects without changing the reference set or aggregate citation declarations.

### Fixed

- Bibliographic metadata, article numbers, issue numbers, author lists, and proceedings records.
- Two unsupported quantitative claims were softened to match their sources.
- Turkish prose hygiene and bilingual parity were restored.

### Archived

- Zenodo version DOI [10.5281/zenodo.20773322](https://doi.org/10.5281/zenodo.20773322).

## [3.0.0] - 2026-06-12

Major release. The Journal of Open Source Education paper was refreshed to the twenty-one-booklet, twelve-category, twenty-skill surface, and a submission preparation package was added.

### Added

- The anti-AI-trace revision method was added to the paper and grounded in verified literature on detector unreliability and bias.
- `meta/jose-submission.md` and a draft paper PDF workflow.

### Archived

- Zenodo version DOI [10.5281/zenodo.20665696](https://doi.org/10.5281/zenodo.20665696).

## [2.9.0] - 2026-06-12

Minor release. Four booklets raised the released total from seventeen to twenty-one and filled every one of the twelve then-current categories.

### Added

- Material Passport, Ritual Hooks, MCP for the Researcher, and bilingual conference materials.

### Changed

- Citation cores were verified before drafting.
- Pages opted into the Node 24 JavaScript actions runtime.

### Archived

- Zenodo version DOI [10.5281/zenodo.20663876](https://doi.org/10.5281/zenodo.20663876).

## [2.8.0] - 2026-06-12

Minor release. Four booklets raised the released total from thirteen to seventeen and aggregate verified citation declarations from 248 to 306, with zero fabricated citations.

### Added

- IMRAD Scaffolding, Journal Fit and Cover Letters, Qualitative Coding with AI Assistance and Human Oversight, and Managing AI Style Traces in Revisions.
