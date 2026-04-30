# Design Decisions

## Why "Goblin"?

Small, specialized, territorial. The name reinforces the key principle: agents are bounded creatures that own a defined patch of work. Also: memorable names beat generic ones.

## Why separation of thinking and acting?

LLMs that jump straight to output lose traceability. The Think→Plan→Produce→Flag structure gives reviewers (human or Skeptic) something to audit. Every decision has a rationale, not just a result.

## Why structured output instead of free-form?

Structured output (YAML artifacts) enables:
- Programmatic validation
- Automated handoffs between goblins
- Ledger entries that are machine-parseable
- Easier testing and evaluation

Free-form text is fine for humans. Goblins need contracts.

## Why is budget optional?

Some tasks genuinely have no budget constraint (internal tooling, quick scripts). Making budget required adds friction for zero gain. Instead, budget defaults to null (unlimited) and goblins are expected to note when they're approaching limits.

## Why is Scout not just "context gathering"?

Because context gathering without structure produces information dumps. Scout produces a structured context report that maps directly to an offering packet for Tinker. The output format matters as much as the data.

## Why is Skeptic a separate goblin and not a system prompt?

System prompts get ignored under pressure. A separate goblin with its own output format, explicit checklist, and blocking authority is harder to bypass. Skeptic doesn't just "consider" safety — it has a verdict field that can stop the pipeline.

## Why YAML for schemas?

Human-readable, composable, easy to edit by hand. JSON works too but YAML is friendlier for the offering-packet and workflow files that users will write frequently. The goblins themselves can output in YAML or JSON — the schema is format-agnostic.

## Merged prompts/ and goblins/ — why separate?

A goblin's role definition (what it is) and its prompt (what it says) serve different purposes. The role definition is documentation and design reference. The prompt is operational. They change on different schedules. You might update a prompt's tone without changing the role definition. Keeping them separate lets you iterate on prompts without losing the design intent.

## Design mode vs execution mode

The first grudge recorded in this framework came from Hermes itself: interpreting "build the repo" as permission to push code to GitHub. This taught us that design and execution must be explicitly distinguished. A goblin in design mode produces drafts — nothing more. Execution requires explicit approval from an orchestrator or human. No goblin should assume it has permission to act in the real world.