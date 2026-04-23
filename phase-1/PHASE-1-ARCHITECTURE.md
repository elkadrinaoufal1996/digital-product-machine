# PHASE-1-ARCHITECTURE
## Digital Product Machine — Phase 1 Agent Chain

---

## Overview

Phase 1 is a fully autonomous 5-skill agent pipeline for US digital product market intelligence.
It requires a single command to launch, produces a single sellable deliverable, and uses no pre-defined niche, seed, or budget as input.

**Launch command:**
```bash
claude-code run phase-1 --market=US
```

**Final output:** `PHASE-1-OUTPUT.md` — complete positioning, Value Stack, hooks, and 30-day launch plan.

---

## Chain Architecture

```
INPUT: --market=US
        │
        ▼
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 01 — market-discovery                                     │
│ Agent: Scraper                                                  │
│ Tools: Apify (×3 jobs), Tavily (Reddit)                         │
│ Output: 01-market-discovery.json                                │
│ Content: 15 niches + raw demand signals + preliminary UVZs      │
└─────────────────────────┬───────────────────────────────────────┘
                          │ 01-market-discovery.json
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 02 — niche-idea-scorer                                    │
│ Agent: Analyst                                                  │
│ Tools: Apify (×2 jobs), Firecrawl (LP scraping), Web Search     │
│ Output: 02-scored.json                                          │
│ Content: Top 5 niches /100 + Top 3 ebook ideas /100 per niche  │
│ PREREQUISITE: Web search must be available (BLOCKING)           │
└─────────────────────────┬───────────────────────────────────────┘
                          │ 02-scored.json
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 03 — competitor-xray                                      │
│ Agent: Analyst                                                  │
│ Tools: Apify (Amazon reviews + TikTok comments), Firecrawl (LP) │
│ Output: 03-xray.json                                            │
│ Content: 1 final niche + 6-gap analysis + 3 ranked UVZs        │
│ PREREQUISITE: Web search must be available (BLOCKING)           │
└─────────────────────────┬───────────────────────────────────────┘
                          │ 03-xray.json
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 04 — buyer-intelligence                                   │
│ Agent: Analyst                                                  │
│ Tools: Tavily (Reddit), Apify (Amazon reviews + TikTok)         │
│ Output: 04-personas.json                                        │
│ Content: 3 empirical personas + verbatim banks + collab dim.    │
│ PREREQUISITE: Web search must be available (BLOCKING)           │
└─────────────────────────┬───────────────────────────────────────┘
         ┌────────────────┘
         │ 02-scored.json + 03-xray.json + 04-personas.json
         ▼
┌─────────────────────────────────────────────────────────────────┐
│ SKILL 05 — positioning-launch                                   │
│ Agent: Analyst                                                  │
│ Tools: Firecrawl (pricing + VSL pages), Web Search              │
│ Output: PHASE-1-OUTPUT.md                                       │
│ Content: Promises × 3, Value Stack, 18 Hooks, J1-J30 plan,     │
│          Confidence Score /10                                    │
│ PREREQUISITE: Web search must be available (BLOCKING)           │
└─────────────────────────────────────────────────────────────────┘
                          │
                          ▼
OUTPUT: PHASE-1-OUTPUT.md (single sellable deliverable)
```

---

## Skill-by-Skill Reference

### SKILL 01 — market-discovery

| Property | Value |
|----------|-------|
| Agent type | Scraper |
| Input | `--market=US` (CLI only) |
| Output | `01-market-discovery.json` |
| Tools | Apify (Gumroad scraper, Kindle BSR scraper, TikTok hashtag scraper), Tavily (Reddit search) |
| Blocking condition | Amazon Kindle source returns < 5 categories |
| Unique responsibility | Binary elimination filter (LEGAL, SATURATED, NO-PAY, SEASONAL, PLATFORM-RISK) |
| What it does NOT do | Scoring, ranking, hook writing, persona building |
| Key output fields | 15 niches × demand_signals × preliminary_uvz |

---

### SKILL 02 — niche-idea-scorer

| Property | Value |
|----------|-------|
| Agent type | Analyst |
| Input | `01-market-discovery.json` |
| Output | `02-scored.json` |
| Tools | Apify (Gumroad niche sales, Kindle BSR comps), Firecrawl (LP top 3 competitors), Web Search |
| Blocking conditions | Web search unavailable; Skill 01 output < 10 niches |
| Unique responsibility | Matrix A (niche /100) + Matrix B (ebook idea /100) — separate, not combined |
| Protocols | Zero-Error Calc, Payment Reality Filter (Tier 1/2/3), VC Pessimism |
| What it does NOT do | Hook writing (→ 05), Value Stack (→ 05), influence outreach (→ 04) |
| Key output fields | Top 5 niches with matrix_a_score + tier_demand + verdict + 3 ebook ideas with matrix_b_score |

---

### SKILL 03 — competitor-xray

| Property | Value |
|----------|-------|
| Agent type | Analyst |
| Input | `02-scored.json` |
| Output | `03-xray.json` |
| Tools | Apify (Amazon 1-2★ reviews, TikTok comments), Firecrawl (Gumroad/Etsy LP) |
| Blocking conditions | Web search unavailable; Skill 02 shortlist < 3 niches |
| Unique responsibility | 6-gap analysis (G1-G6) — the only skill that produces gap intelligence |
| What it does NOT do | Hook writing (→ 05), persona building (→ 04), niche scoring (done in 02) |
| Key output fields | 1 final_niche + gap_analysis (6 gaps × CONFIRMED/PARTIAL/ABSENT) + 3 uvz_ranked |

---

### SKILL 04 — buyer-intelligence

| Property | Value |
|----------|-------|
| Agent type | Analyst |
| Input | `03-xray.json` |
| Output | `04-personas.json` |
| Tools | Tavily (Reddit threads), Apify (Amazon 1★ reviews, TikTok comments) |
| Blocking conditions | Web search unavailable; Skill 03 output missing final_niche |
| Unique responsibility | Primary-data-only personas + verbatim banks + influence collab dimension (absorbed from Collab-Ability) |
| Key rule | Minimum 5 verbatims per persona, each with URL and date. Zero LLM archetypes. |
| What it does NOT do | Hook writing (→ 05), offer design (→ 05), scoring (→ 02/03) |
| Key output fields | 3 personas × (verbatim_bank + consciousness_level + dominant_emotion + verbatim_glossary + influence_collab_dimension) |

---

### SKILL 05 — positioning-launch

| Property | Value |
|----------|-------|
| Agent type | Analyst |
| Inputs | `02-scored.json` + `03-xray.json` + `04-personas.json` (all 3 required simultaneously) |
| Output | `PHASE-1-OUTPUT.md` |
| Tools | Firecrawl (competitor pricing pages, VSL/LP pages), Web Search |
| Blocking conditions | Web search unavailable; any of the 3 input files missing |
| Unique responsibility | ALL copy hooks (18 total), ALL Value Stack design, ALL promise versions — this is the single hook-writing node in the chain |
| Key rule | Confidence Score /10 derived from prior skill outputs — not self-assessed |
| What it does NOT do | Rescoring niches (trust 02), re-analyzing competitors (trust 03), building new personas (trust 04) |
| Key output fields | 3 promise versions + recommended title/subtitle + Value Stack (3 tiers) + 18 hooks + J1-J30 plan + Confidence Score /10 |

---

## Redundancy Map — What Lives Where (Single Source of Truth)

| Concept | Skill | Notes |
|---------|-------|-------|
| Elimination filters | 01 only | Binary only — no scoring |
| Niche scoring matrix /100 | 02 only | Matrix A |
| Ebook idea scoring matrix /100 | 02 only | Matrix B |
| Zero-Error Calc protocol | 02 only | Both matrices |
| Payment Reality Filter (Tier) | 02 only | Blocks false demand scores |
| VC Pessimism protocol | 02 only | Counter-arguments for scores ≥7 |
| Gap analysis (6 types) | 03 only | G1-G6 |
| UVZ construction | 03 only | 3 ranked UVZs |
| Buyer verbatim collection | 04 only | 3 primary sources |
| Consciousness levels | 04 only | L1-L5 framework |
| Purchase emotions | 04 only | 5 emotions |
| Influence collab dimension | 04 only | Absorbed from former Collab-Ability |
| Hooks (all types) | 05 only | 9 persona hooks + 9 UVZ hooks |
| Value Stack design | 05 only | Lead magnet + Ebook + Upsell |
| Promise architecture | 05 only | 3 versions (Rational/Emotional/Urgency) |
| Launch calendar | 05 only | J-7 to J30 |
| Confidence Score /10 | 05 only | Derived from 02+03+04 outputs |

---

## File Structure

```
phase-1/
├── PHASE-1-ARCHITECTURE.md          ← This file
│
├── 01-market-discovery/
│   ├── SKILL.md
│   ├── input-schema.json
│   ├── output-schema.json
│   └── references/
│       └── elimination-filters.md
│
├── 02-niche-idea-scorer/
│   ├── SKILL.md
│   ├── input-schema.json
│   ├── output-schema.json
│   └── references/
│       └── scoring-protocols.md
│
├── 03-competitor-xray/
│   ├── SKILL.md
│   ├── input-schema.json
│   ├── output-schema.json
│   └── references/
│       └── gap-framework.md
│
├── 04-buyer-intelligence/
│   ├── SKILL.md
│   ├── input-schema.json
│   ├── output-schema.json
│   └── references/
│       └── persona-framework.md
│
└── 05-positioning-launch/
    ├── SKILL.md
    ├── input-schema.json
    ├── output-schema.json
    └── references/
        └── value-stack-rules.md
```

**At runtime, the chain produces these files (in order):**
```
01-market-discovery.json     ← Skill 01 output
02-scored.json               ← Skill 02 output
03-xray.json                 ← Skill 03 output
04-personas.json             ← Skill 04 output
PHASE-1-OUTPUT.md            ← Skill 05 final output (delivered to user)
```

---

## Dependency Graph (JSON Flow)

```
Skill 01 ─────────────────────────────────────► 01-market-discovery.json
                                                          │
Skill 02 ◄────────────────────────────────────────────────┘
Skill 02 ─────────────────────────────────────► 02-scored.json
                                                          │
Skill 03 ◄────────────────────────────────────────────────┘
Skill 03 ─────────────────────────────────────► 03-xray.json
                                                          │
Skill 04 ◄────────────────────────────────────────────────┘
Skill 04 ─────────────────────────────────────► 04-personas.json
                                                          │
Skill 05 ◄──── 02-scored.json ◄───────────────────────────┤
Skill 05 ◄──── 03-xray.json                               │
Skill 05 ◄──── 04-personas.json ◄─────────────────────────┘
Skill 05 ─────────────────────────────────────► PHASE-1-OUTPUT.md
```

---

## Error Handling

| Error Type | Where | Response |
|-----------|-------|----------|
| Amazon Kindle < 5 categories | Skill 01 | HALT — log [BLOCKING ERROR] |
| Web search unavailable | Skills 02, 03, 04, 05 | HALT — log [BLOCKING ERROR] |
| Input JSON missing | Any skill | HALT — specify missing file |
| Niche shortlist < 3 | Skill 03 | HALT — re-run Skill 02 |
| Verbatim count < 5 per persona | Skill 04 | Do not deliver — collect more data |
| Value Stack ratio < 5:1 | Skill 05 | Rework upsell — do not deliver |
| Confidence Score < 6/10 | Skill 05 | 🔴 DO NOT LAUNCH — specify remediation |

---

## Design Principles

1. **One role per skill** — each skill has a single, non-overlapping responsibility
2. **JSON-in, JSON-out** — every skill reads structured input and writes structured output
3. **Evidence-first** — no invented data; every claim traces to a live source with URL
4. **Blocking conditions over silent failures** — halt with clear error rather than produce weak output
5. **Single source of truth** — each concept (hooks, scoring, gaps, personas) lives in exactly one skill
6. **Execution without seed input** — the chain runs autonomously from `--market=US` alone
