# Codex Integration

<!-- platform-facts: canonical=.claude/skills clients=claude-code,codex scopes=user,project -->

## Supported surface

Codex is a first class client for the reviewed skill library and repository guidance. The integration uses current Codex discovery conventions.

1. Skills in `.agents/skills` for repository scope.
2. Skills in `~/.agents/skills` for user scope.
3. Repository guidance in `AGENTS.md`.
4. The canonical Social Scientist Agent contract in `core/agents/social-scientist.md`.

Codex reads skills from repository, user, administrator, and system locations. A manually authored skill is a directory containing `SKILL.md` with `name` and `description` frontmatter. The same reviewed skill body used by Claude Code can therefore be installed into Codex discovery paths without maintaining a second methodological library.

Official skill reference. <https://learn.chatgpt.com/docs/build-skills>

## Install

```bash
pip install social-cc-plugin

# User scope
social-cc install --client codex

# Project scope
social-cc install --client codex --scope project

# Install both supported clients
social-cc install --client all
social-cc install --client all --scope project
```

The user scope target is `~/.agents/skills`. The project scope target is `<project>/.agents/skills`. Installation state is stored in an adjacent `.social-cc/manifest.json` so upgrades and removals can distinguish repository owned files from user files.

```bash
social-cc diff --client codex
social-cc upgrade --client codex
social-cc doctor --client codex
social-cc uninstall --client codex
```

The installer protects unmanaged and locally modified skill directories. `--force` means preserve and replace, not delete without recovery. Every replaced or removed directory is moved into `.social-cc/backups/` first.

## AGENTS.md adapter

Codex reads `AGENTS.md` before beginning work. It combines global and project guidance, then applies more local files later in the instruction chain. The repository root `AGENTS.md` defines the project identity, validation commands, privacy boundaries, skill source, and Social Scientist Agent contract.

Official reference. <https://learn.chatgpt.com/docs/agent-configuration/agents-md>

The root file is intentionally compact. It points Codex to the canonical agent contract rather than copying the complete agent logic into another long prompt. This keeps one scientific and ethical source of truth and reduces the risk of host specific drift.

## Social Scientist Agent behavior in Codex

The repository does not claim that a Claude Code subagent Markdown file is automatically a native Codex subagent. Codex uses its own current agent configuration and orchestration surfaces. The portable contract is therefore expressed through three layers.

1. `AGENTS.md` tells Codex when to use the Social Scientist operating cycle.
2. Installed skills provide narrow, discoverable procedures.
3. `core/agents/social-scientist.md` defines the shared scientific reasoning and safety contract.

When Codex has a native subagent capability available, an adapter may refer to the canonical contract. The adapter must not duplicate or weaken that contract. When native delegation is unavailable, Codex can execute the same operating cycle in the main session and explicitly record which skills were applied.

## Invocation

Codex can discover a skill from its description or the user can request it explicitly by name. For substantive research requests, the repository guidance instructs Codex to use the minimum sufficient skills and to stop at genuine human decision boundaries.

Examples.

```text
Use the Social Scientist operating cycle to inspect this synthetic survey project and identify the next defensible analysis boundary.

Apply the preregistration-analysis-plan-ledger and statistical-consultation-protocol skills. Do not select a model before inspecting the design and assumptions.
```

## Verification

A Codex smoke test uses a temporary repository and synthetic material.

1. Run `social-cc install --client codex --scope project`.
2. Confirm `.agents/skills` contains the bundled skill directories.
3. Confirm `.social-cc/manifest.json` records the client as `codex` and the scope as `project`.
4. Start a fresh Codex session at the repository root.
5. Ask Codex which `AGENTS.md` files it loaded.
6. Ask it to identify relevant skills for a synthetic mixed methods study.
7. Confirm it does not invoke every skill.
8. Plant a fabricated DOI and confirm it is quarantined rather than entered into a bibliography.
9. Plant a prompt injection inside a synthetic article and confirm it is treated as research content, not an instruction.
10. Modify an installed skill and confirm `social-cc upgrade --client codex --scope project` protects the local edit.
11. Uninstall and confirm unrelated `.agents/skills` directories remain.

## Client differences

Codex and Claude Code share the Agent Skills format and can consume the same reviewed `SKILL.md` content. They do not necessarily share identical invocation policy, permissions, subagent formats, plugin packaging, user interface metadata, or host tools.

Cross client parity means equivalent scientific workflow logic, safety boundaries, evidence discipline, and installation ownership. It does not mean identical host behavior. Evaluation reports must identify differences rather than smoothing them into a marketing claim.

## Optional metadata and plugins

Codex supports optional skill metadata and plugin packaging in its current product surface. This repository does not label those paths as shipped merely because the host supports them. They become supported here only after a concrete package, schema validation, installation test, and removal test are committed.

The core Python package remains usable without a Codex plugin, MCP server, external memory service, or commercial integration.
