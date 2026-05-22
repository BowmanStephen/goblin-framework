---
title: "Introducing the Goblin Framework — Small, Bounded, Cooperative AI Agents"
description: "Unbounded agents are dangerous. Multi-agent systems need governance. Enter the Goblin Framework."
date: 2026-05-22
tags: [ai, agent-architecture, python, opensource, governance]
---

# Introducing the Goblin Framework

**Small, bounded, cooperative AI agents. Governed by principle, enforced by code.**

If you've been shipping AI agents to production, you already know the nightmare. You give a model a goal and hope it doesn't:

- `rm -rf /` your deployment
- Exfiltrate customer PII because nobody said "don't"
- Run up $4,000 in API costs before anyone checks the bill
- Hal itself into a recursive loop generating 50,000 lines of unrequested code

Monolithic agents fail because they have no boundaries. Multi-agent systems fail because they have no governance.

I've been building AI systems long enough to know that **trust is not an architecture**. You can't prompt-engineer your way out of a system that has no cage. You can't say "be safe" and expect a stochastic parrot to interpret that the same way you do.

So I built a cage.

## Enter: The Goblin Framework

Goblin Framework is an open-source architecture for building AI agent systems that don't lie, don't drift, and don't set things on fire.

Instead of one monolithic "do everything" agent, you get a pipeline of small, specialized agents — **goblins** — each with a tight scope, explicit permissions, and **mechanical enforcement gates**.

No interpreting. No "seems fine." No exceptions.

## The 8 Principles

These aren't suggestions. They're load-bearing walls.

1. **Small over large** — No goblin owns the full problem.
2. **Explicit over implicit** — Every task starts with an offering packet.
3. **Boundaries over freedom** — Declared territory, defined permissions.
4. **Enforcement before trust** — Steward checks mechanically before Skeptic reviews qualitatively.
5. **Review before action** — Skeptic blocks before damage.
6. **Memory with evidence** — Grudges reference real failures, not vibes.
7. **Actions are reversible** — Rollback or approval required.
8. **Everything leaves a trace** — Every decision recorded in the ledger.

## The Loop

```
┌──────────┐   ┌──────────┐   ╔═══════════════╗   ┌──────────┐
│ OFFERING │──▶│  SCOUT   │──▶║   STEWARD    ║──▶│  TINKER  │
│ (Packet) │   │ (Survey) │   ║ (Enforcement)║   │ (Produce)│
└──────────┘   └──────────┘   ╚═══════════════╝   └──────────┘
                                       │
                                       ▼
                                 ╔═══════════════╗
                                 ║   STEWARD    ║── BLOCK ──▶  ⛔
                                 ║ (Enforcement)║
                                 ╚═══════════════╝
                                       │
                                       ▼
                                 ┌──────────┐   ╔═══════════════╗
                                 │ SKEPTIC  │──▶║   STEWARD    ║──┐
                                 │ (Review) │   ║ (Enforcement)║  │
                                 └──────────┘   ╚═══════════════╝  │
                                                         │        │
                                                         ▼        │
                                                    ┌──────────┐  │
                                                    │  LEDGER  │◀─┘
                                                    │ (Record) │
                                                    └──────────┘
```

The Steward gates three times — pre-Scout, pre-Skeptic, and at the exit. Territory checks. Permission checks. `do_not_do` checks. Grudge pattern matches. If it's blocked, it stops. No LLM in the gate. No judgment calls.

## How It Works

Every task starts with an **offering packet** — a YAML file that declares exactly what the task is, what territory it operates in, what permissions it has, what constraints apply, and — crucially — what it must **not** do.

```yaml
task: "Design an analytics event schema for onboarding"
territory: "Product requirements, analytics docs, privacy policy"
permissions: [read_product_requirements, read_analytics_docs]
constraints: ["Must comply with GDPR and CCPA"]
do_not_do:
  - implement tracking code
  - select an analytics vendor
  - access real user data
```

Then you run it:

```bash
python runtime/run.py my-task.yaml
```

The loop executes. Scout surveys. Steward enforces. Tinker produces. Steward enforces again. Skeptic reviews. Steward enforces a third time. Ledger records everything.

## Why This Matters Now

We're entering the era where AI agents don't just chat — they act. They write code, deploy infrastructure, access databases, make API calls, send emails. Every action is a blast radius.

The industry is focused on making agents more capable. I'm focused on making them more **contained**. Because capability without containment is just a bigger fire when it goes wrong.

The Goblin Framework gives you a repeatable, mechanical, auditable way to govern AI agents. Not through corporate policy. Through code.

## What's in the Box

- **Runtime** — Deterministic Python orchestrator with mechanical Steward enforcement
- **Default workflow** — Scout → Steward → Tinker → Steward → Skeptic → Steward → Ledger
- **Offering packet schema** — YAML structure for task definition
- **Role definitions** — Scout, Tinker, Skeptic, Steward with must/must-not contracts
- **Example run** — Complete analytics schema design with trap detection
- **Charter** — The vocabulary and principles that make the framework work

Alpha release covers the mechanical layer. LLM integration for Scout, Tinker, and Skeptic is next.

## The Road Ahead

- LLM runtime integration (bring your own model)
- pip package
- Domain-specific workflows (code review, compliance, data ops)
- More Steward rules and grudge patterns
- Budget enforcement (token, time, cost)

## Get It

```bash
git clone https://github.com/BowmanStephen/goblin-framework.git
cd goblin-framework
pip install pyyaml
python runtime/run.py examples/tasks/your-task.yaml
```

Or just read the [Charter](https://github.com/BowmanStephen/goblin-framework/blob/main/goblin-charter.md). It's 5 minutes and will tell you everything about how this thing thinks.

---

*Goblins don't get big jobs. They get small jobs they can't screw up. That's the whole point.*

*The lab is open.*

— Bowman Labs
