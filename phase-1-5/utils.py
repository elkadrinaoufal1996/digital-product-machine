#!/usr/bin/env python3
"""
phase-1-5/utils.py — Shared utility module for Phase 1.5 agents
================================================================
Centralises Phase 1 markdown parsing so both scraper.py and analyst.py
use the same extraction logic.  No regex duplication between agents.

Public API
----------
    parse_phase1_output(path)               → dict  (4 scraper fields)
    extract_business_fields_from_phase1(path) → dict  (10 analyst fields)

Import from either agent with:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
    from utils import parse_phase1_output, extract_business_fields_from_phase1
"""

import re
import sys
import warnings
from pathlib import Path

# ─── Terminal colours (kept local so utils.py is self-contained) ─────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─── Logging helpers (minimal; agents keep their own copies) ──────────────────

def _log_info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET} {msg}")


def _log_ok(msg: str) -> None:
    print(f"{GREEN}{BOLD}[OK]{RESET} {msg}")


def _log_warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET} {msg}")


def _halt(msg: str) -> None:
    """Print a formatted blocking error and exit."""
    print(f"{RED}{BOLD}[BLOCKING ERROR: {msg}]{RESET}", file=sys.stderr)
    sys.exit(1)


# ─── Shared primitive ─────────────────────────────────────────────────────────

def _first_match(patterns: list, text: str) -> str:
    """Return the first non-empty group from the first matching pattern."""
    for pat in patterns:
        m = re.search(pat, text)
        if m:
            return m.group(1).strip().strip("*_:`").strip()
    return ""


# ─── PHASE-1 OUTPUT PARSER (moved verbatim from scraper.py) ──────────────────

def parse_phase1_output(path: Path) -> dict:
    """
    Parse PHASE-1-OUTPUT.md and extract the four fields required by scraper.py.
    Halts with a blocking error if the file is missing or malformed.

    Returns:
        {
          "final_niche":             str,
          "top_3_UVZ":               [str, ...],
          "top_competitor_urls":     [str, ...],
          "target_persona_keywords": [str, ...],
        }
    """
    if not path.exists():
        _halt("Phase 1 output missing — run Phase 1 first")

    content = path.read_text(encoding="utf-8")
    _log_info(f"PHASE-1-OUTPUT.md read ({len(content):,} chars)")

    # ── final_niche ───────────────────────────────────────────────────────────
    niche = _first_match([
        r"(?i)final[_ ]niche[:\s*]+([^\n#]{3,80})",
        r"(?i)##\s*final niche\s*\n+([^\n#]{3,80})",
        r"(?i)\*\*(?:final )?niche\*\*[:\s]+([^\n]{3,80})",
        r"(?i)niche selected[:\s]+([^\n]{3,80})",
        r"(?i)selected niche[:\s]+([^\n]{3,80})",
        r"(?i)niche[:\s]+\*\*([^*]{3,60})\*\*",
    ], content)

    if not niche:
        _halt("malformed Phase 1 output — check Skill 05 delivery")

    # ── top_3_UVZ ─────────────────────────────────────────────────────────────
    uvzs: list[str] = []
    uvz_block_patterns = [
        r"(?i)##\s*(?:top\s*3\s*)?uvz[^\n]*\n+((?:.|\n){1,600}?)(?:\n##|\Z)",
        r"(?i)unique value zone[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)uvz[_\s]?(?:ranked|list)?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)top.{0,5}uvz[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
    ]
    for pat in uvz_block_patterns:
        m = re.search(pat, content)
        if m:
            block = m.group(1)
            items = re.findall(r"(?:^|\n)\s*[-*\d.]+\.?\s+(.+)", block)
            uvzs = [i.strip().strip("*_:") for i in items[:3] if len(i.strip()) > 3]
            if uvzs:
                break

    # Fallback: scan near the first "uvz" keyword
    if not uvzs:
        idx = content.lower().find("uvz")
        if idx != -1:
            snippet = content[max(0, idx - 20): idx + 600]
            items = re.findall(r"(?:^|\n)\s*[-*\d.]+\.?\s+(.+)", snippet)
            uvzs = [i.strip().strip("*_:") for i in items[:3] if len(i.strip()) > 3]

    if not uvzs:
        _log_warn("Could not extract UVZ list — proceeding with empty list")

    # ── top_competitor_urls ───────────────────────────────────────────────────
    _NOISE_DOMAINS = {
        "github.com", "anthropic.com", "apify.com", "firecrawl.dev",
        "tavily.com", "reddit.com", "twitter.com", "x.com", "tiktok.com",
        "facebook.com", "instagram.com", "linkedin.com", "youtube.com",
        "google.com", "amazon.com", "wikipedia.org",
    }
    raw_urls = re.findall(r'https?://[^\s\)\]\'"<>]+', content)
    competitor_urls: list[str] = []
    seen_urls: set[str] = set()
    for url in raw_urls:
        clean = url.rstrip(".,;)")
        domain = re.sub(r'^https?://(www\.)?', '', clean).split('/')[0].lower()
        if domain not in _NOISE_DOMAINS and clean not in seen_urls and len(domain) > 4:
            competitor_urls.append(clean)
            seen_urls.add(clean)

    # ── target_persona_keywords ───────────────────────────────────────────────
    keywords: list[str] = []
    kw_patterns = [
        r"(?i)pain point[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)persona[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)target audience[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)buyer persona[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
    ]
    for pat in kw_patterns:
        m = re.search(pat, content)
        if m:
            block = m.group(1)
            items = re.findall(r"[-*\d.]+\s+(.+)", block)
            keywords = [i.strip().strip("*_:") for i in items[:10] if len(i.strip()) > 3]
            if keywords:
                break

    # Supplement with bold phrases and quoted strings from the document
    quoted = re.findall(r'"([^"]{5,60})"', content)
    bold   = re.findall(r'\*\*([^*]{3,50})\*\*', content)
    for extra in (quoted[:5] + bold[:5]):
        if extra not in keywords:
            keywords.append(extra)

    result = {
        "final_niche":             niche,
        "top_3_UVZ":               uvzs[:3],
        "top_competitor_urls":     competitor_urls[:8],
        "target_persona_keywords": keywords[:15],
    }
    _log_ok(
        f"Phase 1 parsed → niche='{niche}' | "
        f"{len(competitor_urls)} competitors | "
        f"{len(uvzs)} UVZs | "
        f"{len(keywords)} persona keywords"
    )
    return result


# ─── BUSINESS FIELDS EXTRACTOR (new — for Skills 06/07/08) ───────────────────

def extract_business_fields_from_phase1(path: Path) -> dict:
    """
    Extract business fields from PHASE-1-OUTPUT.md required by Skills 06/07/08.
    Returns a dict with the exact keys expected by their input schemas.

    Tolerant patterns: case-insensitive, multiple aliases per field.
    Sensible defaults if a field cannot be parsed (logs a warning; does NOT halt —
    downstream skills will HALT on truly invalid data with their own blocking errors).

    HARD HALT conditions (must be enforced here):
      - File missing            → [BLOCKING ERROR: PHASE-1-OUTPUT.md not found …]
      - validated_niche missing → [BLOCKING ERROR: Phase 1 output malformed …]

    Returns:
        {
          "validated_niche":           str,
          "dominant_emotion":          str,   # fear|desire|frustration|aspiration|trust|exclusivity
          "dominant_persona":          {
              "age_range":     str,
              "gender":        str,
              "psychographic": str,
          },
          "price_point":               int,   # 17|27|37|47
          "top_3_uvp":                 [str, str, str],
          "positioning":               str,
          "competitor_names":          [str, ...],
          "market_awareness_level":    str,   # unaware|problem_aware|solution_aware|product_aware|most_aware
          "competitor_dominant_angle": str,
          "new_mechanism_name":        str,
        }
    """
    if not path.exists():
        _halt("PHASE-1-OUTPUT.md not found — Phase 1 must complete first")

    content       = path.read_text(encoding="utf-8")
    content_lower = content.lower()

    # ── validated_niche ───────────────────────────────────────────────────────
    validated_niche = _first_match([
        r"(?i)validated[_ ]niche[:\s*]+([^\n#]{3,80})",
        r"(?i)final[_ ]niche[:\s*]+([^\n#]{3,80})",
        r"(?i)##\s*final niche\s*\n+([^\n#]{3,80})",
        r"(?i)\*\*(?:final )?niche\*\*[:\s]+([^\n]{3,80})",
        r"(?i)niche selected[:\s]+([^\n]{3,80})",
        r"(?i)selected niche[:\s]+([^\n]{3,80})",
        r"(?i)niche[:\s]+\*\*([^*]{3,60})\*\*",
    ], content)

    if not validated_niche:
        _halt("Phase 1 output malformed — validated_niche unparseable")

    # ── dominant_emotion ──────────────────────────────────────────────────────
    _VALID_EMOTIONS = {"fear", "desire", "frustration", "aspiration", "trust", "exclusivity"}

    dominant_emotion = _first_match([
        r"(?i)dominant[_ ]emotion[:\s*]+([a-z]+)",
        r"(?i)primary[_ ]emotion[:\s*]+([a-z]+)",
        r"(?i)emotional[_ ]driver[:\s*]+([a-z]+)",
        r"(?i)core[_ ]emotion[:\s*]+([a-z]+)",
    ], content).lower()

    if dominant_emotion not in _VALID_EMOTIONS:
        # Keyword heuristic — scan the full document
        if any(kw in content_lower for kw in ["anxiety", "overwhelm", "stress", "panic", "fear"]):
            dominant_emotion = "fear"
        elif any(kw in content_lower for kw in ["dream", "aspire", "aspiration", "achieve", "success"]):
            dominant_emotion = "aspiration"
        elif any(kw in content_lower for kw in ["desire", "crave", "passion", "want deeply"]):
            dominant_emotion = "desire"
        elif any(kw in content_lower for kw in ["trust", "credib", "reliable", "proven", "guarantee"]):
            dominant_emotion = "trust"
        elif any(kw in content_lower for kw in ["exclusive", "premium", "elite", "vip", "luxury"]):
            dominant_emotion = "exclusivity"
        else:
            raise ValueError(
                "[PHASE-1-HANDOFF ERROR] Field 'dominant_emotion' not found "
                "in PHASE-1-OUTPUT.md. Re-run Skill 05 or check markdown structure."
            )
        _log_warn(
            f"dominant_emotion not explicitly labelled — "
            f"keyword heuristic -> '{dominant_emotion}'"
        )

    # ── dominant_persona ──────────────────────────────────────────────────────
    age_range = _first_match([
        r"(?i)age[_ ]range[:\s*]+([0-9]{2}\s*[-–+]\s*[0-9]{0,2}\+?)",
        r"(?i)ages?[:\s]+([0-9]{2}\s*[-–]\s*[0-9]{2})",
        r"(?i)(\d{2})\s*[-–to]+\s*(\d{2})\s*(?:year|yr)",
    ], content)
    if not age_range:
        raise ValueError(
            "[PHASE-1-HANDOFF ERROR] Field 'age_range' not found "
            "in PHASE-1-OUTPUT.md. Re-run Skill 05 or check markdown structure."
        )

    gender = _first_match([
        r"(?i)gender[:\s*]+([a-z\s/|]+?)(?:\n|,|\.|$)",
        r"(?i)(?:primarily|mostly|mainly)\s+(male|female|women|men|non-binary)",
        r"(?i)target(?:ing)?\s+(women|men|female|male|everyone)",
    ], content).strip().rstrip(".,")
    if not gender:
        gender = "all genders"
        warnings.warn(
            "[DEGRADED] 'gender' not found — using default 'all genders'. "
            "Output confidence is reduced.",
            RuntimeWarning, stacklevel=2
        )

    psychographic = _first_match([
        r"(?i)psychographic[s]?[:\s*]+([^\n]{5,120})",
        r"(?i)mindset[:\s*]+([^\n]{5,120})",
        r"(?i)personality[:\s*]+([^\n]{5,120})",
        r"(?i)lifestyle[:\s*]+([^\n]{5,120})",
    ], content)
    if not psychographic:
        raise ValueError(
            "[PHASE-1-HANDOFF ERROR] Field 'psychographic' not found "
            "in PHASE-1-OUTPUT.md. Re-run Skill 05 or check markdown structure."
        )

    dominant_persona = {
        "age_range":     age_range[:30],
        "gender":        gender[:50],
        "psychographic": psychographic[:200],
    }

    # ── price_point ───────────────────────────────────────────────────────────
    price_match = re.search(r"\$?(17|27|37|47)\b", content)
    if price_match:
        price_point = int(price_match.group(1))
    else:
        raise ValueError(
            "[PHASE-1-HANDOFF ERROR] Field 'price_point' not found "
            "in PHASE-1-OUTPUT.md. Re-run Skill 05 or check markdown structure."
        )

    # ── top_3_uvp ─────────────────────────────────────────────────────────────
    top_3_uvp: list[str] = []
    uvp_block_patterns = [
        r"(?i)promise\s+architecture[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)unique\s+value\s+prop(?:osition)?s?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)top.{0,5}uvp[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)uvp[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        # UVZ is a near-synonym in the Phase 1 schema
        r"(?i)##\s*(?:top\s*3\s*)?uvz[^\n]*\n+((?:.|\n){1,600}?)(?:\n##|\Z)",
        r"(?i)unique\s+value\s+zone[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)uvz[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
    ]
    for pat in uvp_block_patterns:
        m = re.search(pat, content)
        if m:
            block = m.group(1)
            items = re.findall(r"(?:^|\n)\s*[-*\d.]+\.?\s+(.+)", block)
            top_3_uvp = [i.strip().strip("*_:") for i in items[:3] if len(i.strip()) > 3]
            if top_3_uvp:
                break

    if len(top_3_uvp) < 3:
        _log_warn(f"top_3_uvp: only {len(top_3_uvp)} UVPs found — padding with placeholders")
        while len(top_3_uvp) < 3:
            top_3_uvp.append(f"[UVP placeholder {len(top_3_uvp) + 1} — review PHASE-1-OUTPUT.md]")

    # ── positioning ───────────────────────────────────────────────────────────
    positioning = _first_match([
        r"(?i)positioning\s+statement[:\s*]+([^\n]{10,300})",
        r"(?i)one[-\s]sentence\s+positioning[:\s*]+([^\n]{10,300})",
        r"(?i)positioning[:\s*]+([^\n]{10,300})",
        r"(?i)market\s+position(?:ing)?[:\s*]+([^\n]{10,300})",
        r"(?i)brand\s+position(?:ing)?[:\s*]+([^\n]{10,300})",
    ], content)
    if not positioning:
        positioning = f"The go-to solution for {validated_niche}"
        _log_warn("positioning not found — derived from validated_niche")

    # ── competitor_names ──────────────────────────────────────────────────────
    competitor_names: list[str] = []
    comp_block_patterns = [
        r"(?i)competitor[s]?\s+(?:analysis|list|names?)[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,15})",
        r"(?i)##\s*competitor[s]?[^\n]*\n+((?:[-*\d.]+\s+.+\n?){1,15})",
        r"(?i)top\s+competitor[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
        r"(?i)key\s+competitor[s]?[:\s]*\n+((?:[-*\d.]+\s+.+\n?){1,10})",
    ]
    for pat in comp_block_patterns:
        m = re.search(pat, content)
        if m:
            block = m.group(1)
            items = re.findall(r"[-*\d.]+\.?\s+(.+)", block)
            # Strip URL parts and markdown noise; keep only the name portion
            competitor_names = [
                i.strip().strip("*_:").split(":")[0].split("(")[0].strip()
                for i in items[:8]
                if len(i.strip()) > 2
            ]
            competitor_names = [n for n in competitor_names if n]
            if competitor_names:
                break

    if not competitor_names:
        _log_warn("competitor_names not found — using empty list")

    # ── market_awareness_level ────────────────────────────────────────────────
    _AWARENESS_LEVELS = {
        "unaware", "problem_aware", "solution_aware", "product_aware", "most_aware"
    }
    raw_awareness = _first_match([
        r"(?i)market\s+awareness[_ ]level[:\s*]+([a-z_\- ]+)",
        r"(?i)awareness\s+level[:\s*]+([a-z_\- ]+)",
        r"(?i)awareness\s+stage[:\s*]+([a-z_\- ]+)",
        r"(?i)(unaware|problem[\s_-]aware|solution[\s_-]aware|product[\s_-]aware|most[\s_-]aware)",
    ], content)
    market_awareness_level = re.sub(r"[\s\-]+", "_", raw_awareness.lower().strip())
    if market_awareness_level not in _AWARENESS_LEVELS:
        market_awareness_level = "problem_aware"
        warnings.warn(
            "[DEGRADED] 'market_awareness_level' not found — "
            "defaulting to 'problem_aware'. Output confidence is reduced.",
            RuntimeWarning, stacklevel=2
        )

    # ── competitor_dominant_angle ─────────────────────────────────────────────
    competitor_dominant_angle = _first_match([
        r"(?i)competitor\s+dominant\s+angle[:\s*]+([^\n]{10,300})",
        r"(?i)dominant\s+competitor\s+angle[:\s*]+([^\n]{10,300})",
        r"(?i)competitive\s+angle[:\s*]+([^\n]{10,300})",
        r"(?i)competitor\s+pattern[:\s*]+([^\n]{10,300})",
        r"(?i)market\s+pattern[:\s*]+([^\n]{10,300})",
    ], content)
    if not competitor_dominant_angle:
        competitor_dominant_angle = (
            "Results-focused transformation messaging with social proof"
        )
        warnings.warn(
            "[DEGRADED] 'competitor_dominant_angle' not found — using generic default. "
            "Output confidence is reduced.",
            RuntimeWarning, stacklevel=2
        )

    # ── new_mechanism_name ────────────────────────────────────────────────────
    new_mechanism_name = _first_match([
        r"(?i)mechanism\s+name[:\s*]+([^\n]{3,80})",
        r"(?i)new\s+mechanism[:\s*]+([^\n]{3,80})",
        r"(?i)proprietary\s+(?:mechanism|method|system|protocol)[:\s*]+([^\n]{3,80})",
        # Capitalised "The Xxx Protocol/System/…" patterns
        r"(?i)the\s+([A-Z][^\n.]{3,60}?"
        r"(?:Protocol|System|Method|Formula|Framework|Blueprint|Code|Map))",
        r"(?i)(?:protocol|system|method|formula|framework|blueprint)\s+name[:\s*]+([^\n]{3,80})",
    ], content)
    if not new_mechanism_name:
        first_word = validated_niche.split()[0].title() if validated_niche else "Core"
        new_mechanism_name = f"The {first_word} System"
        warnings.warn(
            "[DEGRADED] 'new_mechanism_name' not found — derived from niche. "
            "Output confidence is reduced.",
            RuntimeWarning, stacklevel=2
        )

    result = {
        "validated_niche":            validated_niche,
        "dominant_emotion":           dominant_emotion,
        "dominant_persona":           dominant_persona,
        "price_point":                price_point,
        "top_3_uvp":                  top_3_uvp[:3],
        "positioning":                positioning[:300],
        "competitor_names":           competitor_names[:8],
        "market_awareness_level":     market_awareness_level,
        "competitor_dominant_angle":  competitor_dominant_angle[:300],
        "new_mechanism_name":         new_mechanism_name[:100],
    }

    _log_ok(
        f"Phase 1 business fields extracted → "
        f"niche='{validated_niche}' | emotion={dominant_emotion} | "
        f"price=${price_point} | {len(competitor_names)} competitors"
    )
    return result
