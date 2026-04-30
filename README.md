# Goblin Framework

A framework for building AI systems as small, bounded, cooperative agents.

Read the [Charter](goblin-charter.md) first — it defines the vocabulary and principles.

## Quick Start

```bash
# Run a goblin manually
cat goblins/tinker.md        # Understand the role
cat core/offering-packet.yaml  # Build your offering
cat prompts/tinker.prompt.md   # See how the prompt works
```

## Structure

| Directory | Purpose |
|-----------|---------|
| `core/` | Schemas: offering packets, ward rules, grudge book, ledger |
| `goblins/` | Role definitions: what each goblin is and does |
| `prompts/` | Executable prompts: what you actually feed the model |
| `workflows/` | Multi-goblin pipelines (YAML) |
| `evals/` | Test cases and red-team scenarios |
| `examples/` | Sample runs and before/after comparisons |
| `notes/` | Design decisions and known limitations |

## Principles

1. **Small over large** — no goblin owns the full problem
2. **Explicit over implicit** — all tasks need an offering
3. **Boundaries over freedom** — defined territory, defined permissions
4. **Review before action** — skeptic blocks before damage
5. **Memory with evidence** — grudges reference real failures
6. **Actions are reversible** — rollback or approval required
7. **Everything leaves a trace** — all decisions recorded in ledger