# Changelog

All notable changes to the Goblin Framework.

## [0.2.0-alpha] - 2026-04-30

### Added
- **Runtime alpha**: Deterministic orchestrator that loads offering packets, validates fields, builds scope, runs Steward gates mechanically
- **Steward enforcement**: Mechanical ward checks — territory, permissions, do_not_do, approval_requests, blocked_scope, grudge patterns, output format
- **Schema validation**: Offering packet field validation with required/recommended checks
- **Scope construction**: Derives approved_scope and blocked_scope from permissions, do_not_do, constraints, and inferred blocks
- **Ledger writing**: Structured JSON run tracking with task IDs, timestamps, goblin records, decisions
- **Default workflow**: Generic 7-step Goblin loop (scout → steward → tinker → steward → skeptic → steward → ledger)
- **Scout prompt**: Context-gathering prompt for pre-production intelligence
- **Skeptic prompt**: Review/quality prompt for post-production evaluation
- **Version tracking**: VERSION file and CHANGELOG.md
- **Steward checklist**: YAML checklist defining mechanical gate criteria

### Known Issues
- Steward checks run against offering when no goblin output available (alpha limitation)
- `check_output_format()` is a no-op
- Grudge matching is keyword-based and fragile
- No LLM integration — Scout, Tinker, Skeptic are skipped steps
- No tests
- Inferred blocks hardcoded in Python instead of loaded from ward-rules.yaml

## [0.1.0-spec] - 2026-04-29

### Added
- Goblin Charter: principles, vocabulary, enforcement-before-trust
- Four goblin roles: Scout, Tinker, Skeptic, Steward
- Offering packet schema
- Ward rules schema
- Grudge book format
- Tinker, Steward, Scout, Skeptic definitions
- Tinker, Steward prompts
- Sample token-drift workflow and run
- Analytics schema workflow and run
- Design decisions and known limitations
- README with quickstart