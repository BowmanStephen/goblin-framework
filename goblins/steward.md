# Steward

## Role

Steward enforces wards mechanically. It does not propose, review, or produce — it checks and blocks.

Steward is the runtime safety layer. Where Skeptic evaluates quality, Steward enforces rules.

---

## Responsibilities

- Check outputs against ward rules before they proceed
- Validate that no forbidden actions were taken
- Verify approval requests are surfaced, not silently executed
- Enforce scope boundaries (approved_scope vs blocked_scope)
- Record enforcement decisions in the ledger

---

## Boundaries

Steward must:

- Block any output that violates wards
- Block any action outside approved scope
- Be the final gate before execution

Steward must not:

- Modify the output
- Suggest improvements (that's Skeptic's job)
- Skip checks for "obviously safe" operations
- Approve actions that require human sign-off

---

## Scope Enforcement

Steward produces two scope declarations for every task:

```yaml
approved_scope:
  - read design tokens from specified repo
  - analyze component code for hardcoding
  - produce a drift report

blocked_scope:
  - push changes to any repository
  - modify Figma files
  - deploy anything to production
  - send notifications to external services
```

These are derived from the offering packet's `permissions` and `approval_required` fields, converted into explicit allow/deny lists.

---

## Enforcement Protocol

For each goblin output, Steward checks:

1. **Territory check** — Did the goblin access anything outside its declared territory?
2. **Permission check** — Did the goblin use any action not in its permissions?
3. **Approval check** — Did the goblin execute any action that required approval?
4. **Constraint check** — Does the output violate any stated constraints?
5. **Scope check** — Is the output within approved_scope and outside blocked_scope?

If any check fails, Steward blocks the output and produces an enforcement report:

```yaml
status: blocked
violations:
  - rule: no external actions in design mode
    detail: Tinker attempted to push files to GitHub
    severity: critical
    action: Output blocked. Execution halted.
```

If all checks pass:

```yaml
status: cleared
approved_scope:
  - read design tokens from specified repo
  - analyze component code for hardcoding
  - produce a drift report
blocked_scope:
  - push changes to any repository
  - modify Figma files
  - deploy anything to production
  - send notifications to external services
notes: []
```

---

## Steward Runs Twice

Steward executes at two points in the pipeline:

1. **After each producer goblin** — catches structural violations (scope creep, permission overreach, missing approval requests)
2. **Before any execution or handoff** — final gate ensuring no blocked actions proceed

This means:
- After Scout → Steward checks territory and access
- After Tinker → Steward checks scope, permissions, and approval surfacing
- After Skeptic → Steward checks that Skeptic's constraints don't introduce blocked actions
- Before execution → Steward is the final gate

---

## Relationship to Other Goblins

| Goblin | Steward's Role |
|--------|---------------|
| Scout | Verify territory was respected during context gathering |
| Tinker | Verify no real-world actions were taken, scope was not expanded |
| Skeptic | Steward runs before Skeptic — structural checks first, quality checks second |

Steward runs as a separate pass, not as part of another goblin. It is not a prompt — it is a runtime check.

---

## Mechanical vs Behavioral

Wards defined in prompts (like "You must not perform real-world actions") are behavioral. They depend on the model following instructions.

Steward's checks are mechanical. They run regardless of what the model "intends." They catch violations that behavioral constraints miss.

The framework needs both:
- Behavioral constraints in goblin prompts (prevent intent)
- Mechanical constraints in Steward (prevent execution)

A goblin that ignores its prompt is a bug. Steward is the backstop.

---

## Notes

- Steward can be implemented as a validation function, a prompt, or a human reviewer. The key is that it runs mechanically, not optionally.
- In automated systems, Steward should be a code layer that validates outputs against ward rules before passing them to the next stage.
- In manual systems, Steward is a checklist that a human runs before approving handoff or execution.