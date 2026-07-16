# Skill Responsibility and Handoff Matrix

## Contract

Every skill has one primary job. A skill may prepare an input for another skill or recommend a next step. It must not silently perform another skill's professional or methodological responsibility.

The Social Scientist Agent selects the minimum sufficient skills and records each relevant skill as applied, recommended next, not applicable, blocked by missing input, requiring a human specialist, or replaced by a stronger deterministic check.

## Responsibility matrix

| Skill | Primary responsibility | Explicit boundary | Typical handoffs |
|---|---|---|---|
| `social-science-literature-triage` | Define search scope, databases, language layers, inclusion logic, and source status before review work | Does not complete formal screening or verify every citation | `regional-access-workflow`, `prisma-scoping-review-pipeline`, `source-passport-ledger` |
| `apa-doi-verifier` | Verify reference identity, DOI metadata, APA 7 structure, and fabrication risk | Does not determine whether a source supports a substantive claim without source inspection | `source-passport-ledger`, `repo-release-integrity-check` |
| `bilingual-booklet-pairing` | Check Turkish and English booklet pairing, structure, frontmatter, citations, and adaptation notes | Does not certify conceptual validity from structural parity alone | `multilingual-concept-validity-audit`, `ai-disclosure-auditor` |
| `ai-disclosure-auditor` | Audit AI contribution, model, human review, citation counts, and disclosure fields | Does not decide authorship or journal policy compliance by itself | `authorship-contribution-ledger`, `repo-release-integrity-check` |
| `ethics-irb-ai-protocol` | Structure ethics, privacy, data minimization, institutional review, and disclosure questions | Does not approve a study or replace legal, clinical, or ethics authority | `sensitive-data-anonymization-gate`, human ethics authority |
| `rebuttal-traceability-matrix` | Map reviewer comments to responses, manuscript changes, evidence, and status | Does not concede, reject, or reinterpret a scientific claim without author decision | `apa-doi-verifier`, `anti-ai-trace-revision` |
| `memory-vault-architect` | Design durable research folders, maps of content, metadata, and retrieval conventions | Does not act as an external memory service or store secrets by default | `source-passport-ledger`, `research-ritual-hooks` |
| `regional-access-workflow` | Route lawful literature access through regional and institutional systems | Does not bypass paywalls, credentials, or access controls | `social-science-literature-triage`, `source-passport-ledger` |
| `agentic-session-debugger` | Diagnose scope, context, permissions, paths, loops, and host state | Does not weaken safety controls to make a task run | `mcp-research-stack-triage`, `agent-portability-matrix` |
| `repo-release-integrity-check` | Verify release metadata, counts, links, citations, disclosure, packaging, and public claims | Does not declare scientific validity or publish automatically | `ai-disclosure-auditor`, `apa-doi-verifier`, `open-science-release-packager` |
| `anti-ai-trace-revision` | Restore author voice and remove repetitive machine style while preserving evidence and disclosure | Does not conceal required AI disclosure or silently alter results | `bilingual-manuscript-scaffold`, `ai-disclosure-auditor` |
| `bilingual-manuscript-scaffold` | Build Turkish and English manuscripts from one claim architecture with conceptual adaptation | Does not certify translation validity or journal fit | `multilingual-concept-validity-audit`, `journal-fit-screening` |
| `journal-fit-screening` | Assess scope, audience, index status, policies, and predatory risk | Does not guarantee acceptance or fabricate current journal metrics | `grant-proposal-workpackage-builder`, `bilingual-manuscript-scaffold` |
| `qualitative-coding-discipline` | Structure human led coding, reflexivity, quote integrity, negative cases, and audit trail | Does not replace interpretive authority or infer prevalence | `sensitive-data-anonymization-gate`, `multilingual-concept-validity-audit` |
| `statistical-consultation-protocol` | Match design and estimand to analyses, assumptions, effect sizes, uncertainty, and reproducible reporting | Does not act as statistician of record or select tests from labels alone | `preregistration-analysis-plan-ledger`, human statistical specialist |
| `research-ritual-hooks` | Convert explicit research rituals into bounded lifecycle automation and checks | Does not execute hidden network activity or transmit research content by default | `memory-vault-architect`, `repo-release-integrity-check` |
| `research-lifecycle-pipeline` | Diagnose research stage and route to the minimum relevant skills | Is a router, not the Social Scientist Agent and not an executor of every stage | Any method or lifecycle skill selected at the boundary |
| `mcp-research-stack-triage` | Assess MCP publisher, data flow, permissions, trust, and known answer behavior | Does not grant credentials or certify a server as universally safe | `agentic-session-debugger`, `sensitive-data-anonymization-gate` |
| `source-passport-ledger` | Track source discovery, access, identity, verification, claims, and citation status | Does not turn unverified records into references | `apa-doi-verifier`, `prisma-scoping-review-pipeline` |
| `conference-materials-bilingual` | Create evidence traceable slides and posters with bilingual adaptation | Does not overstate findings or invent visual evidence | `public-scholarship-ethics-adapter`, `multilingual-concept-validity-audit` |
| `prisma-scoping-review-pipeline` | Run logged search, deduplication, screening, exclusion reasons, extraction, and flow counts | Does not silently change eligibility criteria or fabricate screening decisions | `social-science-literature-triage`, `source-passport-ledger`, `apa-doi-verifier` |
| `sensitive-data-anonymization-gate` | Minimize, deidentify, classify, and approve or block data before tool access | Does not guarantee zero reidentification risk or authorize processing outside consent | `ethics-irb-ai-protocol`, human data authority |
| `open-science-release-packager` | Assemble code, data decisions, metadata, license, DOI, embargo, and reproducibility materials | Does not make restricted data public or decide consent compatibility alone | `repo-release-integrity-check`, `authorship-contribution-ledger` |
| `authorship-contribution-ledger` | Record authorship order, CRediT roles, evidence, disputes, and AI assistance | Does not assign authorship without contributor agreement and policy review | `ai-disclosure-auditor`, human author group |
| `peer-review-confidentiality-protocol` | Decide whether and how AI may assist confidential peer review | Does not upload a manuscript without authorization or replace reviewer judgment | `sensitive-data-anonymization-gate`, human editor or institution |
| `multilingual-concept-validity-audit` | Assess construct equivalence, translation decisions, cultural adaptation, and drift | Does not certify psychometric invariance without appropriate data and analysis | `bilingual-manuscript-scaffold`, `statistical-consultation-protocol` |
| `grant-proposal-workpackage-builder` | Build work packages, milestones, risks, dependencies, and budget logic | Does not invent feasibility evidence, costs, partners, or institutional commitments | `ethics-irb-ai-protocol`, `authorship-contribution-ledger` |
| `teaching-feedback-ai-boundaries` | Define AI boundaries for course design, assessment, and student feedback | Does not process protected student data or decide misconduct without institutional authority | `sensitive-data-anonymization-gate`, human academic authority |
| `public-scholarship-ethics-adapter` | Adapt findings for public audiences while preserving evidence, uncertainty, and disclosure | Does not convert association into causation or simplify away material limitations | `conference-materials-bilingual`, `apa-doi-verifier` |
| `preregistration-analysis-plan-ledger` | Freeze confirmatory decisions, estimands, exclusions, analyses, and deviations | Does not relabel deviations as confirmatory or choose methods without design information | `statistical-consultation-protocol`, `open-science-release-packager` |
| `agent-portability-matrix` | Compare host capabilities, file access, memory, permissions, skill support, and migration risk | Does not claim parity from copied files or infer undocumented product behavior | `agentic-session-debugger`, `mcp-research-stack-triage` |
| `cross-agent-second-opinion` | Obtain an independent verification attempt and surface disagreement for human adjudication | Does not vote scientific truth into existence or transmit sensitive data silently | Relevant primary skill, human researcher |

## Handoff rules

1. A handoff names the receiving skill and the unresolved input it needs.
2. A skill may not mark another skill's output as verified without running its verification contract or a stronger deterministic check.
3. Ethics, privacy, legal, clinical, and professional gates cannot be bypassed by routing to a different skill.
4. A circular handoff is a defect unless it represents an explicit iterative method with a termination condition.
5. The router and Social Scientist Agent must not duplicate a method skill's detailed procedure.
6. A deterministic script replaces a language model step when the task is exact, reproducible, and safely bounded.
7. Human specialist escalation is an outcome, not a failed workflow.

## Capability gaps under evaluation

The existing library has useful lifecycle coverage but does not yet claim complete operational depth in several high value areas.

1. Research question and theory development.
2. Sampling and power planning.
3. Survey and instrument design.
4. Psychometric development and validation.
5. Experimental and quasi experimental design.
6. Causal inference.
7. Measurement invariance.
8. Formal mixed methods integration.
9. Meta analysis and evidence grading.
10. Data management plans and replication packages.

A new skill is added only when the responsibility is distinct, bounded, testable, methodologically defensible, and supported by an educational need. The absence of a skill does not authorize the Social Scientist Agent to improvise a hidden replacement.

## Review conclusion

No current skill should be treated as a professional certification mechanism. The most important overlap risk is between `research-lifecycle-pipeline` and the Social Scientist Agent. The pipeline remains a lightweight stage router. The agent owns cross stage orientation, risk classification, skill selection, verification synthesis, and handoff. Detailed methods remain inside the narrow skills.
