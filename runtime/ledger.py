#!/usr/bin/env python3
"""
Ledger — Structured Run Tracking

Writes a ledger entry for each Goblin workflow run.
Tracks actions, decisions, costs, and outcomes.
"""

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path


def write_ledger(offering: dict, scope: dict, workflow: str,
                 results: list, output_dir: str = "ledgers") -> dict:
    """
    Write a structured ledger entry for a workflow run.

    Args:
        offering: The offering packet
        scope: The approved/blocked scope
        workflow: Name of the workflow
        results: List of step results
        output_dir: Directory to write ledger files

    Returns:
        Ledger entry dict with path included
    """
    data = offering.get("offering", offering)

    # Generate task ID
    task = data.get("task", "unknown")
    task_id = _generate_task_id(task, workflow)

    # Build goblin records
    goblins = []
    for result in results:
        goblins.append({
            "name": result.get("name", result.get("goblin", "unknown")),
            "role": result.get("goblin", "unknown"),
            "status": result.get("status", "unknown"),
            "violations": result.get("violations", []),
            "timestamp": result.get("timestamp", ""),
        })

    # Determine final status
    blocked = any(r.get("status") == "blocked" for r in results)
    final_status = "blocked" if blocked else "completed"

    # Build decisions from offering
    decisions = []
    if scope.get("approved_scope"):
        decisions.append({
            "decision": "Approved scope derived from permissions",
            "rationale": f"Offering grants {len(scope['approved_scope'])} permissions",
        })
    if scope.get("blocked_scope"):
        decisions.append({
            "decision": "Blocked scope derived from do_not_do and constraints",
            "rationale": f"Offering prohibits {len(scope['blocked_scope'])} actions",
        })

    # Build ledger entry
    ledger = {
        "task_id": task_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "workflow": workflow,
        "task": task[:100] if task else "unknown",
        "offering_summary": {
            "permissions": data.get("permissions", []),
            "constraints_count": len(data.get("constraints", [])),
            "do_not_do_count": len(data.get("do_not_do", [])),
            "risk_level": data.get("risk_level", "unknown"),
        },
        "scope": {
            "approved": scope.get("approved_scope", []),
            "blocked": scope.get("blocked_scope", []),
        },
        "goblins": goblins,
        "decisions": decisions,
        "tools_used": [],
        "cost": None,
        "errors": [v for r in results for v in r.get("violations", [])],
        "final_status": final_status,
    }

    # Write to file
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    filename = f"{task_id}.json"
    filepath = output_path / filename

    with open(filepath, "w") as f:
        json.dump(ledger, f, indent=2, default=str)

    ledger["path"] = str(filepath)

    return ledger


def _generate_task_id(task: str, workflow: str) -> str:
    """Generate a deterministic task ID from task description and workflow."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    # Sanitize task for ID use
    task_slug = task[:30].lower().replace(" ", "-").replace(".", "")
    # Remove non-alphanumeric
    task_slug = "".join(c for c in task_slug if c.isalnum() or c == "-")
    return f"{task_slug}-{timestamp}"