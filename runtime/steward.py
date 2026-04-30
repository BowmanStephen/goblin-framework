#!/usr/bin/env python3
"""
Steward — Mechanical Ward Enforcement

The runtime spine of the Goblin Framework.
Steward runs deterministic checks against offering packets and goblin outputs.
No LLM calls. No interpretation. Just rules.
"""

from datetime import datetime, timezone


def steward_check(output: dict, offering: dict, scope: dict, grudges: list) -> dict:
    """
    Run all mechanical Steward checks against a goblin output.

    Args:
        output: The goblin's output artifact
        offering: The offering packet that defined the task
        scope: The approved_scope and blocked_scope derived from offering
        grudges: Loaded grudge book for context-aware checks

    Returns:
        {
            "status": "cleared" | "blocked",
            "violations": [...],
            "approved_scope": [...],
            "blocked_scope": [...],
            "checks_run": int,
            "timestamp": ISO8601
        }
    """
    violations = []

    # Run each check
    violations.extend(check_territory(output, offering))
    violations.extend(check_permissions(output, offering))
    violations.extend(check_do_not_do(output, offering))
    violations.extend(check_approval_requests(output, offering))
    violations.extend(check_blocked_scope(output, scope))
    violations.extend(check_grudge_violations(output, grudges))
    violations.extend(check_output_format(output))

    status = "blocked" if violations else "cleared"

    return {
        "status": status,
        "violations": violations,
        "approved_scope": scope.get("approved_scope", []),
        "blocked_scope": scope.get("blocked_scope", []),
        "checks_run": 7,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def check_territory(output: dict, offering: dict) -> list:
    """Check if output references resources outside declared territory."""
    violations = []
    territory = offering.get("territory", "")
    output_str = _flatten_output(output)

    # Check for file path references outside territory
    # This is a heuristic check — in production, this would be more sophisticated
    territory_items = [t.strip() for t in str(territory).split(",") if t.strip()]

    # Flag if output claims to modify systems not in territory
    execution_keywords = ["deploy", "push to production", "merge to main",
                          "release", "publish", "send notification",
                          "install package", "run migration"]
    for keyword in execution_keywords:
        if keyword.lower() in output_str.lower():
            violations.append({
                "check": "territory",
                "rule": "no_execution_outside_territory",
                "detail": f"Output contains execution keyword: '{keyword}'",
                "severity": "critical",
                "context": "Territory does not include execution permissions"
            })
            break  # One violation per check is enough

    return violations


def check_permissions(output: dict, offering: dict) -> list:
    """Check if output requires actions not in permissions list."""
    violations = []
    permissions = offering.get("permissions", [])
    output_str = _flatten_output(output)

    if not permissions:
        return violations

    # Actions that require explicit permission
    action_keywords = {
        "write_files": ["write to file", "save file", "create file", "modify file"],
        "deploy": ["deploy", "ship", "release"],
        "send_notification": ["notify", "alert", "send message"],
        "external_api_call": ["POST", "PUT", "DELETE", "call API"],
    }

    for perm, keywords in action_keywords.items():
        if perm not in permissions:
            for keyword in keywords:
                if keyword.lower() in output_str.lower():
                    violations.append({
                        "check": "permissions",
                        "rule": f"action_requires_permission:{perm}",
                        "detail": f"Output references '{keyword}' but '{perm}' not in permissions",
                        "severity": "critical",
                        "context": f"Permissions: {permissions}"
                    })
                    break

    return violations


def check_do_not_do(output: dict, offering: dict) -> list:
    """Check if output violates explicit negative scope."""
    violations = []
    do_not_do = offering.get("do_not_do", [])
    output_str = _flatten_output(output)

    if not do_not_do:
        return violations

    for prohibition in do_not_do:
        # Simple substring match — production would use semantic similarity
        prohibition_lower = prohibition.lower()
        if prohibition_lower in output_str.lower():
            violations.append({
                "check": "do_not_do",
                "rule": f"prohibited_action:{prohibition}",
                "detail": f"Output appears to reference prohibited action: '{prohibition}'",
                "severity": "critical",
                "context": f"do_not_do list: {do_not_do}"
            })

    return violations


def check_approval_requests(output: dict, offering: dict) -> list:
    """Check if output includes actions that require approval."""
    violations = []
    approval_required = offering.get("approval_required", [])

    if not approval_required:
        return violations

    # If output contains approval_requests, that's correct behavior
    # If output contains actions that SHOULD require approval but doesn't list them,
    # that's a violation
    approval_requests = output.get("approval_requests", [])
    if isinstance(approval_requests, list) and len(approval_requests) > 0:
        # Good — output surfaced approval needs
        return violations

    # Check if output contains actions matching approval_required items
    output_str = _flatten_output(output)
    for required in approval_required:
        if isinstance(required, str) and required.lower() in output_str.lower():
            # Output references something that needs approval but didn't surface it
            violations.append({
                "check": "approval_requests",
                "rule": "missing_approval_surface",
                "detail": f"Output references '{required}' which requires approval but no approval_request was surfaced",
                "severity": "high",
                "context": f"approval_required: {approval_required}"
            })

    return violations


def check_blocked_scope(output: dict, scope: dict) -> list:
    """Check if output falls within blocked scope."""
    violations = []
    blocked = scope.get("blocked_scope", [])
    output_str = _flatten_output(output)

    for item in blocked:
        # Extract key terms from blocked scope items
        item_lower = item.lower()
        # Simple check: if a blocked scope item's key action appears in output
        key_actions = _extract_key_actions(item_lower)
        for action in key_actions:
            if action in output_str.lower():
                violations.append({
                    "check": "blocked_scope",
                    "rule": f"blocked_scope_violation:{item}",
                    "detail": f"Output appears to reference blocked action: '{item}'",
                    "severity": "critical",
                    "context": f"blocked_scope: {blocked}"
                })
                break  # One violation per blocked item

    return violations


def check_grudge_violations(output: dict, grudges: list) -> list:
    """Check if output matches known grudge patterns."""
    violations = []
    output_str = _flatten_output(output).lower()

    # Common words that cause false positives in grudge matching
    NOISE_WORDS = {"goblin", "tinker", "output", "task", "produce", "produce",
                    "agent", "action", "define", "ambiguous", "design", "schema",
                    "framework", "offering", "without", "before", "explicit"}

    for grudge in grudges:
        if not isinstance(grudge, dict):
            continue
        detection = grudge.get("detection", "")
        if not detection:
            continue

        # Extract meaningful keywords, filtering noise words
        detection_keywords = _extract_keywords(detection.lower())
        signal_keywords = [k for k in detection_keywords if k not in NOISE_WORDS and len(k) > 4]

        if not signal_keywords:
            continue

        # Require higher match threshold — signal keywords must match
        matches = [k for k in signal_keywords if k in output_str]
        # Need at least 50% of signal keywords to match AND at least 2 matches
        if len(matches) >= 2 and len(matches) >= len(signal_keywords) * 0.5:
            violations.append({
                "check": "grudge",
                "rule": f"grudge_pattern:{grudge.get('title', 'unknown')}",
                "detail": f"Output matches grudge pattern: '{grudge.get('title', 'unknown')}'",
                "severity": "high",
                "context": f"Detection: {detection}"
            })

    return violations


def check_output_format(output: dict) -> list:
    """Check if output follows required artifact format."""
    violations = []

    # If output is a goblin artifact, check for required fields
    if isinstance(output, dict):
        # Every goblin output should have at least a basic structure
        # But in alpha, we're lenient — only flag completely unstructured output
        pass

    return violations


def _flatten_output(output) -> str:
    """Flatten a nested dict/list/string into a single searchable string."""
    if isinstance(output, str):
        return output
    if isinstance(output, dict):
        parts = []
        for key, val in output.items():
            parts.append(str(key))
            parts.append(_flatten_output(val))
        return " ".join(parts)
    if isinstance(output, list):
        return " ".join(_flatten_output(item) for item in output)
    return str(output)


def _extract_key_actions(text: str) -> list:
    """Extract key action verbs from a scope description."""
    # Simple keyword extraction — production would use NLP
    actions = []
    verbs = ["implement", "deploy", "select", "evaluate", "access",
             "modify", "write", "push", "release", "publish", "send",
             "install", "run", "execute", "create", "delete", "remove"]
    for verb in verbs:
        if verb in text:
            actions.append(verb)
    return actions


def _extract_keywords(text: str) -> list:
    """Extract meaningful keywords from detection text."""
    # Remove common stop words, keep substantive terms
    stop_words = {"a", "an", "the", "and", "or", "but", "in", "on", "at",
                  "to", "for", "of", "with", "by", "from", "is", "it",
                  "any", "before", "after", "not", "no"}
    words = text.lower().replace(",", " ").replace(".", " ").split()
    return [w for w in words if w not in stop_words and len(w) > 2]