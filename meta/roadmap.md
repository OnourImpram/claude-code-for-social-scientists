# Roadmap

<!-- release-facts: version=5.0.0 booklets=33 language_files=66 categories=14 skills=32 verified=566 fabricated=0 -->

This roadmap describes the public development direction of `OnourImpram/claude-code-for-social-scientists`. Dates are planning targets rather than commitments. Repository claims are limited to capabilities that are implemented, reachable, and tested.

## Current baseline

The current release metadata is v5.0.0, dated 2026-07-26. The repository contains thirty three released bilingual booklets, sixty six language files, fourteen categories, thirty two reviewed skills, 566 verified citation declarations, and zero fabricated citation declarations.

The v4 platform line adds a safe cross client installer, Claude Code and Codex skill discovery paths, ownership manifests, reviewable upgrades, recoverable removal, release truth validation, immutable GitHub Action pins, and a canonical Social Scientist Agent with host specific adapters.

The repository name remains unchanged. The broader product subtitle is a Claude Code and Codex social science toolkit and open educational resource.

## Capability status

| Capability | Status | Evidence surface |
|---|---|---|
| Bilingual curriculum | Shipped | `booklets/`, `CATALOG.md` |
| Thirty two reviewed skills | Shipped | `.claude/skills/` |
| Claude Code project skills | Shipped | `.claude/skills/`, installer |
| Codex project skills | Shipped | installer target `.agents/skills` |
| User and project scope install | Shipped | `social-cc install --scope` |
| Ownership manifest | Shipped | `.social-cc/manifest.json` |
| Reviewable diff and upgrade | Shipped | `social-cc diff`, `social-cc upgrade` |
| Safe uninstall | Shipped | `social-cc uninstall` |
| Claude Code plugin | Shipped | `.claude-plugin/` |
| Codex plugin package | Not yet shipped | Requires a concrete current schema, packaging, install, and removal test |
| Canonical Social Scientist Agent | Shipped in source | `core/agents/social-scientist.md` |
| Claude Code agent adapter | Shipped | `.claude/agents/`, `agents/` |
| Codex repository adapter | Shipped | `AGENTS.md` |
| Cross client agent evaluation | In progress | Evaluation corpus and host smoke tests remain release gates |
| Optional Mneme and Mergen integration | Experimental design only | No core dependency and no silent data transmission |

## Phase 1. Release truth and architecture

**Status: implemented.**

- One machine readable release record in `meta/release.json`.
- Derived checks for booklet, language, category, skill, and citation totals.
- Version alignment across package, Python source, CFF, plugin, marketplace, and changelog.
- Public release markers in README, Turkish README, catalog, roadmap, paper, website, and package landing page.
- Architecture documentation for canonical sources and client adapters.

## Phase 2. Scholarly and bilingual integrity

**Status: ongoing maintenance.**

- Reverify load bearing claims and sources.
- Separate DOI identity, bibliographic metadata, source status, and claim level support.
- Extend source manifests beyond DOI records to books, laws, standards, reports, official guidance, and product documentation.
- Preserve Turkish and English conceptual equivalence without enforcing literal sentence parity.
- Record corrections, retractions, and expressions of concern.

## Phase 3. Skill library contracts

**Status: responsibility matrix implemented, trigger evaluation expanding.**

- One primary responsibility per skill.
- Explicit positive and negative triggers.
- Inputs, workflow, output, verification, safety, handoff, and human authority boundaries.
- Deterministic scripts permitted when they materially improve reliability.
- Skill responsibility matrix and handoff graph.
- Positive, negative, ambiguous, collision, safety, Turkish, and English trigger cases.

High value capability gaps remain under evaluation. They include theory development, sampling and power, survey design, psychometrics, experimental and quasi experimental design, causal inference, measurement invariance, formal mixed methods integration, meta analysis, and replication packages.

## Phase 4. Dual client distribution

**Status: core installer implemented.**

- Canonical reviewed source remains `.claude/skills` for backward compatibility.
- Claude Code user target is `~/.claude/skills`.
- Claude Code project target is `<project>/.claude/skills`.
- Codex user target is `~/.agents/skills`.
- Codex project target is `<project>/.agents/skills`.
- Existing unmanaged and locally modified files are protected.
- Forced replacement and removal create recoverable backups.
- Diff, upgrade, doctor, dry run, and uninstall are available.

Future work includes tested Windows PowerShell paths, interrupted upgrade recovery fixtures, and a native Codex plugin package if the current host contract justifies it.

## Phase 5. Security, privacy, licensing, and supply chain

**Status: substantially hardened.**

- Executable surface documented in `SECURITY.md`.
- Research data threat model and untrusted content rule.
- Symlink, path, ownership, and destructive operation protections.
- Full GitHub Action commit pinning with a structural gate.
- Least privilege workflow permissions.
- Wheel content and isolated installation checks.
- Clear Apache 2.0 and CC BY NC SA 4.0 boundaries.

Remaining work includes periodic dependency review, CodeQL evaluation, accessibility automation, and signed or provenance bearing release artifacts where supported.

## Phase 6. Educational platform

**Status: learning architecture implemented, sample project expanding.**

The learning pathways are:

1. First session.
2. Research workflow foundations.
3. Method specific practice.
4. Advanced agentic research.

The next curriculum milestone is a complete synthetic sample project that demonstrates question formation, source triage, preregistration, synthetic data, analysis, manuscript drafting, citation verification, disclosure, and open science packaging.

## Phase 7. Contract freeze and evaluation foundation

**Status: core contracts frozen, evaluation corpus expanding.**

Frozen contracts include skill identity, handoffs, evidence vocabulary, research stages, data sensitivity, human decisions, verification, bilingual behavior, installer ownership, and agent outputs.

The evaluation corpus must measure valid completion as well as safe refusal. A system trained only to reject adversarial cases is not acceptable.

## Phase 8. Social Scientist Agent

**Status: canonical agent and Claude adapters implemented.**

The agent follows:

```text
ORIENT → INSPECT → CLASSIFY → SELECT SKILLS → WORK → VERIFY → HAND OFF
```

It selects the minimum sufficient skills, preserves method specific boundaries, protects sensitive data, distinguishes evidence from inference, and stops at human decision boundaries.

The agent is not an autonomous principal investigator, ethics committee, statistician of record, legal adviser, clinical supervisor, automatic coauthor, or source of invented evidence.

## Phase 9. Cross client evaluation

**Status: focused installer tests implemented, full host dogfooding pending.**

Required scenarios include psychology literature review, sociology survey, education interview study, public health observational study, political science mixed methods project, anthropology fieldnote workflow, systematic review, grant proposal, reviewer response, teaching workflow, open science package, and Turkish English manuscript work.

Adversarial fixtures include fabricated and misapplied DOI values, retracted papers, unsupported causal language, identifiable interview material, confidential peer review content, hidden preregistration deviations, inappropriate statistical tests, altered qualitative quotations, construct changing translation, skill collisions, prompt injection, and false host parity.

## Phase 10. Release candidate hardening

**Status: branch level hardening in progress.**

Before the next release candidate:

- Reinspect the repository from zero.
- Run the complete feasible Node, Python, documentation, package, installer, plugin, and citation suite.
- Perform Claude Code and Codex smoke tests in clean temporary projects.
- Verify user and project scope install, upgrade, diff, backup, and uninstall.
- Verify generated agent adapters.
- Verify the website, paper, package, catalog, changelog, and citation record.
- Confirm no unresolved P0 or P1 issue remains.
- Document all environmental limitations and host asymmetries.

## Release policy

A pull request is prepared for review and is not merged automatically. A green build establishes only the claims covered by the executed checks. It does not certify methodological validity, ethics approval, legal compliance, or professional judgment.

**Last updated:** 2026-07-16.
