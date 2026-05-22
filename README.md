# 🧌 Goblin Framework

**Small, bounded, cooperative AI agents. Governed by principle, enforced by code.**

[![Version](https://img.shields.io/badge/version-0.2.0--alpha-blue)]()
[![License](https://img.shields.io/badge/license-MIT-green)]()

Goblin Framework is an open-source architecture for building AI agent systems that don't lie, don't drift, and don't burn your prod database down. Instead of one monolithic "do everything" agent, you get a pipeline of small, specialized agents — **goblins** — each with a tight scope, explicit permissions, and mechanical enforcement gates.

**The loop:** Offering → Scout → Steward → Tinker → Steward → Skeptic → Steward → Ledger.

No unbounded LLM calls. No scope creep. No "I thought you meant..." No surprise bills.

---

## The Problem

Current AI agent architectures are a gamble. You give a big model a big goal and hope it doesn't:

- Write a `rm -rf /` into your deployment pipeline
- Exfiltrate customer PII because nobody said "don't"
- Run up $4,000 in API costs before someone notices
- "Hal" itself into a recursive loop generating 50,000 lines of unrequested code

Monolithic agents fail because they have no boundaries. Multi-agent systems fail because they have no governance.

**Goblin Framework solves both.** Not through trust. Through enforcement.

---

## The 8 Goblin Principles

These aren't suggestions. They're the architecture. Violate any one and the framework stops working.

| # | Principle | What It Means |
|---|-----------|---------------|
| 1 | **Small over large** | No goblin owns the full problem. Each does one thing. |
| 2 | **Explicit over implicit** | Every task starts with an offering packet. No guessing. |
| 3 | **Boundaries over freedom** | Every goblin has a declared territory and defined permissions. |
| 4 | **Enforcement before trust** | Steward checks mechanically before the Skeptic reviews qualitatively. |
| 5 | **Review before action** | Skeptic blocks before damage reaches production. |
| 6 | **Memory with evidence** | Grudges reference real failures — not vibes. |
| 7 | **Actions are reversible** | Rollback or approval required before irreversible moves. |
| 8 | **Everything leaves a trace** | Every decision, every check, every violation — written to the ledger. |

---

## Architecture

### The Goblin Loop

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  ┌──────────┐    ┌──────────┐    ╔═══════════════╗    ┌──────────┐ │
│  │ OFFERING │───▶│  SCOUT   │───▶║   STEWARD    ║───▶│  TINKER  │ │
│  │ (Packet) │    │ (Survey) │    ║ (Enforcement) ║    │ (Produce)│ │
│  └──────────┘    └──────────┘    ╚═══════════════╝    └──────────┘ │
│                                        │                           │
│                                        ▼                           │
│                                  ╔═══════════════╗                 │
│                                  ║   STEWARD    ║──BLOCK──▶  ⛔    │
│                                  ║ (Enforcement) ║                 │
│                                  ╚═══════════════╝                 │
│                                        │                           │
│                                        ▼                           │
│                                  ┌──────────┐    ╔═══════════════╗ │
│                                  │ SKEPTIC  │───▶║   STEWARD    ║─┐│
│                                  │ (Review) │    ║ (Enforcement) ║ ││
│                                  └──────────┘    ╚═══════════════╝ ││
│                                                         │         ││
│                                                         ▼         ││
│                                                    ┌──────────┐   ││
│                                                    │  LEDGER  │◀──┘│
│                                                    │ (Record) │    │
│                                                    └──────────┘    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### How It Works

1. **Offering** — A YAML packet that defines the task, territory, permissions, constraints, and `do_not_do` rules. No offering, no task. No exceptions.
2. **Scout** — Gathers context, identifies gaps, surfaces risks. Scouts don't produce — they illuminate.
3. **Steward** (Gate 1) — Mechanically checks Scout stayed in territory. No interpretation. No judgment. Block or pass.
4. **Tinker** — Produces output within approved scope. Minimal. One pass. No gold-plating.
5. **Steward** (Gate 2) — Checks Tinker didn't drift, over-produce, or violate constraints.
6. **Skeptic** — Reviews for quality, hidden risks, scope compliance. Returns: approve, approve_with_changes, or block.
7. **Steward** (Gate 3) — Final mechanical check before anything leaves the loop.
8. **Ledger** — Every decision, violation, and output recorded for audit.

**Steward gates are mechanical.** Territory, permissions, `do_not_do`, `approval_requests`, `blocked_scope`, grudge patterns. If it's blocked, it stops. No LLM in the gate. No "seems fine." No exceptions.

---

## Installation

### Option 1: Clone & Run (Current)

```bash
git clone https://github.com/BowmanStephen/goblin-framework.git
cd goblin-framework

# Install dependencies
pip install pyyaml

# Run the default workflow with the example offering
python runtime/run.py examples/offerings/analytics-schema-offering.yaml

# Or run with a custom workflow
python runtime/run.py my-task.yaml -w workflows/token-drift.yaml
```

### Option 2: pip Install (Coming Soon)

```bash
pip install goblin-framework
```

> **Note:** pip package is in development. For now, clone the repo.

---

## Quick Start

### 1. Create an Offering Packet

```yaml
# my-first-task.yaml
task: >
  Design an analytics event schema for tracking a new user onboarding flow.
  Define what to track, naming conventions, and privacy boundaries.

territory: "Product requirements, analytics docs, privacy policy"

permissions:
  - read_product_requirements
  - read_analytics_docs
  - review_privacy_policy
  - propose_schema_designs

constraints:
  - "Must comply with GDPR and CCPA"
  - "Must not define PII-adjacent fields without explicit consent gating"

do_not_do:
  - implement tracking code
  - select an analytics vendor
  - write production code
  - access real user data

success_criteria:
  - "Clear event taxonomy with minimum viable set"
  - "Privacy boundaries are explicit"

risk_level: medium
approval_required:
  - "Final schema adoption"
  - "Any tracking before user consent"
```

### 2. Run the Workflow

```bash
python runtime/run.py my-first-task.yaml
```

### 3. Review the Ledger

```bash
cat ledgers/<task-id>.json
```

---

## Usage Examples

### Basic Task Run

```bash
# Copy the template
cp core/offering-packet.yaml my-task.yaml

# Edit your task, then run
python runtime/run.py my-task.yaml
```

### Custom Workflow

```bash
# Run with a specific workflow
python runtime/run.py my-task.yaml -w workflows/token-drift.yaml
```

### Full Example

See [`examples/analytics-schema-run.md`](examples/analytics-schema-run.md) for a complete walkthrough of an onboarding analytics schema design task — including trap detection (over-instrumentation, scope creep, PII leakage, consent gating).

### Running Programmatically

```python
from runtime.run import run_workflow

result = run_workflow(
    offering_path="my-task.yaml",
    workflow_path="workflows/default.yaml"
)

print(f"Status: {result['ledger']['final_status']}")
print(f"Steps completed: {len(result['results'])}")
```

---

## Repository Structure

| Directory | Purpose |
|-----------|---------|
| [`core/`](core/) | Schemas: offering packets, ward rules, grudge book, ledger, steward checklist |
| [`goblins/`](goblins/) | Role definitions: what each goblin is and does |
| [`prompts/`](prompts/) | Executable prompts for LLM-integrated goblins |
| [`workflows/`](workflows/) | Multi-goblin pipeline definitions (YAML) |
| [`runtime/`](runtime/) | Python orchestrator: deterministic Steward enforcement |
| [`ledgers/`](ledgers/) | Run tracking output (JSON, gitignored) |
| [`examples/`](examples/) | Sample runs with before/after comparisons |
| [`notes/`](notes/) | Design decisions and known limitations |

---

## Version

Current: **0.2.0-alpha** — Runtime alpha with mechanical Steward checks, default workflow, complete prompt set.

See [VERSION](VERSION) and [CHANGELOG.md](CHANGELOG.md).

---

## Contributing

We welcome contributions — but read the Charter first.

1. **Read the [Charter](goblin-charter.md)** — it defines the vocabulary and principles. All contributions must align.
2. **Check [issues](https://github.com/BowmanStephen/goblin-framework/issues)** — find something to work on or open a new one.
3. **Fork & branch** — create a feature branch from `main`.
4. **Keep it small** — one PR, one concern. No gold-plating.
5. **Keep it mechanical** — Steward enforcement must remain deterministic. No LLM in the gate.
6. **Leave a trace** — update the ledger schema if you add new check types.
7. **Open the PR** — describe what you changed and why.

### What We Need Help With

- **LLM runtime integration** — connecting Scout, Tinker, and Skeptic to model backends
- **pip package** — packaging for PyPI
- **More workflows** — domain-specific pipelines (code review, data analysis, compliance)
- **Steward rules** — new mechanical check patterns
- **Documentation** — tutorial, API docs, video walkthroughs

---

## License

[MIT](LICENSE) — goblins are free.

---

## Bowman Labs

> *"The lab is open."*

— Stephen Bowman, [Bowman Labs](https://github.com/BowmanStephen)

Built with Arsenal red, 8-bit grit, and the unshakable conviction that every agent needs a fence.
