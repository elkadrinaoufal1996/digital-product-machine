# Gap Analysis Framework — Skill 03

Reference for identifying and validating the 6 gap types in competitor analysis.
Used exclusively by Skill 03. No scoring, no personas, no hooks produced here.

---

## The 6 Gap Types

### G1 — Gap Promesse (Promise Gap)
**What it is:** All top competitors make the same promise to the same audience using the same framing.

**How to detect:**
- Scrape top 5 competitor headlines from Firecrawl
- If 3+ competitors use identical outcome language ("get rich", "lose weight fast", "be more productive") → Gap confirmed
- If each product frames the same outcome differently → Gap absent

**Exploitation angle:** Enter with a promise that reframes the SAME outcome for a specific sub-audience or in a counter-intuitive way.

---

### G2 — Gap Audience (Audience Gap)
**What it is:** Existing products all target the same demographic, leaving an adjacent segment unaddressed.

**How to detect:**
- Read "Who this is for" sections from Firecrawl-scraped competitor pages
- Map the demographics and life situations described
- Identify who is NOT described

**Exploitation angle:** Build specifically for the excluded segment (e.g., beginners ignored by advanced products, working moms ignored by career-focused products).

---

### G3 — Gap Format (Format Gap)
**What it is:** The market offers ebooks but no templates, or courses but no quick-start guides, leaving buyers without their preferred format.

**How to detect:**
- Catalog formats of top 10 competitor products (Gumroad + Etsy)
- Identify format categories absent from top sellers
- Cross-reference with TikTok comment requests ("I wish someone made a...")

**Exploitation angle:** Deliver the same transformation in the preferred format of the underserved segment.

---

### G4 — Gap Émotionnel (Emotional Gap)
**What it is:** Competitors address the logical pain but ignore the emotional dimension driving purchase decisions.

**How to detect:**
- Analyze TikTok comments with ≥5 likes in the niche
- Identify recurring emotional language not reflected in any competitor's sales page
- Look for: shame, fear of judgment, identity threats, hope for recognition, desire for belonging

**Exploitation angle:** Lead with the emotional dimension in positioning copy (→ Skill 05 will execute this).

---

### G5 — Gap Influence (Influence Gap)
**What it is:** No solution-oriented mid-tier creator covers this niche effectively, leaving the recommendation channel open.

**How to detect:**
- Web search: "[niche] ebook review" + "[niche] recommendation" on TikTok/YouTube
- Evaluate creator profiles: solution-oriented vs. entertainment-only
- Check if any mid-tier creator (10K-200K) has made product recommendations in this niche

**Note:** Gap Influence detection stops here. Exploitation strategy (collab-ability) is handled in Skill 04.

---

### G6 — Gap Résultat (Result Gap)
**What it is:** Buyers tried existing products and the same promise was not delivered — documented in 1-2★ reviews.

**How to detect:**
- Analyze Apify-scraped 1-2★ Amazon Kindle reviews
- Group complaints by pattern: methodology, clarity, depth, results claimed vs. delivered
- A gap is confirmed if ≥3 reviews cite the same undelivered promise

**Exploitation angle:** Enter with explicit credibility on the exact point where competitors fail. Name the failure in positioning (→ Skill 05).

---

## Evidence Validation Rules

| Status | Minimum Evidence | Action |
|--------|-----------------|--------|
| CONFIRMED | ≥3 independent data points from the designated source | Include in UVZ construction |
| PARTIAL | 1-2 data points | Include with [PARTIAL EVIDENCE] flag |
| ABSENT | 0 data points | Exclude from UVZ construction |

**Source integrity rule:** Evidence must come from the designated source for each gap type. Do not substitute sources (e.g., using Reddit comments to confirm a Promise Gap that should be validated via Firecrawl LP scraping).
