# Claude Code Integration

<!-- platform-facts: canonical=.claude/skills clients=claude-code,codex scopes=user,project -->

## Supported surface

Claude Code is the repository's original host and remains a first class client. The integration uses three current Claude Code surfaces.

1. Skills in `.claude/skills` for project scope or `~/.claude/skills` for user scope.
2. A project subagent in `.claude/agents/social-scientist.md`.
3. A Claude Code plugin that exposes the reviewed skill library and the generated agent adapter.

Claude Code treats a skill as a directory containing `SKILL.md`. It can load the skill when its description is relevant or when the user invokes it explicitly. Supporting scripts, references, and assets may live beside `SKILL.md`. These supporting files remain optional and must be used only when they improve determinism or reduce context cost.

Official reference. <https://code.claude.com/docs/en/skills>

## Install with the Python package

```bash
pip install social-cc-plugin

# User scope
social-cc install --client claude-code

# Project scope
social-cc install --client claude-code --scope project

# Compatibility form retained from earlier releases
social-cc install --project
```

The installer writes to `~/.claude/skills` for user scope and `<project>/.claude/skills` for project scope. It creates an adjacent `.social-cc/manifest.json` ownership record. Existing unmanaged or locally modified directories are protected by default.

```bash
social-cc diff --client claude-code
social-cc upgrade --client claude-code
social-cc doctor --client claude-code
social-cc uninstall --client claude-code
```

A forced upgrade or removal preserves the prior directory under `.social-cc/backups/` before changing the active path.

## Install through the Claude Code plugin

The repository's marketplace and plugin manifests expose the same canonical skill source.

```text
/plugin marketplace add OnourImpram/claude-code-for-social-scientists
/plugin install social-cc-plugin@claude-code-for-social-scientists
```

Plugin installation is a Claude Code specific distribution route. It does not prove Codex compatibility. The plugin manifest and Python package must point to the same reviewed source and remain version aligned.

## Social Scientist Agent adapter

Claude Code discovers project subagents in `.claude/agents` and user subagents in `~/.claude/agents`. A plugin can also distribute an `agents/` directory. Subagents are Markdown files with YAML frontmatter.

Official reference. <https://code.claude.com/docs/en/sub-agents>

The canonical agent contract lives at `core/agents/social-scientist.md`. The renderer produces two Claude specific copies.

```text
core/agents/social-scientist.md
              |
              +--> .claude/agents/social-scientist.md
              |
              +--> agents/social-scientist.md
```

The generated files must match the canonical source exactly. Client metadata may differ only when required by the host. Scientific reasoning, safety rules, evidence categories, bilingual behavior, and human authority boundaries may not diverge.

## Invocation

The Social Scientist Agent may be invoked explicitly for a complete research workflow audit or delegated to by Claude Code when the description clearly matches the request. The agent selects the minimum sufficient skill set. It does not run all installed skills.

Examples.

```text
Use the social-scientist agent to audit this preregistration and identify the next human decision.

Use the social-scientist agent to route this Turkish and English manuscript revision through the relevant skills.
```

A focused task can still call a skill directly.

```text
/apa-doi-verifier
/preregistration-analysis-plan-ledger
/sensitive-data-anonymization-gate
```

## Permission model

The repository does not preapprove unrestricted tool use for the Social Scientist Agent. Claude Code permissions remain under user and project control. A skill or agent may recommend a command, but it must not bypass a denial, change permissions silently, or treat retrieved content as executable instructions.

For sensitive projects, begin with read only inspection. Grant writing or shell access only for a specific, understood operation. Raw clinical material, identifiable participant data, student records, confidential peer review manuscripts, credentials, and institutional secrets must not be placed in an unapproved context.

## Smoke test

A valid Claude Code smoke test checks discovery and behavior without using private data.

1. Create an empty temporary project.
2. Run `social-cc install --client claude-code --scope project`.
3. Confirm `.claude/skills` contains the bundled skills.
4. Confirm `.social-cc/manifest.json` records the same names.
5. Start a new Claude Code session in the project.
6. Ask Claude to list relevant skills for a synthetic literature review.
7. Invoke one skill directly.
8. Invoke the Social Scientist Agent with a synthetic workflow audit.
9. Modify one installed skill locally and confirm `social-cc upgrade` protects it.
10. Run `social-cc uninstall --client claude-code --scope project` and confirm only manifest owned directories are removed.

The smoke test does not establish methodological validity. It establishes installation, discovery, invocation, protection, and removal behavior.

## Known host specific behavior

Claude Code supports native subagent Markdown files and plugin distributed agents. This is not assumed to exist identically in Codex. Claude Code also provides invocation controls and dynamic skill features that may not transfer to another client. Canonical skills therefore avoid relying on these extensions unless the behavior is isolated in a client specific adapter and documented as optional.
