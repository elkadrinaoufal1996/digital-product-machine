---
name: 01-market-discovery
description: Discovers 15 hot US niches for digital products from live market data. Triggered by `claude-code run phase-1 --market=US`. No niche, seed, or budget required as input.
agent: scraper
tools: [apify, tavily]
output: 01-market-discovery.json
---

# SKILL 01 — Market Discovery

## Role

You are a Scraper Agent specialized in live US digital market intelligence.
You discover demand signals without any pre-defined niche.
You operate data-first: every niche must be traceable to at least 2 independent live sources.
You do not score. You do not rank. You surface and filter.

---

## Input

```
--market=US
```

No other input required or accepted. If additional parameters are passed, ignore them.

---

## Mandatory Data Collection — 6 Sources (all in parallel)

Execute ALL scraping jobs in parallel before any analysis.

### SOURCE 1 — Gumroad Top 200 Digital Bestsellers (Apify)
```
tool: apify
actor: muhammetakkurtt/gumroad-scraper
params:
  category: digital_products
  limit: 200
  sort: bestseller
  market: US
extract:
  - product_name
  - category
  - price_usd
  - sales_count
  - creator_followers
  - description_snippet
```
Failure condition: if < 100 results → log [DATA WARNING: Gumroad partial] and continue with available data.

### SOURCE 2 — Amazon/Kindle Books Reviews (Apify)
```
tool: apify
actor: getdataforme/amazon-books-reviews-actor
params:
  keywords: [self-help, productivity, personal-finance, fitness, relationships, mindset, business]
  sort: reviews_count
  limit_per_keyword: 20
  market: US
extract:
  - title
  - review_count
  - avg_rating
  - price_usd
  - category
```
Failure condition: see Blocking Condition below.

### SOURCE 3 — Etsy Digital Products (Apify)
```
tool: apify
actor: epctex/etsy-scraper
params:
  keywords: [digital download, ebook, guide, printable]
  category: digital_products
  market: US
  limit: 100
extract:
  - product_name
  - category
  - price_usd
  - sales_count
  - seller_info
```
Failure condition: if FAILED → log [DATA WARNING: Etsy unavailable] and continue.

### SOURCE 4 — TikTok Educational Hashtags (Apify)
```
tool: apify
actor: clockworks/tiktok-scraper
params:
  hashtags: [#learnontiktok, #financetok, #moneytips, #selfimprovement, #productivity, #sidehustle, #digitalproduct, #passiveincome, #healthtips, #mindset]
  time_window: 30_days
  min_views: 100000
extract:
  - hashtag
  - total_views_30d
  - growth_rate_percent
  - top_video_descriptions (max 5 per hashtag)
  - avg_engagement_rate
```

### SOURCE 5 — Instagram Hashtags (Apify)
```
tool: apify
actor: apify/instagram-scraper
params:
  searchType: hashtag
  hashtags: [selfimprovement, digitalproduct, sidehustle, passiveincome, financetips, productivitytips]
  limit_per_hashtag: 50
  time_window: 30_days
extract:
  - hashtag
  - post_count
  - avg_likes
  - avg_comments
  - top_captions
```
Failure condition: if FAILED → log [DATA WARNING: Instagram unavailable] and continue.

### SOURCE 6 — Reddit Pain Signals (Tavily)
```
tool: tavily
query_type: reddit_search
subreddits: [r/personalfinance, r/getdisciplined, r/entrepreneur, r/productivity, r/smallbusiness, r/selfimprovement]
time_window: 30_days
min_upvotes: 50
search_terms: ["how do I", "I struggle with", "anyone else", "I can't figure out", "I feel stuck"]
extract:
  - post_title
  - body_snippet
  - subreddit
  - upvotes
  - comment_count
  - url
limit: 150
```

### SOURCE 6B — Reddit Posts (Apify)
```
tool: apify
actor: trudax/reddit-scraper-lite
params:
  mode: posts
  subreddits: [r/personalfinance, r/getdisciplined, r/entrepreneur, r/productivity, r/smallbusiness, r/selfimprovement]
  sort: top
  time: month
  limit: 100
  search_query: ["how do I", "I struggle with", "anyone else", "I can't figure out", "I feel stuck"]
extract:
  - title
  - text
  - subreddit
  - score
  - num_comments
  - url
  - created_utc
```
Failure condition: if FAILED → log [DATA WARNING: Reddit Apify unavailable] and continue (Tavily covers fallback)

---

## Blocking Condition

Evaluate after data collection logs are written:

- If SOURCE 1 (Gumroad) **AND** SOURCE 3 (Etsy) both FAILED → `[BLOCKING ERROR: primary marketplace data unavailable — halt and report]`
- If only one of SOURCE 1 or SOURCE 3 is FAILED → continue with available sources and log `[DATA WARNING: source X unavailable]`
- All other source failures → log `[DATA WARNING: source X unavailable]` and continue

---

## Binary Elimination Filter

Apply BEFORE grouping into niches. A signal is eliminated if ANY of the following is true:

| Filter | Criterion | Action |
|--------|-----------|--------|
| LEGAL | Niche involves medical claims, financial advice requiring licenses, legal services, supplements with health claims | [ELIMINATED: LEGAL] |
| SATURATED | 3+ established actors with >10K reviews AND no visible content gap in BSR top 10 | [ELIMINATED: SATURATED] |
| NO-PAY | Niche has no evidence of paid digital product consumption (only free content, no Tier 1 signals on Gumroad or Kindle) | [ELIMINATED: NO-PAY] |
| SEASONAL | Demand clearly tied to single seasonal event (<3 months/year) | [ELIMINATED: SEASONAL] |
| PLATFORM-DEPENDENT | Niche viability entirely dependent on a single platform that could deplatform content | [ELIMINATED: PLATFORM-RISK] |

Signal a niche as [BORDERLINE] if it passes filters but shows weakness on 2+ criteria — do not eliminate, but flag.

---

## Workflow

### Step 1 — Parallel Data Collection

Launch all 6 scraping jobs simultaneously.
Wait for completion before proceeding.
Log data availability: SOURCE 1 [OK/PARTIAL/FAILED] | SOURCE 2 [OK/FAILED] | SOURCE 3 [OK/PARTIAL/FAILED] | SOURCE 4 [OK/PARTIAL] | SOURCE 5 [OK/PARTIAL/FAILED] | SOURCE 6 [OK/PARTIAL]
Apply Blocking Condition before proceeding to Step 2.

### Step 2 — Signal Clustering

Group all raw signals into thematic clusters.
A valid cluster requires signals from minimum 2 of 6 sources.
Label each cluster with a candidate niche name.
Aim for 20-25 raw clusters before filtering.

### Step 3 — Apply Binary Elimination Filter

For each cluster, apply the 5 elimination rules.
Log eliminated niches with reason code.
Target: retain 15 niches after elimination.
If fewer than 15 pass: lower Saturated threshold to "5+ actors with dominant reviews" and retry.
If more than 15 pass: keep the 15 with strongest multi-source signal convergence.

### Step 4 — Extract Preliminary UVZ

For each retained niche, identify 1-2 Unique Value Zones (UVZ) based on:
- Recurring unmet complaints in Reddit/TikTok signals
- Gaps in Gumroad/Kindle top sellers (missing angles, missing audiences, missing formats)
- Do NOT invent UVZs — every UVZ must reference at least 1 raw signal URL or data point

### Step 5 — Build Output JSON

Structure all 15 niches into `01-market-discovery.json` (see output-schema.json).

---

## Output

**File:** `01-market-discovery.json`

Structure per niche:
```json
{
  "niche_id": "N01",
  "niche_name": "string",
  "status": "ACTIVE | BORDERLINE",
  "signal_sources": ["gumroad", "kindle", "etsy", "tiktok", "instagram", "reddit"],
  "demand_signals": {
    "gumroad": { "product_count": 0, "avg_sales_comparable": 0, "price_range": "" },
    "kindle": { "bsr_range": "", "review_velocity": "", "category": "" },
    "etsy": { "product_count": 0, "avg_sales": 0, "price_range": "" },
    "tiktok": { "hashtag": "", "views_30d": 0, "growth_rate_percent": 0 },
    "instagram": { "hashtag": "", "post_count": 0, "avg_engagement": 0 },
    "reddit": { "pain_posts_count": 0, "top_pain_verbatim": "", "subreddit": "", "url": "" }
  },
  "preliminary_uvz": [
    { "uvz_label": "string", "signal_anchor": "string", "source_url": "string" }
  ],
  "eliminated_niches_log": []
}
```

---

## Quality Check Before Delivering Output

- [ ] All 6 data sources attempted and logged
- [ ] Blocking Condition evaluated — HALT only if SOURCE 1 AND SOURCE 3 both FAILED
- [ ] Binary filter applied to every cluster
- [ ] Exactly 15 niches in output (adjust methodology if needed, document adjustment)
- [ ] Every niche has signals from minimum 2 sources
- [ ] Every preliminary UVZ references a real signal with source
- [ ] No invented data — [DATA MISSING] tag used where applicable
- [ ] Eliminated niches logged with reason code
- [ ] Output written to `01-market-discovery.json`
- [ ] No scoring, no ranking performed (that is Skill 02's job)
