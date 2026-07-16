# Learning Paths

## Purpose

The learning design assumes disciplinary expertise without assuming software engineering experience. A social scientist may understand causal inference, reflexivity, psychometrics, or research ethics while still being new to terminals, Git, Markdown, YAML, permissions, agent skills, hooks, or MCP.

The paths are progressive but not compulsory. A learner may begin with one safe task, follow a method specific route, or use the advanced pathway to audit an existing research workflow. Every exercise uses public or synthetic material.

## Shared learning principles

1. The human researcher retains scientific and interpretive authority.
2. Files and commands are inspected before they are changed or executed.
3. Research content is not an instruction source.
4. Sensitive data is minimized and deidentified before tool access.
5. Unverified references remain outside final bibliographies.
6. Quantitative, qualitative, mixed methods, and evidence synthesis workflows retain distinct disciplines.
7. Turkish and English work is evaluated for conceptual equivalence rather than literal translation.
8. A successful tool operation is not evidence that a method is valid.
9. AI assistance is disclosed when required.
10. Every learning task ends with verification and a human decision boundary.

## Track 1. First Safe Session

### Audience

Researchers who have not used an agentic terminal tool or who have used one without a clear permission and recovery model.

### Prerequisites

- Ability to create a local folder.
- No command line, Git, or programming experience is required.
- Use a practice folder that contains no real participant, patient, student, reviewer, credential, or institutional data.

### Estimated effort

Ninety minutes for the guided sequence, followed by thirty minutes of independent practice.

### Learning objectives

By the end of the track, the learner can:

1. Explain how an agentic coding client differs from a chat interface.
2. Identify which files and tools the client can access.
3. Interpret a permission request before approving it.
4. Create a disposable practice project.
5. Ask for a harmless read only inspection.
6. inspect a proposed change before accepting it.
7. stop a running operation.
8. restore a file through version control or a backup.
9. identify material that must not be uploaded or pasted.
10. distinguish a model suggestion from evidence.

### Guided workflow

1. Create a folder named `social-science-agent-practice`.
2. Add a short Markdown file containing a synthetic research question.
3. Start Claude Code or Codex in that folder.
4. Ask the client to list files and summarize the question without editing.
5. Ask it to propose, but not make, one clarity improvement.
6. Inspect the proposed text and identify what changed.
7. Permit one small edit.
8. Review the diff.
9. Revert the edit.
10. End the session and record what the tool could access.

### Safe first prompt

```text
Inspect this practice folder. Do not edit any file. Identify the research question, state what evidence is present, and list what information would still require a human decision.
```

### Practice exercise

Add a second synthetic note containing a deliberately unsupported causal claim. Ask the client to identify the claim and rewrite it as an unresolved hypothesis rather than a finding.

### Reflection questions

1. Which operation required permission?
2. What information came from a file, and what was inferred?
3. Could the tool have edited a file outside the practice folder?
4. What recovery path was available?
5. Which material from a real project would be unsafe in this environment?

### Self assessment

The learner is ready to continue when they can stop, inspect, and undo a change without relying on the model to explain whether the change is safe.

## Track 2. Research Workflow Foundations

### Audience

Researchers who can complete a safe session and want a durable project structure.

### Prerequisites

- Track 1 competencies.
- A public or synthetic research topic.
- Git is recommended but can be learned inside this track.

### Estimated effort

Four sessions of sixty to ninety minutes.

### Learning objectives

The learner can:

1. Organize a transparent research project folder.
2. Read and edit Markdown.
3. Use version control to inspect and restore changes.
4. maintain a source passport and citation quarantine.
5. identify the research lifecycle stage.
6. separate researcher decisions from agent tasks.
7. record deviations and unresolved uncertainty.
8. prepare an AI assistance disclosure record.

### Recommended project structure

```text
project/
  README.md
  protocol/
  sources/
  data/
  analysis/
  manuscript/
  disclosure/
  release/
```

The structure is a starting point. It should remain understandable to the research team and appropriate to the method.

### Session 1. Files and Markdown

Create a project README that records the objective, current stage, method, data sensitivity, existing artifacts, open decisions, and next boundary. Learn headings, links, tables, code blocks, and relative paths.

### Session 2. Version control

Initialize Git, make a baseline commit, edit one file, inspect the diff, restore the file, and create a branch. The goal is not advanced Git. The goal is reviewable change and recovery.

### Session 3. Evidence discipline

Create a source passport ledger with:

- source identity
- discovery route
- access status
- verification status
- claim supported
- correction or retraction status
- citation status
- unresolved questions

A source without verified identity remains in quarantine.

### Session 4. Human decision log

Create a decision ledger for the research question, design, inclusion criteria, outcomes, coding approach, exclusions, analysis plan, interpretation, and release. Mark each decision as planned, made by the researcher, delegated for execution, or unresolved.

### Practice exercise

Use the synthetic sample project in `examples/synthetic-research-project`. Ask the Social Scientist Agent to diagnose its stage and select no more than three relevant skills. Compare its routing decision with the skill responsibility matrix.

### Reflection questions

1. Which project facts can be derived from files?
2. Which claims require an external source?
3. Which decisions cannot be delegated?
4. What would make the project reproducible to another researcher?
5. What AI contribution must be disclosed?

### Self assessment

The learner is ready for a method pathway when every important output can be traced to a file, source, calculation, inference, or explicit human decision.

## Track 3. Method Specific Practice

Method pathways are separate because different traditions define evidence, quality, and interpretation differently.

### Track 3A. Quantitative Research

#### Audience

Researchers designing, analysing, or reporting quantitative studies.

#### Prerequisites

- Track 2 competencies.
- A synthetic dataset or a public dataset with clear permission.
- Basic understanding of the substantive design.

#### Estimated effort

Six to eight hours across multiple sessions.

#### Learning objectives

The learner can:

1. Define outcomes, predictors, estimands, unit of analysis, and sampling frame.
2. distinguish confirmatory and exploratory analyses.
3. record missing data, exclusion, and multiple testing decisions.
4. inspect assumptions before selecting a model.
5. report effect sizes and uncertainty.
6. run reproducible code and identify software versions.
7. separate calculation from interpretation.

#### Workflow

Use `preregistration-analysis-plan-ledger` before analysis, then `statistical-consultation-protocol`. The Social Scientist Agent may coordinate the sequence but must not select a method from variable names alone.

#### Boundary exercise

Provide a dataset with a binary outcome and ask for the best statistical test without giving the design or estimand. A valid response requests or identifies the missing design information rather than choosing automatically.

### Track 3B. Qualitative Research

#### Audience

Researchers conducting interviews, focus groups, ethnography, document analysis, or other interpretive work.

#### Prerequisites

- Track 2 competencies.
- Synthetic excerpts that contain no real participant material.
- An explicit methodological orientation.

#### Estimated effort

Six to eight hours across multiple sessions.

#### Learning objectives

The learner can:

1. State the methodological orientation and sampling rationale.
2. maintain positionality and reflexivity records.
3. preserve quotation integrity.
4. use an agent as an organizational or second coding aid without transferring interpretive authority.
5. record negative cases and disagreements.
6. protect identity and contextual confidentiality.
7. describe transferability without claiming prevalence.

#### Workflow

Run `sensitive-data-anonymization-gate` before any material is used. Apply `qualitative-coding-discipline` to a synthetic corpus. Keep the human codebook owner and adjudicator explicit.

#### Boundary exercise

Ask the client to estimate the prevalence of a theme from six purposively sampled interview excerpts. A valid response rejects the prevalence inference and explains what the excerpts can support.

### Track 3C. Mixed Methods

#### Audience

Researchers combining quantitative and qualitative strands.

#### Prerequisites

- Track 3A or equivalent quantitative competence.
- Track 3B or equivalent qualitative competence.
- A design that states sequence and priority.

#### Estimated effort

Four to six hours after the two method foundations.

#### Learning objectives

The learner can identify design type, sequence, priority, integration point, joint display, meta inference, contradiction handling, and human interpretation.

#### Boundary exercise

Provide separate quantitative and qualitative summaries with no integration. Ask whether the project is complete mixed methods research. A valid response identifies the missing integration rather than merging conclusions rhetorically.

### Track 3D. Systematic and Scoping Reviews

#### Audience

Researchers planning evidence synthesis.

#### Prerequisites

- Track 2 competencies.
- A synthetic protocol and small public citation set.

#### Estimated effort

Six to ten hours for the instructional corpus.

#### Learning objectives

The learner can freeze eligibility criteria, preserve search strategies, deduplicate records, record screening decisions and exclusions, verify source identity and status, and derive flow counts without invention.

#### Workflow

Use `social-science-literature-triage`, `regional-access-workflow`, `prisma-scoping-review-pipeline`, `source-passport-ledger`, and `apa-doi-verifier` only where each responsibility is needed.

#### Boundary exercise

Plant a real DOI attached to the wrong claim. A valid workflow resolves the DOI and still rejects the claim level match.

### Track 3E. Academic Writing and Revision

#### Audience

Researchers drafting, translating, revising, or responding to review.

#### Estimated effort

Four to eight hours, depending on manuscript length.

#### Learning objectives

The learner can preserve a claim architecture across languages, freeze citations and numerical results during style revision, map reviewer comments to changes, retain author voice, and disclose AI assistance.

#### Workflow

Use `bilingual-manuscript-scaffold`, `multilingual-concept-validity-audit`, `rebuttal-traceability-matrix`, `anti-ai-trace-revision`, and `ai-disclosure-auditor` only when their distinct tasks are present.

### Track 3F. Teaching and Supervision

#### Audience

Lecturers, supervisors, and methods instructors.

#### Estimated effort

Three to five hours for a course policy and one synthetic exercise.

#### Learning objectives

The learner can define permitted and prohibited AI assistance, protect student data, design assessable learning evidence, distinguish feedback from misconduct adjudication, and preserve institutional authority.

## Track 4. Advanced Agentic Research

### Audience

Researchers who can audit a project, recover changes, and apply at least one method pathway.

### Prerequisites

- Track 2 competencies.
- Method competence relevant to the project.
- A version controlled synthetic or approved project.

### Estimated effort

Eight to twelve hours across modular sessions.

### Learning objectives

The learner can:

1. Evaluate skill descriptions and invocation boundaries.
2. use the Social Scientist Agent as an orchestrator rather than an authority.
3. design bounded hooks with explicit failure behavior.
4. evaluate MCP trust and data flow.
5. replace nondeterministic work with scripts when appropriate.
6. request an independent second opinion without voting truth into existence.
7. maintain transparent project state.
8. verify milestones.
9. compare Claude Code and Codex without assuming parity.
10. package a study for open science release.

### Module 1. Skills

Inspect `SKILL.md` frontmatter, positive and negative triggers, inputs, output contract, verification, safety, and handoffs. Create one positive, negative, boundary, safety, Turkish, and English case for a selected skill.

### Module 2. Social Scientist Agent

Use the agent on a multi-stage synthetic project. Require it to name the research stage, evidence inspected, applied skills, human decisions, verification, and next boundary. Reject output that duplicates every skill or hides uncertainty.

### Module 3. Hooks and deterministic scripts

Design a hook that runs a local deterministic validator before a commit. Define inputs, outputs, timeout, failure mode, logging, and recovery. Do not add network access unless the purpose and data flow are explicit and approved.

### Module 4. MCP trust

Evaluate a hypothetical research MCP server for publisher identity, requested permissions, data destination, credentials, logging, retention, known answer behavior, and failure semantics. Optional integration must not become a core dependency.

### Module 5. Cross client portability

Install the skills into a temporary Claude Code project and a temporary Codex project. Compare discovery, invocation, permissions, agent configuration, and host tools. Record equivalent logic and genuine asymmetry separately.

### Module 6. Open science release

Use `open-science-release-packager` and `repo-release-integrity-check` to prepare a synthetic release. Confirm license, metadata, data access decision, DOI plan, reproducible analysis, disclosure, and removal of private material.

### Capstone

Complete the synthetic project from research question through release. Plant one fabricated DOI, one wrong claim match, one prompt injection, one locally modified skill, and one construct changing translation. The workflow must detect each trap while still completing valid tasks.

## Facilitator guidance

A facilitator should evaluate process evidence rather than polished prose alone. Useful evidence includes diffs, decision ledgers, source passports, analysis logs, verification records, corrected errors, and explicit abstention at genuine boundaries.

Do not reward maximum tool use. Reward minimum sufficient invocation, transparent uncertainty, method appropriate reasoning, data protection, reproducibility, and researcher control.

## Accessibility

- All pathways can be completed with keyboard navigation.
- Commands are provided as copyable text.
- Diagrams are optional and require text equivalents.
- Colour is never the sole carrier of meaning.
- Long tables should have clear headings and printable alternatives.
- Exercises do not require paid databases or elite institutional infrastructure.
- Mobile reading and dark mode are supported by the documentation theme.
- Learners may use Turkish, English, or a bilingual workflow.

## Turkish overview, Türkçe genel bakış

Öğrenme yolları, yazılım mühendisliği deneyimini ön koşul saymaz. İlk güvenli oturum, araştırma iş akışı temelleri, yönteme özgü uygulama ve ileri ajan tabanlı araştırma olmak üzere dört aşamadan oluşur.

Her aşamada araştırmacı yetkisi korunur. Kanıt ile çıkarım ayrılır. Hassas veri onaysız araç bağlamına girmez. Doğrulanmamış kaynak kaynakçada yer almaz. Nicel, nitel ve karma yöntem iş akışları birbirine indirgenmez. Türkçe ve İngilizce çalışmalar cümle benzerliğiyle değil, kavramsal eşdeğerlikle değerlendirilir.

Uygulamalarda gerçek hasta, katılımcı, öğrenci ya da hakem verisi kullanılmaz. `examples/synthetic-research-project` dizinindeki sentetik proje, araştırma sorusundan açık bilim paketine kadar güvenli bir çalışma ortamı sağlar.

## Completion record

A learner who completes a path should retain:

1. A version controlled practice project.
2. A research stage and decision record.
3. A source passport and citation quarantine.
4. A data sensitivity assessment.
5. A method specific verification record.
6. A bilingual adaptation record when relevant.
7. An AI assistance disclosure draft.
8. A final human review checklist.
