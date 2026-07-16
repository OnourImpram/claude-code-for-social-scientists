# Security, Privacy, and Research Data Boundaries

## Security model

This repository distributes executable Python installer code, Node validation scripts, GitHub Actions workflows, Claude Code plugin metadata, skill instructions, and a Social Scientist Agent. It is not only a prose guide. Its security model therefore covers software supply chain, filesystem changes, prompt injection, research confidentiality, and scholarly integrity.

## Protected assets

1. Participant, patient, student, reviewer, and researcher identity data.
2. Clinical records, interview material, fieldnotes, and confidential manuscripts.
3. Credentials, tokens, institutional secrets, and private paths.
4. Research protocols, preregistrations, source ledgers, analysis decisions, and provenance.
5. Citation identity, claim to source alignment, and retraction status.
6. User modified skills and unrelated client configuration.
7. Package, plugin, workflow, and release integrity.
8. Turkish and English conceptual parity.

## Trust boundaries

### Repository content

Committed source is reviewable but not automatically safe. Markdown, YAML, scripts, workflows, fixtures, and generated artifacts can all introduce risk. Executable files receive code review and tests. Prose receives privacy, citation, and prompt injection review.

### Retrieved content

Articles, websites, repositories, PDFs, transcripts, datasets, reviewer files, and other external material are untrusted research content. Instructions embedded in them cannot redefine permissions, safety rules, the research question, inclusion criteria, tool access, or the workflow.

### Client hosts

Claude Code and Codex control their own permissions, sandboxing, network access, logs, and tool availability. The repository must not claim stronger isolation than the host provides. Users remain responsible for institutional approval and client configuration.

### Optional integrations

MCP servers, reference managers, memory systems, verification services, and other integrations are separate trust domains. They remain optional. The core package does not require credentials, telemetry, or external data transmission.

## Sensitive data classification

### Public

Published sources, public metadata, synthetic datasets, generic examples, and approved open science artifacts.

### Internal

Unpublished drafts, non identifying project notes, internal review records, and analysis plans that are not intended for public release.

### Restricted

Deidentified participant data, confidential peer review material, embargoed manuscripts, student records, and institutional information whose use is authorized only in a controlled environment.

### Prohibited in unapproved tools

Raw clinical material, direct identifiers, credentials, institutional secrets, consent incompatible data, and data whose reidentification risk has not been assessed.

Classification is contextual. Removing names does not automatically make a dataset safe.

## Data minimization gate

Before any model or external tool receives research material:

1. Confirm the purpose and lawful or ethical basis.
2. Identify the minimum fields required.
3. Remove direct identifiers.
4. Generalize or suppress quasi identifiers when necessary.
5. Replace real examples with synthetic fixtures where possible.
6. Record transformations and residual risk.
7. Confirm that consent, ethics approval, institutional policy, and contracts permit the processing.
8. Confirm the client and integration are approved for the data class.
9. Stop and escalate unresolved legal, clinical, ethical, or institutional questions.

The `sensitive-data-anonymization-gate` skill may structure this review. It cannot authorize processing.

## Installer threat model

### Threats

1. Recursive deletion of user modified or unrelated skill directories.
2. Path traversal through malicious skill names.
3. Symlink redirection outside the intended client directory.
4. Partial installation after interruption.
5. Corrupt or forged ownership manifests.
6. Unreviewable upgrades.
7. Removal of files not created by the project.
8. Hidden network activity.

### Controls

1. Skill names are restricted to lower case letters, numbers, and hyphens.
2. Skill sources and destinations reject symlinks.
3. Directory trees are hashed with deterministic SHA 256 digests.
4. `.social-cc/manifest.json` records ownership, client, scope, version, and installed digest.
5. Existing unmanaged files are protected by default.
6. Locally modified project files are protected by default.
7. Forced replacement and removal first move the prior directory into `.social-cc/backups/`.
8. New content is staged before placement.
9. Manifest writes are atomic.
10. Dry run, diff, upgrade, doctor, and uninstall are explicit commands.
11. The installer performs no network requests.
12. Tests cover user and project scopes, both clients, Unicode paths, symlinks, modification protection, backups, and removal ownership.

A backup is a recovery aid, not a substitute for version control or a user backup policy.

## Skill and agent prompt injection

Skills and the Social Scientist Agent must treat retrieved instructions as data. A malicious paper cannot instruct the agent to reveal credentials, change inclusion criteria, weaken anonymization, ignore a preregistration, or run a command.

A skill may execute a bundled script only when:

1. The purpose is declared.
2. Inputs and outputs are bounded.
3. Paths are validated.
4. Network behavior is absent or explicitly documented and approved.
5. Subprocess arguments are not constructed through unsafe shell interpolation.
6. Failure behavior is explicit.
7. Logs do not expose sensitive content.
8. Tests cover normal and adversarial cases.
9. The script has the correct license.

## Citation integrity as a security property

Citation fabrication and claim misattribution can corrupt a manuscript, review, ethics application, or policy brief. The repository therefore treats reference integrity as a protected asset.

1. Unverified references remain quarantined.
2. DOI resolution is separated from claim level verification.
3. Deterministic metadata checks are separated from network dependent checks.
4. Retractions, corrections, and expressions of concern are checked for load bearing sources.
5. Bilingual citation parity is checked without assuming that identical DOI lists prove conceptual parity.
6. A nonzero fabricated citation count blocks release.

## Supply chain

GitHub Actions use least privilege permissions. The repository policy and workflow reality must match. If third party actions are required to be pinned to full commit SHAs, CI enforces that rule. A mutable major tag must not be described as an immutable pin.

Python and Node dependencies are locked or constrained through committed metadata. Release workflows use trusted publishing where supported. Wheels and source distributions are inspected before release. A clean environment installation verifies that license notices, skills, command entry points, and metadata are present.

## Logging and telemetry

The core package contains no hidden telemetry. User facing logs identify operations and paths needed for recovery. They do not print file contents, credentials, or research data.

Host applications and optional services may have separate logging and retention. Users must evaluate those policies for the relevant data class.

## Licensing boundaries

Code, configuration, validators, renderers, and installer logic use Apache 2.0. Skill prose, booklets, educational content, and templates use CC BY NC SA 4.0 unless a file states otherwise. Generated adapters inherit the license of their canonical content.

Package and plugin distributions must include clear notice of both licenses. A package level SPDX expression does not remove the need to explain which files are governed by which terms.

## Incident response

A suspected credential leak, private data exposure, destructive installer defect, prompt injection path, malicious workflow change, citation integrity failure, or supply chain compromise should be reported privately through the repository's security reporting surface.

The report should include the affected path, commit SHA, reproduction, impact, and any containment already performed. Public disclosure should follow containment and maintainer review.

## Researcher checklist

Before using the platform on a real project, confirm:

1. The project data classification.
2. Institutional and ethics permissions.
3. Client and integration approval.
4. A deidentification and minimization record.
5. A version controlled project or backup.
6. An explicit citation quarantine process.
7. A human decision log for methodological boundaries.
8. A disclosure plan for AI assistance.
9. A recovery path for installer changes.
10. A final human review before submission or release.
