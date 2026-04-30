# Goblin Charter (v0.1)

## 1. Purpose

The Goblin Framework defines a way to build AI systems as small, bounded, cooperative agents instead of a single general-purpose assistant.

It prioritizes:
- Clear scope
- Explicit inputs
- Controlled behavior
- Traceable decisions
- Recoverable failures

---

## 2. Core definitions

**Goblin**
A small, task-specific agent with a defined role, limited scope, and constrained capabilities.

**Territory**
The exact domain a goblin can access or act within.
Examples: a document, a repo, a dataset, a workflow step.

**Offering**
The structured input given to a goblin.
Includes context, constraints, permissions, and success criteria.

**Ward**
A rule or system that prevents unsafe or undesired behavior.
Includes permissions, approval gates, and policy checks.

**Steward**
A goblin that enforces wards mechanically. It checks outputs against rules and blocks violations. It does not propose, review, or produce — it gates.

**Grudge**
A recorded failure or undesirable outcome, with instructions to avoid repeating it.

**Ledger**
A record of actions, decisions, inputs, outputs, and costs for a task.

**Approved Scope**
Explicit list of what a goblin is permitted to do in a given task. Derived from the offering packet's permissions field.

**Blocked Scope**
Explicit list of what a goblin is forbidden from doing. Complements approved scope as a hard boundary — not behavioral, but mechanical.

---

## 3. System principles

### 3.1 Small over large
No single goblin should own the full problem. Work is divided into narrow roles.

### 3.2 Explicit over implicit
All tasks must include an offering. No vague requests.

### 3.3 Boundaries over freedom
Every goblin operates within a defined territory and permission set.

### 3.4 Review before action
Non-trivial outputs pass through a skeptic or evaluation step.

### 3.5 Enforcement before trust
Behavioral constraints (prompts) are necessary but insufficient. Mechanical enforcement (Steward) is the backstop. A goblin that ignores its prompt is a bug. Steward is the catch.

### 3.6 Memory with evidence
Grudges must reference a real failure, not intuition.

### 3.7 Actions are reversible
Any operation that changes state must have a rollback or require approval.

### 3.8 Everything leaves a trace
All decisions and tool calls are recorded in the ledger.

---

## 4. Goblin roles (v0)

**Scout**
- Gathers context
- Identifies missing information
- Defines the problem space

**Tinker**
- Proposes solutions
- Produces drafts (not executions)
- Surfaces approval requests for any action requiring sign-off

**Skeptic**
- Reviews outputs
- Identifies risks and weak assumptions
- Blocks unsafe or low-quality results

**Steward**
- Enforces wards mechanically
- Checks scope, permissions, and approval gates
- Blocks outputs that violate rules
- Runs before Skeptic (structural checks first, quality checks second)

---

## 5. Operating loop

1. Receive request
2. Define territory
3. Build offering
4. Derive approved_scope and blocked_scope
5. Assign goblins
6. Scout gathers context
7. **Steward checks Scout output**
8. Tinker proposes solution
9. **Steward checks Tinker output**
10. Skeptic reviews
11. Produce output
12. Record ledger
13. Add grudge if needed

---

## 6. Safety model (Wards)

Minimum required wards:
- **Permission boundary**: limit accessible tools and data
- **Approval gate**: required for risky actions
- **Constraint enforcement**: validate outputs against rules
- **Audit log**: record all actions
- **Scope enforcement**: approved_scope and blocked_scope as hard boundaries

Wards are enforced at two levels:
- **Behavioral**: goblin prompts instruct the model what not to do
- **Mechanical**: Steward validates outputs against rules programmatically

Both are required. Behavioral wards prevent intent. Mechanical wards prevent execution.

---

## 7. Memory model

Memory is structured and scoped:
- **Task memory**: context for the current run
- **Preference memory**: user-specific patterns
- **Grudge memory**: past failures and blocked behaviors

Memory must be:
- **Attributed** (source, time)
- **Testable** (can be validated)
- **Expirable** (optional)

---

## 8. Non-goals

The system does not aim to:
- Create fully autonomous agents without oversight
- Allow unrestricted tool access
- Replace human approval in high-risk actions
- Maintain hidden or opaque reasoning
- Eliminate the need for mechanical enforcement