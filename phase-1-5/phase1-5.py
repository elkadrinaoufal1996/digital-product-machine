#!/usr/bin/env python3
"""
phase1-5.py — Orchestrateur Principal Phase 1.5
================================================
Lance le pipeline Brand Foundation en 4 étapes séquentielles.

Usage:
    python phase-1-5/phase1-5.py
    python phase-1-5/phase1-5.py --input=path/to/PHASE-1-OUTPUT.md

Dépendances requises:
    pip install anthropic apify-client firecrawl-py tavily-python python-dotenv

Variables d'environnement requises (dans phase-1-5/.env):
    ANTHROPIC_KEY, APIFY_TOKEN, FIRECRAWL_KEY, TAVILY_KEY
"""

import argparse
import json
import os
import re
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# ─── Chemins ────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.resolve()
OUTPUTS_DIR = BASE_DIR / "outputs"
AGENTS_DIR  = BASE_DIR / "agents"

# ─── Couleurs terminal ───────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─── Logging helpers (verbatim from phase1.py) ───────────────────────────────

def log_info(message: str):
    """Log informatif."""
    print(f"{CYAN}[INFO]{RESET} {message}")


def log_ok(message: str):
    """Log de succès."""
    print(f"{GREEN}{BOLD}[OK]{RESET} {message}")


def log_warn(message: str):
    """Log avertissement non-bloquant."""
    print(f"{YELLOW}[WARN]{RESET} {message}")


def log_error(message: str):
    """Log d'erreur bloquante."""
    print(f"{RED}{BOLD}[BLOCKING ERROR: {message}]{RESET}")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 1.5 — Brand Foundation Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python phase-1-5/phase1-5.py
  python phase-1-5/phase1-5.py --input=path/to/PHASE-1-OUTPUT.md
        """
    )
    parser.add_argument(
        "--input",
        default=str(Path(__file__).parent.parent / "phase-1" / "outputs" / "PHASE-1-OUTPUT.md"),
        help="Path to PHASE-1-OUTPUT.md (default: ../phase-1/outputs/PHASE-1-OUTPUT.md)"
    )
    return parser.parse_args()


# ─── Pre-flight checks ───────────────────────────────────────────────────────

def preflight(input_path: Path) -> bool:
    """
    Vérifie toutes les préconditions avant de lancer le pipeline.
    Retourne True si tout est OK, False (+ message) sinon.
    """
    all_ok = True

    # 1. Input file
    if not input_path.exists():
        log_error(f"PHASE-1-OUTPUT.md not found at {input_path}")
        all_ok = False

    # 2. .env file
    env_file = BASE_DIR / ".env"
    if not env_file.exists():
        log_error("phase-1-5/.env file not found")
        all_ok = False
    else:
        load_dotenv(env_file)
        log_info(".env loaded.")

    # 3. Required env vars
    required_vars = ["ANTHROPIC_KEY", "APIFY_TOKEN", "FIRECRAWL_KEY", "TAVILY_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]
    if missing:
        log_error(f"missing env vars: {', '.join(missing)}")
        all_ok = False
    else:
        log_info("All required environment variables are present.")

    return all_ok


# ─── Step runner ─────────────────────────────────────────────────────────────

def run_step(
    step_num: int,
    total_steps: int,
    script_path: Path,
    extra_args: list,
    expected_outputs: list,
) -> bool:
    """
    Runs one pipeline step as a subprocess.
    - Streams stdout/stderr live (capture_output=False).
    - Returns False (after printing error) on non-zero exit or missing outputs.
    """
    cmd_display = script_path.name + (" " + " ".join(extra_args) if extra_args else "")
    print(f"\n{BOLD}{CYAN}[STEP {step_num}/{total_steps}]{RESET} Running {cmd_display}...")
    print(f"  {'─' * 60}")

    cmd = [sys.executable, str(script_path)] + extra_args
    result = subprocess.run(
        cmd,
        cwd=str(BASE_DIR),
        capture_output=False,
        check=False,
    )

    if result.returncode != 0:
        log_error(f"Step {step_num} failed — see {script_path.name} output above")
        return False

    # Verify each expected output exists and is non-empty
    for out_file in expected_outputs:
        if not out_file.exists() or out_file.stat().st_size <= 10:
            log_error(f"{out_file.name} not produced by {script_path.name}")
            return False

    # Print per-output success lines
    for out_file in expected_outputs:
        size_kb = out_file.stat().st_size / 1024
        print(f"{GREEN}{BOLD}[STEP {step_num}/{total_steps} ✓]{RESET} OK — {out_file.name} created ({size_kb:.1f} KB)")

    return True


# ─── Confidence Score gate ────────────────────────────────────────────────────

def check_confidence(output_md: Path) -> tuple[bool, int | None]:
    """
    Reads PHASE-1.5-OUTPUT.md and parses the Confidence Score.
    Returns (gate_passed: bool, score: int | None).
    """
    content = output_md.read_text(encoding="utf-8")
    matches = re.findall(r"confidence score[:\s]+(\d+)/10", content, re.IGNORECASE)

    if not matches:
        log_warn("Confidence Score not found in PHASE-1.5-OUTPUT.md — skipping gate.")
        return True, None

    score = int(matches[-1])  # Take the LAST occurrence

    if score >= 6:
        print(f"{GREEN}{BOLD}[CONFIDENCE GATE ✓]{RESET} Score {score}/10 — Phase 1.5 cleared for handoff")
        return True, score
    else:
        log_error(
            f"Phase 1.5 confidence too low ({score}/10) — "
            f"DO NOT proceed to Phase 2 — remediation required"
        )
        return False, score


# ─── Final summary ────────────────────────────────────────────────────────────

def print_summary(start_time: float, confidence_score: int | None):
    elapsed = time.time() - start_time
    output_files = [
        OUTPUTS_DIR / "00-brand-intel.json",
        OUTPUTS_DIR / "06-visual-identity.json",
        OUTPUTS_DIR / "07-brand-voice.json",
        OUTPUTS_DIR / "08-marketing-angles.json",
        OUTPUTS_DIR / "PHASE-1.5-OUTPUT.md",
    ]
    score_str = f"{confidence_score}/10" if confidence_score is not None else "N/A"

    print(f"\n{BOLD}{'─' * 56}{RESET}")
    print(f"{GREEN}{BOLD}  PHASE 1.5 — BRAND FOUNDATION : COMPLETE ✓{RESET}")
    print(f"{BOLD}{'─' * 56}{RESET}")
    print(f"  Total runtime : {elapsed:.1f} seconds")
    print(f"  Confidence    : {score_str}")
    print(f"  Outputs :")
    for f in output_files:
        if f.exists():
            size_kb = f.stat().st_size / 1024
            suffix = " ← Phase 2 input" if f.name == "PHASE-1.5-OUTPUT.md" else ""
            print(f"    phase-1-5/outputs/{f.name:<35} ({size_kb:.0f} KB){suffix}")
        else:
            print(f"    phase-1-5/outputs/{f.name:<35} (MISSING)")
    print(f"{BOLD}{'─' * 56}{RESET}\n")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    args    = parse_args()
    input_path = Path(args.input).resolve()
    start_time = time.time()

    # ── Banner ───────────────────────────────────────────────────────────────
    print(f"\n{BOLD}{'═' * 65}{RESET}")
    print(f"{BOLD}  PHASE 1.5 — Brand Foundation Pipeline{RESET}")
    print(f"{BOLD}{'═' * 65}{RESET}\n")

    # ── Pre-flight checks ────────────────────────────────────────────────────
    print(f"{BOLD}Pre-flight checks{RESET}")
    print(f"  Input  : {input_path}")
    print(f"  Output : {OUTPUTS_DIR}")
    print(f"  Model  : claude-sonnet-4-20250514 (set in agents)")
    print()

    if not preflight(input_path):
        sys.exit(1)

    OUTPUTS_DIR.mkdir(exist_ok=True)
    print()

    # ── STEP 0/4 : Phase-1 Handoff (MACHINE-READABLE → phase-1-output.json) ─
    print(f"\n{BOLD}{CYAN}[STEP 0/4]{RESET} Running phase-1-handoff (convert.py)...")
    print(f"  {'─' * 60}")
    handoff_script = BASE_DIR / "skills" / "05b-handoff" / "convert.py"
    handoff_result = subprocess.run(
        [sys.executable, str(handoff_script)],
        cwd=str(BASE_DIR),
        capture_output=False,
        check=False,
    )
    if handoff_result.returncode != 0:
        log_error("Phase-1 handoff failed — PHASE-1-OUTPUT.md missing ## MACHINE-READABLE block or schema invalid")
        sys.exit(1)

    phase1_json_path = OUTPUTS_DIR / "phase-1-output.json"
    if not phase1_json_path.exists():
        log_error("phase-1-output.json not produced by convert.py")
        sys.exit(1)

    phase1_data = json.loads(phase1_json_path.read_text(encoding="utf-8"))
    log_ok(f"phase-1-output.json loaded — niche='{phase1_data.get('validated_niche', '?')}' | confidence={phase1_data.get('confidence_score', '?')}/10")

    # ── STEP 1/4 : Scraper ───────────────────────────────────────────────────
    ok = run_step(
        step_num=1,
        total_steps=4,
        script_path=AGENTS_DIR / "scraper.py",
        extra_args=[],  # scraper takes no CLI args
        expected_outputs=[OUTPUTS_DIR / "00-brand-intel.json"],
    )
    if not ok:
        sys.exit(1)

    # ── STEP 2/4 : Analyst skill=06 ──────────────────────────────────────────
    ok = run_step(
        step_num=2,
        total_steps=4,
        script_path=AGENTS_DIR / "analyst.py",
        extra_args=["--skill=06"],
        expected_outputs=[OUTPUTS_DIR / "06-visual-identity.json"],
    )
    if not ok:
        sys.exit(1)

    time.sleep(2)  # Rate limit guard — Claude API

    # ── STEP 3/4 : Analyst skill=07 ──────────────────────────────────────────
    ok = run_step(
        step_num=3,
        total_steps=4,
        script_path=AGENTS_DIR / "analyst.py",
        extra_args=["--skill=07"],
        expected_outputs=[OUTPUTS_DIR / "07-brand-voice.json"],
    )
    if not ok:
        sys.exit(1)

    time.sleep(2)  # Rate limit guard — Claude API

    # ── STEP 4/4 : Analyst skill=08 ──────────────────────────────────────────
    ok = run_step(
        step_num=4,
        total_steps=4,
        script_path=AGENTS_DIR / "analyst.py",
        extra_args=["--skill=08"],
        expected_outputs=[
            OUTPUTS_DIR / "08-marketing-angles.json",
            OUTPUTS_DIR / "PHASE-1.5-OUTPUT.md",
        ],
    )
    if not ok:
        sys.exit(1)

    # ── Confidence Score gate ────────────────────────────────────────────────
    print()
    gate_passed, confidence_score = check_confidence(OUTPUTS_DIR / "PHASE-1.5-OUTPUT.md")
    if not gate_passed:
        sys.exit(1)

    # ── Final summary ────────────────────────────────────────────────────────
    print_summary(start_time, confidence_score)


if __name__ == "__main__":
    main()
