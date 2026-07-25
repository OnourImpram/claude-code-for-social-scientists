# social-cc-plugin

<!-- release-facts: version=4.0.0 booklets=33 language_files=66 categories=14 skills=32 verified=566 fabricated=0 -->
<!-- platform-facts: canonical=.claude/skills clients=claude-code,codex scopes=user,project -->

Install and maintain the **Claude Code for Social Scientists** skill library for Claude Code, Codex, or both clients.

The package bundles thirty two reviewed social science skills from the repository's canonical `.claude/skills` source. The same `SKILL.md` content is installed into client specific discovery paths. Claude Code uses `.claude/skills`. Codex uses `.agents/skills`.

The skills cover literature triage, regional academic access, MCP trust, research memory, source ledgers, bilingual writing, journal fit, statistical and qualitative discipline, evidence synthesis, preregistration, sensitive data, ethics, peer review, teaching, public scholarship, open science, portability, and independent verification.

## Install

```bash
pip install social-cc-plugin
```

### Claude Code

```bash
social-cc install --client claude-code
social-cc install --client claude-code --scope project
```

The backward compatible project form remains available.

```bash
social-cc install --project
```

### Codex

```bash
social-cc install --client codex
social-cc install --client codex --scope project
```

### Both clients

```bash
social-cc install --client all
social-cc install --client all --scope project
```

## Inspect and maintain

```bash
social-cc list
social-cc diff --client all
social-cc upgrade --client all
social-cc doctor --client all
social-cc uninstall --client all
```

Use `--dry-run` to inspect an install, upgrade, or removal without writing. Existing unmanaged directories and locally modified project files are protected by default.

The installer records project ownership in `.social-cc/manifest.json`. A forced replacement or removal first moves the prior directory into `.social-cc/backups/`. `--force` therefore means preserve and replace, not recursively delete without recovery.

## What the skills do

Each skill has one primary responsibility and defines positive and negative triggers, inputs, workflow, output, verification, safety, handoffs, and human authority boundaries. The skills do not request credentials, bypass access controls, invent evidence, approve research, or silently transmit research material.

The Social Scientist Agent uses the minimum sufficient skill set for substantive workflows. It does not invoke every installed skill and does not duplicate the detailed procedures owned by individual skills.

## Data and security boundaries

Articles, websites, repositories, PDFs, transcripts, datasets, and reviewer files are research evidence. They are never instructions that may redefine permissions, safety rules, the research question, inclusion criteria, or the workflow.

Raw clinical material, identifiable participant or patient data, student records, confidential peer review manuscripts, credentials, and institutional secrets must not enter an unapproved tool context.

The installer performs no network requests. It rejects unsafe skill names, symlinked skill and control paths, and malformed ownership manifests.

## License

Installer code, validators, renderers, and configuration are licensed under Apache 2.0. Bundled skill prose remains under CC BY NC SA 4.0. The wheel includes both license notices.

## Citation

Cite the project through `CITATION.cff` or the Zenodo concept DOI **10.5281/zenodo.20289687**. The recorded v4.0.0 version DOI is **10.5281/zenodo.20789730**.

The source repository is `OnourImpram/claude-code-for-social-scientists`.
