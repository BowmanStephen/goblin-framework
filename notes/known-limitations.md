# Known Limitations (v0.1)

## Tinker over-produces on ambiguous tasks

Tinker has a tendency to define complete systems when only a minimal starting point is needed. This is especially dangerous on tasks with no clear source of truth and high ambiguity (analytics schemas, API designs, data models).

**Mitigation added:**
- Minimality constraint in `goblins/tinker.md`: prefer minimal viable output over complete coverage
- `do_not_do` field in offering packet: explicit negative scope
- `event_decision_map` requirement: every element must justify its inclusion

**Remaining gap:** No mechanical enforcement of minimality. Steward checks scope and permissions but not output volume. A Limiter goblin that cuts excess output could address this.

## Missing "decision mapping" primitive

The analytics schema run revealed that events without a clear decision they support are noise. This should be a required field in any schema or taxonomy output:

```
event:
  name: onboarding.step_completed
  decision_supported: "Where do users stall?"
```

This pattern — every element must justify its inclusion — should generalize beyond analytics to any structured output task.

## Composition model is underspecified

The current operating loop is linear: Scout → Steward → Tinker → Steward → Skeptic. Real work often requires:
- Parallel goblins working on different subtasks
- Iterative loops (Tinker → Skeptic → Tinker revision)
- Conditional branching (different goblins for different outputs)

The token-drift workflow introduces Steward as a separate enforcement pass, which adds structure. But the general composition model (how goblins connect, what triggers which, how loops work) still needs a formal definition.

## Steward is defined but not implemented

Steward is defined as a "mechanical" check but currently exists only as a prompt and a spec. To be truly mechanical, it needs:
- A code layer that validates outputs against ward rules programmatically
- JSON Schema validation for output formats
- Rule-based checks (does the output reference files outside territory? did it call APIs not in permissions?)
- A blocking mechanism that prevents downstream execution

Until Steward is code, it's behavioral — which is exactly the problem it's supposed to solve.

## Grudge decay is manual

Grudges have an `expires` field but no guidance on:
- Who reviews expiring grudges
- What triggers a review
- Whether expired grudges should be archived or deleted

This needs a lifecycle model.

## Budget enforcement is aspirational

Budget fields exist in the offering packet but there's no enforcement mechanism. A goblin that blows past its token budget has no automatic cutoff. This needs either:
- A runtime that tracks token usage and halts
- A post-hoc ledger check that flags budget violations

## Ward enforcement is half behavioral, half mechanical

Ward rules are defined in YAML but enforced in two ways:
- **Behavioral**: prompts tell goblins not to do things
- **Mechanical**: Steward checks outputs against rules

The gap is that behavioral enforcement depends on model compliance, which isn't reliable. The more checks that move to Steward (mechanical), the safer the system. The current balance is tilted toward behavioral.

## No orchestration engine

The framework defines roles, schemas, and workflows conceptually but provides no runtime. Currently this is a specification, not a system. To run goblins, you need either:
- A manual orchestrator (human following the workflow)
- A Hermes skill or delegate_task that implements the loop
- A custom orchestration script

## Testing and evaluation are stubs

The `evals/` directory has schema stubs but no actual test cases or evaluation harness. To make this production-ready:
- Write test cases for each goblin role
- Build a red-team suite for ward violations
- Define pass/fail criteria for Skeptic reviews
- Create automated regression tests for known grudges
- Add Steward-specific tests that verify mechanical enforcement

## approved_scope / blocked_scope is a new pattern

The token-drift workflow introduces explicit scope declarations (approved_scope and blocked_scope) derived from the offering packet. This pattern needs to be generalized — every workflow should produce these, and Steward should enforce them. Currently it's defined in one workflow file but not in the core schema.

## Negative scope (do_not_do) is a new pattern

The analytics schema run revealed that `do_not_do` (explicit negative scope) is as important as `permissions` (positive scope). Without it, Tinker fills in gaps with assumptions about what's allowed. This field has been added to the offering packet schema but needs validation that it's used in every workflow.

## Steward needs intent classification

Steward currently checks permissions, scope, and approvals. It may also need to classify intent:
- "design schema" ✅ (within scope)
- "instrument events in code" ❌ (execution, not design)

Without intent classification, a clever Tinker can reframe execution as design and bypass scope boundaries.