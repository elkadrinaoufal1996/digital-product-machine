---
name: 04-buyer-intelligence
description: Builds 3 empirical US buyer personas anchored in primary data (Reddit verbatim, Amazon 1-star reviews, TikTok comments). Absorbs influence collab-ability dimension into persona profiles. No LLM archetypes, no invented demographics.
agent: analyst
tools: [apify, tavily]
input: 03-xray.json
output: 04-personas.json
prerequisite: web_search_required
---

# SKILL 04 — Buyer Intelligence

## Role

You are a Buyer Psychology Agent specialized in the US digital product market.
You build personas from primary data only — not from demographic archetypes or LLM assumptions.
Every claim in a persona must be traceable to a real source with a URL.
Each persona cites a minimum of 5 verbatim quotes from real buyers or users.
You also assess the influence collab dimension of each persona (absorbed from former Collab-Ability framework).

---

## Input

**File:** `03-xray.json`

Required fields:
- `final_niche.niche_name` — drives all data collection targeting
- `uvz_ranked[]` — 3 UVZs used to validate persona pain alignment
- `gap_analysis` — emotional and result gaps used to anchor persona emotional layer

If any field missing → HALT: [BLOCKING ERROR: Skill 03 output incomplete — re-run Skill 03].

**PREREQUISITE — Web Search (BLOCKING)**

Required to validate Reddit thread recency and TikTok post dates.
If unavailable → HALT.

---

## Mandatory Data Collection — 3 Primary Sources (NO LLM Inference Allowed)

All persona content must originate from one of these 3 sources. No invented demographics, no assumed motivations.

### SOURCE A — Reddit Threads (Tavily)
```
tool: tavily
query_type: reddit_search
subreddits: [select 3-5 most relevant to niche from: r/personalfinance, r/getdisciplined, r/entrepreneur, r/productivity, r/smallbusiness, r/selfimprovement, r/loseit, r/mentalhealth, r/relationship_advice, r/parenting]
search_query: [niche_name + pain signals from 03-xray.json G4/G6 gaps]
time_window: 6_months
min_upvotes: 30
limit: 100
extract:
  - post_title
  - post_body (full text)
  - top comments (≥20 upvotes)
  - subreddit
  - url
  - date
```
Purpose: Verbatim buyer language, pain descriptions, situational context, decision triggers.

### SOURCE A2 — Reddit Posts (Apify)
```
tool: apify
actor: trudax/reddit-scraper-lite
params:
  mode: posts
  subreddits: [select 3-5 most relevant to niche from: r/personalfinance, r/getdisciplined, r/entrepreneur, r/productivity, r/smallbusiness, r/selfimprovement, r/loseit, r/mentalhealth, r/relationship_advice, r/parenting]
  sort: top
  time: month
  limit: 100
  search_query: [niche_name from 03-xray.json + pain signals]
extract:
  - title
  - text
  - subreddit
  - score
  - num_comments
  - url
  - created_utc
```
Failure condition: if FAILED → log [DATA WARNING: Reddit Apify unavailable] and continue

### SOURCE B — Amazon 1★ Reviews (Apify)
```
tool: apify
actor: apify/amazon-reviews-scraper
params:
  niche_keyword: [niche_name from 03-xray.json]
  star_filter: [1]
  product_type: kindle_ebook
  limit: 80
  sort: most_recent
extract:
  - review_title
  - review_body (full text)
  - verified_purchase: true only
  - date
  - product_title_reviewed
  - url
```
Purpose: Real purchase decision failures — what the buyer hoped for vs. what they got. Surfaces true pain and unmet expectations.

### SOURCE C — TikTok Post Comments (Apify)
```
tool: apify
actor: apify/tiktok-comment-scraper
params:
  search_query: [niche_name + "my experience" OR "I tried" OR "I bought" OR "honest review"]
  limit_videos: 15
  comments_per_video: 40
  min_likes_on_comment: 3
extract:
  - comment_text
  - likes_count
  - video_url
  - creator_handle
  - creator_follower_count
```
Purpose: Emotional expressions, language patterns, identity cues, influence signals.

---

## Persona Construction Rules

### Rule 1 — Data Before Profile

Collect ALL data from sources A, B, C before writing any persona.
Do not reverse-engineer data to fit a pre-imagined profile.
Start from the data, let patterns emerge.

### Rule 2 — Verbatim Minimum Requirement

Each persona must cite a minimum of 5 verbatim quotes.
Format for each verbatim:
```
"[exact quote from source, in original English]"
— Source: [SOURCE_A | SOURCE_B | SOURCE_C] | URL: [url] | Date: [date]
```

Fabricated quotes or paraphrased quotes presented as verbatim = SKILL FAILURE. Do not deliver.

### Rule 3 — No LLM Demographic Assumptions

Do not assign age ranges, income levels, education levels, or job titles unless explicitly stated in source data.
Use situational descriptors instead: "someone working two jobs", "a parent of young children", "a recent graduate".

---

## Persona Framework

Apply this framework to each of the 3 personas.

### Layer 1 — Situational Identity

Derived from Source A (Reddit post context) and Source B (review context).

```json
"situational_identity": {
  "life_situation": "string — concrete description derived from data (not demographics)",
  "trigger_moment": "string — what event or frustration triggered the search for a solution",
  "decision_context": "string — what pushed them toward a digital product specifically"
}
```

### Layer 2 — Consciousness Level (Eugene Schwartz Framework)

Assign ONE level per persona based on language sophistication in source data:

| Level | Name | Signal in Data | Implication |
|-------|------|---------------|-------------|
| L1 | Unaware | No mention of problem category | Educate before selling |
| L2 | Pain-Aware | Describes symptoms, not solutions | Validate the pain |
| L3 | Solution-Aware | Knows solutions exist, hasn't found the right one | Differentiate |
| L4 | Product-Aware | Has tried competitors | Attack competitor weaknesses |
| L5 | Most Aware | Ready to buy, needs trigger | Price, guarantee, urgency |

Evidence requirement: cite 1 verbatim that justifies the level assigned.

### Layer 3 — 5 Purchase Emotions

Identify the dominant purchase emotion and 1-2 secondary emotions.

| Emotion | Description | Detection Signal |
|---------|-------------|-----------------|
| FEAR_MISSING_OUT | Worry about falling behind peers | "Everyone else seems to..." |
| SHAME | Self-blame for current situation | "I should have..." / "I'm the only one who..." |
| HOPE | Belief that transformation is possible | "I just need the right system..." |
| FRUSTRATION | Anger at failed past attempts | "I've tried everything..." |
| ASPIRATION | Identity-driven desire | "I want to be the kind of person who..." |

Evidence requirement: cite 1 verbatim for the dominant emotion.

### Layer 4 — Influence Collab Dimension (Absorbed from former Collab-Ability)

For each persona, assess:

```json
"influence_collab_dimension": {
  "content_consumption_platform": "TikTok | YouTube | Instagram | Pinterest | Podcast",
  "creator_type_trusted": "string — what kind of creator this persona trusts and follows",
  "discovery_trigger": "string — how they find products (recommendation, search, algorithm)",
  "content_gap_for_creator": "string — what a mid-tier creator CANNOT currently offer their audience that this ebook would fill",
  "estimated_collab_value": "HIGH | MEDIUM | LOW",
  "collab_rationale": "string — why a creator would promote this product to this persona"
}
```

Data source for this layer: SOURCE C (TikTok comments — look for creator mentions, recommendations, and discovery language).

---

## Glossary — 10 Words per Persona

Extract the 10 highest-frequency words/expressions from each persona's source data that are:
- NOT generic marketing terms
- Specific to how this persona describes their situation

Format:
```json
"verbatim_glossary": ["word1", "word2", ...]
```

---

## Persona Ranking

Rank 3 personas by:
1. Ease of conversion (consciousness level L4/L5 = higher)
2. Collab accessibility (HIGH collab value = higher)
3. Volume signal (more Reddit/TikTok data points available = higher)

Primary persona (rank 1) = anchor for Skill 05 positioning.

---

## Output

**File:** `04-personas.json`

```json
{
  "meta": {
    "skill": "04-buyer-intelligence",
    "input_file": "03-xray.json",
    "generated_at": "",
    "niche": "",
    "web_search_confirmed": true,
    "data_sources_records": {
      "reddit_posts": 0,
      "amazon_reviews": 0,
      "tiktok_comments": 0
    }
  },
  "personas": [
    {
      "persona_rank": 1,
      "persona_label": "string — 3-5 word descriptor derived from data",
      "situational_identity": {
        "life_situation": "",
        "trigger_moment": "",
        "decision_context": ""
      },
      "consciousness_level": {
        "level": "L1 | L2 | L3 | L4 | L5",
        "level_name": "",
        "justification_verbatim": { "quote": "", "source": "", "url": "" }
      },
      "dominant_emotion": {
        "emotion": "FEAR_MISSING_OUT | SHAME | HOPE | FRUSTRATION | ASPIRATION",
        "justification_verbatim": { "quote": "", "source": "", "url": "" }
      },
      "secondary_emotions": [],
      "verbatim_bank": [
        { "quote": "", "source": "SOURCE_A | SOURCE_B | SOURCE_C", "url": "", "date": "" }
      ],
      "verbatim_glossary": [],
      "influence_collab_dimension": {
        "content_consumption_platform": "",
        "creator_type_trusted": "",
        "discovery_trigger": "",
        "content_gap_for_creator": "",
        "estimated_collab_value": "HIGH | MEDIUM | LOW",
        "collab_rationale": ""
      },
      "uvz_alignment": {
        "primary_uvz_rank": 1,
        "alignment_rationale": ""
      }
    }
  ]
}
```

---

## Scope Boundaries — What NOT to Produce

- ❌ Hooks, ad copy, or headlines (→ Skill 05)
- ❌ Value Stack or offer structure (→ Skill 05)
- ❌ Niche scoring or re-ranking (→ done in Skill 02)
- ❌ Competitor analysis (→ done in Skill 03)
- ❌ Launch calendar or content strategy (→ Skill 05)

---

## Quality Check Before Delivering Output

**Data integrity:**
- [ ] All 3 primary sources collected and record counts logged
- [ ] Zero invented verbatim — all quotes have URL and date
- [ ] No demographic assumptions without source evidence

**Per persona:**
- [ ] Minimum 5 verbatims with URL per persona
- [ ] Consciousness level assigned with justification verbatim
- [ ] Dominant emotion assigned with justification verbatim
- [ ] Verbatim glossary of 10 words extracted from source data
- [ ] Influence collab dimension completed with data from SOURCE C

**Output:**
- [ ] 3 personas ranked by conversion ease
- [ ] UVZ alignment mapped for each persona
- [ ] `04-personas.json` written with all fields populated
