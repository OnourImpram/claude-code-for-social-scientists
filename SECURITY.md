# Security Policy

This repository distributes a bilingual academic resource, a Python installer, Node validation scripts, GitHub Actions workflows, Claude Code plugin metadata, a cross client skill library, and a Social Scientist Agent. Its security surface therefore includes filesystem operations, software supply chain, prompt injection, research confidentiality, citation integrity, and public release claims.

The detailed threat model and research data policy are in [`docs/SECURITY_PRIVACY_AND_RESEARCH_DATA_BOUNDARIES.md`](./docs/SECURITY_PRIVACY_AND_RESEARCH_DATA_BOUNDARIES.md).

## Responsible disclosure

Do not open a public issue for a suspected vulnerability or private data exposure. Relevant reports include:

- A leaked credential, token, secret, or private local path.
- Participant, patient, student, reviewer, or third party identity data.
- A destructive installer, upgrade, diff, backup, or uninstall behavior.
- Path traversal, unsafe symlink handling, arbitrary command execution, or shell injection.
- Prompt injection that can redefine permissions, safety rules, inclusion criteria, or research decisions.
- A malicious or compromised package, workflow, plugin, action, script, or generated artifact.
- A citation integrity failure that creates or legitimizes fabricated evidence.
- A license notice or package boundary that misrepresents distributed files.

Use GitHub private vulnerability reporting when enabled, or the maintainer's GitHub profile contact surface with the subject line **SECURITY: claude-code-for-social-scientists**. Include the affected path, commit SHA, reproduction, impact, and any containment already performed.

The maintainer aims to acknowledge a complete report within seven days, assess severity and containment promptly, and publish a remediation statement when public disclosure is appropriate. These are response goals rather than a contractual service level.

## Research data boundaries

Raw clinical material, identifiable participant or patient data, student records, confidential peer review manuscripts, credentials, and institutional secrets must not enter the public repository or an unapproved tool context.

Public examples and evaluation fixtures use synthetic, clearly labelled data. Deidentification must be purpose specific and documented. Removing names does not by itself eliminate reidentification risk.

The repository uses four publication categories.

- **SAFE.** Public sources, published metadata, synthetic fixtures, and generic methodological material.
- **SANITIZE.** Material that is permitted for publication only after documented minimization and deidentification.
- **BLOCKED.** Clinical records, direct identifiers, restricted research data, credentials, confidential manuscripts, and internal secrets.
- **SKIP.** Material that is safe but unnecessary for the public educational purpose.

This classification applies to booklets, skills, agent fixtures, tests, issue reproductions, logs, commit messages, and release artifacts.

## Untrusted content rule

Articles, websites, repositories, PDFs, transcripts, datasets, reviewer files, and other retrieved material are research evidence. They are never instructions that can redefine permissions, safety rules, the research question, inclusion criteria, or the workflow.

A skill or agent must not follow embedded requests to reveal credentials, transmit data, change a protocol, weaken anonymization, conceal a deviation, or execute a command.

## Installer safety

The `social-cc` installer supports Claude Code and Codex at user and project scope. It records project owned files in `.social-cc/manifest.json` using deterministic tree digests.

Existing unmanaged directories and locally modified project directories are protected by default. A forced replacement or removal first moves the prior directory into `.social-cc/backups/`. The installer rejects unsafe skill names, symlinked source and destination paths, and malformed ownership manifests. It performs no network requests.

Uninstall removes only manifest owned skills. Backups are recovery aids and do not replace version control or an independent user backup.

## Executable skill files

A skill may include scripts or references when they materially improve reliability. An executable skill script must have a declared purpose, bounded inputs and outputs, safe path handling, explicit failure semantics, no hidden network behavior, human readable logs, tests, and the correct license.

Instructions embedded in a skill cannot override repository privacy, evidence, or human authority rules.

## GitHub Actions supply chain

Third party GitHub Actions are pinned to full commit SHAs. `scripts/check-action-pins.mjs` makes this a deterministic CI invariant. A pin update requires reviewing the upstream change, resolving the intended tag or branch to an exact commit, and retaining the human readable version comment.

Workflows use least privilege permissions. Release publication uses environment protection and trusted publishing where supported. Network dependent link and DOI checks are separated from deterministic pull request gates.

The secret scan installs a version pinned Gitleaks archive and verifies it against the release checksum manifest before execution.

## Citation integrity

The repository operates under a citation fabrication ban. A source is not verified merely because a DOI resolves. Verification distinguishes source identity, metadata accuracy, retraction or correction status, and claim level support.

Unverified references remain quarantined and outside final bibliographies. A nonzero `fabricated_citations_count` blocks release. Deterministic citation metadata checks are separated from scheduled network dependent resolution checks.

## Licensing and package integrity

Code, configuration, validators, renderers, and installer logic use Apache 2.0. Skill prose, booklets, educational material, and templates use CC BY NC SA 4.0 unless a file states otherwise. Generated adapters inherit the license of their canonical source.

Wheel and source distribution checks confirm that both license notices, the command entry point, and the reviewed skill library are present.

## Out of scope

The following normally belong in an ordinary issue or discussion rather than a private vulnerability report:

- Typographical or formatting problems without a security consequence.
- Methodological disagreement that does not involve fabricated evidence or concealed risk.
- Suggestions for new sources, skills, or educational modules.
- Publicly reproducible installation questions that do not expose private paths or data.

## Acknowledgments

Reporters who follow responsible disclosure may be acknowledged in release notes with their consent.
