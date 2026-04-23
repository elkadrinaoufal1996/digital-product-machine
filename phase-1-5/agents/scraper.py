#!/usr/bin/env python3
"""
phase-1-5/agents/scraper.py — Phase 1.5 Agent: Brand Intelligence Scraper
==========================================================================
Reads phase-1/outputs/PHASE-1-OUTPUT.md, then scrapes competitor brand
intelligence (visual identity, voice patterns, marketing angles) from
three sources in parallel:

  SOURCE 1 — Firecrawl  : Competitor landing pages → visual_intel
  SOURCE 2 — Apify      : TikTok hashtag feed      → angles_intel
  SOURCE 3 — Tavily     : Reddit/forum threads      → voice_intel

Output: phase-1-5/outputs/00-brand-intel.json

Usage (no CLI args):
    python phase-1-5/agents/scraper.py

Dependencies:
    pip install firecrawl-py apify-client tavily-python python-dotenv
"""

import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date
from pathlib import Path

from dotenv import load_dotenv

# ─── Shared utilities (Phase 1 markdown parsing) ──────────────────────────────
# utils.py lives one level up: phase-1-5/utils.py
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils import parse_phase1_output  # noqa: E402

# ─── Paths ────────────────────────────────────────────────────────────────────
# scraper.py lives at: <workspace>/phase-1-5/agents/scraper.py
# BASE_DIR             → <workspace>/                    (project root)
# PHASE1_OUTPUT_PATH   → <workspace>/phase-1/outputs/PHASE-1-OUTPUT.md
# OUTPUT_DIR           → <workspace>/phase-1-5/outputs/
# ENV_PATH             → <workspace>/phase-1-5/.env

AGENT_DIR          = Path(__file__).parent.resolve()
BASE_DIR           = AGENT_DIR.parent.parent.resolve()
PHASE1_OUTPUT_PATH = BASE_DIR / "phase-1" / "outputs" / "PHASE-1-OUTPUT.md"
OUTPUT_DIR         = AGENT_DIR.parent / "outputs"
OUTPUT_PATH        = OUTPUT_DIR / "00-brand-intel.json"
ENV_PATH           = AGENT_DIR.parent / ".env"

# ─── Terminal colours ─────────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─── Logging helpers ──────────────────────────────────────────────────────────

def log_info(msg: str) -> None:
    print(f"{CYAN}[INFO]{RESET} {msg}")


def log_ok(msg: str) -> None:
    print(f"{GREEN}{BOLD}[OK]{RESET} {msg}")


def log_warn(msg: str) -> None:
    print(f"{YELLOW}[WARN]{RESET} {msg}")


def _halt(msg: str) -> None:
    """Print a formatted blocking error and exit."""
    print(f"{RED}{BOLD}[BLOCKING ERROR: {msg}]{RESET}", file=sys.stderr)
    sys.exit(1)


# ─── ENV LOADING ──────────────────────────────────────────────────────────────

def load_env() -> None:
    """Load phase-1-5/.env; halt loudly on any missing required variable."""
    if ENV_PATH.exists():
        load_dotenv(ENV_PATH)
        log_info(f".env loaded from {ENV_PATH.relative_to(BASE_DIR)}")
    else:
        log_warn(f".env not found at {ENV_PATH.relative_to(BASE_DIR)} — reading from system environment")

    required = ["ANTHROPIC_KEY", "APIFY_TOKEN", "FIRECRAWL_KEY", "TAVILY_KEY"]
    missing  = [v for v in required if not os.getenv(v)]
    if missing:
        _halt(f"missing env var {', '.join(missing)}")


# ─── COLOR EXTRACTION ─────────────────────────────────────────────────────────

def extract_colors_from_html(html: str) -> list[str]:
    """
    Extract the top-5 most-frequent hex colour codes from raw HTML/CSS.
    Normalises 3-digit shorthand (#abc → #AABBCC).
    Excludes pure white/black/near-white to surface brand colours.
    """
    _EXCLUDE = {"#FFFFFF", "#000000", "#FEFEFE", "#FDFDFD", "#FFFFFE", "#111111"}
    hex_re = re.compile(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b')
    freq: dict[str, int] = {}
    for c in hex_re.findall(html):
        norm = ('#' + ''.join(ch * 2 for ch in c)).upper() if len(c) == 3 else '#' + c.upper()
        if norm not in _EXCLUDE:
            freq[norm] = freq.get(norm, 0) + 1
    top = sorted(freq, key=freq.__getitem__, reverse=True)[:5]
    return top if top else ["#FFFFFF", "#000000"]


# ─── SOURCE 1 — FIRECRAWL (Visual Intel) ─────────────────────────────────────

def run_firecrawl(competitor_urls: list[str], niche: str) -> tuple[str, list[dict], str]:
    """
    Scrape competitor pages with Firecrawl → visual_intel entries.

    Returns:
        (status: "ok"|"partial"|"failed", visual_intel: list[dict], error_msg: str)
    """
    try:
        from firecrawl import FirecrawlApp  # type: ignore
    except ImportError:
        return "failed", [], "firecrawl-py not installed — run: pip install firecrawl-py"

    try:
        app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_KEY"))
    except Exception as exc:
        return "failed", [], str(exc)

    visual_intel: list[dict] = []

    for url in competitor_urls[:8]:
        try:
            log_info(f"  Firecrawl → {url}")
            result = app.scrape_url(url, params={"formats": ["html", "markdown"]})

            html = result.get("html", "") or ""
            md   = result.get("markdown", "") or ""
            meta = result.get("metadata", {}) or {}

            # Dominant colours (CSS parse)
            colors = extract_colors_from_html(html)

            # Font families
            font_raw = re.findall(r'font-family\s*:\s*([^;}\n]{3,80})', html, re.IGNORECASE)
            fonts = list({f.strip().split(',')[0].strip('"\'') for f in font_raw})[:5]

            # Hero copy: first <h1> tag, fallback to first # heading in markdown
            h1 = re.search(r'<h1[^>]*>\s*([^<]{5,300})\s*</h1>', html, re.IGNORECASE)
            hero_copy = h1.group(1).strip() if h1 else ""
            if not hero_copy and md:
                hm = re.search(r'^#+\s+(.+)$', md, re.MULTILINE)
                hero_copy = hm.group(1).strip() if hm else md[:120].strip()

            # CTA copy: button or prominent link
            cta_copy = ""
            for cta_pat in (
                r'<button[^>]*>\s*([^<]{2,80})\s*</button>',
                r'(?:class="[^"]*btn[^"]*"|role="button")[^>]*>\s*([^<]{2,80})\s*<',
                r'<a[^>]+(?:class="[^"]*(?:cta|button)[^"]*")[^>]*>\s*([^<]{2,80})\s*</a>',
            ):
                m = re.search(cta_pat, html, re.IGNORECASE)
                if m:
                    cta_copy = m.group(1).strip()
                    break

            # Screenshot URL from OG tags
            screenshot_url = meta.get("ogImage") or meta.get("og:image") or None

            visual_intel.append({
                "competitor_url":     url,
                "dominant_colors_hex": colors,
                "fonts":              fonts if fonts else ["sans-serif"],
                "hero_copy":          hero_copy[:300],
                "cta_copy":           cta_copy[:150],
                "screenshot_url":     screenshot_url,
            })

        except Exception as exc:
            log_warn(f"  Firecrawl error for {url}: {exc}")
            visual_intel.append({
                "competitor_url":     url,
                "dominant_colors_hex": [],
                "fonts":              [],
                "hero_copy":          "",
                "cta_copy":           "",
                "screenshot_url":     None,
            })

    # Best-effort scrape of /about + /newsletter pages for extra voice copy
    for url in competitor_urls[:3]:
        for suffix in ("/about", "/newsletter", "/email"):
            extra_url = url.rstrip("/") + suffix
            try:
                result = app.scrape_url(extra_url, params={"formats": ["markdown"]})
                md = result.get("markdown", "") or ""
                if len(md) > 100:
                    log_info(f"  Firecrawl extra page: {extra_url}")
            except Exception:
                pass  # Best-effort; ignored

    valid_count = sum(1 for v in visual_intel if v["dominant_colors_hex"] or v["hero_copy"])
    status = "ok" if valid_count >= 5 else ("partial" if valid_count >= 1 else "failed")
    print(f"[SOURCE 1] {'OK' if status == 'ok' else status.upper()} — {valid_count} items collected")
    return status, visual_intel, ""


# ─── SOURCE 2 — APIFY TIKTOK (Angles Intel) ──────────────────────────────────

def run_apify_tiktok(niche: str, persona_keywords: list[str]) -> tuple[str, list[dict], str]:
    """
    Scrape TikTok via Apify actor clockworks/tiktok-hashtag-scraper.

    Returns:
        (status: "ok"|"partial"|"failed", angles_intel: list[dict], error_msg: str)
    """
    try:
        from apify_client import ApifyClient  # type: ignore
    except ImportError:
        return "failed", [], "apify-client not installed — run: pip install apify-client"

    try:
        client = ApifyClient(os.getenv("APIFY_TOKEN"))
    except Exception as exc:
        return "failed", [], str(exc)

    # Build hashtag list from niche slug + top persona keywords
    def slugify(text: str) -> str:
        return re.sub(r'[^a-z0-9]', '', text.lower().replace(' ', ''))

    niche_slug = slugify(niche)
    hashtags = [niche_slug] + [
        slugify(kw) for kw in persona_keywords[:4]
        if len(slugify(kw)) > 2
    ]
    hashtags = list(dict.fromkeys(hashtags))[:5]  # dedup, cap at 5
    log_info(f"  TikTok hashtags: {hashtags}")

    angles_intel: list[dict] = []

    try:
        run_input = {
            "hashtags":          hashtags,
            "resultsPerPage":    20,
            "maxRequestRetries": 3,
        }

        # Start the actor run (non-blocking) then poll manually with sleep(1)
        # to avoid rate-limit bursts on the Apify status endpoint.
        actor_run = client.actor("clockworks/tiktok-hashtag-scraper").start(
            run_input=run_input
        )
        run_id = actor_run.get("id")
        if not run_id:
            raise ValueError("No run ID returned when starting Apify actor")

        log_info(f"  Apify run started (id={run_id}) — polling for completion…")
        _TERMINAL = {"SUCCEEDED", "FAILED", "ABORTED", "TIMED-OUT"}
        while True:
            time.sleep(1)  # rate-limit guard between status checks
            run_info = client.run(run_id).get()
            status   = (run_info or {}).get("status", "UNKNOWN")
            log_info(f"  Apify status: {status}")
            if status in _TERMINAL:
                break

        if status != "SUCCEEDED":
            raise RuntimeError(f"Apify actor finished with status: {status}")

        dataset_id = (run_info or {}).get("defaultDatasetId")
        if not dataset_id:
            raise ValueError("No defaultDatasetId in completed Apify run")

        items = client.dataset(dataset_id).list_items().items
        log_info(f"  Apify TikTok returned {len(items)} raw items")

        for item in items[:50]:
            # Hook text: first line of the video description
            desc = item.get("text") or item.get("description") or ""
            hook = desc.split('\n')[0][:150].strip() if desc else ""
            if not hook:
                continue  # Skip items with no hook

            # Engagement rate = likes / plays
            plays    = item.get("playCount") or item.get("plays") or 0
            likes    = item.get("diggCount") or item.get("likes") or 0
            eng_rate = round(likes / plays, 4) if plays > 0 else 0.0

            # Hashtag list
            ht_raw = item.get("hashtags") or []
            if isinstance(ht_raw, list):
                tags = [
                    (h.get("name") if isinstance(h, dict) else str(h))
                    for h in ht_raw
                ]
            else:
                tags = re.findall(r'#(\w+)', desc)

            # Creator handle
            author = item.get("authorMeta") or item.get("author") or {}
            if isinstance(author, dict):
                handle = author.get("name") or author.get("uniqueId") or ""
            else:
                handle = str(author)

            # Video URL
            video_url = item.get("webVideoUrl") or item.get("url") or ""

            angles_intel.append({
                "platform":        "tiktok",
                "hook":            hook,
                "engagement_rate": eng_rate,
                "hashtags":        [str(t) for t in tags[:10]],
                "creator_handle":  str(handle)[:50],
                "url":             video_url,
            })

    except Exception as exc:
        msg = str(exc)
        log_warn(f"  Apify TikTok error: {msg}")
        print(f"[SOURCE 2] FAILED — {msg}")
        return "failed", [], msg

    count  = len(angles_intel)
    status = "ok" if count >= 30 else ("partial" if count >= 1 else "failed")
    print(f"[SOURCE 2] {'OK' if status == 'ok' else status.upper()} — {count} items collected")
    return status, angles_intel, ""


# ─── SOURCE 3 — TAVILY (Voice Intel / Reddit) ────────────────────────────────

def _tavily_search(tavily_client, query: str, max_results: int = 20) -> list[dict]:
    """Thin wrapper around tavily.search(); returns result list or []."""
    try:
        resp = tavily_client.search(
            query=query,
            search_depth="advanced",
            max_results=max_results,
            include_domains=["reddit.com"],
        )
        return resp.get("results", [])
    except Exception as exc:
        log_warn(f"  Tavily query failed [{query[:50]}]: {exc}")
        return []


def _result_to_verbatims(result: dict) -> list[dict]:
    """Convert a single Tavily search result into ≤3 verbatim entries."""
    url     = result.get("url", "")
    title   = result.get("title", "")
    content = result.get("content", "") or result.get("snippet", "")
    raw_date = result.get("published_date") or result.get("date") or ""
    norm_date = raw_date[:10] if len(raw_date) >= 10 else str(date.today())
    platform  = "reddit" if "reddit.com" in url else "forum"

    verbatims: list[dict] = []

    # Include the post title as a verbatim (often a pain statement)
    if title and url:
        verbatims.append({
            "source_url": url,
            "platform":   platform,
            "quote":      title[:400],
            "date":       norm_date,
        })

    # Include up to 2 sentences from the body
    if content:
        sentences = [
            s.strip()
            for s in re.split(r'(?<=[.!?])\s+', content)
            if len(s.strip()) > 30
        ]
        for sentence in sentences[:2]:
            verbatims.append({
                "source_url": url,
                "platform":   platform,
                "quote":      sentence[:400],
                "date":       norm_date,
            })

    return verbatims


def run_tavily(
    niche: str,
    persona_keywords: list[str],
    uvzs: list[str],
) -> tuple[str, dict, str]:
    """
    Search Reddit via Tavily for persona verbatims.

    Returns:
        (status: "ok"|"partial"|"failed", voice_intel: dict, error_msg: str)
    """
    try:
        from tavily import TavilyClient  # type: ignore
    except ImportError:
        return "failed", {}, "tavily-python not installed — run: pip install tavily-python"

    try:
        tavily = TavilyClient(api_key=os.getenv("TAVILY_KEY"))
    except Exception as exc:
        return "failed", {}, str(exc)

    # Build 5 search queries: 3 persona-pain angles + 2 niche-general
    queries: list[str] = []
    for kw in persona_keywords[:3]:
        queries.append(f'"{niche}" {kw} site:reddit.com')
    queries.append(f'"{niche}" tips advice forum')
    queries.append(f'"{niche}" review experience reddit')

    raw_verbatims: list[dict] = []

    for query in queries:
        log_info(f"  Tavily → {query[:70]}...")
        for r in _tavily_search(tavily, query, max_results=20):
            raw_verbatims.extend(_result_to_verbatims(r))

    # Deduplicate by quote text
    seen: set[str] = set()
    unique: list[dict] = []
    for v in raw_verbatims:
        if v["quote"] not in seen:
            seen.add(v["quote"])
            unique.append(v)

    voice_intel = {
        "competitor_copy_samples": [],  # populated best-effort from Firecrawl hero/CTA
        "persona_verbatims":       unique,
    }

    count  = len(unique)
    status = "ok" if count >= 15 else ("partial" if count >= 5 else "failed")
    print(f"[SOURCE 3] {'OK' if status == 'ok' else status.upper()} — {count} items collected")
    return status, voice_intel, ""


# ─── RETRY — VERBATIM TOP-UP ──────────────────────────────────────────────────

def retry_verbatims(
    niche: str,
    persona_keywords: list[str],
    current_count: int,
) -> list[dict]:
    """
    Run broader Tavily queries to top up persona_verbatims toward the ≥15 minimum.
    Returns a list of additional verbatim dicts (may include duplicates — caller deduplicates).
    """
    try:
        from tavily import TavilyClient  # type: ignore
        tavily = TavilyClient(api_key=os.getenv("TAVILY_KEY"))
    except Exception:
        return []

    retry_queries = [
        f"{niche} beginner mistakes reddit",
        f"{niche} what nobody tells you",
        f"{niche} frustrations community",
        f"{niche} real results transformation reddit",
        f"{niche} questions answers forum",
    ]
    extra: list[dict] = []
    for q in retry_queries:
        if current_count + len(extra) >= 15:
            break
        log_info(f"  Tavily retry → {q[:60]}")
        try:
            resp = tavily.search(q, search_depth="basic", max_results=10, include_domains=["reddit.com"])
            for r in resp.get("results", []):
                extra.extend(_result_to_verbatims(r))
        except Exception as exc:
            log_warn(f"  Retry query failed: {exc}")
    return extra


# ─── POST-PROCESS: ENRICH voice_intel WITH FIRECRAWL COPY ────────────────────

def enrich_voice_with_visual(voice_intel: dict, visual_intel: list[dict]) -> dict:
    """
    Back-fill voice_intel.competitor_copy_samples from Firecrawl hero/CTA copy.
    Extracts tone markers via simple heuristics.
    """
    samples: list[dict] = []
    _TONE_WORDS = {
        "urgent": ["now", "today", "immediately", "don't wait", "limited"],
        "aspirational": ["dream", "transform", "achieve", "success", "finally"],
        "social_proof": ["join", "thousands", "community", "trusted", "proven"],
        "fear": ["risk", "fail", "missing", "struggle", "never"],
        "empathetic": ["understand", "know how", "been there", "feel", "we get it"],
    }

    for v in visual_intel:
        hero = v.get("hero_copy", "")
        cta  = v.get("cta_copy", "")
        if not hero:
            continue
        body = f"{hero}\n{cta}"
        tone_markers: list[str] = []
        for tone, words in _TONE_WORDS.items():
            if any(w in body.lower() for w in words):
                tone_markers.append(tone)
        samples.append({
            "url":          v["competitor_url"],
            "headline":     hero[:200],
            "body":         cta[:200],
            "tone_markers": tone_markers,
        })

    voice_intel["competitor_copy_samples"] = samples
    return voice_intel


# ─── VALIDATION ───────────────────────────────────────────────────────────────

def validate_output(data: dict) -> list[str]:
    """
    Check the four quantitative validation criteria from the brief.
    Returns a list of warning strings (non-empty → not all criteria met).
    """
    warnings: list[str] = []

    vi = data.get("visual_intel", [])
    valid_vi = [v for v in vi if v.get("dominant_colors_hex") and v.get("hero_copy")]
    if len(valid_vi) < 5:
        warnings.append(
            f"visual_intel: only {len(valid_vi)} entries with colors+hero_copy (need ≥5)"
        )

    verbatims = data.get("voice_intel", {}).get("persona_verbatims", [])
    if len(verbatims) < 15:
        warnings.append(
            f"persona_verbatims: only {len(verbatims)} entries (need ≥15)"
        )

    ai = data.get("angles_intel", [])
    hooked = [a for a in ai if a.get("hook") and a.get("engagement_rate") is not None]
    if len(hooked) < 30:
        warnings.append(
            f"angles_intel: only {len(hooked)} entries with engagement_rate (need ≥30)"
        )

    return warnings


# ─── MAIN ─────────────────────────────────────────────────────────────────────

def main() -> None:
    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  PHASE 1.5 — BRAND INTELLIGENCE SCRAPER{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

    t_start = time.time()

    # ── 1. Load environment variables ─────────────────────────────────────────
    load_env()

    # ── 2. Parse Phase 1 output ───────────────────────────────────────────────
    phase1           = parse_phase1_output(PHASE1_OUTPUT_PATH)
    niche            = phase1["final_niche"]
    uvzs             = phase1["top_3_UVZ"]
    competitor_urls  = phase1["top_competitor_urls"]
    persona_keywords = phase1["target_persona_keywords"]

    print(f"\n  Niche       : {niche}")
    print(f"  UVZs        : {uvzs}")
    print(f"  Competitors : {len(competitor_urls)} URL(s)")
    print(f"  Kw sample   : {persona_keywords[:3]}\n")

    # ── 3. Run 3 sources IN PARALLEL ─────────────────────────────────────────
    log_info("Launching 3 source scrapers in parallel (ThreadPoolExecutor, max_workers=3)...")

    results: dict[str, tuple] = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_map = {
            executor.submit(run_firecrawl,    competitor_urls, niche):        "firecrawl",
            executor.submit(run_apify_tiktok, niche, persona_keywords):       "apify_tiktok",
            executor.submit(run_tavily,       niche, persona_keywords, uvzs): "tavily",
        }
        for future in as_completed(future_map):
            key = future_map[future]
            try:
                results[key] = future.result()
            except Exception as exc:
                log_warn(f"  Source '{key}' raised an unhandled exception: {exc}")
                # Produce a safe default so unpacking never fails
                results[key] = ("failed", [] if key != "tavily" else {}, str(exc))

    # ── 4. Unpack results ─────────────────────────────────────────────────────
    fc_status, visual_intel,  fc_err = results.get("firecrawl",    ("failed", [], ""))
    tk_status, angles_intel,  tk_err = results.get("apify_tiktok", ("failed", [], ""))
    tv_status, voice_intel,   tv_err = results.get("tavily",       ("failed", {}, ""))

    # ── 5. Apply blocking conditions ──────────────────────────────────────────
    if fc_status == "failed" and tv_status == "failed":
        _halt("brand intel impossible — visual + voice both unavailable")

    if tk_status == "failed":
        log_warn(
            "[SOURCE 2] TikTok FAILED — angles_intel will be empty; "
            "Skill 08 will degrade gracefully"
        )

    # ── 6. Retry verbatims if under threshold ─────────────────────────────────
    if not isinstance(voice_intel, dict):
        voice_intel = {"competitor_copy_samples": [], "persona_verbatims": []}

    verbatims = voice_intel.get("persona_verbatims", [])
    if len(verbatims) < 15:
        log_warn(f"Only {len(verbatims)} verbatims collected — running Tavily retry...")
        extra = retry_verbatims(niche, persona_keywords, len(verbatims))
        # Deduplicate
        seen: set[str] = {v["quote"] for v in verbatims}
        for v in extra:
            if v["quote"] not in seen:
                seen.add(v["quote"])
                verbatims.append(v)
        voice_intel["persona_verbatims"] = verbatims
        log_info(f"  After retry: {len(verbatims)} verbatims")

    final_verbatims = voice_intel.get("persona_verbatims", [])
    if len(final_verbatims) < 15:
        _halt("insufficient verbatim data — Skill 07 cannot calibrate voice")

    # ── 7. Enrich voice_intel with Firecrawl copy samples ────────────────────
    voice_intel = enrich_voice_with_visual(voice_intel, visual_intel)

    # ── 8. Assemble final JSON ────────────────────────────────────────────────
    output = {
        "metadata": {
            "niche":          niche,
            "uvz":            uvzs,
            "scraped_at":     datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "sources_status": {
                "firecrawl":    fc_status,
                "apify_tiktok": tk_status,
                "tavily":       tv_status,
            },
        },
        "visual_intel": visual_intel,
        "voice_intel":  voice_intel,
        "angles_intel": angles_intel if isinstance(angles_intel, list) else [],
    }

    # ── 9. Write output ───────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    size_kb = OUTPUT_PATH.stat().st_size / 1024
    log_ok(f"Output written → {OUTPUT_PATH.relative_to(BASE_DIR)} ({size_kb:.1f} KB)")

    # ── 10. Validate JSON round-trip ─────────────────────────────────────────
    with open(OUTPUT_PATH, encoding="utf-8") as fh:
        json.load(fh)
    log_ok("JSON validated — parseable with json.load()")

    # ── 11. Quantitative validation report ───────────────────────────────────
    validation_warnings = validate_output(output)
    if validation_warnings:
        for w in validation_warnings:
            log_warn(f"Validation: {w}")
    else:
        log_ok("All validation criteria passed ✓")

    # ── Summary ───────────────────────────────────────────────────────────────
    t_elapsed = time.time() - t_start
    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{GREEN}{BOLD}  BRAND INTEL SCRAPER — COMPLETE ✓{RESET}")
    print(f"  Runtime     : {t_elapsed:.1f}s  (parallel — sources ran concurrently)")
    print(f"  Visual      : {len(visual_intel)} competitor entries")
    print(f"  Verbatims   : {len(final_verbatims)} persona quotes")
    print(f"  Angles      : {len(output['angles_intel'])} TikTok hooks")
    print(f"  Output      : {OUTPUT_PATH.relative_to(BASE_DIR)}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")


if __name__ == "__main__":
    main()
