#!/usr/bin/env python3
"""
Goblin Framework Runtime — Main Orchestrator

Deterministic first. No LLM calls.
Loads offering packet, validates, builds scope, runs Steward checks, writes ledger.
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone

from schema import validate_offering, build_scope
from steward import steward_check
from ledger import write_ledger


def load_offering(path: str) -> dict:
    """Load an offering packet from YAML file."""
    p = Path(path)
    if not p.exists():
        print(f"ERROR: Offering packet not found: {path}")
        sys.exit(1)
    with open(p) as f:
        return yaml.safe_load(f)


def load_workflow(path: str) -> dict:
    """Load a workflow definition from YAML file."""
    p = Path(path)
    if not p.exists():
        print(f"ERROR: Workflow not found: {path}")
        sys.exit(1)
    with open(p) as f:
        return yaml.safe_load(f)


def load_grudges(grudge_path: str = None) -> list:
    """Load grudge book if available."""
    if grudge_path is None:
        grudge_path = Path(__file__).parent.parent / "core" / "grudge-book.yaml"
    p = Path(grudge_path)
    if not p.exists():
        return []
    with open(p) as f:
        data = yaml.safe_load(f)
    return data if isinstance(data, list) else []


def run_step(step: dict, offering: dict, scope: dict, grudges: list, context: dict) -> dict:
    """Run a single workflow step deterministically."""
    goblin = step.get("goblin", "unknown")
    description = step.get("description", "")
    name = step.get("name", goblin)

    print(f"\n{'='*60}")
    print(f"STEP: {name} ({goblin})")
    print(f"{'='*60}")
    if description:
        print(f"  {description}")

    result = {
        "goblin": goblin,
        "name": name,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pending",
        "violations": [],
        "output": None,
    }

    if goblin == "steward":
        # Steward runs mechanically — no LLM needed
        check_input = context.get("previous_output", offering)
        check_result = steward_check(check_input, offering, scope, grudges)
        result["status"] = check_result["status"]
        result["violations"] = check_result.get("violations", [])
        result["output"] = check_result

        if check_result["status"] == "blocked":
            print(f"\n  ⛔ STEWARD BLOCKED")
            for v in check_result.get("violations", []):
                print(f"    - {v.get('rule', 'unknown')}: {v.get('detail', '')}")
            print(f"\n  Halting workflow.")
            return result

        print(f"  ✅ Steward cleared")

    elif goblin == "ledger":
        # Ledger step — write the final ledger
        result["status"] = "completed"
        result["output"] = context

    else:
        # Scout, Tinker, Skeptic — placeholder for LLM integration
        # In runtime alpha, these are logged but not executed
        print(f"  ⏳ {goblin.title()} step — requires LLM integration")
        print(f"  In production, this would invoke the {goblin} prompt.")
        result["status"] = "skipped_alpha"
        result["output"] = {
            "note": f"{goblin} requires LLM integration; skipped in alpha runtime",
            "description": description,
        }

    return result


def run_workflow(offering_path: str, workflow_path: str) -> dict:
    """Run a complete Goblin workflow deterministically."""
    print("GOBLIN FRAMEWORK RUNTIME v0.2.0-alpha")
    print("=" * 60)

    # Load resources
    offering = load_offering(offering_path)
    workflow = load_workflow(workflow_path)
    grudges = load_grudges()

    print(f"\nOffering: {offering_path}")
    print(f"Workflow: {workflow_path}")
    print(f"Grudges loaded: {len(grudges)}")

    # Validate offering packet
    print(f"\n{'='*60}")
    print("VALIDATING OFFERING PACKET")
    print(f"{'='*60}")

    validation = validate_offering(offering)
    if not validation["valid"]:
        print("  ⛔ Invalid offering packet:")
        for err in validation["errors"]:
            print(f"    - {err}")
        sys.exit(1)

    print("  ✅ Offering packet valid")
    for key in ["task", "permissions", "constraints", "do_not_do"]:
        val = offering.get(key, "")
        if isinstance(val, list):
            print(f"    {key}: {len(val)} items")
        else:
            print(f"    {key}: {str(val)[:60]}...")

    # Build scope from offering
    scope = build_scope(offering)
    print(f"\n  Approved scope: {len(scope['approved_scope'])} items")
    print(f"  Blocked scope: {len(scope['blocked_scope'])} items")

    # Run each step
    results = []
    context = {
        "offering": offering,
        "scope": scope,
        "grudges": grudges,
        "workflow": workflow.get("name", "unknown"),
        "previous_output": None,
    }

    steps = workflow.get("steps", [])
    print(f"\nWorkflow: {workflow.get('name', 'unnamed')}")
    print(f"Steps: {len(steps)}")

    for step in steps:
        result = run_step(step, offering, scope, grudges, context)
        results.append(result)

        # If Steward blocked, halt
        if result.get("status") == "blocked":
            break

        # Pass output to next step
        context["previous_output"] = result.get("output", {})
        context[f"step_{result['name']}"] = result

    # Write ledger
    print(f"\n{'='*60}")
    print("WRITING LEDGER")
    print(f"{'='*60}")

    ledger = write_ledger(
        offering=offering,
        scope=scope,
        workflow=workflow.get("name", "unnamed"),
        results=results,
        output_dir=str(Path(__file__).parent.parent / "ledgers"),
    )

    print(f"  ✅ Ledger written: {ledger['path']}")
    print(f"  Task: {ledger['task_id']}")
    print(f"  Status: {ledger.get('final_status', 'unknown')}")

    # Summary
    print(f"\n{'='*60}")
    print("RUN SUMMARY")
    print(f"{'='*60}")
    completed = sum(1 for r in results if r["status"] == "completed")
    blocked = sum(1 for r in results if r["status"] == "blocked")
    skipped = sum(1 for r in results if r["status"] == "skipped_alpha")

    print(f"  Steps run: {len(results)}")
    print(f"  Completed: {completed}")
    print(f"  Blocked: {blocked}")
    print(f"  Skipped (alpha): {skipped}")

    if blocked > 0:
        print(f"\n  ⛔ Workflow halted by Steward enforcement.")
        print(f"  Fix violations and re-run.")

    return {
        "offering": offering,
        "scope": scope,
        "results": results,
        "ledger": ledger,
    }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Goblin Framework Runtime")
    parser.add_argument("offering", help="Path to offering packet YAML")
    parser.add_argument("-w", "--workflow", default=None,
                       help="Path to workflow YAML (default: workflows/default.yaml)")
    parser.add_argument("-o", "--output", default=None,
                       help="Output directory for ledger (default: ledgers/)")

    args = parser.parse_args()

    # Default workflow path
    if args.workflow is None:
        args.workflow = str(Path(__file__).parent.parent / "workflows" / "default.yaml")

    result = run_workflow(args.offering, args.workflow)

    # Exit code
    blocked = any(r.get("status") == "blocked" for r in result["results"])
    sys.exit(1 if blocked else 0)


if __name__ == "__main__":
    main()