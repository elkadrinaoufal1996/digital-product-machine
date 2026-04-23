#!/usr/bin/env python3
"""
phase-1-5/agents/analyst.py — Agent: Brand Intelligence Analyst
================================================================
Loads Skill 06/07/08 SKILL.md files into Claude API system prompts,
processes brand intelligence sequentially, and produces:

  Skill 06 → phase-1-5/outputs/06-visual-identity.json
  Skill 07 → phase-1-5/outputs/07-brand-voice.json
  Skill 08 → phase-1-5/outputs/08-marketing-angles.json
             phase-1-5/outputs/PHASE-1.5-OUTPUT.md

Architecture mirrors phase-1/agents/analyst.py exactly.
Helper functions are reused verbatim; only SKILL_CONFIG and
skill-specific logic differ.

Usage (one skill per call):
    python phase-1-5/agents/analyst.py --skill=06
    python phase-1-5/agents/analyst.py --skill=07
    python phase-1-5/agents/analyst.py --skill=08

Model : claude-sonnet-4-20250514
Max tokens : 8000

Dependencies:
    pip install anthropic python-dotenv
"""

import argparse
import json
import os
import re
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

# ─── Shared utilities (Phase 1 markdown parsing) ──────────────────────────────
# utils.py lives one level up: phase-1-5/utils.py
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import extract_business_fields_from_phase1  # noqa: E402

# ─── Paths ────────────────────────────────────────────────────────────────────
# analyst.py lives at: <workspace>/phase-1-5/agents/analyst.py
# BASE_DIR          → <workspace>/phase-1-5/
# PHASE1_OUTPUT_PATH → <workspace>/phase-1/outputs/PHASE-1-OUTPUT.md
BASE_DIR           = Path(__file__).parent.parent.resolve()
SKILLS_DIR         = BASE_DIR / "skills"
OUTPUTS_DIR        = BASE_DIR / "outputs"
PHASE1_OUTPUT_PATH = BASE_DIR.parent / "phase-1" / "outputs" / "PHASE-1-OUTPUT.md"

# Delimiter used in Skill 08 dual-output response
_SK08_DELIMITER = "---PHASE-1.5-OUTPUT-MARKDOWN---"

# ─── Claude configuration ─────────────────────────────────────────────────────
CLAUDE_MODEL      = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 8000

# ─── Terminal colours (verbatim from phase-1/agents/analyst.py) ───────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─── Logging helpers (verbatim from phase-1) ──────────────────────────────────

def log_info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET} {msg}")


def log_ok(msg: str) -> None:
    print(f"{GREEN}{BOLD}[OK]{RESET} {msg}")


def log_warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET} {msg}")


def log_error(msg: str) -> None:
    print(f"{RED}{BOLD}[BLOCKING ERROR: {msg}]{RESET}")


# ─── SKILL_CONFIG ─────────────────────────────────────────────────────────────
# FIX 2: added "phase1_business_fields": True to skills 06/07/08
# FIX 3: all outputs use numbered prefix; Skill 08 carries output_json key
# blocking_check receives parsed data (dict for JSON, str for Markdown).

def _check_skill06(data: dict) -> bool:
    """Skill 06 output must contain color_system, typography_system, emotional_journey."""
    return (
        isinstance(data, dict)
        and "color_system" in data
        and "typography_system" in data
        and "emotional_journey" in data
    )


def _count_banned_words(data: dict) -> int:
    """
    Count total banned words in Skill 07 output.
    Handles both flat list and category-dict structures.
    """
    bw = data.get("banned_words", [])
    if isinstance(bw, list):
        return len(bw)
    if isinstance(bw, dict):
        return sum(
            len(v) if isinstance(v, list) else 0
            for v in bw.values()
        )
    return 0


def _check_skill07(data: dict) -> bool:
    """
    Skill 07 output must contain:
      - voice_models (list ≥ 5)
      - banned_words (total count ≥ 30)
      - tactile_realism key
    """
    if not isinstance(data, dict):
        return False
    vm     = data.get("voice_models", [])
    vm_ok  = isinstance(vm, list) and len(vm) >= 5
    bw_ok  = _count_banned_words(data) >= 30
    tr_ok  = "tactile_realism" in data
    return vm_ok and bw_ok and tr_ok


def _check_skill08(raw: str) -> bool:
    """
    Skill 08 raw response must:
      - contain the dual-output delimiter
      - have a Markdown section ≥ 1000 chars with required headings
    """
    if not isinstance(raw, str) or _SK08_DELIMITER not in raw:
        return False
    _, md_part = raw.split(_SK08_DELIMITER, 1)
    md = md_part.strip()
    return (
        len(md) > 1000
        and "Marketing Angles" in md
        and "Recycling Plan"   in md
        and "Confidence Score" in md
    )


SKILL_CONFIG: dict[str, dict] = {
    "06": {
        "name":                 "Visual Identity",
        "skill_dir":            "06-visual-identity",
        "inputs":               ["00-brand-intel.json"],
        "phase1_business_fields": True,           # FIX 2 — triggers Phase 1 enrichment
        "output":               "06-visual-identity.json",   # FIX 3
        "output_format":        "json",
        "blocking_check":       _check_skill06,
        "blocking_msg":         "06-visual-identity.json missing required keys",
    },
    "07": {
        "name":                 "Brand Voice",
        "skill_dir":            "07-brand-voice",
        "inputs":               ["00-brand-intel.json", "06-visual-identity.json"],  # FIX 3
        "phase1_business_fields": True,           # FIX 2
        "output":               "07-brand-voice.json",       # FIX 3
        "output_format":        "json",
        "blocking_check":       _check_skill07,
        "blocking_msg":         "07-brand-voice.json incomplete — Skill 07 must regenerate",
    },
    "08": {
        "name":                 "Marketing Angles",
        "skill_dir":            "08-marketing-angles",
        "inputs":               [                            # FIX 3
            "00-brand-intel.json",
            "06-visual-identity.json",
            "07-brand-voice.json",
        ],
        "phase1_business_fields": True,           # FIX 2
        "output":               "PHASE-1.5-OUTPUT.md",       # primary (markdown)
        "output_json":          "08-marketing-angles.json",  # FIX 3 — intermediate JSON
        "output_format":        "dual",           # signals dual-output mode
        "blocking_check":       _check_skill08,
        "blocking_msg":         "Skill 08 incomplete response — both JSON and MD required",
    },
}


# ─── Helper: parse_args (adapted from phase-1) ────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Parse CLI arguments — mirrors phase-1 parse_args, choices updated to 06/07/08."""
    parser = argparse.ArgumentParser(
        description="Analyst Agent — Brand Intelligence (Phase 1.5)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Skills available:
  --skill=06   Visual Identity   → outputs/06-visual-identity.json
  --skill=07   Brand Voice       → outputs/07-brand-voice.json
  --skill=08   Marketing Angles  → outputs/08-marketing-angles.json
                                   outputs/PHASE-1.5-OUTPUT.md
        """,
    )
    parser.add_argument(
        "--skill",
        required=True,
        choices=["06", "07", "08"],
        help="Skill number to execute (06, 07, or 08)",
    )
    return parser.parse_args()


# ─── Helper: load_skill_md (verbatim from phase-1) ───────────────────────────

def load_skill_md(skill_dir_name: str) -> str:
    """
    Load the SKILL.md for the requested skill.
    Truncates at 16 000 chars to fit the context window.
    Exits with a blocking error if the file is missing.
    """
    skill_path = SKILLS_DIR / skill_dir_name / "SKILL.md"
    if not skill_path.exists():
        log_error(f"SKILL.md not found: {skill_path}")
        sys.exit(1)

    content = skill_path.read_text(encoding="utf-8")
    if len(content) > 16000:
        content = (
            content[:16000]
            + "\n[SKILL TRUNCATED — remaining content omitted to fit context window]"
        )
    log_ok(f"SKILL.md loaded: {skill_path.relative_to(BASE_DIR)}")
    return content


# ─── Helper: load_input_files (verbatim from phase-1) ────────────────────────

def load_input_files(input_filenames: list[str]) -> dict[str, str]:
    """
    Load one or more JSON input files from outputs/.
    Returns {filename: raw_text}.
    Exits with a blocking error if any file is missing or empty.
    """
    loaded: dict[str, str] = {}
    for filename in input_filenames:
        filepath = OUTPUTS_DIR / filename
        if not filepath.exists():
            # Emit the exact blocking error messages required by the brief
            if filename == "00-brand-intel.json":
                log_error("brand intel missing — run scraper.py first")
            elif filename == "06-visual-identity.json":
                log_error("06-visual-identity.json missing — run --skill=06 first")
            elif filename == "07-brand-voice.json":
                log_error("07-brand-voice.json required for Skill 08 — run --skill=07 first")
            else:
                log_error(
                    f"input file missing: {filename} — "
                    f"check that the previous skill ran successfully"
                )
            sys.exit(1)

        if filepath.stat().st_size < 10:
            log_error(f"input file empty or invalid: {filepath}")
            sys.exit(1)

        raw = filepath.read_text(encoding="utf-8")
        loaded[filename] = raw
        log_ok(f"Input loaded: {filename} ({filepath.stat().st_size / 1024:.1f} KB)")
    return loaded


# ─── Helper: build_user_prompt (FIX 2 — Phase 1 enrichment) ──────────────────

def build_user_prompt(skill_id: str, inputs: dict[str, str]) -> str:
    """
    Build the user-turn prompt from loaded input files.

    FIX 2: When config["phase1_business_fields"] is True (all skills 06/07/08),
    prepend a PHASE 1 BUSINESS FIELDS JSON block extracted from PHASE-1-OUTPUT.md.

    FIX 3: Skill 08 requests both a JSON block AND a Markdown block, separated
    by the _SK08_DELIMITER sentinel so write_output() can split and save both.
    """
    config = SKILL_CONFIG[skill_id]
    parts  = [
        "Execute the skill instructions above using the following input data.\n",
        "Produce output matching the skill's output schema.\n\n",
    ]

    # ── FIX 2: inject Phase 1 business fields ────────────────────────────────
    if config.get("phase1_business_fields"):
        if not PHASE1_OUTPUT_PATH.exists():
            log_error(
                f"PHASE-1-OUTPUT.md not found at {PHASE1_OUTPUT_PATH} — "
                f"Phase 1 must complete first"
            )
            sys.exit(1)
        business_fields = extract_business_fields_from_phase1(PHASE1_OUTPUT_PATH)
        parts.append(
            f"## PHASE 1 BUSINESS FIELDS (from PHASE-1-OUTPUT.md)\n\n"
            f"```json\n"
            f"{json.dumps(business_fields, indent=2, ensure_ascii=False)}\n"
            f"```\n\n"
        )

    # ── Inject all input files (brand intel + previous skill outputs) ─────────
    for fname, content in inputs.items():
        parts.append(f"## INPUT FILE: {fname}\n\n```json\n{content}\n```\n\n")

    # ── Output instructions ───────────────────────────────────────────────────
    if skill_id == "08":
        # FIX 3: Skill 08 dual-output — JSON portion first, then MD portion
        parts.append(
            f"## OUTPUT INSTRUCTIONS\n\n"
            f"You must produce TWO outputs separated by the exact delimiter below.\n\n"
            f"**Part 1 — JSON** (parseable by json.loads()):\n"
            f"Return the complete `08-marketing-angles.json` object first, "
            f"with no markdown fences.\n\n"
            f"**Delimiter** (copy exactly, on its own line):\n"
            f"{_SK08_DELIMITER}\n\n"
            f"**Part 2 — Markdown** (after the delimiter):\n"
            f"Produce the complete PHASE-1.5-OUTPUT.md deliverable in Markdown format.\n"
            f"All sections must be filled with real, actionable content — no placeholders.\n"
            f"Include a 'Confidence Score: X/10' line at the end of the document.\n\n"
            f"Important: the delimiter must appear exactly once, on its own line, "
            f"with no leading or trailing spaces."
        )
    elif config["output_format"] == "json":
        parts.append(
            "Important: Return ONLY valid JSON. No markdown code fences, no explanatory text "
            "before or after the JSON. The response must be parseable directly by json.loads()."
        )
    else:
        parts.append(
            "Important: Produce a complete, ready-to-use Markdown document. "
            "All sections must be filled with real, actionable content. "
            "Do not use placeholders or skeleton structures. "
            "Include a 'Confidence Score: X/10' line at the end of the document."
        )

    return "".join(parts)


# ─── Helper: call_claude_api (adapted from phase-1 — adds web_search for 08) ─

def call_claude_api(
    system_prompt: str,
    user_prompt: str,
    skill_name: str,
    skill_id: str,
) -> str:
    """
    Call the Claude API with the skill's system prompt and user data.
    For Skill 08: enables the web_search tool so Claude can validate angles
    against current market trends.

    Returns the text content of the response.
    Exits with a blocking error on any API failure.
    """
    api_key = os.getenv("ANTHROPIC_KEY")
    if not api_key:
        log_error("ANTHROPIC_KEY not set")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    log_info(f"Claude API call — model: {CLAUDE_MODEL} — skill: {skill_name}")
    log_info(
        f"System prompt: {len(system_prompt):,} chars | "
        f"User prompt: {len(user_prompt):,} chars"
    )

    # Build kwargs — Skill 08 gets web_search; others do not
    call_kwargs: dict = {
        "model":      CLAUDE_MODEL,
        "max_tokens": CLAUDE_MAX_TOKENS,
        "system":     system_prompt,
        "messages":   [{"role": "user", "content": user_prompt}],
    }
    if skill_id == "08":
        call_kwargs["tools"]       = [{"type": "web_search_20250305", "name": "web_search"}]
        call_kwargs["tool_choice"] = {"type": "auto"}
        log_info("Skill 08: web_search tool enabled")

    try:
        message = client.messages.create(**call_kwargs)

        # Collect all text blocks; skip tool_use / tool_result blocks
        response_text = ""
        for block in message.content:
            if hasattr(block, "text"):
                response_text += block.text

        log_ok(
            f"Response received — {len(response_text):,} chars | "
            f"Tokens: {message.usage.input_tokens} in / "
            f"{message.usage.output_tokens} out | "
            f"Stop reason: {message.stop_reason}"
        )

        if message.stop_reason == "max_tokens":
            log_warn(
                "Response hit max_tokens — output may be truncated"
            )

        return response_text

    except anthropic.AuthenticationError:
        log_error("ANTHROPIC_KEY invalid or expired — check your API key")
        sys.exit(1)

    except anthropic.RateLimitError:
        log_error("Anthropic rate limit reached — wait a few seconds and retry")
        sys.exit(1)

    except anthropic.APIConnectionError as exc:
        log_error(f"Cannot reach Anthropic API: {exc}")
        sys.exit(1)

    except anthropic.APIStatusError as exc:
        log_error(f"Anthropic API error [{exc.status_code}]: {exc.message}")
        sys.exit(1)

    except Exception as exc:
        log_error(f"Unexpected error during Claude call: {exc}")
        sys.exit(1)


# ─── Helper: parse_json_response (verbatim from phase-1) ─────────────────────

def parse_json_response(raw: str, skill_id: str) -> dict:
    """
    Parse Claude's response as JSON.
    Strips markdown code fences if Claude added them.
    Exits with a blocking error if the JSON is invalid.
    """
    text = raw.strip()

    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        data = json.loads(text)
        log_ok("JSON parsed successfully")
        return data
    except json.JSONDecodeError as exc:
        log_error(f"Claude response is not valid JSON: {exc}")
        log_warn("First 500 chars of response:")
        print(text[:500])
        sys.exit(1)


# ─── Helper: check_blocking_conditions (verbatim from phase-1) ───────────────

def check_blocking_conditions(skill_id: str, output_data) -> bool:
    """
    Run the blocking_check lambda for the given skill.
    Returns True if all conditions pass, False otherwise.
    """
    config    = SKILL_CONFIG[skill_id]
    check_fn  = config["blocking_check"]
    block_msg = config["blocking_msg"]

    try:
        if check_fn(output_data):
            log_ok("Blocking conditions OK")
            return True
        else:
            log_error(block_msg)
            return False
    except Exception as exc:
        log_error(f"Blocking condition check raised an exception: {exc}")
        return False


# ─── Helper: write_output (FIX 3 — Skill 08 dual-output) ─────────────────────

def write_output(skill_id: str, raw_response: str) -> Path:
    """
    Write the skill output(s) to outputs/.

    - Skills 06/07 → JSON pretty-printed (ensure_ascii=False, indent=2)
    - Skill 08     → splits on _SK08_DELIMITER:
                       JSON portion → 08-marketing-angles.json
                       MD  portion  → PHASE-1.5-OUTPUT.md  (returned path)

    Returns the path of the primary written file.
    """
    config      = SKILL_CONFIG[skill_id]
    output_name = config["output"]
    output_path = OUTPUTS_DIR / output_name

    OUTPUTS_DIR.mkdir(exist_ok=True)

    try:
        if skill_id == "08":
            # ── FIX 3: dual-output for Skill 08 ──────────────────────────────
            # Delimiter presence already verified by _check_skill08; split safely.
            json_raw, md_raw = raw_response.split(_SK08_DELIMITER, 1)

            # Write 08-marketing-angles.json
            json_data     = parse_json_response(json_raw, skill_id)
            json_out_name = config["output_json"]
            json_out_path = OUTPUTS_DIR / json_out_name
            json_out_path.write_text(
                json.dumps(json_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log_ok(
                f"Output written: {json_out_name} "
                f"({json_out_path.stat().st_size / 1024:.1f} KB)"
            )

            # Write PHASE-1.5-OUTPUT.md
            md_content = md_raw.strip()
            output_path.write_text(md_content, encoding="utf-8")
            log_ok(
                f"Output written: {output_name} "
                f"({output_path.stat().st_size / 1024:.1f} KB)"
            )

        elif config["output_format"] == "json":
            # ── Skills 06/07: parse from raw then pretty-print ────────────────
            json_data = parse_json_response(raw_response, skill_id)
            output_path.write_text(
                json.dumps(json_data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            log_ok(
                f"Output written: {output_name} "
                f"({output_path.stat().st_size / 1024:.1f} KB)"
            )

        else:
            # Pure Markdown (non-08 fallback — should not be reached)
            output_path.write_text(raw_response, encoding="utf-8")
            log_ok(
                f"Output written: {output_name} "
                f"({output_path.stat().st_size / 1024:.1f} KB)"
            )

        return output_path

    except OSError as exc:
        log_error(f"Cannot write {output_path}: {exc}")
        sys.exit(1)


# ─── Skill 08 — Confidence Score check ───────────────────────────────────────

def check_confidence_score(markdown_content: str, output_path: Path) -> None:
    """
    Parse the Confidence Score from PHASE-1.5-OUTPUT.md.
    Writes the file first (for diagnostic purposes), then halts if score < 6.
    """
    pattern = r"Confidence Score[:\s]+(\d+)/10"
    match   = re.search(pattern, markdown_content, re.IGNORECASE)

    if not match:
        log_warn(
            "Confidence Score line not found in PHASE-1.5-OUTPUT.md — "
            "skipping score gate (ask Claude to include it explicitly)"
        )
        return

    score = int(match.group(1))
    if score >= 6:
        log_ok(f"Confidence Score: {score}/10 — threshold passed (≥6)")
    else:
        log_error(
            f"Phase 1.5 confidence too low ({score}/10) — "
            f"DO NOT proceed to Phase 2 — remediation required"
        )
        log_warn(f"Diagnostic output already written to: {output_path}")
        sys.exit(1)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    args     = parse_args()
    skill_id = args.skill
    config   = SKILL_CONFIG[skill_id]

    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  ANALYST AGENT — Skill {skill_id}: {config['name']}{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

    # ── Load .env ─────────────────────────────────────────────────────────────
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        log_info(".env loaded.")
    else:
        log_warn(".env not found — reading env vars from system.")

    api_key = os.getenv("ANTHROPIC_KEY")
    if not api_key:
        log_error("ANTHROPIC_KEY not set")
        sys.exit(1)

    # ── Load SKILL.md → system prompt ─────────────────────────────────────────
    log_info(f"Loading SKILL.md: {config['skill_dir']}/SKILL.md")
    system_prompt = load_skill_md(config["skill_dir"])

    # ── Load input files ───────────────────────────────────────────────────────
    log_info(f"Loading inputs: {', '.join(config['inputs'])}")
    inputs = load_input_files(config["inputs"])

    # ── Build user prompt ──────────────────────────────────────────────────────
    user_prompt = build_user_prompt(skill_id, inputs)

    # ── Call Claude API ────────────────────────────────────────────────────────
    raw_response = call_claude_api(system_prompt, user_prompt, config["name"], skill_id)

    # ── Check blocking conditions ──────────────────────────────────────────────
    # For skills 06/07 pass raw_response (JSON string); blocking_check parses it.
    # For skill 08 pass raw_response directly (_check_skill08 inspects the delimiter).
    if not check_blocking_conditions(skill_id, raw_response):
        diag_path = OUTPUTS_DIR / f"{skill_id}-DIAGNOSTIC-FAILED.txt"
        OUTPUTS_DIR.mkdir(exist_ok=True)
        diag_path.write_text(raw_response, encoding="utf-8")
        log_warn(f"Raw output saved for diagnostics: {diag_path.name}")
        sys.exit(1)

    # ── Write output ───────────────────────────────────────────────────────────
    output_path = write_output(skill_id, raw_response)

    # ── Skill 08 only: Confidence Score gate ──────────────────────────────────
    # Read from the written PHASE-1.5-OUTPUT.md so the gate always uses the
    # same content that was persisted (not the raw API response string).
    if skill_id == "08":
        md_path = OUTPUTS_DIR / "PHASE-1.5-OUTPUT.md"
        check_confidence_score(md_path.read_text(encoding="utf-8"), md_path)

    # ── Summary ───────────────────────────────────────────────────────────────
    print(f"\n{GREEN}{BOLD}  Skill {skill_id} — {config['name']}: DONE ✓{RESET}")
    if skill_id == "08":
        print(f"  Outputs: {OUTPUTS_DIR.relative_to(BASE_DIR)}/08-marketing-angles.json")
        print(f"           {OUTPUTS_DIR.relative_to(BASE_DIR)}/PHASE-1.5-OUTPUT.md\n")
    else:
        print(f"  Output: {output_path.relative_to(BASE_DIR)}\n")

    # ── Rate-limit guard (for automated sequential 06→07→08 orchestration) ────
    time.sleep(2)


if __name__ == "__main__":
    main()
