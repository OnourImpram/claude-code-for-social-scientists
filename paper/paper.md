---
title: "Claude Code for Social Scientists: A Bilingual Open Platform for Agentic AI in Research Practice"
tags:
  - claude code
  - codex
  - AI literacy
  - research methods
  - open educational resources
  - bilingual education
  - social science
authors:
  - name: Onour Impram
    orcid: 0000-0003-1076-3928
    corresponding: true
    affiliation: 1
affiliations:
  - name: "Independent Researcher and Clinical Psychologist"
    index: 1
date: 16 July 2026
bibliography: paper.bib
---

<!-- release-facts: version=5.0.0 booklets=33 language_files=66 categories=14 skills=32 verified=566 fabricated=0 -->

# Summary

Claude Code for Social Scientists is a bilingual open educational resource and research workflow toolkit for researchers in psychology, sociology, education, public health, communication, political science, anthropology, and adjacent fields. It teaches safe and methodologically explicit use of agentic computing while providing installable skills for Claude Code and Codex. The resource is authored and maintained by a clinical psychologist and postdoctoral researcher who uses agentic tools in research, teaching, scholarly writing, and open science work.

Version 5.0.0 contains thirty three released booklets in Turkish and English, sixty six language files across fourteen categories, and thirty two companion skills. The disclosed booklet metadata contains 566 verified citation declarations and zero fabricated citation declarations. The count represents declarations across language files rather than unique sources. Prose and instructional content are licensed under Creative Commons Attribution NonCommercial ShareAlike 4.0, while installer code, validators, renderers, and configuration are licensed under Apache 2.0.

The platform adds a safe cross client installer, ownership manifests, reviewable upgrades, recoverable removal, deterministic release truth checks, and a canonical Social Scientist Agent. Claude Code and Codex share the reviewed skill bodies. Host specific permissions, invocation, plugin, metadata, and agent surfaces remain explicit rather than being described as identical.

# Statement of Need

Social scientists encounter a combined methodological, linguistic, and infrastructural problem when adopting agentic AI. General coding agent documentation is usually written for software engineering. General AI literacy materials often focus on conversational prompting. Neither orientation adequately addresses preregistration, source verification, participant confidentiality, qualitative interpretive authority, statistical assumptions, bilingual construct validity, reviewer confidentiality, or open science release requirements.

Researchers outside English dominant academic infrastructure also work through regional access systems and legal contexts that are rarely integrated into agentic AI guidance. DergiPark, ULAKBİM TR Dizin, HEAL Link, institutional VPNs, KVKK, GDPR, multilingual scholarship, and local ethics procedures affect what evidence can be found, what data can be processed, and how a workflow should be disclosed.

Citation integrity is a further discipline specific risk. Language models can produce bibliographic records that appear plausible but do not correspond to genuine publications [@walters2023; @bhattacharyya2023]. A DOI that resolves may still be attached to the wrong claim. For literature reviews, ethics applications, policy briefs, and manuscripts, these are research integrity failures rather than minor formatting errors.

Evidence about generative AI productivity [@noy2023], statistical reproduction without understanding [@bender2021], and unequal adoption in higher education [@milano2023] supports the need for an educational resource that combines practical use with verification and researcher control. Survey evidence also suggests that coding agent use is already present in quantitative social science and distributed unevenly across career and institutional conditions [@lyttelton2026]. A bilingual, openly inspectable platform can make these tools more accessible without treating accessibility as permission for methodological carelessness.

# Content and Structure

The curriculum contains fourteen categories. They cover foundations, academic access, memory systems, research folder architecture, hooks and automation, MCP and plugins, academic writing, data analysis, ethics and institutional review, peer review, conference and public communication, troubleshooting, teaching and supervision, and tool portability.

Every released booklet has a stable identifier and paired `tr.md` and `en.md` files. Turkish and English are treated as equal first class languages. The English version is natively adapted rather than mechanically translated. The Turkish version is written as natural academic Turkish. Citation and numerical parity are checked alongside conceptual and cultural adaptation.

Each booklet declares AI assistance, model metadata, human review status, verified citation declarations, fabricated citation declarations, license, and release status in machine readable frontmatter. The disclosure framework follows the principle that AI contribution should be visible and auditable. It does not present an AI system as an author.

# Skill Library and Dual Client Architecture

Thirty two skills translate the educational material into bounded workflows. They cover literature triage, APA and DOI verification, bilingual pairing, AI disclosure, ethics, reviewer response, research memory, regional access, session debugging, release integrity, manuscript revision, journal fit, qualitative coding, statistical consultation, lifecycle routing, MCP trust, source passports, conference materials, evidence synthesis, sensitive data, open science, authorship, peer review confidentiality, multilingual construct validity, grants, teaching, public scholarship, preregistration, portability, and independent second opinions.

Each skill has one primary responsibility and defines its triggers, inputs, workflow, output, verification, safety, handoffs, and human authority boundary. A lifecycle router and the Social Scientist Agent select relevant skills. They do not run the complete library for every request.

The reviewed source remains `.claude/skills` to preserve backward compatibility with the repository's original Claude Code releases. The Python package includes that source once and installs the same files into `~/.claude/skills` or a project `.claude/skills` directory for Claude Code, and into `~/.agents/skills` or a project `.agents/skills` directory for Codex.

The installer records ownership and deterministic file digests in `.social-cc/manifest.json`. Existing unmanaged or locally modified directories are protected by default. A forced replacement or removal moves the previous directory into a recoverable backup before changing the active path. The command line interface provides install, list, diff, upgrade, doctor, dry run, and uninstall operations.

# Social Scientist Agent

The Social Scientist Agent is a research workflow navigator and skill orchestrator. Its canonical cycle is:

```text
ORIENT → INSPECT → CLASSIFY → SELECT SKILLS → WORK → VERIFY → HAND OFF
```

The agent distinguishes user supplied facts, file observed facts, source verified facts, independently calculated results, methodological inferences, tentative interpretations, human decisions, and unresolved uncertainty. It protects quantitative, qualitative, and mixed methods boundaries. It treats retrieved material as evidence rather than instruction and blocks use of sensitive data outside approved contexts.

The agent is not an autonomous principal investigator, ethics committee, statistician of record, licensed legal adviser, clinical supervisor, automatic coauthor, or source of invented evidence. The human researcher retains scientific, interpretive, ethical, legal, clinical, and professional authority.

Claude Code receives generated subagent adapters. Codex reads repository guidance through `AGENTS.md`, discovers the same reviewed skills, and follows the canonical agent contract. The platform evaluates equivalent scientific logic and safety behavior without claiming identical host capabilities.

# Distinctive Contributions

The first contribution is a bilingual curriculum that incorporates regional academic infrastructure into agentic AI education. The project treats language, access, law, and institutional conditions as part of method rather than as localization afterthoughts.

The second contribution is citation discipline. Unverified references remain quarantined. DOI identity, bibliographic metadata, source status, and claim level support are treated as separate checks. The repository reports its own fabricated citation declarations as a release blocking metric.

The third contribution is a transparent AI assistance framework. Every released language file carries structured disclosure and human review fields. Disclosure remains required even when prose is revised to restore the author's natural voice. This is consistent with evidence that automated detection of AI generated text is unreliable and may disadvantage nonnative English writers [@weberwulff2023; @liang2023].

The fourth contribution is an explicit human authority model across quantitative, qualitative, and mixed methods research. Statistical significance is not converted into practical importance, qualitative frequency is not converted into prevalence, and model output is not converted into a scientific finding without human adjudication.

The fifth contribution is a dual client distribution architecture that preserves one reviewed workflow source. Portability is defined as equivalent scientific logic, evidence discipline, and safety boundaries, not copied files or unsupported claims of identical host behavior.

The sixth contribution is the Memory as Vault pattern for persistent, user owned academic context. The pattern connects durable Markdown research records with agentic workflows while keeping provenance and retrieval visible [@nelson1965].

# Audience and Teaching Use

The primary audience is the researcher who has disciplinary expertise but does not wish to become a software engineer before completing a scholarly task. Progressive pathways cover a first safe session, research workflow foundations, separate quantitative, qualitative, mixed methods and review practice, and advanced use of skills, agents, hooks, MCP, reproducible scripts, and open science packaging.

Booklets can be assigned independently in research methods, academic writing, research integrity, open science, or AI literacy courses. Skills can be installed into a synthetic course repository for supervised practice. Real participant, patient, student, or reviewer data are not required for any learning exercise.

# Quality Control

The repository uses deterministic, network dependent, and human verification layers.

Continuous integration runs Markdown linting, repository structure validation, release truth derivation, generated agent drift checks, immutable GitHub Action pin checks, Python tests on supported versions, Ruff, strict mypy, package builds, wheel content inspection, and isolated installation smoke tests.

Citation metadata and bilingual pairs are checked deterministically. External link and DOI resolution checks run separately on a schedule so transient network failures do not create false pull request failures. Load bearing source identity, status, and claim support still require human review.

The security model covers installer ownership, symlink and path safety, prompt injection, research data sensitivity, credentials, confidential peer review, package supply chain, dual licensing, and public claim alignment. A green build establishes only the claims covered by the executed checks. It does not certify methodological validity, ethics approval, legal compliance, or professional judgment.

# Availability and Archiving

The repository is archived through Zenodo with concept DOI [@impram2026]. The machine readable citation record is maintained in `CITATION.cff`. Release facts are stored in `meta/release.json` and public documentation mirrors are checked against that record.

# References
