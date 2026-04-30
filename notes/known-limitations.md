# Known Limitations

## Current Limitations (v0.2.0-alpha)

### Runtime

- **Steward checks run against offering when no goblin output is available.** In alpha mode, Scout, Tinker, and Skeptic are skipped. Steward falls back to checking the offering packet against itself, which always clears. This will be fixed when LLM goblins are integrated.

- **check_output_format() is a no-op.** The function exists but performs no validation. It always returns an empty list. Expected output shapes per goblin type need to be defined and enforced.

- **check_territory() only checks for 7 hardcoded execution keywords.** It does not validate that goblin output stayed within declared territory. A goblin accessing backend APIs while claiming territory as "frontend" would not be caught.

- **Grudge matching is fragile.** Keywords are extracted from grudge detection text, filtered by noise words and length, then matched against goblin output. New grudges with short or common detection text can false-positive or false-negative. The `len(k) > 4` filter makes hyphenated single-word grudges impossible to trigger.

- **Inferred blocks are hardcoded in Python.** `schema.py` lines 126-131 add 4 universal blocks ("Deploy to production without explicit approval", etc.) that should come from `ward-rules.yaml` instead. The `ward-rules.yaml` file exists with `forbidden:` and `requires_approval:` lists but the runtime ignores it.

- **No LLM integration.** Scout, Tinker, and Skeptic run as skipped steps in alpha mode. The runtime can only execute Steward gates mechanically. There is no mechanism to invoke LLM goblins with offering context.

- **No prompt template interpolation.** Prompts are static markdown files. There is no code that loads a prompt, injects offering context (task, territory, permissions), and sends it to an LLM.

- **Budget fields are validated but not enforced.** `schema.py` checks that budget is a dict, but the runtime never uses it. No token counting, time tracking, or cost accounting. The ledger always writes `"cost": null`.

- **Ledger schema is not validated.** `core/ledger-schema.yaml` defines the expected ledger structure, but `ledger.py` builds the structure in Python without referencing or validating against this schema.

- **Workflows embed offering packets.** The `analytics-schema.yaml` file bundles the offering packet AND workflow steps AND scope AND expected outputs. The runtime expects a separate offering packet and workflow, and uses `offering.get("offering", offering)` to unwrap. This is confusing and should be cleaner.

- **No rollback mechanism.** Ward rules say "stop_on_violation: true" and the runtime halts. There is no way to resume from a blocked state or roll back partial output.

- **No workflow validation.** `run.py` loads any YAML for workflows. No schema check that required fields (goblin, name) exist. A malformed workflow would crash at runtime.

### Missing Tests

- No test files exist. Not for Steward, not for schema validation, not for runtime integration. For a deterministic enforcement framework, this is a significant gap.

### Structural

- **Scout, Skeptic goblin definitions exist but have no runtime behavior.** They're defined in `goblins/scout.md` and `goblins/skeptic.md` but have no executable code path.

- **Steward prompt exists but is not loaded by the runtime.** `prompts/steward.prompt.md` is the human-readable guide, not the machine-loaded version.

- **prd-cleanup.yaml workflow is untested.** It exists in `workflows/` but hasn't been validated against the runtime.

## Design Decisions (Not Limitations)

These are intentional choices, not bugs:

- **Mechanical over semantic.** Steward checks are keyword-based and deterministic by design. They catch what can be caught with rules, not interpretation. Semantic checks are Skeptic's job.

- **Stop on violation.** When Steward blocks, the workflow halts. No recovery, no partial output. This is intentional — it forces the user to fix the offering or goblin output before proceeding.

- **No rollback.** Blocked runs produce a ledger with violations listed. The user reads the ledger, fixes the issue, and re-runs. Resuming mid-workflow would require understanding partial state, which adds complexity without clear benefit.

- **One offering = one run.** Each run takes one offering packet and produces one ledger. There is no batch mode or multi-offering orchestration yet.