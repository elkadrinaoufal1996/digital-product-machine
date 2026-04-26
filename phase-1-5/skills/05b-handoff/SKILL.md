# SKILL 05b — PHASE-1-HANDOFF

## ROLE
Convert PHASE-1-OUTPUT.md into a validated phase-1-output.json consumed
by Phase 1.5. This skill does NOT analyze, score, or infer — pure
extraction and schema validation. No LLM call is made.

## INPUTS
- phase-1/outputs/PHASE-1-OUTPUT.md (must contain ## MACHINE-READABLE block)

## OUTPUT
- phase-1-5/outputs/phase-1-output.json

## AGENT
convert.py (deterministic — no LLM)

## EXECUTION
    python phase-1-5/skills/05b-handoff/convert.py

## BLOCKING CONDITIONS
- HALT if PHASE-1-OUTPUT.md not found
- HALT if ## MACHINE-READABLE block absent → re-run Skill 05
- HALT if JSON in block is malformed → fix Skill 05 output manually
- HALT if schema validation fails → lists every missing/invalid field
- HALT if confidence_score < 6.0 → do not launch Phase 1.5
