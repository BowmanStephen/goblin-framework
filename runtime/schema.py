#!/usr/bin/env python3
"""
Schema — Offering Packet Validation and Scope Construction

Validates offering packets against required fields and derives
approved_scope / blocked_scope from permissions and constraints.
"""

from typing import Any

# Required fields for a valid offering packet
REQUIRED_FIELDS = ["task", "permissions"]
RECOMMENDED_FIELDS = ["territory", "constraints", "do_not_do", "success_criteria"]

def validate_offering(offering: dict) -> dict:
    """
    Validate an offering packet has required fields and structure.

    Returns:
        {
            "valid": bool,
            "errors": [...],
            "warnings": [...]
        }
    """
    errors = []
    warnings = []

    if not isinstance(offering, dict):
        return {"valid": False, "errors": ["Offering must be a dictionary"], "warnings": []}

    # Check offering is nested under 'offering' key or flat
    data = offering.get("offering", offering)

    # Required fields
    for field in REQUIRED_FIELDS:
        if field not in data or not data[field]:
            errors.append(f"Missing required field: '{field}'")

    # Check task is specific enough
    task = data.get("task", "")
    if isinstance(task, str) and len(task) < 20 and task:
        warnings.append(f"Task description may be too vague: '{task[:50]}...'")

    # Check permissions is a list
    permissions = data.get("permissions", [])
    if not isinstance(permissions, list):
        errors.append("'permissions' must be a list")
    elif len(permissions) == 0:
        errors.append("'permissions' must not be empty — specify what the goblin CAN do")

    # Check do_not_do is a list if present
    do_not_do = data.get("do_not_do", [])
    if do_not_do and not isinstance(do_not_do, list):
        errors.append("'do_not_do' must be a list")

    # Check budget structure if present
    budget = data.get("budget", {})
    if budget and not isinstance(budget, dict):
        errors.append("'budget' must be a dictionary")

    # Recommended fields
    for field in RECOMMENDED_FIELDS:
        if field not in data:
            warnings.append(f"Missing recommended field: '{field}'")

    # Check risk_level if present
    risk = data.get("risk_level", "")
    if risk and risk not in ("low", "medium", "high"):
        warnings.append(f"risk_level should be 'low', 'medium', or 'high', got: '{risk}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def build_scope(offering: dict) -> dict:
    """
    Derive approved_scope and blocked_scope from the offering packet.

    Approved scope comes from permissions + territory.
    Blocked scope comes from do_not_do + constraints + inferred prohibitions.

    Returns:
        {
            "approved_scope": [...],
            "blocked_scope": [...]
        }
    """
    data = offering.get("offering", offering)

    approved_scope = []
    blocked_scope = []

    # Approved scope from permissions
    permissions = data.get("permissions", [])
    approved_scope.extend(permissions)

    # Approved scope from territory
    territory = data.get("territory", "")
    if territory:
        approved_scope.append(f"Access resources in: {territory}")

    # Blocked scope from do_not_do
    do_not_do = data.get("do_not_do", [])
    blocked_scope.extend(do_not_do)

    # Blocked scope from constraints — inferred prohibitions
    constraints = data.get("constraints", [])
    for constraint in constraints:
        constraint_str = str(constraint).lower()
        # Extract prohibitions from constraint text
        if "must not" in constraint_str:
            blocked_scope.append(f"Constraint prohibits: {constraint}")
        elif "must never" in constraint_str:
            blocked_scope.append(f"Constraint prohibits: {constraint}")
        elif "no " in constraint_str:
            blocked_scope.append(f"Constraint prohibits: {constraint}")

    # Inferred blocked scope — actions no offering should allow without
    # explicit permission
    inferred_blocks = [
        "Deploy to production without explicit approval",
        "Modify systems outside declared territory",
        "Access secrets or credentials not in territory",
        "Send communications without approval",
    ]
    blocked_scope.extend(inferred_blocks)

    # Deduplicate
    approved_scope = list(dict.fromkeys(approved_scope))
    blocked_scope = list(dict.fromkeys(blocked_scope))

    return {
        "approved_scope": approved_scope,
        "blocked_scope": blocked_scope,
    }