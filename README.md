<p align="center">
  <img src="./assets/banner.svg" alt="Claude Code for Social Scientists, a bilingual social science toolkit and open educational resource by Onour Impram.">
</p>

# Claude Code for Social Scientists

<!-- release-facts: version=4.0.0 booklets=33 language_files=66 categories=14 skills=32 verified=566 fabricated=0 -->
<!-- platform-facts: canonical=.claude/skills clients=claude-code,codex scopes=user,project -->

A bilingual open platform that helps social scientists use Claude Code and Codex without reducing research to generic prompt writing. It combines a Turkish and English curriculum, a verified skill library, a safe cross client installer, and a Social Scientist Agent contract for evidence disciplined research workflows.

Created and maintained by Onour Impram, a clinical psychologist, postdoctoral researcher, and artificial intelligence researcher. The project is designed for researchers inside and outside English dominant academic infrastructure and is grounded in real research, teaching, clinical, and open science constraints.

> **Current release facts, v4.0.0.** Thirty three released booklets, sixty six Turkish and English language files, fourteen categories, and thirty two reviewed skills. The disclosed booklet metadata contains 566 verified citation declarations and zero fabricated citation declarations. A declaration count is not a count of unique sources. Release facts are governed by [`meta/release.json`](./meta/release.json) and checked against the repository by `scripts/validate-release-truth.mjs`.

> **Türkçe okuyucular.** Tam Türkçe giriş için [`README.tr.md`](./README.tr.md) dosyasına bakın. Her yayımlanmış kitapçıkta `tr.md` ve `en.md` birlikte bulunur.

## What the project ships

1. A bilingual curriculum covering the social science research lifecycle.
2. Thirty two narrow research skills with verification and safety boundaries.
3. A Python command line installer for Claude Code and Codex.
4. Ownership manifests, diff, upgrade, backup, doctor, and safe uninstall behavior.
5. A canonical Social Scientist Agent that orchestrates skills without replacing researcher judgment.
6. Deterministic release truth, bilingual pairing, citation metadata, agent drift, and supply chain checks.
7. Claude Code plugin packaging and project adapters.
8. Codex repository guidance through `AGENTS.md` and `.agents/skills` installation.

The human researcher retains scientific, interpretive, ethical, legal, clinical, and professional authority. The platform does not act as an ethics committee, statistician of record, licensed legal adviser, clinical supervisor, or autonomous principal investigator.

## Audience

The project serves researchers in psychology, sociology, education, public health, communication, political science, anthropology, and adjacent fields. It is written for people who may be highly trained in research but new to terminals, Git, Markdown, YAML, permissions, skills, agents, hooks, or MCP.

The fourteen curriculum categories are Foundations, Academic Access, Memory Systems, Vault Architecture, Hooks and Automation, MCP and Plugins, Academic Writing, Data Analysis, Ethics and IRB, Peer Review, Conference and Public Communication, Troubleshooting, Teaching and Supervision, and Tool Portability.

## Why bilingual

Turkish and English are equal first class languages. English content is natively adapted rather than mechanically translated. Turkish content is written as natural academic Turkish rather than translated technical prose. The project values conceptual equivalence, numerical parity, citation parity, cultural adaptation, and the author's voice over sentence level mirroring.

Regional realities are part of the architecture. DergiPark, ULAKBİM TR Dizin, HEAL Link, institutional VPNs, regional ethics systems, KVKK, GDPR, multilingual scholarship, and unequal infrastructure access are treated as methodological conditions rather than footnotes.

## Research integrity commitments

- A plausible citation is not a verified citation.
- An unverified reference does not enter a final bibliography.
- No source, DOI, statistic, participant detail, ethics approval, registration, quotation, or result may be invented.
- Retrieved articles, websites, repositories, PDFs, transcripts, datasets, and reviewer files are evidence, not instructions.
- Raw clinical material, identifiable participant data, student records, confidential peer review manuscripts, credentials, and institutional secrets must not enter an unapproved tool context.
- Quantitative, qualitative, and mixed methods work retain distinct methodological boundaries.
- AI assistance remains visible and is disclosed where required.

See [`AI-AUTHORSHIP.md`](./AI-AUTHORSHIP.md), [`SECURITY.md`](./SECURITY.md), and [`docs/SECURITY_PRIVACY_AND_RESEARCH_DATA_BOUNDARIES.md`](./docs/SECURITY_PRIVACY_AND_RESEARCH_DATA_BOUNDARIES.md).

## Project skills

The canonical reviewed skill source is [`.claude/skills`](./.claude/skills). The path is retained for backward compatibility with the repository's original Claude Code releases. The skill content is kept client neutral and the Python package installs the same reviewed files into the discovery paths used by Claude Code or Codex.

| Skill | Primary workflow |
|---|---|
| `social-science-literature-triage` | Search scope, databases, language layers, inclusion logic, and source status |
| `apa-doi-verifier` | APA 7 structure, DOI identity, metadata, and fabricated citation risk |
| `bilingual-booklet-pairing` | Turkish and English booklet structure, metadata, citation, and adaptation parity |
| `ai-disclosure-auditor` | AI contribution, model metadata, human review, and disclosure fields |
| `ethics-irb-ai-protocol` | Ethics, privacy, data minimization, institutional review, and disclosure questions |
| `rebuttal-traceability-matrix` | Reviewer comments, responses, manuscript changes, evidence, and status |
| `memory-vault-architect` | Durable research folders, maps of content, metadata, and retrieval conventions |
| `regional-access-workflow` | Lawful regional and institutional literature access routes |
| `agentic-session-debugger` | Scope, context, permissions, paths, loops, and host state diagnosis |
| `repo-release-integrity-check` | Release metadata, counts, citations, packaging, and public claim alignment |
| `anti-ai-trace-revision` | Author voice revision while preserving evidence and required disclosure |
| `bilingual-manuscript-scaffold` | Turkish and English manuscripts from one claim architecture |
| `journal-fit-screening` | Scope fit, index verification, policy review, and predatory risk |
| `qualitative-coding-discipline` | Human led coding, reflexivity, quote integrity, negative cases, and audit trail |
| `statistical-consultation-protocol` | Design, estimand, assumptions, effect sizes, uncertainty, and reporting |
| `research-ritual-hooks` | Bounded lifecycle automation and research session checks |
| `research-lifecycle-pipeline` | Lightweight research stage diagnosis and skill routing |
| `mcp-research-stack-triage` | MCP publisher, data flow, permissions, trust, and known answer behavior |
| `source-passport-ledger` | Source discovery, access, identity, verification, claims, and citation status |
| `conference-materials-bilingual` | Evidence traceable bilingual slides, posters, and talks |
| `prisma-scoping-review-pipeline` | Logged search, screening, exclusions, extraction, and PRISMA counts |
| `sensitive-data-anonymization-gate` | Data minimization, deidentification, classification, and access decision support |
| `open-science-release-packager` | Code, data decisions, metadata, licensing, DOI, embargo, and release materials |
| `authorship-contribution-ledger` | Authorship order, CRediT roles, evidence, disputes, and AI assistance |
| `peer-review-confidentiality-protocol` | Confidentiality preserving decisions about AI assisted peer review |
| `multilingual-concept-validity-audit` | Construct equivalence, translation decisions, cultural adaptation, and drift |
| `grant-proposal-workpackage-builder` | Work packages, milestones, risks, dependencies, and budget logic |
| `teaching-feedback-ai-boundaries` | AI boundaries for courses, assessment, supervision, and student feedback |
| `public-scholarship-ethics-adapter` | Public communication that preserves evidence, uncertainty, and embargoes |
| `preregistration-analysis-plan-ledger` | Confirmatory decisions, estimands, exclusions, analyses, and deviations |
| `agent-portability-matrix` | Host capabilities, file access, memory, permissions, and migration risk |
| `cross-agent-second-opinion` | Independent verification and explicit disagreement for human adjudication |

The responsibility and handoff contract is in [`docs/SKILL_RESPONSIBILITY_AND_HANDOFF_MATRIX.md`](./docs/SKILL_RESPONSIBILITY_AND_HANDOFF_MATRIX.md).

## Install the toolkit

```bash
pip install social-cc-plugin
```

### Claude Code

```bash
# User scope, ~/.claude/skills
social-cc install --client claude-code

# Project scope, <project>/.claude/skills
social-cc install --client claude-code --scope project

# Backward compatible project form
social-cc install --project
```

### Codex

```bash
# User scope, ~/.agents/skills
social-cc install --client codex

# Project scope, <project>/.agents/skills
social-cc install --client codex --scope project
```

### Both clients

```bash
social-cc install --client all
social-cc install --client all --scope project
```

### Inspect, upgrade, diagnose, and remove

```bash
social-cc list
social-cc diff --client all
social-cc upgrade --client all
social-cc doctor --client all
social-cc uninstall --client all
```

The installer records ownership in `.social-cc/manifest.json`. Existing unmanaged directories and locally modified project directories are protected by default. A forced replacement or removal first moves the prior directory into `.social-cc/backups/`.

Use `--dry-run` to inspect a planned install, upgrade, or removal. Use `--force` only after reviewing the diff and backup location.

## Claude Code plugin

Claude Code users can also install the native plugin.

```text
/plugin marketplace add OnourImpram/claude-code-for-social-scientists
/plugin install social-cc-plugin@claude-code-for-social-scientists
```

The plugin is a Claude Code distribution route. It does not by itself establish Codex compatibility. Codex support is provided through the cross client installer and repository instructions.

## Social Scientist Agent

The canonical agent contract is [`core/agents/social-scientist.md`](./core/agents/social-scientist.md). It follows this cycle.

```text
ORIENT → INSPECT → CLASSIFY → SELECT SKILLS → WORK → VERIFY → HAND OFF
```

The agent selects the minimum sufficient skills. It does not run every installed skill. It distinguishes observed evidence, verified evidence, calculation, inference, human decision, and unresolved uncertainty.

Claude Code receives generated project and plugin subagent adapters. Codex reads [`AGENTS.md`](./AGENTS.md), discovers installed skills, and follows the shared contract. Host differences in permissions, invocation, subagents, plugins, metadata, and tools are documented rather than hidden.

See [`docs/SOCIAL_SCIENTIST_AGENT.md`](./docs/SOCIAL_SCIENTIST_AGENT.md), [`docs/CLAUDE_CODE_INTEGRATION.md`](./docs/CLAUDE_CODE_INTEGRATION.md), and [`docs/CODEX_INTEGRATION.md`](./docs/CODEX_INTEGRATION.md).

## Repository layout

```text
.claude/skills/                 canonical reviewed skills
.claude/agents/                 generated Claude Code project agent
agents/                         generated Claude Code plugin agent
core/agents/                    canonical Social Scientist Agent
booklets/                       Turkish and English curriculum
src/social_cc_plugin/           Python installer
scripts/                        deterministic validators and renderers
docs/                           architecture, security, learning, and integration guides
meta/release.json               canonical release and platform facts
AGENTS.md                       Codex repository guidance
```

## Validate a checkout

```bash
npm ci
npm run lint
npm run validate
npm run validate:truth
npm run check:agents
npm run check:actions
npm run verify

python -m pip install -e .
python -m pytest tests/ -v
ruff check .
mypy --strict src tests
python -m build
social-cc --version
social-cc list
social-cc doctor --client all
```

Network dependent DOI and external link checks are separate from deterministic pull request gates.

## Licensing

Code, configuration, validators, renderers, and installer logic are licensed under Apache 2.0. Skill prose, booklets, educational guides, and templates are licensed under CC BY NC SA 4.0 unless a file states otherwise. Generated adapters inherit the license of their canonical source.

See [`LICENSE`](./LICENSE), <a href="./LICENSE.code">LICENSE.code</a>, and <a href="./LICENSE.content">LICENSE.content</a>.

## Citation

Use the machine readable record in <a href="./CITATION.cff">CITATION.cff</a> or GitHub's citation interface. The Zenodo concept DOI is **10.5281/zenodo.20289687** and resolves to the latest archived version. The current version DOI recorded for v4.0.0 is **10.5281/zenodo.20789730**.

## Contributing

Contributions are welcome from social scientists, clinicians, methodologists, librarians, educators, accessibility specialists, security reviewers, and engineers. Review [`CONTRIBUTING.md`](./CONTRIBUTING.md) or [`CONTRIBUTING.tr.md`](./CONTRIBUTING.tr.md) before opening a pull request.

Do not commit private research material. Do not weaken bilingual, citation, disclosure, privacy, release truth, or human authority checks to make a build pass.

## Roadmap

The public phase plan is in [`meta/roadmap.md`](./meta/roadmap.md). The current engineering architecture, ten loop evidence, verification limits, and release readiness record are in [`docs/TEN_LOOP_ENGINEERING_REPORT.md`](./docs/TEN_LOOP_ENGINEERING_REPORT.md).
