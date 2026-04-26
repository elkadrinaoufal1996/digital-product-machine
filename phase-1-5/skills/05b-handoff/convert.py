#!/usr/bin/env python3
"""
phase-1-5/skills/05b-handoff/convert.py
========================================
Deterministic converter: PHASE-1-OUTPUT.md -> phase-1-output.json
No LLM calls. No inference. Pure extraction + schema validation.

Usage:
    python phase-1-5/skills/05b-handoff/convert.py
"""

import json
import re
import sys
from pathlib import Path

try:
    import jsonschema
except ImportError:
    print(
        "[BLOCKING ERROR: phase-1-handoff — jsonschema not installed. "
        "Run: pip install jsonschema]",
        file=sys.stderr,
    )
    sys.exit(1)

ROOT       = Path(__file__).resolve().parents[3]
INPUT_PATH = ROOT / "phase-1" / "outputs" / "PHASE-1-OUTPUT.md"
OUTPUT_PATH = ROOT / "phase-1-5" / "outputs" / "phase-1-output.json"
SCHEMA_PATH = Path(__file__).parent / "output-schema.json"


def main() -> None:
    # ── 1. Read input ──────────────────────────────────────────────────────
    if not INPUT_PATH.exists():
        print(
            f"[BLOCKING ERROR: phase-1-handoff — PHASE-1-OUTPUT.md not found at {INPUT_PATH}]",
            file=sys.stderr,
        )
        sys.exit(1)

    text = INPUT_PATH.read_text(encoding="utf-8")

    # ── 2. Extract ## MACHINE-READABLE block ───────────────────────────────
    match = re.search(
        r"##\s*MACHINE-READABLE\s*\n```json\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    if not match:
        print(
            "[BLOCKING ERROR: phase-1-handoff — ## MACHINE-READABLE block not found in "
            "PHASE-1-OUTPUT.md. Re-run Skill 05 and ensure the block is populated.]",
            file=sys.stderr,
        )
        sys.exit(1)

    raw_json = match.group(1).strip()

    # ── 3. Parse JSON ──────────────────────────────────────────────────────
    try:
        data = json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(
            f"[BLOCKING ERROR: phase-1-handoff — Invalid JSON in ## MACHINE-READABLE block: {e}]",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── 4. Validate against schema ─────────────────────────────────────────
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = jsonschema.Draft7Validator(schema)
    errors = list(validator.iter_errors(data))
    if errors:
        print("[BLOCKING ERROR: phase-1-handoff — Schema validation failed:]", file=sys.stderr)
        for err in errors:
            field = " -> ".join(str(p) for p in err.absolute_path) or "root"
            print(f"  FIELD '{field}': {err.message}", file=sys.stderr)
        sys.exit(1)

    # ── 5. Confidence score gate ───────────────────────────────────────────
    score = data.get("confidence_score", 0)
    if score < 6.0:
        print(
            f"[BLOCKING ERROR: phase-1-handoff — confidence_score {score}/10 below launch "
            f"threshold (6.0). Do not launch Phase 1.5. Re-run Skill 05.]",
            file=sys.stderr,
        )
        sys.exit(1)

    # ── 6. Write output ────────────────────────────────────────────────────
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[HANDOFF OK] phase-1-output.json written — confidence_score: {score}/10")


if __name__ == "__main__":
    main()
