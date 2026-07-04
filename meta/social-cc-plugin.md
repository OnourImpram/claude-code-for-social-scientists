# social-cc-plugin

Install the **Claude Code for Social Scientists** project skills into your Claude configuration.

This package bundles twenty Claude Code project skills that turn the booklets in
[claude-code-for-social-scientists](https://github.com/OnourImpram/claude-code-for-social-scientists)
into repeatable, auditable workflows for academic work. The set covers the research lifecycle:
literature triage, regional academic access, MCP stack triage, research vault architecture, source
passport ledgers, bilingual manuscript scaffolding, statistical consultation, qualitative coding
discipline, APA 7 DOI verification, AI disclosure auditing, ethics and IRB protocols, rebuttal
traceability, anti-AI-trace revision, journal fit screening, bilingual conference materials,
research ritual hooks, lifecycle routing, bilingual booklet pairing, agentic session debugging, and
pre-release repository integrity checks. Every skill closes with a Turkish usage section alongside
its English protocol.

## Install

```bash
pip install social-cc-plugin
social-cc install
```

`social-cc install` copies the skills into `~/.claude/skills/`. Use `social-cc install --project` to
write them into the current project's `.claude/skills/` directory instead, `--dry-run` to preview
without writing, and `--force` to overwrite existing skill directories. `social-cc list` shows what
is bundled.

## What the skills do

The skills carry repeatable operating protocols, not new scholarly content. Each skill states when
to use it, expected inputs, a workflow, an output format, verification checks, and explicit safety
boundaries. They never request credentials, never bypass paywalls or access controls, and never
invent citations.

## License

The installer code is licensed under Apache-2.0. The bundled skill content is licensed under
CC-BY-NC-SA-4.0, the same terms as the guide's prose: non-commercial use with attribution and
share-alike. Full license text lives in the
[repository](https://github.com/OnourImpram/claude-code-for-social-scientists).

## Citation

Cite the guide through its Zenodo concept DOI
[10.5281/zenodo.20289687](https://doi.org/10.5281/zenodo.20289687), which always resolves to the
latest version.
