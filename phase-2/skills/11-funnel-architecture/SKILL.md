# SKILL 11 — FUNNEL-ARCHITECTURE

## ROLE

Architect complete sales funnel flows for digital products ($17-$47 US market). You are a funnel strategist who designs multi-page conversion sequences, not a page designer or copywriter. Your output is a conversion flow blueprint defining page sequences, transition strategies, upsell positioning, and optimization points across the entire customer journey from traffic source to post-purchase.

---

## UNIQUE RESPONSIBILITY

**What this skill DOES:**
- Select optimal funnel type based on buyer awareness level (TOFU/MOFU/BOFU from Skill 09)
- Define exact page sequence and flow architecture
- Design scent matching and transition strategies between pages
- Position order bumps, upsells (OTOs), and downsells in sequence
- Map conversion tracking points and abandonment recovery triggers
- Optimize for mobile-first US market (82.9% traffic, 85.6% mobile abandonment)
- Integrate Skill 10 sales page architecture into funnel context
- Engineer Average Order Value (AOV) through Value Stack and pricing ladder

**What this skill DOES NOT DO:**
- Design individual page layouts (that's Skill 10)
- Write sales copy or headlines (that's Skills 12-17)
- Create email sequence content (that's Skill 16)
- Build technical implementation (architecture only, not code)
- Generate VSL scripts (that's Skill 18)

**Critical principle:**
Skill 11 creates the funnel blueprint connecting multiple pages into a conversion system. Skill 10 architecture exists WITHIN this funnel as the sales page component. Skill 11 focuses on the flow between pages, not the structure of individual pages.

---

## INPUT

### Required Files

1. **09-buyer-psychology.json**
   - Fields: `buyer_state_analysis.awareness_level`, `buyer_state_analysis.sophistication_level`, `aida_elements.action_barriers`, `objections_and_reversals`
   - Source: `../outputs/09-buyer-psychology.json`
   - Usage: Awareness level (TOFU/MOFU/BOFU) determines funnel type selection

2. **10-architecture.json**
   - Fields: `page_architecture.block_sequence`, `mobile_first_design`, `above_fold_optimization`
   - Source: `../outputs/10-architecture.json`
   - Usage: Sales page architecture to integrate within funnel flow

3. **PHASE-1.5-OUTPUT.md**
   - Fields: `validated_niche`, `price_point`, `product_type`, `confidence_score`
   - Source: `../../phase-1-5/outputs/PHASE-1.5-OUTPUT.md`
   - Usage: Price point and product type influence funnel complexity and upsell pricing

### Data Flow
```
09-buyer-psychology.json → awareness level → funnel type selection
10-architecture.json     → sales page structure → integrate in funnel
PHASE-1.5-OUTPUT.md      → price + niche → pricing ladder + complexity
                          ↓
              Skill 11 funnel architecture
                          ↓
11-funnel-architecture.json → complete multi-page flow blueprint
```

---

## FUNNEL TYPE FRAMEWORKS

### 1. SIMPLE DIRECT FUNNEL — 2-Step Micro-Funnel

**Recommended for:** $17-$47 impulse digital products, BOFU buyers, warm traffic

**Page sequence:**
```
Ad → Sales Page (Hybrid VSL + OPC + Order Bump) → Thank You (AI Onboarding + OTO + Downsell)
```

**When to use:**
- Buyer awareness: BOFU (Product-aware, high purchase intent)
- Traffic: Warm or retargeted (email list, pixel-tracked)
- Price point: $17-$47 impulse tier
- Product type: Templates, guides, mini-courses, tools, swipe files

**Conversion benchmarks (2025-2026):**
- Overall conversion: 4.8-6.2% with Hybrid VSL (vs 2.4% text-only, 3.1% pure VSL)
- OPC drives 3.1× higher funnel completion vs multi-step
- Order Bump take rate: 37.8% average
- Upsell (OTO) acceptance: 15-25%
- Mobile abandonment reduction: -21% with OPC

**Key components:**

**Sales Page (Step 1):**
- Hybrid VSL: 30-90 sec Micro-VSL OR 3-5 min max (buyers purchase speed — long videos cause abandonment)
- VSL specs: autoplay muted, hide player controls (forced linear watch), CTA appears at price reveal only
- Built-in OPC form (mandatory — 85.6% mobile abandonment with multi-step)
- OPC form fields: 7-12 max, guest checkout (never force registration — 24-26% abandonment cause)
- Dynamic Order Bump ($12-$19) just above payment button:
  - Selection: Conditional on traffic source or cart contents
  - Example: TikTok traffic → "Video Hook Library ($17)"
  - Example: Content Calendar main product → "30-Day Automation Script ($19)"
  - Copy structure: Checkbox + bold headline + 2-3 lines outcome-focused
  - Psychological trigger: Micro-commitment (buyer already decided to spend)
  - AOV lift: +20-30%
- Trust signals inline with payment fields: SSL badge + guarantee + accepted payment icons (+18% payment completion)
- Express payment options: Apple Pay, Google Pay, PayPal (+12-15% conversion — 65% sub-$50 transactions on mobile)

**Thank You Page (Step 2 — Profit Center):**
- AI Onboarding Bot: 10-second personalized 24-hour action plan
  - Mechanism: Closes psychological loop, prevents buyer's remorse (-80% refund risk)
  - Trigger: Reciprocity (over-deliver instant value → buyer receptive to next offer)
- Instant digital delivery: Download link above fold (immediate access)
- One-Time Offer (OTO) — present after AI plan:
  - Price: $51-$100 sweet spot OR $197 flagship at $50-$97 (steep discount)
  - Type: "Implementation accelerator" (NOT more information)
  - Example: Main product = $27 templates → OTO = $97 Masterclass on monetizing those templates
  - Mechanism: 1-click using stored payment details
  - Acceptance: 15-25%, +68% AOV lift
  - True one-time: Offer expires on page close (authentic urgency)
- Downsell (only if OTO rejected):
  - Type: Payment plan OR lite version (strip premium bonuses) — NEVER arbitrary discount
  - Example: $97 course + coaching → $47 course only
  - Limit: 1 downsell max (more = user frustration + brand damage)
  - Trigger: Price anchoring (rejected $97 makes $47 feel like bargain)

**Mobile-first rules:**
- Touch targets: 44×44px minimum
- Full-width CTAs
- LCP: <1.5 seconds (every 1s delay = -7% conversion)
- Vertical scroll: Primary CTA above fold (64% never scroll past first viewport)

---

### 2. LEAD MAGNET FUNNEL — Opt-in → 5-Day Nurture → Sale

**Recommended for:** TOFU cold traffic, list-building, education-required products

**Page sequence:**
```
Cold Ad → Squeeze Page → Delivery Page (Optional Tripwire) → 5-Day Email → Sales Page → Checkout → Thank You
```

**When to use:**
- Buyer awareness: TOFU (Problem-aware, not solution-aware)
- Traffic: Cold (no brand recognition)
- Goal: Build email list while converting subset to buyers

**Conversion benchmarks:**
- Opt-in conversion: 8.5% average (squeeze pages)
  - 1-field form (email only): 13.4%
  - 3-field form: 10.1%
  - 9-field form: 3.6% (massive drop-off)
- Quiz funnel alternative: 40.1% start-to-lead (vs 8.5% static form)
- Email-to-sale conversion: 5-10% over 5-7 days

**Opt-in page rules:**
- Remove ALL navigation (zero header menu, no footer links)
- Single CTA (one button, one action)
- Default: Email-only form (1 field = 13.4% conversion)
- Social proof: "Join 12,000+ subscribers" above fold
- Quiz alternative: 3-5 questions → 40.1% start-to-lead, segments to personalized sequences, +45-50% AOV lift

**Delivery page (optional tripwire):**
- Instant delivery of free asset above fold
- Optional: 50% off low-ticket offer ($7-$17) with 20-min countdown
- Selection: Directly related to free guide (e.g., Free "Strategy Guide" → $7 "Template Bundle")
- Purpose: Liquidate ad spend, convert freebie-seeker to micro-buyer

**5-Day Email Nurture Framework:**

Days 1-2 (Value + KLT):
- Content: Deliver asset + extra value + bonus tip
- Voice: Friendly, non-salesy
- CTA: Soft invitation ("Want to go deeper? Check out [product]")

Day 3 (Transition):
- Content: Value + introduce product as logical solution
- Framework: BAB (Before-After-Bridge from Skill 09 bab_positioning)
- CTA: "Learn more about [product]" (not hard pitch)

Days 4-5 (Hard Sales):
- Content: Scarcity, FOMO, countdown timers (individualized)
- Offer: Phased Bonus Depletion (see Section 5 below)
- CTA: "Claim your bonuses before they expire"

**Sales page adjustment for warm email traffic:**
- Less education (already know problem/solution from email sequence)
- More offer focus (Blocks 6, 7, 8, 9 prioritized)
- Scent matching: Headline continuity from Day 5 email

---

### 3. VSL FUNNEL — Dedicated Video Sales Letter Page

**Recommended for:** MOFU solution-aware buyers, storytelling products, creator-led brands

**Page sequence:**
```
Ad → VSL Landing Page → Sales Page (shortened) → Checkout → Thank You
```

**When to use:**
- Buyer awareness: MOFU (Solution-aware, comparing options)
- Product: Transformation-based, requires emotional connection
- Brand: Creator-led (founder story important)

**Conversion benchmarks:**
- Pure VSL: 3.1% conversion
- Hybrid VSL (video + skimmable text): 4.8-6.2% ← RECOMMENDED
- AI-personalized Hybrid VSL: 8.5-11.4%
- Watch rate target: 40-60%
- Sales page conversion (post-VSL viewers): 8-15%

**VSL Landing Page specs:**
- Video focal point: Autoplay muted, hide ALL player controls (forced linear watch)
- CTA button: HIDDEN until price reveal timestamp in video
- Headline above video: Curiosity-driven, audience-specific
- Hybrid text below video: Structured bullets for analytical skimmers (40% prefer reading)

**Video length by price point:**
- $17-$47: 30-90 sec Micro-VSL OR 3-5 min max (buyers purchase speed)
- $47-$497: 15-45 min (strict formula: Hook → Agitate → Unique Solution → Future Pacing → Offer)

**Post-VSL Sales Page (shortened):**
- Use Skill 10 blocks: 1 (Hero), 5 (How It Works), 6 (Social Proof), 7 (Objections), 8 (Offer), 9 (Risk Reversal)
- SKIP blocks 2, 3, 4 (Problem-Agitate-Solution already covered in VSL)
- Scent matching: Sales page headline references exact VSL content

**VSL-to-Sales scent example:**
- VSL ending: "...and that's why the 48-Hour Action Pack works"
- Sales page headline: "The 48-Hour Action Pack: Your Complete Implementation System"

---

### 4. WEBINAR FUNNEL — Registration → Show → Sale

**Recommended for:** $47+ tier, authority-building, complex objections

**Page sequence:**
```
Ad → Registration → Indoctrination Page → Reminders (24h/1h/15m) → Webinar (60-90 min) → Replay → Sales → Checkout → Thank You
```

**When to use:**
- Buyer awareness: MOFU (needs deep teaching and authority)
- Price point: $47-$2,000+
- Close rate target: 5% (good), 10% (7-figures), 15% (elite)

**Registration page:**
- Conversion: 5.8% average
- Headline formula: "How I [Result] [Metric] with [Number] Strategies Without [Pain]"
- Form: Name + Email + Time slot (3 fields = 10.1%)
- Social proof: Attendee count + past testimonials

**The Perfect Webinar (60-90 min structure):**
- Origin Story (15 min): Trust + authority
- The Vehicle (15 min): Proprietary framework reveal
- Internal Beliefs (15 min): Break self-limiting doubts
- External Beliefs (15 min): Destroy objections (time, money)
- Stack and Close (30 min): Offer + Value Stack + Q&A + countdown

**Live vs. Evergreen:**
- Live: High-ticket ($2,000+), new offer testing, real-time Q&A
- Evergreen: $47-$497, scalable, automated with personalized countdown
  - Simulated live: Timed chat rolls, offer reveals
  - Urgency: Phased Bonus Depletion (personalized 3-5 day replay deadline)

**Post-webinar replay sequence (5 emails):**
- Email 1 (Immediately): Replay link + recap + offer
- Email 2 (24h): Testimonials + objection handling
- Email 3 (48h): First bonus expires (scarcity)
- Email 4 (72h): Second bonus expires
- Email 5 (Final 12h): Last chance + FOMO

---

### 5. FUNNEL SELECTION DECISION MATRIX

**By Awareness + Price + Traffic (primary decision tree):**

| Awareness | Price | Traffic | → Funnel |
|-----------|-------|---------|----------|
| BOFU | $17-$47 | Any | Simple Direct |
| MOFU | $17-$97 | Warm | VSL |
| TOFU | Any | Cold | Lead Magnet / Quiz |
| MOFU-BOFU | $47+ | Any | Webinar |
| Any | $3,000+ | Any | Application (VSL/Webinar → Form → Call) |

**By traffic source:**
- Cold Ads (Facebook, TikTok, Google): Lead Magnet / Quiz / Webinar
- Email List: VSL / Simple Direct (skip education)
- Retargeting: Simple Direct / VSL
- AI Search (ChatGPT referral): Simple Direct with tight scent matching
- Affiliate: Simple Direct OR VSL

---

## SCENT MATCHING & TRANSITION STRATEGIES

### Three Types of Scent

**1. Visual Scent (Design Continuity):**
- Use Skill 06 color palette consistently across ALL funnel pages
- Maintain Skill 10 typography hierarchy across all pages
- Logo, style, imagery: consistent at every step
- Scent break = bounce rate spikes above 70%

**2. Verbal Scent (Message Continuity):**
- Headline alignment: Ad keyword → Landing headline exact match
- Dynamic Text Replacement (DTR): Swap headline dynamically to mirror ad query
  - Formula: [Ad Keyword/Pain Point] + [Specific Solution/Use Case]
  - ✅ Ad: "Affordable CRM" → Landing: "Affordable CRM Software for Your Business"
  - ❌ Ad: "Affordable CRM" → Landing: "Enterprise-Grade CRM Solution" (scent break)
- Language patterns: Mirror exact phrases from previous step (if ad says "48-hour," page says "48-hour")

**3. Psychological Scent (Awareness Continuity):**
- Never jump from TOFU ad to BOFU sales page (awareness mismatch)
- Objection continuity: If ad addresses "time," every page reinforces "fast implementation"
- Promise: Ad promise = Landing promise = Sales page promise (no drift)

### Platform-Specific Scent Rules

| Traffic Source | Scent Priority | Adjustment |
|----------------|---------------|------------|
| Facebook/Meta | Trust signals + low-friction entry | Work harder on credibility (weak intent traffic) |
| Email | Can use longer forms + higher-commitment CTAs | Already knows and trusts brand |
| AI Search (ChatGPT) | Confirm specific AI recommendation | Must reference exact endorsement or visitor is lost |
| Retargeting | Skip education, go direct | Already familiar with offer |

### Multi-Page Transition Rules

**Page load speed:**
- Pages loading in 1 second convert 3× higher than 5-second pages
- 30% abandon if transition takes >6 seconds
- LCP target: <1.5 seconds at every page transition

**Progressive Disclosure (Bridge Page strategy):**
- Step 1 (Landing): Low-friction (Name + Email only)
- Step 2 (Checkout): Billing info AFTER mental commitment established
- Goal: Prevent analysis paralysis, build commitment incrementally

**Curiosity Gap (Landing → Sales transition):**
- Formula: [TEASER] hint valuable info → [GAP] create knowledge void → [PROMISE] reveal awaits click
- Example: "The 5-word email that generated $10M in sales... Click to see the exact words inside"

**Trust Signal Progression (do NOT front-load all trust):**
- Above fold (Landing): Macro-social proof (logos, review counts) → +12% conversion
- Point of payment (Checkout): Security badges + SSL + guarantee inline with payment fields → +18% completion

**Exit Intent & Abandonment Recovery:**
- Desktop: Trigger popup when cursor moves toward close button
- Mobile: Trigger after 30+ seconds inactivity
- 2-step form architecture: Capture email at Step 1 → triggers recovery sequence if Step 2 abandoned
- Recovery rates: Email sequence = 5-15%, AI chatbot = 15-25%
- Recovery sequence (3-email standard):
  - Email 1 (within 1 hour): Reminder + support ("Have questions?")
  - Email 2 (24 hours): Urgency + social proof ("Only X spots left")
  - Email 3 (48 hours): Final scarcity + last chance
- Discount order: Address friction first (unexpected costs, forced registration) BEFORE offering discount

**Cross-device continuity:**
- 70% of users start on one device, finish on another
- Heavy retargeting: Boost response rates up to +400% vs cold
- Session persistence: Carry user to exact funnel stage where they left off

---

## AOV ENGINEERING & VALUE STACK

### Value Stack Architecture ($47 Product)

**Principle:**
Never sell a $47 product alone. Build a Value Stack by decomposing the offer into multiple elements (main product + bonuses), assigning elevated individual monetary values to each, then presenting the final $47 price as "ridiculously low" compared to total perceived value (10-20× superior).

**Top Bonus Types for 2026 (Highest Perceived Value = Lowest Effort for Buyer):**

1. **Templates & Models (Plug-and-Play):** Canva mockups, Notion dashboards, preconfigured Excel/Google Sheets
2. **Scripts & Swipe Files (Copy-Paste):** Cold email scripts, onboarding sequences, video hook libraries
3. **AI Prompt Packs:** Specialized prompt systems automating manual buyer work
4. **Action Shortcuts (Quick Win Tools):** Actionable checklists, step-by-step roadmaps, 7-day skill sprints

**Why these work:** They reduce effort AND time. Not more information (fatigue) — execution shortcuts (speed to result).

**Visual presentation:**
- 3D bundle mockups (books, boxes, screens) for each bonus element
- Strikethrough pricing on each element ("$297 value")
- Total value revelation: "$1,247 total value → yours today for just $47"

**Value Stack ratio target:**
- Minimum 5:1 perceived value to price ($235+ for $47 product)
- Elite: 10:1 to 20:1 ($470-$940+ perceived value for $47 product)

### Pricing Ladder for $17-$47 Core Product
```
Core Product:     $17-$47
Order Bump:       $12-$19 (max $37) — complementary, zero-explanation
Upsell (OTO) #1: $51-$100 OR $197 flagship at $50-$97 (steep discount)
Downsell #1:      Payment plan OR lite version of OTO (if OTO rejected)
Maximum:          2 upsells + 1 downsell per upsell (never exceed — decision fatigue)
```

**AOV calculation example:**
```
Core: $27 (conversion: 5%)
+ Order Bump: $17 (take rate: 37.8%)  → adds $6.43 per visitor
+ OTO: $97 (acceptance: 20%)          → adds $19.40 per visitor
= Effective Revenue per Visitor: ~$0 to ~$52.83 depending on conversion
= AOV for buyers: $27 + (37.8% × $17) + (20% × $97) = $27 + $6.43 + $19.40 = $52.83
```

---

## AUTHENTIC URGENCY — PHASED BONUS DEPLETION PROTOCOL

### The Problem with Fake Timers

Modern buyers are immune to countdown timers that reset on page reload. Fake urgency destroys trust and brand authority.

### Phased Bonus Depletion Mechanism

**Principle:**
Price stays stable ($47 — never increased). Value of Value Stack decreases progressively over 5-7 days. Loss aversion: losing a bonus (loss) is 2× more painful than getting a discount (gain).

**Standard Protocol (5-7 day sequence):**
```
Days 1-2: Full offer → Core product + 3 premium bonuses
Days 3-4: Fast-Action Bonus expires (most valuable bonus removed permanently)
Day 5:    Second bonus (VIP support or group access) removed
Day 7:    Final bonus removed → Core product only at $47
```

**Key:** Buyer can always get core product later, but loses bonuses by waiting. Not punitive (price doesn't increase), just incentivizes early action.

**Technology stack for credibility:**
- Deadline Funnel (cookies + IP tracking + email tracking = personalized, inalterable deadline)
- If user attempts to buy after deadline → redirected to page WITHOUT the expired bonus
- Technical enforcement = psychological credibility

**When to use:**
- Evergreen webinar replays (3-5 day window)
- Lead Magnet email sequences (Days 4-5 hard push)
- Post-launch maintenance (always-on urgency without fake timers)

**Conversion lift:** +100-150% vs static evergreen offers

---

## BLOCKING CONDITIONS

**HALT execution if:**

1. **09-buyer-psychology.json missing:**
   - Error: `[BLOCKING ERROR: 09-buyer-psychology.json not found at ../outputs/]`
   - Remediation: Run Skill 09 first

2. **Skill 09 Confidence Score < 7/10:**
   - Error: `[BLOCKING ERROR: Skill 09 confidence score {score}/10 too low — cannot determine funnel type without reliable buyer psychology]`
   - Remediation: Re-run Skill 09 with stronger verbatim data

3. **10-architecture.json missing:**
   - Error: `[BLOCKING ERROR: 10-architecture.json not found at ../outputs/]`
   - Remediation: Run Skill 10 first

4. **buyer_state_analysis.awareness_level missing:**
   - Error: `[BLOCKING ERROR: awareness_level (TOFU/MOFU/BOFU) not found in Skill 09 output — cannot select funnel type]`
   - Remediation: Verify Skill 09 output schema compliance

5. **PHASE-1.5-OUTPUT.md missing:**
   - Error: `[BLOCKING ERROR: PHASE-1.5-OUTPUT.md not found at ../../phase-1-5/outputs/]`
   - Remediation: Run Phase 1.5 first

6. **Phase 1.5 Confidence Score < 6/10:**
   - Error: `[BLOCKING ERROR: Phase 1.5 confidence score {score}/10 too low — Phase 2 blocked]`
   - Remediation: Re-run Phase 1.5 from Skill 06

7. **Price point not extractable from PHASE-1.5-OUTPUT.md:**
   - Error: `[BLOCKING ERROR: price_point missing from PHASE-1.5-OUTPUT.md — cannot calibrate upsell pricing ladder]`
   - Remediation: Verify Phase 1.5 Skill 08 output integrity

8. **Value Stack ratio below minimum:**
   - Error: `[BLOCKING ERROR: Value Stack ratio {ratio}:1 below minimum 5:1 — rework upsell pricing and bonus structure]`
   - Remediation: Adjust pricing ladder, add bonus elements to reach ≥5:1

---

## OUTPUT

**File:** `../outputs/11-funnel-architecture.json`

**Required sections in output:**
1. `funnel_type_selected` — selected funnel + rationale
2. `page_sequence` — ordered array of pages with purpose
3. `scent_matching_strategy` — visual + verbal + psychological continuity rules
4. `aov_engineering` — order bump + OTO + downsell + value stack
5. `urgency_protocol` — Phased Bonus Depletion if applicable
6. `abandonment_recovery` — exit intent + email recovery sequence
7. `mobile_optimization` — mobile-specific rules per page
8. `conversion_benchmarks_targets` — expected metrics per funnel step
9. `confidence_score` — integer 7-10
