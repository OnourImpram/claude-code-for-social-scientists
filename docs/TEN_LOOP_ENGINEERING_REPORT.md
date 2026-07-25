# Ten Loop Engineering Report

## Executive status

Repository: `OnourImpram/claude-code-for-social-scientists`

Starting default branch: `main`

Starting commit: `ddc15210e5f3790adb0da7f71a465a5cada23f2a`

Development branch: `upgrade/social-scientist-dual-client-agent`

Target release metadata: `4.0.0`, dated `2026-06-22`

Report date: `2026-07-16`

Release readiness at this report draft: **review candidate, not automatically mergeable**. Clean GitHub-hosted validation and maintainer review remain required. Native authenticated Claude Code and Codex sessions are not available in the execution environment and are reported as an explicit limitation rather than a passed smoke test.

## Scope and method

The work followed ten iterative engineering loops covering repository truth, scholarly and bilingual integrity, skill responsibilities, cross-client distribution, security, education, contract freeze, agent development, evaluation, and release hardening.

Each loop used repository inspection, explicit hypotheses, evidence gathering, prioritized implementation, focused verification, adversarial review, documentation truth review, and a cohesive commit group. Full clean-environment validation is concentrated in the release-candidate loop because the local container could not clone the repository after a DNS failure and the connected development workspace was unavailable. Focused Python work was tested in an isolated local fixture. Repository-wide verification is delegated to the branch pull request checks and is not described as passed until GitHub reports it.

A process deviation is recorded transparently. The first canonical Social Scientist Agent draft was committed after the installer, release truth, evidence vocabulary, privacy model, and client architecture were established, but before the final skill responsibility matrix and evaluation corpus were committed. The agent was subsequently rechecked against the frozen contracts. The history was not rewritten to conceal this sequencing deviation.

## Baseline results

### Repository preflight

| Item | Result |
|---|---|
| Repository identity | Confirmed |
| Default branch | `main` |
| Starting SHA | `ddc15210e5f3790adb0da7f71a465a5cada23f2a` |
| Dedicated branch | Created |
| Direct work on `main` | Avoided |
| Connected development workspace | Unavailable |
| Local Git clone | Failed because the execution container could not resolve GitHub |
| Full baseline command suite | Not executed locally, therefore not claimed as passed |
| Focused CLI tests | Executed in an isolated local fixture |
| Official client documentation | Verified against current Anthropic and OpenAI documentation |

### Initial product truth discrepancies

1. `package.json` and `pyproject.toml` described version `4.0.0`, while the README pair, roadmap, paper, website, and package landing page contained older versions, counts, and capability claims.
2. Public surfaces disagreed on booklet count, language file count, category count, skill count, supported clients, and installation methods.
3. The Python source fallback version was stale.
4. The installer could recursively delete an existing skill directory under `--force` without an ownership manifest, provenance check, diff, backup, upgrade path, or uninstall path.
5. The project described itself as having no executable application surface despite shipping Python, Node, workflows, and plugin metadata.
6. The security policy stated that third-party GitHub Actions were pinned to immutable commit SHAs, while workflows used mutable tags.
7. Codex portability was discussed without a complete installed distribution route.
8. The existing validator hardcoded skill names and treated executable files inside skill directories as categorically invalid.
9. No canonical Social Scientist Agent, generated adapter parity check, or cross-client evaluation corpus existed.
10. Educational onboarding assumed more terminal and repository familiarity than the target social science audience should be required to possess.

## Current architecture map

```text
                                  meta/release.json
                                         |
                                         v
                         deterministic release truth checks
                                         |
                                         v
.claude/skills/<skill>/SKILL.md ----> Python wheel bundle
        canonical source              social_cc_plugin/skills
             |                                  |
             |                                  v
             |                         social-cc lifecycle CLI
             |                         install, diff, upgrade,
             |                         doctor, uninstall, backup
             |                           /                 \
             |                          v                   v
             |                 .claude/skills        .agents/skills
             |                  Claude Code              Codex
             |
             +----> Claude Code plugin skill distribution

core/agents/social-scientist.md
             |
             +----> .claude/agents/social-scientist.md
             |
             +----> agents/social-scientist.md
             |
             +----> AGENTS.md guidance for Codex

booklets/<category>/<booklet-id>/{tr.md,en.md}
             |
             +----> MkDocs educational platform
             |
             +----> companion skill responsibility matrix
             |
             +----> synthetic research project and evaluation corpus
```

## Current product truth table

| Capability | Classification | Evidence |
|---|---|---|
| Thirty-three bilingual released booklets | Shipped and reachable | `booklets/`, `CATALOG.md`, release truth validator |
| Thirty-two reviewed skills | Shipped and reachable | `.claude/skills/` |
| Claude Code user skill installation | Shipped | `social-cc install --client claude-code` |
| Claude Code project skill installation | Shipped | `social-cc install --client claude-code --scope project` |
| Codex user skill installation | Shipped | `social-cc install --client codex` |
| Codex project skill installation | Shipped | `social-cc install --client codex --scope project` |
| Both-client installation | Shipped | `social-cc install --client all` |
| Dry run, diff, upgrade, doctor, uninstall | Shipped | CLI implementation and tests |
| Ownership manifest | Shipped | `.social-cc/manifest.json` at installation target |
| Modified-file protection and backups | Shipped | digest comparison and `.social-cc/backups/` |
| Claude Code plugin | Shipped | `.claude-plugin/` |
| Native Codex plugin package | Not shipped | Explicitly excluded from public claims |
| Canonical Social Scientist Agent | Shipped in source | `core/agents/social-scientist.md` |
| Claude Code agent adapters | Shipped | `.claude/agents/`, `agents/` |
| Codex repository guidance | Shipped | `AGENTS.md` |
| Native authenticated host invocation | Environmentally unverified | Requires installed, authenticated clients |
| Release truth derivation | Shipped | `meta/release.json`, `validate-release-truth.mjs` |
| Skill and booklet structural validation | Shipped | `validate-platform.mjs` |
| Immutable action pin validation | Shipped | `check-action-pins.mjs` |
| Bilingual routing corpus | Shipped | thirty-two skills and 192 generated cases |
| Agent scenario corpus | Shipped | eighteen valid and adversarial scenarios |
| Synthetic end-to-end research project | Shipped | `examples/synthetic-research-project/` |
| Optional Mneme or Mergen integration | Design only | No dependency or public capability claim |

## Master issue ledger

| ID | Priority | Loop | Subsystem | Evidence and impact | Correction | Verification | Status |
|---|---|---|---|---|---|---|---|
| RT-001 | P1 | 1 | Release truth | Public versions and counts disagreed, making citation and installation claims unreliable | Added canonical release record and deterministic mirrors | Release truth script and CI gate | Fixed |
| RT-002 | P2 | 1 | Author metadata | Public surfaces contained stale academic-status wording | Replaced with maintainer-approved current role descriptions and removed unsupported affiliation detail | Documentation review and CFF alignment | Fixed |
| CLI-001 | P1 | 4 | Installer | `--force` could recursively delete an existing directory without ownership evidence or recovery | Added manifests, digests, staged replacement, protection, and backups | Focused unit tests, Ruff, strict mypy | Fixed |
| CLI-002 | P1 | 4 | Client support | Package installed only to Claude Code paths | Added Claude Code, Codex, and all-client targets at user and project scope | Target-resolution and lifecycle tests | Fixed |
| CLI-003 | P2 | 4 | Lifecycle | Upgrade, diff, and uninstall were absent | Added explicit commands and ownership-safe behavior | Focused tests | Fixed |
| VAL-001 | P2 | 3 | Validation | Skill names were hardcoded and scripts were forbidden regardless of safety | Made an extensible platform validator authoritative and retained the old validator as legacy | Dynamic skill discovery and extension-layout checks | Fixed |
| SEC-001 | P1 | 5 | Security policy | Policy denied the executable surface that actually existed | Rewrote security policy and detailed threat model | Documentation truth review | Fixed |
| SEC-002 | P1 | 5 | Supply chain | Policy promised immutable action pins while workflows used tags | Resolved every third-party action to a full commit SHA and added a structural gate | Action pin validator | Fixed |
| SEC-003 | P1 | 5 | Prompt injection | Retrieved research content had no repository-wide instruction boundary | Added untrusted-content rule to agent, skills architecture, security, education, and fixtures | Adversarial scenario corpus | Fixed |
| LIC-001 | P2 | 5 | Licensing | Package users needed clearer code and prose license boundaries | Added architecture, security, README, package, and wheel-content notices | Wheel inspection gate | Fixed |
| EDU-001 | P2 | 6 | Onboarding | Curriculum did not provide a complete progressive route for terminal-new researchers | Added four learning tracks, exercises, reflection, self-assessment, and accessibility guidance | Documentation review | Fixed |
| EDU-002 | P2 | 6 | Safe practice | No end-to-end synthetic study demonstrated the real toolkit | Added protocol, preregistration, data, analysis, source ledger, traps, disclosure, and release checklist | Reproducibility tests | Fixed |
| SKL-001 | P2 | 3 | Skill boundaries | Overlap and handoffs were not centrally auditable | Added a responsibility and handoff matrix for all thirty-two skills | Platform and evaluation validators | Fixed |
| AGT-001 | P1 | 8 | Agent | No dedicated Social Scientist Agent existed | Added canonical evidence-disciplined orchestration contract | Exact adapter parity and contract tests | Fixed |
| AGT-002 | P2 | 8 | Agent parity | Separate adapters could drift | Added deterministic renderer and check | Byte-for-byte parity test | Fixed |
| EVAL-001 | P2 | 7 and 9 | Evaluation | No complete routing and adversarial corpus existed | Added 192 generated skill cases and eighteen agent scenarios | Evaluation corpus validator | Fixed |
| DOC-001 | P2 | 1 and 10 | Documentation | README pair, catalog, roadmap, paper, site, package page, and CFF described different products | Reauthored and aligned public mirrors | Release truth markers and documentation review | Fixed |
| DOC-002 | P3 | 6 and 10 | MkDocs | Manual navigation omitted the platform architecture and learning surface | Added a platform navigation section and strict build workflow | MkDocs strict CI | Fixed pending branch CI |
| SCI-001 | P2 | 2 | Scholarly audit | A complete new claim-level reread of every source in all thirty-three pairs was not feasible in the execution environment | Preserved citation quarantine, DOI parity, existing verified declarations, and scheduled liveness checks, while recording this limit | Deterministic checks do not substitute for human source review | Open limitation |
| HOST-001 | P2 | 9 and 10 | Host smoke tests | Native authenticated Claude Code and Codex sessions were unavailable | Added install-path tests, official integration docs, and honest parity boundaries | Native invocation remains unverified | Open limitation |

No unresolved P0 issue was found. No unresolved P1 issue is recorded at this report stage.

## Product invariant ledger

| Invariant | Enforcement |
|---|---|
| No fabricated citation enters a release | Booklet metadata, zero-count gate, source quarantine, evaluation traps |
| Unverified references remain quarantined | Source passport, DOI verifier, agent evidence contract |
| Turkish and English pairs remain discoverable | Derived pair checks and MkDocs navigation |
| Stable booklet identifiers do not change | Directory and frontmatter validation |
| Current release facts remain consistent | `meta/release.json` and public marker validation |
| Skills have one reviewed source | `.claude/skills`, no committed `.agents/skills` mirror |
| Generated agent adapters do not drift | Renderer and byte-for-byte parity checks |
| Client metadata does not change scientific logic | Shared canonical skill and agent source |
| Installation does not destroy unrelated files | Ownership manifest and unmanaged-file protection |
| Upgrades are reviewable and recoverable | `diff`, dry run, digest comparison, backups |
| Uninstall removes only project-owned artifacts | Manifest-owned removal |
| Skills retain bounded responsibilities | Responsibility matrix and routing corpus |
| Safety gates cannot be weakened by another skill | Agent and skill safety contract |
| Human scientific authority remains final | Agent identity, method boundaries, documentation |
| Observed evidence, inference, and uncertainty remain distinct | Evidence vocabulary and contract tests |
| Optional integrations remain optional | No core dependency or silent transmission |
| Code and educational licensing remain explicit | Dual license files, docs, package and wheel checks |

## Loop 1. Repository truth, architecture, and release integrity

### Hypotheses

1. Public mirrors describe different releases.
2. Counts are manually repeated and vulnerable to drift.
3. Package, plugin, paper, website, CFF, and changelog are not aligned.

### Inspection and evidence

The package metadata described version `4.0.0`, while several public surfaces described older versions and smaller product counts. The repository already contained thirty-three released bilingual pairs and thirty-two skills, but the README pair, paper, roadmap, and package landing page did not consistently expose that state.

### Changes

- Added `meta/release.json` as the canonical machine-readable release record.
- Added `scripts/validate-release-truth.mjs` to derive booklet, language, category, skill, and citation declaration counts.
- Validated version mirrors in Python, Node, CFF, plugin, marketplace, and changelog metadata.
- Rewrote the README pair, catalog, roadmap, paper, website, package landing page, and citation record.
- Added exact machine-readable markers to public mirrors without replacing readable prose.

### Focused verification

The release-truth script was exercised against a synthetic repository fixture before commit. Repository-wide execution is delegated to branch CI.

### Adversarial review

The validator distinguishes a declaration count from a unique source count. It does not infer that DOI parity proves claim-level parity. It rejects nonzero fabricated citation declarations.

### Documentation truth review

Public claims now distinguish shipped Claude Code support, shipped Codex skill installation, and unshipped native Codex plugin packaging.

### Next-loop seed

Release truth can still conceal a source that resolves but does not support the claim. Scholarly and bilingual integrity required a separate loop.

## Loop 2. Scholarly content, citation, and bilingual integrity

### Hypotheses

1. Existing citation counts could be misdescribed as unique sources.
2. DOI equality could conceal conceptual or claim-level drift.
3. Author role and affiliation wording could be stale.

### Inspection and evidence

Booklet frontmatter contains language, stable identifier, release status, human review, verified citation declaration count, and fabricated citation declaration count. Existing infrastructure verified DOI presence and bilingual parity but could not itself prove source-to-claim support.

### Changes

- Clarified declaration counts across public surfaces.
- Added bilingual frontmatter and DOI parity validation.
- Preserved the distinction between source identity, bibliographic metadata, source status, and claim support.
- Replaced stale author-status language with current maintainer-approved roles.
- Added explicit limits stating that deterministic checks do not certify claim-level validity.

### Focused verification

The platform validator checks paired language files, stable identifiers, release status, human review, verified count parity, zero fabricated declarations, and DOI-set parity.

### Adversarial review

The synthetic source ledger contains both a fabricated DOI and untrusted embedded instructions. Neither can enter a bibliography or change workflow rules.

### Documentation truth review

The paper, CFF, README pair, and package page now use consistent author and release metadata.

### Limitation

This loop did not re-read every full-text source supporting every claim in all thirty-three bilingual pairs. That human scholarly audit remains explicitly open.

### Next-loop seed

The project required an auditable responsibility boundary for every operational skill.

## Loop 3. Skill library quality and capability coverage

### Hypotheses

1. Skill responsibilities and handoffs overlap without a central registry.
2. Static skill-name lists create drift.
3. A categorical ban on skill scripts prevents useful deterministic checks.

### Inspection and evidence

Thirty-two canonical skill directories existed. Skill files shared a common heading structure, but public documentation did not centrally state each primary responsibility, boundary, and handoff.

### Changes

- Added a complete skill responsibility and handoff matrix.
- Classified the lifecycle pipeline as a router rather than the Social Scientist Agent.
- Added dynamic skill discovery to the authoritative platform validator.
- Permitted bounded `scripts`, `references`, `assets`, and `client` directories.
- Required script-purpose documentation and safe extension checks when a skill ships executable helpers.
- Prevented a second committed `.agents/skills` library.

### Focused verification

The evaluation registry covers every canonical skill name. Public skill mirrors must name every current skill. The platform validator compares the canonical directory set with the routing registry.

### Adversarial review

Candidate gaps were not converted automatically into new skills. Theory construction, sampling and power, survey design, psychometrics, causal inference, measurement invariance, formal mixed-methods integration, meta-analysis, and replication packages remain evaluated gaps rather than fabricated completeness claims.

### Documentation truth review

The README pair and catalog expose all thirty-two skill names and link to the responsibility matrix.

### Next-loop seed

A coherent skill library still needed safe, real distribution paths for both clients.

## Loop 4. Single-source architecture and dual-client support

### Hypotheses

1. Copying skills into another directory would create a second source of truth.
2. The existing installer could not distinguish user files from project files.
3. Codex support was descriptive rather than installed and testable.

### Inspection and evidence

The Python package bundled `.claude/skills` and installed to Claude Code paths. No ownership manifest, Codex target, upgrade, diff, or uninstall existed.

### Changes

- Retained `.claude/skills` as the canonical reviewed source for backward compatibility.
- Added Claude Code and Codex user and project targets.
- Added `--client claude-code`, `--client codex`, and `--client all`.
- Preserved the existing `--project` alias.
- Added manifests, tree digests, staged copies, dry runs, diffs, upgrades, backups, doctor checks, and safe uninstall.
- Added Unicode path and symlink protections.
- Documented real client differences rather than claiming identical host behavior.

### Focused verification

The initial redesign passed twenty-six focused tests, Ruff, and strict mypy in the isolated local fixture. Tests cover client and scope combinations, unmanaged files, modified files, backup behavior, Unicode paths, invalid names, and symlinks.

### Adversarial review

`--force` now means preserve and replace. It does not mean recursive deletion without recovery. Uninstall consults manifest ownership and does not remove unrelated skill directories.

### Documentation truth review

README, package page, architecture, and integration guides expose the complete lifecycle commands and recovery semantics.

### Next-loop seed

Executable distribution expanded the repository threat model and made supply-chain claims enforceable rather than descriptive.

## Loop 5. Security, privacy, licensing, and supply chain

### Hypotheses

1. Security documentation understates the executable attack surface.
2. Workflow pin policy and workflow reality disagree.
3. Research content can carry prompt injection.
4. License boundaries may be unclear in installed artifacts.

### Inspection and evidence

The project ships Python, Node, workflows, plugin metadata, skills, and agent files. Mutable GitHub Action tags contradicted the written policy.

### Changes

- Rewrote `SECURITY.md` for the actual executable and research-data surface.
- Added a detailed threat model and data classification policy.
- Added a repository-wide untrusted-content rule.
- Pinned every third-party GitHub Action to a full commit SHA.
- Added a structural action-pin validator.
- Added least-privilege workflow permissions.
- Added checksum verification for the pinned Gitleaks archive.
- Separated deterministic checks from scheduled network-dependent link and DOI checks.
- Added wheel license and skill-content inspection.

### Focused verification

Action references were resolved to exact commits before workflow edits. The pin validator rejects any nonlocal `uses:` reference without a forty-character commit SHA.

### Adversarial review

Threats include path traversal, symlinks, destructive replacement, unsafe deletion, hidden telemetry, credential disclosure, clinical and participant data, confidential review material, malicious Markdown and YAML, prompt injection, and source fabrication.

### Documentation truth review

Security claims now match the executable surface. Dual licensing is explained by file category rather than a single package-level label.

### Next-loop seed

The platform required a safe entry path for researchers who are not software engineers.

## Loop 6. Educational platform and onboarding

### Hypotheses

1. A researcher can be methodologically expert and terminal-new.
2. The educational resource needs progressive practice rather than a flat reference collection.
3. Real data is unnecessary for learning the complete workflow.

### Changes

- Added four progressive learning tracks.
- Added audience, prerequisites, effort, objectives, guided workflows, exercises, reflection, and self-assessment.
- Added accessibility, mobile, print, dark-mode, and regional-infrastructure considerations.
- Added a fully synthetic project with protocol, preregistration, source ledger, prompt injection fixture, generated dataset, standard-library analysis, expected output, disclosure, and release checklist.
- Added platform documentation to MkDocs navigation.
- Rebuilt the landing page with semantic HTML, keyboard access, dark mode, print support, bilingual content, and no tracking.

### Focused verification

The synthetic analysis was executed locally and produced sixty total rows, fifty-eight complete pairs, and a generated guided-minus-comparison mean-change estimate of `4.862069`. A test also checks rejection of a nonsynthetic identifier.

### Adversarial review

The fixture contains a fabricated DOI and embedded prompt injection, both explicitly labelled. It also contains valid work that the agent should complete, preventing an evaluation strategy optimized only for refusal.

### Documentation truth review

The educational material states that the generated result is not empirical evidence and cannot support real-world intervention claims.

### Next-loop seed

Agent development required frozen evidence, skill, safety, installation, and output contracts.

## Loop 7. Contract freeze, evaluation foundation, and capability review

### Frozen contracts

1. Skill identity and directory naming.
2. Skill responsibility and handoff model.
3. Canonical source and generated-client rules.
4. Installer ownership and recovery model.
5. Research stage vocabulary.
6. Evidence vocabulary.
7. Data sensitivity and untrusted-content rules.
8. Human decision boundaries.
9. Agent output and verification contract.
10. Bilingual response and conceptual-equivalence policy.

### Evaluation foundation

- Added a compact responsibility registry for all thirty-two skills.
- Deterministically generates two positive, two negative, one boundary, and one safety case per skill.
- Guarantees Turkish and English cases for every skill.
- Added eighteen interdisciplinary and adversarial agent scenarios.
- Includes at least two valid workflow controls.

### Competitive and platform review

Current official Claude Code documentation was used for `.claude/skills`, `~/.claude/skills`, `.claude/agents`, user agents, and plugin agents. Current official Codex documentation was used for `.agents/skills`, `~/.agents/skills`, and `AGENTS.md` behavior. Shared `SKILL.md` logic was separated from host-specific agent and plugin capabilities.

### Prerequisite decision

#### SOCIAL SCIENTIST AGENT PREREQUISITES: SATISFIED AFTER CONTRACT REVALIDATION

### Recorded process deviation

The first canonical agent commit preceded the final responsibility-matrix and corpus commits. The completed agent was revalidated against the frozen contracts. This sequencing deviation remains visible in history.

### Next-loop seed

The agent could now be developed as an orchestrator rather than a duplicate skill library.

## Loop 8. Social Scientist Agent

### Identity

The agent is a workflow navigator, methodological assistant, skill orchestrator, evidence disciplinarian, reproducibility partner, writing and revision partner, privacy boundary enforcer, bilingual academic companion, and teacher of agentic research practice.

It is not a principal investigator, ethics committee, statistician of record, legal adviser, clinical supervisor, automatic coauthor, or source of evidence.

### Operating cycle

```text
ORIENT → INSPECT → CLASSIFY → SELECT SKILLS → WORK → VERIFY → HAND OFF
```

### Changes

- Added one canonical agent source.
- Added generated Claude Code project and plugin adapters.
- Added Codex repository guidance through `AGENTS.md`.
- Added deterministic adapter rendering and drift detection.
- Added quantitative, qualitative, mixed-methods, review, writing, bilingual, citation, privacy, and abstention boundaries.

### Focused verification

Python contract tests and the Node renderer require both Claude adapters to match the canonical source byte for byte. Required evidence categories and operating-cycle phrases are tested.

### Adversarial review

The agent refuses to convert association into causation, significance into practical importance, qualitative frequency into prevalence, a suggestion into a finding, an unverified citation into a reference, a draft into a final submission, or a preregistration deviation into a confirmatory result.

### Documentation truth review

Codex is not claimed to natively consume the Claude Code subagent Markdown format. Codex receives the shared contract through repository guidance and installed skills.

### Next-loop seed

The agent and skill library required controlled cross-method scenarios and valid controls.

## Loop 9. Cross-client evaluation and dogfooding

### Scenario coverage

The corpus includes psychology literature review, sociology survey boundaries, education interviews, public-health causal claims, political-science mixed methods, anthropology fieldnotes, evidence synthesis, grants, reviewer response, teaching, open science, Turkish-English construct validity, prompt injection, false client parity, and unnecessary all-skill invocation.

### Measures represented

1. Stage diagnosis.
2. Skill routing accuracy.
3. False and missed invocation.
4. Citation fabrication and claim mismatch detection.
5. Methodological boundaries.
6. Privacy and high-trust escalation.
7. Bilingual conceptual fidelity.
8. Researcher control.
9. Cross-client parity and asymmetry.
10. Context efficiency.
11. Abstention quality.
12. Valid workflow acceptance.

### Focused dogfooding

The synthetic project exercises preregistration, statistical summary, missingness, source quarantine, prompt injection, disclosure, and release packaging. Installer tests exercise both client paths without requiring credentials.

### Limitation

The environment did not permit an authenticated native Claude Code or Codex session. Therefore agent discovery and invocation inside the real host user interfaces are not claimed as passed. Official file-location contracts and installer paths are covered, but host-level smoke tests remain a maintainer release action.

### Next-loop seed

A final zero-assumption inspection and clean hosted suite were required.

## Loop 10. Release-candidate hardening

### Reinspection focus

- Release and author metadata.
- Public counts and client claims.
- Installer ownership, recovery, and path safety.
- Agent source and adapter parity.
- Skill registry and evaluation completeness.
- Security and workflow pinning.
- Package contents and dual licenses.
- MkDocs navigation and website accessibility.
- Synthetic fixture reproducibility.
- Stale Claude-only language and unsupported parity claims.

### Changes

- Made the extensible platform validator authoritative.
- Retained the previous validator as a legacy diagnostic rather than the release gate.
- Added evaluation validation to `npm run verify` and CI.
- Added strict MkDocs platform navigation.
- Added complete public documentation alignment and an unreleased changelog section.
- Prepared the branch for a draft pull request without automatic merge.

### Final feasible validation plan

The pull request must report each item separately.

| Check | Expected command or workflow | Status at report draft |
|---|---|---|
| Markdown lint | `npm run lint` | Pending GitHub CI |
| Platform validation | `npm run validate` | Pending GitHub CI |
| Release truth | `npm run validate:truth` | Pending GitHub CI |
| Agent parity | `npm run check:agents` | Pending GitHub CI |
| Action pins | `npm run check:actions` | Pending GitHub CI |
| Evaluation corpus | `npm run check:evaluation` | Pending GitHub CI |
| Python tests | `python -m pytest tests/ -v` | Focused local tests passed, full branch pending CI |
| Ruff | `ruff check .` | Focused local code passed, full branch pending CI |
| Strict mypy | `mypy --strict src tests` | Focused local code passed, full branch pending CI |
| Package build | `python -m build` | Pending GitHub CI |
| Wheel inspection | CI package job | Pending GitHub CI |
| Isolated install | CI package job | Pending GitHub CI |
| MkDocs strict build | Pages build job | Pending GitHub CI |
| CFF validation | Citation workflow | Pending GitHub CI |
| Secret scan | Secret-scan workflow | Pending GitHub CI or schedule |
| External links | Scheduled link workflow | Network-dependent, not a pull-request gate |
| Live DOI resolution | Scheduled DOI workflow | Network-dependent, not a pull-request gate |
| Claude Code native invocation | Authenticated host session | Unavailable |
| Codex native invocation | Authenticated host session | Unavailable |

## Commit groups

The branch uses small thematic commits for:

1. Safe dual-client CLI implementation.
2. Installer regression tests.
3. Version fallback correction.
4. Canonical release facts.
5. Release truth validation.
6. Platform architecture and client integration.
7. Canonical agent and generated adapters.
8. Skill responsibilities and handoffs.
9. Security and privacy threat model.
10. Supply-chain and CI hardening.
11. Public documentation and scholarly metadata alignment.
12. Learning pathways and synthetic research project.
13. Routing and adversarial evaluation corpus.
14. Extensible platform validation and documentation navigation.

## Citation corrections and scholarly decisions

- Public text now calls `566` a verified citation declaration count rather than a unique source count.
- The repository continues to declare zero fabricated citations in released booklet metadata.
- The synthetic fabricated DOI is clearly labelled and quarantined.
- DOI resolution is not treated as claim support.
- Network-dependent source liveness is separated from deterministic release gates.
- No new scholarly source was added merely to increase the citation count.
- The complete claim-level full-text audit remains a human scholarly limitation.

## New skill decisions

No new method skill was added in this upgrade. The existing thirty-two skills were treated as the current shipped library. Candidate additions were rejected for this branch because responsibility, evidence base, boundedness, and evaluation were not yet sufficient.

Rejected automatic additions include theory development, sampling and power, survey design, psychometric scale development, experimental design, causal inference, measurement invariance, meta-analysis, formal mixed-methods integration, and replication package management. Their absence is documented rather than silently covered by an overbroad agent.

## Security findings

The highest-risk corrected defect was destructive installation without ownership evidence or recovery. The second was mismatch between immutable-pin policy and mutable workflows. Prompt injection, research confidentiality, credential exposure, symlink behavior, path traversal, hidden telemetry, and licensing were incorporated into the threat model and tests.

## Licensing findings

The repository uses Apache 2.0 for code, configuration, validators, renderers, and installer logic. Skill prose, booklets, educational guides, and templates use CC BY-NC-SA 4.0 unless a file states otherwise. Generated agent adapters inherit the canonical content license. Package and wheel checks require both license notices.

## Remaining limitations

1. Native authenticated Claude Code and Codex invocation was not available.
2. Full claim-level manual rereading of every cited source in all thirty-three bilingual pairs was not completed in this environment.
3. Scheduled external-link, DOI liveness, correction, and retraction checks remain network-dependent.
4. Windows and PowerShell behavior is covered by path-safe Python design but not by a native Windows runner in the current CI matrix.
5. A native Codex plugin package is not shipped and is not claimed.
6. Optional Mneme and Mergen interoperability remains design-only.
7. Coverage percentage is not yet enforced as a numeric threshold. High-risk installer and platform contracts are prioritized over mechanical test-count growth.
8. Website accessibility is improved structurally, but a dedicated automated accessibility scanner is not yet a blocking CI gate.

## Release readiness decision

At the report-draft stage:

- No known P0 issue remains.
- No known P1 issue remains.
- The branch is suitable for draft pull-request review.
- It must not be merged automatically.
- GitHub-hosted checks must be inspected before the readiness statement is upgraded.
- Native host invocation and full scholarly source rereading remain explicitly outside the verified claim set.

The repository is demonstrably stronger than the starting state in release truth, installer safety, cross-client distribution, agent architecture, evaluation, security, education, accessibility, and documentation honesty. That statement is bounded to the committed changes and the verification results reported here. It is not a claim of zero defects.
