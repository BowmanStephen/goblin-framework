# Design Decisions

## Why Small Agents Over Large Ones

Large language models given a full task tend to: over-produce, expand scope, and make assumptions. The Goblin framework addresses this by bounding every agent.

Each goblin has:
- **Explicit territory** — what it can access
- **Explicit permissions** — what it can do
- **Explicit prohibitions** — what it must not do
- **Explicit success criteria** — how to know it's done

No goblin owns the full problem. Each produces within its cage.

## Why Enforcement Before Trust

Most agent frameworks let the model run free and review afterward. The Goblin framework puts enforcement BEFORE production.

- Steward runs after Scout (context gate)
- Steward runs after Tinker (production gate)
- Steward runs after Skeptic (review gate)

This means Steward can block before damage propagates.

## Why Mechanical Enforcement

Steward doesn't interpret. It doesn't decide if a violation is "okay this time." It checks rules mechanically:

- Is the output within approved_scope? ✓/✗
- Is the output outside blocked_scope? ✓/✗
- Does the output match a grudge pattern? ✓/✗

This removes judgment from enforcement and makes violations unambiguous.

## Why Grudges

Grudges are context-aware memory of past failures. Instead of adding more rules, grudges say: "This went wrong before. Here's how to catch it."

This allows the framework to learn from failures without changing the core rules.

## Why Ledger

Every Goblin workflow run produces a ledger entry. This creates an audit trail:

- What was requested
- What was produced
- What was checked
- What was blocked
- Why decisions were made

Ledgers make failures traceable and success repeatable.

## Why Offerings Instead of Prompts

An offering is structured, not freeform. It has:
- task, territory, permissions, constraints, do_not_do, success_criteria, budget, risk_level

This makes the scope machine-checkable. Steward can derive approved_scope and blocked_scope from an offering. A freeform prompt can't be checked this way.

## Why Blocked Scope Includes Inferred Prohibitions

blocked_scope isn't just what the offering says "don't do." It includes:

- Inferred prohibitions from constraints ("must not" → blocked)
- Forbidden actions from ward rules
- Action-requiring-approval that wasn't approved

This prevents goblins from finding loopholes in the offering's language.

## Why Minimal Output

Tinker is constrained to produce minimal viable output. Not because more output is bad, but because:

1. Over-production is the most common agent failure
2. Minimal output is easier to review
3. Adding is safer than removing
4. Every extra line is a potential scope violation

The offering defines "minimal." If it says "design one event," that's one event. Not three. Not a system.