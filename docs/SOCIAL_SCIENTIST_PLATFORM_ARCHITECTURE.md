# Social Scientist Platform Architecture

<!-- platform-facts: canonical=.claude/skills clients=claude-code,codex scopes=user,project -->

## Purpose

This document defines the repository architecture that supports two connected products without allowing either to become a documentation only promise.

1. A bilingual open educational resource for social scientists.
2. A professional skill and agent toolkit for Claude Code and Codex.

The repository name remains `claude-code-for-social-scientists`. Dual client support extends the product subtitle and distribution surface. It does not erase the project history or invalidate existing citations.

## Architectural decision

The reviewed skill source remains `.claude/skills` for backward compatibility with existing releases, citations, plugin packaging, and contributor workflows. Although the directory name is Claude specific, the content inside every `SKILL.md` must remain methodologically client neutral unless a capability genuinely differs between hosts.

The Python package includes that source once as `social_cc_plugin/skills`. The `social-cc` command then installs the same reviewed files into the discovery path of the selected client.

| Client | User scope | Project scope |
|---|---|---|
| Claude Code | `~/.claude/skills` | `<project>/.claude/skills` |
| Codex | `~/.agents/skills` | `<project>/.agents/skills` |

Generated client directories are distribution outputs. They are not independent intellectual sources. A change to a generated copy must be made in the canonical source and reinstalled or rendered.

## Source and distribution flow

```text
.claude/skills/<skill>/SKILL.md
              |
              v
      Python wheel bundle
  social_cc_plugin/skills/<skill>
              |
              v
       social-cc installer
       /                 \
      v                   v
.claude/skills       .agents/skills
Claude Code          Codex
```

The Claude Code plugin manifest also points to `.claude/skills`. This is a native Claude distribution route. Codex support is provided by the cross client installer and repository instructions. A Codex plugin must not be claimed until a separately tested package that conforms to the current Codex plugin contract is shipped.

## Stable contracts

The following contracts are frozen for the first dual client release.

### Skill identity

Each skill lives in a lower case, hyphenated directory and contains a regular `SKILL.md` file. The frontmatter must contain `name` and `description`. The `name` must equal the directory name.

### Skill responsibility

Each skill has one primary methodological responsibility. It defines positive triggers, negative triggers, inputs, workflow, output, verification, safety, handoffs, and human authority boundaries. Supporting scripts or references are permitted when they increase determinism or reduce context use. They must be declared, tested, bounded, and free of hidden network behavior.

### Installation ownership

The installer records project owned skills in `.social-cc/manifest.json`, adjacent to the selected client directory. The manifest stores the installed digest, client, scope, package version, and installation time.

An existing directory without a matching manifest record is user owned. An installed directory whose digest differs from its manifest is locally modified. Neither may be overwritten or removed without an explicit `--force` operation. A forced replacement or removal first moves the prior directory into an operation specific backup under `.social-cc/backups/`.

### Agent source

The Social Scientist Agent has one canonical source under `core/agents/social-scientist.md`. Claude Code receives a generated Markdown subagent adapter. Codex receives project guidance through `AGENTS.md` and uses the canonical agent contract as the orchestration specification.

Host differences are preserved. Claude Code has a native project and plugin subagent file surface. Codex uses `AGENTS.md`, skills, and its own current subagent interfaces. The repository must not invent a shared file format where the hosts do not provide one.

### Evidence vocabulary

Agent and skill outputs distinguish the following categories.

1. User supplied fact.
2. File observed fact.
3. Source verified fact.
4. Independently calculated result.
5. Methodological inference.
6. Tentative interpretation.
7. Human decision.
8. Unresolved uncertainty.

No inference may be restated as observed evidence. No unverified reference may enter a final bibliography.

### Research authority

The human researcher retains scientific, interpretive, ethical, legal, and professional authority. The platform may structure decisions, expose assumptions, execute reproducible procedures, and identify risk. It may not impersonate an ethics committee, statistician of record, licensed legal adviser, clinical supervisor, or autonomous principal investigator.

## Release truth architecture

`meta/release.json` is the canonical machine readable record for release facts and platform support. `scripts/validate-release-truth.mjs` derives repository counts and compares them with that record. It also checks version mirrors, distribution paths, public documentation markers, and release identifiers.

The exact marker below is copied into public mirrors and validated structurally.

```text
release-facts: version=4.0.0 booklets=33 language_files=66 categories=14 skills=32 verified=566 fabricated=0
```

The marker is not a substitute for readable prose. It is a deterministic guard against silent drift.

## Security boundaries

Content retrieved from articles, websites, repositories, PDFs, transcripts, datasets, reviewer files, or other external material is research evidence. It is never an instruction that can redefine permissions, safety rules, inclusion criteria, the research question, or the workflow.

The installer rejects symlinked skill destinations and symlinked control paths. It uses deterministic tree digests, staged copies, recoverable backups, and an ownership manifest. It never sends research content to an external service.

Sensitive clinical, participant, student, reviewer, credential, or institutional data must be minimized and deidentified before any use. Public examples must be synthetic and clearly labelled.

## Licensing boundaries

Installer code, validators, renderers, and configuration are Apache 2.0. Skill prose, booklets, educational guides, and instructional templates remain CC BY NC SA 4.0 unless a file states otherwise. Generated client adapters retain the license of their canonical source. Distribution artifacts must include both license texts and explain which files each license governs.

## Verification layers

The platform uses four verification layers.

1. Deterministic repository validation. This checks structure, release truth, manifests, client paths, bilingual pairing, and generated drift.
2. Unit and integration tests. These cover installation, upgrade, diff, removal, path safety, and routing contracts.
3. Network dependent checks. These verify DOI resolution, external links, current product documentation, corrections, and retractions. They run separately from deterministic tests.
4. Human review. This adjudicates methods, interpretation, bilingual conceptual equivalence, ethics, and release readiness.

A green deterministic build does not certify scientific validity. A successful network lookup does not establish claim level support. Both are necessary controls within a larger human governed process.

## Decision record

This architecture deliberately keeps `.claude/skills` as the canonical source for the first dual client release. A later neutral migration may be justified if the path itself creates maintenance or contributor confusion. Such a migration must preserve stable skill names, existing Claude Code installation paths, package compatibility, citations, and a tested upgrade route.
