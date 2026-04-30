# Goblin Framework

A framework for building AI systems as small, bounded, cooperative agents.

Read the [Charter](goblin-charter.md) first — it defines the vocabulary and principles.

## Quick Start

**1. Create an offering packet:**

```bash
cp core/offering-packet.yaml my-task.yaml
# Edit my-task.yaml: fill in task, territory, permissions, constraints, do_not_do
```

**2. Run the workflow:**

```bash
cd runtime
pip install pyyaml  # if not already installed
python run.py ../my-task.yaml                    # default workflow
python run.py ../my-task.yaml -w ../workflows/token-drift.yaml  # specific workflow
```

**3. Review the ledger:**

```bash
cat ledgers/<task-id>.json
```

The runtime validates your offering, builds scope, runs Steward checks mechanically, and writes a structured ledger. LLM-integrated goblins (Scout, Tinker, Skeptic) require a model runtime — currently skipped in alpha.

## Structure

| Directory | Purpose |
|-----------|----------|
| `core/` | Schemas: offering packets, ward rules, grudge book, ledger, steward checklist |
| `goblins/` | Role definitions: what each goblin is and does |
| `prompts/` | Executable prompts: what you feed the model |
| `workflows/` | Multi-goblin pipelines (YAML) |
| `runtime/` | Python orchestrator: deterministic Steward enforcement |
| `ledgers/` | Run tracking output (JSON, gitignored) |
| `examples/` | Sample runs and before/after comparisons |
| `notes/` | Design decisions and known limitations |

## The Loop

```
Offering → Scout → Steward ✓/✗ → Tinker → Steward ✓/✗ → Skeptic → Steward ✓/✗ → Ledger
```

Steward gates are **mechanical** — territory, permissions, do_not_do, approval_requests, blocked_scope, grudge patterns. No interpretation. No judgment. If it's blocked, it stops.

## Principles

1. **Small over large** — no goblin owns the full problem
2. **Explicit over implicit** — all tasks need an offering
3. **Boundaries over freedom** — defined territory, defined permissions
4. **Enforcement before trust** — Steward checks mechanically before Skeptic reviews qualitatively
5. **Review before action** — Skeptic blocks before damage
6. **Memory with evidence** — grudges reference real failures
7. **Actions are reversible** — rollback or approval required
8. **Everything leaves a trace** — all decisions recorded in ledger

## Current Version

See [VERSION](VERSION) for the current release. See [CHANGELOG.md](CHANGELOG.md) for version history.

- `0.1.0-spec` — Initial specification, roles, schemas, workflows, sample runs
- `0.2.0-alpha` — Runtime alpha with mechanical Steward checks, default workflow, complete prompt set

## Known Limitations

See [notes/known-limitations.md](notes/known-limitations.md) for the honest list. Key ones:

- **Steward is mechanical but not yet in production** — runtime alpha validates offerings and runs checks, but doesn't block LLM calls yet
- **Scout, Tinker, Skeptic require model integration** — runtime runs them as skipped steps pending LLM runtime
- **No orchestration engine** — you can run the deterministic loop, but LLM goblins need a model backend
- **Budget enforcement is aspirational** — budget fields exist but aren't enforced by the runtime