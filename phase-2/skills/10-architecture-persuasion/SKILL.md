# SKILL 10 — ARCHITECTURE-PERSUASION

## ROLE

Design the structural blueprint of a high-converting sales page for digital products ($17-$47 US market). You are a conversion architect, not a copywriter. Your output is a positioning map that defines WHAT goes WHERE and WHY, using proven visual hierarchy and conversion psychology principles.

---

## UNIQUE RESPONSIBILITY

**What this skill DOES:**
- Define 9-block sequential LP structure with exact positioning rules
- Map Skill 09 psychology elements to page architecture
- Apply visual hierarchy rules (Fitt's Law, Proximity Rule, Gaze Cueing)
- Optimize above-the-fold hero section (3-second Blink Test)
- Position Future Pacing content for maximum desire amplification
- Define mobile-first layout rules (Hybrid VSL, OPC, touch-targets)
- Specify typography hierarchy, whitespace ratios, color psychology
- Map reading patterns (F/Z/Layer-Cake/Spotted) to content placement
- Calculate conversion friction points and removal strategies

**What this skill DOES NOT DO:**
- Write actual sales copy (that's Skills 11-17)
- Generate headlines or CTAs (that's Skills 11, 13)
- Create proof content (that's Skill 12)
- Write email sequences (that's Skill 17)
- Design visual mockups (architecture only, not graphic design)

**Critical principle:**
This skill creates the **positioning map** that all other Phase 2 skills follow. Skills 11-17 populate this architecture with content — they do NOT create their own architecture.

---

## INPUT

### Required Files

1. **09-buyer-psychology.json**
   - Fields needed: `lock_and_key`, `pas_sequence`, `aida_elements`, `bab_positioning`, `persuasion_mechanisms`, `objections_and_reversals`, `buyer_state_analysis`
   - Source: `../outputs/09-buyer-psychology.json`
   - Usage: Extract psychology elements to position on page

2. **PHASE-1.5-OUTPUT.md**
   - Fields needed: `validated_niche`, `top_3_uvp`, `brand_voice`
   - Source: `../../phase-1-5/outputs/PHASE-1.5-OUTPUT.md`
   - Usage: Contextual alignment for architecture decisions

3. **00-persuasion-intel.json** (optional)
   - Fields: `competitor_lp_structures`, `hero_patterns`, `proof_placement_examples`
   - Source: `../outputs/00-persuasion-intel.json`
   - Usage: Competitive LP architecture benchmarking

### Data Flow

```
09-buyer-psychology.json  → psychology elements (lock, PAS, AIDA, objections)
PHASE-1.5-OUTPUT.md       → niche + UVP + brand context
00-persuasion-intel.json  → competitor patterns (optional)
          ↓
    Skill 10 architecture design
          ↓
10-architecture.json → used by skills 11-17 as positioning blueprint
```

---

## FRAMEWORKS REFERENCE (NotebookLM Extract)

### 1. 9-BLOCK LANDING PAGE STRUCTURE

**Concept:** High-converting landing pages follow a predictable psychological progression. For digital products ($17-$47 impulse tier), the 9-block sequential structure balances persuasion with frictionless UX.

**The 9 Blocks (Sequential Order):**

**BLOCK 1 — HERO SECTION (Above-the-Fold):**
- **Components:** Callout (audience ID), Hero Headline, Subheadline, Hero Image/VSL, Primary CTA
- **Positioning Rule:** Must pass 3-Second Blink Test (answers: What is this? Why act now? How to act?)
- **Psychology Trigger:** Attention + Credibility (from Skill 09 AIDA attention_triggers)
- **Placement:** Above fold, zero navigation, single primary CTA
- **Visual Weight:** Highest on page (Fitt's Law)

**BLOCK 2 — PROBLEM ARTICULATION (The Bridge):**
- **Components:** Current frustrating reality (PAS Problem from Skill 09)
- **Positioning Rule:** Immediately after hero scroll (first scroll trigger)
- **Psychology Trigger:** Empathy + Identification (Skill 09 lock_and_key emotional_lock)
- **Content Source:** Skill 09 `pas_sequence.problem` + `bab_positioning.before_state`

**BLOCK 3 — AGITATE & AMPLIFY:**
- **Components:** Negative consequences of inaction (PAS Agitate from Skill 09)
- **Positioning Rule:** Follows Problem block, uses Layer-Cake pattern (headers tell story)
- **Psychology Trigger:** Urgency + Loss Aversion (Skill 09 `pas_sequence.agitate`)
- **Design Note:** Use whitespace to separate agitation points (avoid wall of text)

**BLOCK 4 — MECHANISM / SOLUTION:**
- **Components:** Product introduction as logical bridge (PAS Solution + BAB Bridge from Skill 09)
- **Positioning Rule:** Center of page, transition from problem to solution
- **Psychology Trigger:** Hope + Desire (Skill 09 `pas_sequence.solution` + `bab_positioning.bridge_mechanism`)
- **Visual Element:** Product mockup or Hybrid VSL (if not in hero)

**BLOCK 5 — HOW IT WORKS (Feature-to-Benefit):**
- **Components:** 3-step process visualization + benefit bullets
- **Positioning Rule:** F-Pattern layout (bullets on left side)
- **Psychology Trigger:** Clarity + Confidence
- **Design Rule:** Use numbered steps (1-2-3) with icons, benefits not features

**BLOCK 6 — SOCIAL PROOF & CREDIBILITY:**
- **Components:** Testimonials, case studies, client logos, star ratings
- **Positioning Rule:** **PROXIMITY RULE** — place within 2.5cm of next CTA
- **Psychology Trigger:** Trust + Risk Reduction (Skill 09 `persuasion_mechanisms` social_proof)
- **Content Source:** Skill 12 (preuve-confiance) will populate this block
- **Design Rule:** "Gaze cascade" — validation flows into action

**BLOCK 7 — OBJECTION HANDLING (Pre-emptive FAQ):**
- **Components:** Top 3-5 objections addressed proactively (from Skill 09)
- **Positioning Rule:** Before offer reveal, near CTA (reduce late-funnel friction)
- **Psychology Trigger:** Barrier Removal (Skill 09 `objections_and_reversals.objections`)
- **Format:** FAQ accordion or direct Q&A addressing `aida_elements.action_barriers`

**BLOCK 8 — OFFER & VALUE STACK:**
- **Components:** Core product + bonuses visual stack, price anchor, scarcity/urgency
- **Positioning Rule:** After objection handling, before final CTA
- **Psychology Trigger:** Desire Amplification + Scarcity (Skill 09 `persuasion_mechanisms`)
- **Content Source:** Skill 11 (offre-cta) will populate this block
- **Visual Rule:** 3D mockup bundle, total value crossed out next to actual price

**BLOCK 9 — RISK REVERSAL & FINAL CTA:**
- **Components:** Guarantee (from Skill 09 objections_and_reversals.risk_reversal_recommended), Outcome-driven CTA, Benefit clarifier
- **Positioning Rule:** **PROXIMITY RULE** — guarantee within 2.5cm of CTA button
- **Psychology Trigger:** Final Friction Removal + Action
- **CTA Design:** First-person ("Start My..."), solid contrasting color, benefit clarifier below

**Sequential Flow Logic:**
```
Block 1 (Attention) → Block 2 (Problem) → Block 3 (Agitate) → Block 4 (Solution)
→ Block 5 (How) → Block 6 (Proof) → Block 7 (Objections) → Block 8 (Offer) → Block 9 (CTA)
```

**Rationale:** Follows natural buyer psychology progression from Skill 09 AIDA framework.

---

### 2. 3-SECOND BLINK TEST (Above-the-Fold Hero Optimization)

**Concept:** 57% of desktop visitors and 64% of mobile visitors never scroll past the first viewport. The hero section must answer 3 questions in under 3 seconds or bounce probability doubles.

**The 3 Questions:**
1. **What is this?** → Answered by Hero Headline
2. **Why act now?** → Answered by Subheadline or urgency element
3. **How to act?** → Answered by Primary CTA

**Hero Section Must-Haves:**

**Zero Navigation:**
- Remove all top navigation, footer links, external distractions
- Every additional navigation link visible reduces conversion probability by **11%**
- Exception: Legal links (privacy, terms) in tiny footer text

**Single Primary CTA:**
- Pages focused on one primary action convert **1.6× higher** than pages with multiple options
- Secondary CTAs allowed below fold, but hero = one action only

**Trust Anchors:**
- Place macro-proof (client logos, star ratings, "as seen on" badges) immediately below hero headline
- Builds safety in first 2 seconds of page load

**Headline Formulas (from NotebookLM):**

**Cold Traffic Headline:**
```
"How I/We [Result/Multiplier] Our [Metric] with This [Number] Strategy, and Why It Took/Without [Pain]"
```
Example: "How I Built a $12K/Month Digital Product Business with These 5 Templates, and Why It Took Me 48 Hours (Not 6 Months)"

**Direct Response Headline:**
```
[Audience Callout] + [Specific Promise] + [Timeframe]
```
Example: "For Solopreneurs: Launch Your First Digital Product This Weekend"

**Subheadline Structure:**
- **Length:** 10-20 words (converts **14% better** than 1-liners, **22% better** than dense paragraphs)
- **Purpose:** Clarify headline, add specificity, build curiosity
- **Formula:** Expand on promise + add mechanism hint

Example: "The 48-Hour Action Pack gives you 5 plug-and-play templates that eliminate analysis paralysis and get you to your first sale by Monday."

---

### 3. VISUAL HIERARCHY RULES

**Fitt's Law (The "Dead Weight" Rule):**
- An element's visual "weight" (size + contrast) determines attention
- **Primary CTA must have highest visual weight on page**
- **Mistake to avoid:** Non-clickable elements (badges, graphics) with too much visual weight steal thunder from CTA

**The 2.5cm Proximity Rule:**
- Place high-impact trust signals (star ratings, micro-testimonials) within **exact 2.5cm visual orbit** of primary CTA button
- Creates "gaze cascade" — eye flows from validation to action
- **Conversion lift:** +15-34%

**Gaze Cueing (Directional Psychology):**
- Humans subconsciously follow line of sight in images
- **Hedonic/Lifestyle Products:** Use direct eye contact (model looks at camera) to build emotional connection
- **Functional/Problem-Solving Products:** Use averted gaze (model looks at CTA or product) to direct attention
- **Positioning Rule:** If using person image, ensure eyes point toward CTA or headline

**Reading Pattern Alignment:**

**F-Pattern (Text-Heavy Pages):**
- Eyes scan horizontally across top, then vertically down left
- **Rule:** Place core benefits in bulleted lists on **left side** of page
- **Stat:** Users spend **69% time** on left half, **30% time** on right half

**Z-Pattern (Minimal Landing Pages):**
- Eye travels top-left → top-right → diagonal center → bottom-right
- **Rule:** Headline top-left, hero image right, final CTA bottom-right terminus

**Layer-Cake Pattern:**
- Users skip body text, only read headers
- **Rule:** Subheaders must tell complete narrative story on their own
- **Application:** Use in Blocks 3, 5, 7 (Agitate, How It Works, Objections)

**Spotted Pattern:**
- Eyes jump rapidly looking for pop-out data
- **Rule:** Use boxes, high contrast, whitespace for pricing tiers and guarantees

---

### 4. COLOR PSYCHOLOGY & CTA OPTIMIZATION (Brand Palette Integration)

**Brand First Principle:**
Skill 06 (visual-identity) defines the brand color palette. Skill 10 maps buyer psychology to the **existing palette**, selecting the best-fit color that satisfies both brand identity and conversion psychology.

**Color Palette Source:**
- Read from Skill 06 `visual_identity.json`:
  - `primary` (60% usage — dominant brand color)
  - `secondary` (30% usage — supporting brand color)
  - `accent` (10% usage — action/emphasis color)
  - `neutral` (backgrounds, breathing room)
  - `highlight` (micro-accents, badges)

**The Contrast Rule (Highest Priority):**
- Actual color matters less than its **contrast against page palette**
- **High-contrast CTA button:** +9% conversion
- **Solid vs. Gradient:** Solid outperforms gradient/animated by **+4%** (motion distracts from action)

**Buyer Psychology → Palette Mapping:**

**Step 1: Identify Psychology-Ideal Color (from Skill 09):**
- **Red:** Urgency, danger, immediate action → Best for BOFU + scarcity-driven buyers
- **Orange:** Excitement, movement → Best for mid-funnel urgency
- **Green:** Security, trust, "Go" → Best for MOFU solution-aware buyers, risk-averse personas
- **Blue:** Calm, confidence, control → Best for B2B, enterprise, high-ticket
- **Black:** Exclusivity, luxury → Best for premium positioning

**Step 2: Map to Brand Palette:**
- Match psychology-ideal color to **closest palette color** (primary/secondary/accent/highlight)
- Prioritize `accent` color for CTAs (designed for action triggers in 60-30-10 rule)
- Use `primary` or `secondary` if accent doesn't align with psychology
- **Never invent colors outside the Skill 06 palette**

**Step 3: Validate Contrast:**
- Selected CTA color must have **high contrast** against page background (typically `neutral`)
- If contrast insufficient, select next-best palette color with adequate contrast
- Minimum contrast ratio: **4.5:1** (WCAG AA compliance)

**Color Psychology Decision Matrix (Brand Palette Constrained):**

| Buyer State (Skill 09) | Psychology-Ideal Color | Map to Palette | Rationale |
|------------------------|------------------------|----------------|-----------|
| TOFU curiosity-driven | Blue or Green | → `secondary` or `primary` | Trust-building, low-pressure |
| MOFU solution-aware | Green | → `accent` (if green-ish) or `primary` | Security + "safe to try" |
| BOFU urgency/scarcity | Red or Orange | → `accent` (if warm) or `highlight` | Action trigger |
| High sophistication (skeptical) | Blue or Black | → `secondary` or `primary` | Calm confidence, no hype |
| Low sophistication (enthusiastic) | Orange or Red | → `accent` or `highlight` | Energy + excitement |

**Example Mapping (Course Collector Niche):**
```json
Skill 06 Palette:
{
  "primary": "#2ECC71 (green)",
  "secondary": "#3498DB (blue)",
  "accent": "#E74C3C (red-orange)",
  "neutral": "#ECF0F1 (light gray)",
  "highlight": "#F39C12 (orange-yellow)"
}

Skill 09 Buyer State: MOFU, sophistication level 4 (skeptical), dominant objection = "fear of another failed purchase"

Psychology-Ideal Color: Green (security, "safe to try")

Mapping Decision:
- Primary (#2ECC71 green) aligns perfectly with psychology
- Contrast against neutral (#ECF0F1) = adequate
- Selected CTA Color: primary
- Rationale: "MOFU buyers with purchase anxiety respond to security signals. Brand primary green communicates trust + safety. Contrast against neutral background maintains +9% contrast lift."
```

**CTA Button Design Rules (Unchanged):**
- First-person copy: "Start **My** Free Trial" outperforms "Start **Your** Free Trial" (**+31% clicks**)
- Benefit clarifier below button: "Takes 2 minutes. No credit card." (**+9% conversion**)
- Minimum touch-target size: **44×44px** (mobile)
- Padding around text: **8px minimum** (prevent misclicks)
- Solid color only (no gradients — **-4% penalty**)

**Brand Palette Integrity:**
- All page colors (headers, buttons, accents, backgrounds) sourced from Skill 06 palette
- Skill 10 **never invents new colors**
- If palette lacks adequate contrast or psychology-aligned color, note in output but **still select from available palette**
- Palette updates happen in Skill 06, not Skill 10

---

### 5. TYPOGRAPHY HIERARCHY & WHITESPACE RATIOS

**The Golden Scaling Ratio:**
- Maintain consistent relationship between text levels: **1:1.618** (Golden Ratio) or simple **1:2**
- Establishes visual order, reduces cognitive load

**Heading-to-Body Contrast:**
- Increasing contrast from **1.5:1 to 2.25:1** boosts engagement by **+12%** (Airbnb case study)
- **Rule:** Headings must be significantly heavier/larger than body text

**Font Weights (Limit to 3):**
- **H1 (Primary Headers):** Bold (700+ weight)
- **H2 (Subheaders):** Medium (500-600 weight)
- **Body Text:** Regular (400 weight)
- **Never use more than 3 font weights** (optimizes load speed + visual clarity)

**Exact Typography Sizing Matrix:**

**Desktop:**
- **H1:** 32-40px
- **H2:** 24-32px
- **Body Text:** 16-18px (1rem) — **never go below 16px** (comprehension drops sharply)

**Mobile:**
- **H1:** 28-34px
- **H2:** 22-28px
- **Body Text:** 14-16px

**Line Length (Measure):**
- **Desktop:** 45-75 characters per line (sweet spot: **66 characters**)
- **Mobile:** 35-50 characters per line
- **<45 characters:** Feels choppy
- **>75 characters:** Increases "ocular regression" (eye loses place when returning to left margin)

**WCAG Whitespace Formulas (Accessibility + Conversion):**

**Line Height (Leading):** Exactly **1.5× font size**
- Example: 24px line height for 16px text

**Letter Spacing (Tracking):** **0.12× font size**

**Word Spacing:** **0.16× font size**

**Paragraph Spacing:** **0.5× to 1× line height**

**Mobile-Specific Spacing:**
- **Touch Targets:** Minimum **8px padding** around interactive text/CTAs
- **Heading Breathing Room:** Spacing below heading = **2× header's font size**

**The Disconnect Warning:**
- Do NOT use too much whitespace between related elements
- **Example:** Price placed too far from "Add to Cart" button creates cognitive disconnect
- **Rule:** Group related elements tightly within their own whitespace containers

---

### 6. MOBILE-FIRST DESIGN (US Market 2026)

**Context:** **82.9%** of landing page traffic occurs on mobile devices. Pages must be designed **mobile-first**, not just responsively adapted from desktop.

**Mobile Conversion Optimization:**

**Touch-Target Sizing:**
- CTA buttons: **Full-width**, minimum **44×44px** tall
- Interactive text padding: **8px minimum**

**Vertical Scroll Priority:**
- Mobile users favor vertical scrolling
- **Do NOT force horizontal swiping** (like carousels) for critical information

**Load Speed:**
- Target **Largest Contentful Paint (LCP) < 1.5 seconds**
- **Every 1-second delay** = **-7% conversion drop**

**Hybrid VSL Architecture ($17-$47 Products):**

**The Gold Standard (Cold Traffic):**
- **3-5 minute high-impact video** paired with **skimmable text below**
- **Conversion rate: 4.8-6.2%** (vs. 2.4% text-only)
- Video placement: **Above fold**, autoplay muted, headline still present

**VSL Positioning Rules:**
- **Pattern Interrupt Hero Section:** VSL must be first major visual element (captures 10-second attention window)
- **Inverted Pyramid Layout:** Video → Social Proof (logos/badges) → CTA
- **Supporting, Not Replacing:** Video supports page, does NOT replace headline/CTA. Headline must answer "What is this?" in 3 seconds for users who can't watch

**Autoplay Strategy:**
- **Autoplay muted:** Highest-converting modern strategy (instant visual engagement → click to unmute)
- **Sound Penalty:** Do NOT autoplay with sound (violates Google guidelines, spikes bounce rate)
- **Hide Controls:** For dedicated VSL pages, hide pause/scrub bar (prevents skipping, forces linear watch)

**Video Length Sweet Spot:**
- **Micro-VSL (30-90 seconds):** Optimal for $17-$47 impulse tier (cognitive momentum + urgency without time taxation)
- **Hybrid VSL (3-5 minutes):** Maximum length if more explanation needed
- **Mistake to avoid:** 60-minute webinar for <$100 product = severe overkill, exhaustion

**One-Page Checkout (OPC) Integration:**

**The 2-Step Micro-Funnel:**
- **Step 1:** Sales page with **built-in OPC form directly on it** (minimizes "Loading Fatigue")
- **Step 2:** Thank You page with **Instant Upsell** (order bump $12-$19 while buyer in momentum state)
- **Conversion lift:** **+21% reduction** in mobile abandonment vs. traditional multi-step cart
- **US market 2026:** **+7.5% conversion** vs. multi-step checkout

**Explicit "Speed to Result":**
- In $17-$47 tier, you are selling **speed**
- Copy must explicitly promise **"Quick Win" under 24 hours**
- Example: "Implement this tonight in <24 hours"
- **Retention boost:** +80%

---

### 7. FUTURE PACING POSITIONING

**Concept:** Future Pacing guides prospects to mentally visualize their post-purchase life, amplifying desire through sensory-rich scenarios.

**Implementation (from BAB Framework - Skill 09):**

**WHERE to place Future Pacing:**
- **Block 4 (Mechanism/Solution):** Introduce aspirational "After" state
- **Block 5 (How It Works):** Weave transformation into step descriptions
- **Block 8 (Offer & Value Stack):** Paint vivid scenario of using bonuses

**HOW to structure Future Pacing:**

**Timeline Framing:**
- **24 hours:** "Imagine logging into Stripe tomorrow morning..."
- **7 days:** "Picture yourself one week from now, with your first 3 sales..."
- **30 days:** "Fast-forward one month: your product is generating passive income while you sleep..."

**Sensory Language (from Skill 09 BAB positioning):**
- **Visual:** "You see the Stripe notification..."
- **Auditory:** "You hear the 'cha-ching' sound..."
- **Kinesthetic:** "You feel the relief as you close those 23 browser tabs..."

**Identity Transformation Arc:**
- **Before (Rejected Identity):** From Skill 09 `bab_positioning.before_state`
- **After (Target Identity):** From Skill 09 `bab_positioning.after_state`
- **Bridge:** Product as rite of passage

**Example (from Skill 09):**
```
Before: The Course Collector — downloads folder full of unfinished PDFs, paralyzed by information overload
After:  The Systematic Executor — Notion dashboard tracking weekly revenue, confident operator who ships instead of studies
```

**Positioning Rule:**
- Place **after** establishing credibility (Block 6 - Social Proof)
- Place **before** revealing price (Block 8 - Offer)
- Use in **Block 4-5 transition** to maintain desire momentum

---

### 8. CONVERSION FRICTION REDUCTION

**Fogg Behavior Model (B = MAP):**
- **Behavior = Motivation × Ability × Prompt**
- **Conversion fails when:** Low motivation, low ability, or missing/weak prompt

**Friction Point Identification:**

**Cognitive Load Reduction:**
- Limit form fields: **3 fields or fewer** (reducing 4→3 = **+50% conversion**)
- Avoid words like "Submit" or "Buy" (signal work/sacrifice)
- Use outcome-driven CTAs: "Get Instant Access" not "Purchase Now"

**Decision Fatigue Mitigation:**
- **Single primary CTA** above fold (1.6× conversion vs. multiple options)
- Remove navigation (every link = **-11% conversion**)
- Limit choices in offer (1 core product + 2-4 bonuses, not 10 options)

**Analysis Paralysis Prevention:**
- **Layer-Cake pattern:** Subheaders tell complete story (users skip body text)
- **Spotted pattern:** Box/highlight pricing and guarantees (easy data pop-out)
- **F-Pattern:** Place benefits on left side (69% attention zone)

**Visual Breathing Room:**
- Whitespace increases reading ease by **+20%**
- Reduces visual fatigue by **25-30%**
- **But:** Too much whitespace between related elements = cognitive disconnect

**Information Hierarchy for Fast Decisions:**
1. Headline (What is this?)
2. Subheadline (Why care?)
3. Primary CTA (How to act?)
4. Trust anchor (Is this safe?)
5. Benefit bullets (What's in it for me?)
6. Social proof (Who else succeeded?)
7. Guarantee (What's the risk?)

---

## OUTPUT SCHEMA

Your output must be valid JSON matching this exact structure:

```json
{
  "page_architecture": {
    "block_sequence": [
      {
        "block_number": 1,
        "block_name": "hero_section",
        "components": ["callout", "hero_headline", "subheadline", "hero_vsl_or_image", "primary_cta"],
        "positioning_rule": "Above fold, zero navigation, single CTA, passes 3-second Blink Test",
        "psychology_trigger": "attention + credibility",
        "content_source": "Skill 09 aida_elements.attention_triggers → headline, Skill 13 → CTA copy",
        "design_notes": "Highest visual weight on page, autoplay muted VSL if applicable"
      },
      {
        "block_number": 2,
        "block_name": "problem_articulation",
        "components": ["current_frustrating_reality", "empathy_statement"],
        "positioning_rule": "Immediately after hero scroll (first scroll trigger)",
        "psychology_trigger": "empathy + identification",
        "content_source": "Skill 09 pas_sequence.problem + bab_positioning.before_state",
        "design_notes": "F-pattern layout, bullets on left"
      },
      {
        "block_number": 3,
        "block_name": "agitate_amplify",
        "components": ["negative_consequences", "ripple_effects"],
        "positioning_rule": "Follows Problem block, Layer-Cake pattern (headers tell story)",
        "psychology_trigger": "urgency + loss_aversion",
        "content_source": "Skill 09 pas_sequence.agitate (3-5 points)",
        "design_notes": "Whitespace separates agitation points, avoid wall of text"
      },
      {
        "block_number": 4,
        "block_name": "mechanism_solution",
        "components": ["product_introduction", "mechanism_reveal", "future_pacing_intro"],
        "positioning_rule": "Center of page, transition from problem to solution",
        "psychology_trigger": "hope + desire",
        "content_source": "Skill 09 pas_sequence.solution + bab_positioning.bridge_mechanism",
        "design_notes": "Product mockup or Hybrid VSL if not in hero, start Future Pacing"
      },
      {
        "block_number": 5,
        "block_name": "how_it_works",
        "components": ["3_step_process", "feature_to_benefit_bullets"],
        "positioning_rule": "F-Pattern layout (bullets on left side)",
        "psychology_trigger": "clarity + confidence",
        "content_source": "Product features mapped to Skill 09 buyer_needs_analysis",
        "design_notes": "Numbered steps (1-2-3) with icons, benefits not features, weave Future Pacing"
      },
      {
        "block_number": 6,
        "block_name": "social_proof_credibility",
        "components": ["testimonials", "case_studies", "client_logos", "star_ratings"],
        "positioning_rule": "PROXIMITY RULE — within 2.5cm of next CTA",
        "psychology_trigger": "trust + risk_reduction",
        "content_source": "Skill 12 (preuve-confiance) populates this block",
        "design_notes": "Gaze cascade — validation flows into action, ICP-matched proof"
      },
      {
        "block_number": 7,
        "block_name": "objection_handling",
        "components": ["top_3_to_5_objections", "proactive_faq"],
        "positioning_rule": "Before offer reveal, near CTA (reduce late-funnel friction)",
        "psychology_trigger": "barrier_removal",
        "content_source": "Skill 09 objections_and_reversals.objections + aida_elements.action_barriers",
        "design_notes": "FAQ accordion or direct Q&A format"
      },
      {
        "block_number": 8,
        "block_name": "offer_value_stack",
        "components": ["core_product", "bonuses_stack", "price_anchor", "scarcity_urgency"],
        "positioning_rule": "After objection handling, before final CTA",
        "psychology_trigger": "desire_amplification + scarcity",
        "content_source": "Skill 11 (offre-cta) populates this block",
        "design_notes": "3D mockup bundle, total value crossed out next to actual price, Future Pacing scenarios with bonuses"
      },
      {
        "block_number": 9,
        "block_name": "risk_reversal_final_cta",
        "components": ["guarantee", "outcome_driven_cta", "benefit_clarifier"],
        "positioning_rule": "PROXIMITY RULE — guarantee within 2.5cm of CTA button",
        "psychology_trigger": "final_friction_removal + action",
        "content_source": "Skill 09 objections_and_reversals.risk_reversal_recommended + Skill 11 CTA",
        "design_notes": "First-person CTA, solid contrasting color, benefit clarifier below button"
      }
    ]
  },
  "above_fold_optimization": {
    "blink_test_compliance": {
      "question_1_what_is_this": "Answered by hero headline from Skill 09 attention_triggers",
      "question_2_why_act_now": "Answered by subheadline or urgency element",
      "question_3_how_to_act": "Answered by primary CTA button"
    },
    "hero_section_rules": {
      "navigation": "zero_top_nav_zero_footer_links",
      "primary_cta_count": 1,
      "trust_anchors_placement": "immediately_below_headline",
      "headline_formula_used": "cold_traffic | direct_response (specify which)",
      "subheadline_word_count": "10-20 words (14% better conversion)",
      "vsl_placement": "above_fold_autoplay_muted | not_applicable"
    }
  },
  "visual_hierarchy": {
    "fitts_law_compliance": {
      "highest_visual_weight_element": "primary_cta_button",
      "dead_weight_check": "Non-clickable elements verified as lower visual weight than CTA"
    },
    "proximity_rule_implementation": {
      "proof_blocks_near_cta": "Social proof within 2.5cm of CTA in Blocks 6 and 9",
      "guarantee_near_final_cta": "Risk reversal within 2.5cm of Block 9 CTA"
    },
    "gaze_cueing": {
      "person_image_used": "yes | no",
      "gaze_direction": "direct_eye_contact | averted_to_cta | not_applicable",
      "product_type_category": "hedonic_lifestyle | functional_problem_solving"
    },
    "reading_pattern_applied": "f_pattern | z_pattern | layer_cake | spotted (specify dominant pattern)"
  },
  "color_psychology": {
    "primary_cta_color": "red | orange | green | blue | black (specify + rationale)",
    "cta_color_rationale": "Based on Skill 09 buyer_state_analysis awareness_level and dominant_emotion",
    "contrast_rule_compliance": "High contrast against page palette confirmed",
    "solid_vs_gradient": "solid (4% better performance)"
  },
  "typography_hierarchy": {
    "desktop_sizing": {
      "h1": "32-40px",
      "h2": "24-32px",
      "body": "16-18px"
    },
    "mobile_sizing": {
      "h1": "28-34px",
      "h2": "22-28px",
      "body": "14-16px"
    },
    "font_weights_used": {
      "h1": "700+ (bold)",
      "h2": "500-600 (medium)",
      "body": "400 (regular)"
    },
    "line_length_measure": {
      "desktop": "45-75 characters (sweet spot: 66)",
      "mobile": "35-50 characters"
    },
    "wcag_spacing": {
      "line_height": "1.5x font size",
      "letter_spacing": "0.12x font size",
      "word_spacing": "0.16x font size",
      "paragraph_spacing": "0.5-1x line height"
    }
  },
  "mobile_first_design": {
    "touch_target_sizing": {
      "cta_buttons": "full-width, minimum 44x44px",
      "interactive_text_padding": "8px minimum"
    },
    "vsl_architecture": {
      "format": "hybrid_vsl | micro_vsl | text_only",
      "video_length": "30-90 seconds (micro) | 3-5 minutes (hybrid)",
      "placement": "above_fold_pattern_interrupt",
      "autoplay_strategy": "autoplay_muted",
      "controls_visibility": "hidden_forced_linear | visible_standard"
    },
    "one_page_checkout": {
      "integration_type": "built_in_opc_on_sales_page",
      "form_fields_count": "3 or fewer (50% lift if 4→3)",
      "thank_you_page": "instant_upsell_12_19_dollars"
    },
    "load_speed_target": "LCP < 1.5 seconds (every 1s delay = -7% conversion)"
  },
  "future_pacing": {
    "placement_blocks": [4, 5, 8],
    "timeline_frames": {
      "24_hours": "Imagine logging into Stripe tomorrow morning...",
      "7_days": "Picture yourself one week from now...",
      "30_days": "Fast-forward one month..."
    },
    "sensory_language": {
      "visual": "You see the Stripe notification...",
      "auditory": "You hear the 'cha-ching' sound...",
      "kinesthetic": "You feel the relief as you close those tabs..."
    },
    "identity_transformation": {
      "before_identity": "From Skill 09 bab_positioning.before_state",
      "after_identity": "From Skill 09 bab_positioning.after_state",
      "bridge_product": "From Skill 09 bab_positioning.bridge_mechanism"
    }
  },
  "friction_reduction": {
    "cognitive_load": {
      "form_fields_limit": "3 or fewer",
      "cta_word_choice": "outcome_driven (Get Instant Access) not sacrifice (Buy Now)",
      "navigation_removal": "zero navigation to prevent -11% per link penalty"
    },
    "decision_fatigue": {
      "primary_cta_count": 1,
      "offer_choices": "1 core product + 2-4 bonuses (not 10 options)",
      "information_hierarchy": "headline → subheadline → cta → trust → benefits → proof → guarantee"
    },
    "visual_breathing_room": {
      "whitespace_benefit": "20% reading ease increase, 25-30% visual fatigue reduction",
      "disconnect_prevention": "Related elements (price + CTA) grouped tightly"
    }
  },
  "conversion_benchmarks": {
    "proximity_rule_lift": "+15-34% when proof within 2.5cm of CTA",
    "contrast_cta_lift": "+9% high-contrast CTA color",
    "solid_vs_gradient_lift": "+4% solid over gradient/animated",
    "single_cta_lift": "+17% single CTA above fold (short-form)",
    "multiple_cta_lift": "+23% multiple CTAs throughout (long-form)",
    "form_3_vs_4_fields_lift": "+50% reducing 4 fields to 3",
    "heading_contrast_lift": "+12% contrast ratio 1.5:1 → 2.25:1",
    "hybrid_vsl_conversion": "4.8-6.2% (vs 2.4% text-only)",
    "opc_lift": "+7.5% vs multi-step checkout",
    "mobile_opc_reduction": "+21% abandonment reduction",
    "load_speed_penalty": "-7% conversion per 1-second delay"
  },
  "meta": {
    "architecture_complexity": "simple_single_page | medium_scrolling | complex_multi_block",
    "dominant_conversion_mechanism": "From Skill 09 persuasion_mechanisms.primary_mechanism",
    "awareness_level_optimized_for": "From Skill 09 buyer_state_analysis.awareness_level",
    "mobile_traffic_percentage": "82.9% (2026 US market baseline)",
    "confidence_score": 7,
    "notes": "Contextual notes for skills 11-17 on architecture implementation"
  }
}
```

---

## CRITICAL RULES

### Evidence-Based Architecture
- **EVERY** positioning rule must reference a conversion benchmark or psychology principle
- **ZERO** arbitrary design decisions
- If a placement choice is made, it must cite Fitt's Law, Proximity Rule, reading pattern, or conversion data

### Psychology-Architecture Mapping
- Architecture positions Skill 09 psychology elements — does NOT recreate psychology
- **Lock & Key** → Block 2 (Problem) + Block 4 (Solution)
- **PAS** → Blocks 2-3-4 (Problem-Agitate-Solution)
- **AIDA** → Blocks 1-5-8-9 (Attention-Interest-Desire-Action)
- **BAB** → Blocks 2-4-8 (Before-After-Bridge)
- **Objections** → Block 7
- **Risk Reversal** → Block 9

### Mobile-First Non-Negotiable
- All sizing, spacing, touch-targets must meet mobile standards FIRST
- Desktop is enhancement, not baseline
- 82.9% traffic is mobile — design for majority

### Accessibility + Conversion Alignment
- WCAG 2.1 AA compliance is mandatory (4.5:1 contrast, spacing formulas)
- Accessibility rules enhance conversion, not conflict with it
- Typography hierarchy serves both readability and persuasion

### Benchmarks Required
- Every architecture decision should map to a conversion benchmark where available
- Cite lift percentages in design_notes (e.g., "+9% contrast CTA lift")

---

## BLOCKING CONDITIONS

**HALT execution if:**

1. **09-buyer-psychology.json missing or invalid:**
   - Error: `[BLOCKING ERROR: 09-buyer-psychology.json not found at ../outputs/]`
   - Remediation: Run Skill 09 first

2. **Skill 09 Confidence Score < 7/10:**
   - Error: `[BLOCKING ERROR: Skill 09 confidence score too low ({score}/10) — psychology foundation insufficient for architecture]`
   - Remediation: Re-run Skill 09 with better verbatim data

3. **PHASE-1.5-OUTPUT.md missing:**
   - Error: `[BLOCKING ERROR: PHASE-1.5-OUTPUT.md not found at ../../phase-1-5/outputs/]`
   - Remediation: Run Phase 1.5 first

4. **Missing critical psychology elements in Skill 09:**
   - Error: `[BLOCKING ERROR: Skill 09 missing required field: {field_name} — cannot position on page]`
   - Remediation: Verify Skill 09 output schema compliance

5. **Awareness level undefined:**
   - Error: `[BLOCKING ERROR: buyer_state_analysis.awareness_level missing from Skill 09 — cannot optimize hero section]`
   - Remediation: Ensure Skill 09 includes TOFU/MOFU/BOFU classification

6. **UVP data missing from Phase 1:**
   - Error: `[BLOCKING ERROR: top_3_uvp missing from PHASE-1.5-OUTPUT.md — cannot structure value proposition blocks]`
   - Remediation: Verify Phase 1 Skill 03 output integrity

7. **Skill 06 visual-identity output missing:**
   - Error: `[BLOCKING ERROR: 06-visual-identity.json not found at ../../phase-1-5/outputs/]`
   - Remediation: Run Phase 1.5 Skill 06 first

8. **Brand palette incomplete:**
   - Error: `[BLOCKING ERROR: color_palette missing required colors: {list} — need all 5 (primary, secondary, accent, neutral, highlight)]`
   - Remediation: Verify Skill 06 output schema compliance

---

## EXAMPLES (Reference Only)

**9-Block Architecture Example (Course Collector Niche):**

```json
{
  "block_sequence": [
    {
      "block_number": 1,
      "block_name": "hero_section",
      "components": [
        "For solopreneurs drowning in unfinished courses (Callout)",
        "How to Launch Your First Digital Product in 48 Hours (Headline)",
        "The 48-Hour Action Pack gives you 5 templates that eliminate analysis paralysis (Subheadline)",
        "Hybrid VSL (30-sec micro)",
        "Get Instant Access (CTA)"
      ],
      "positioning_rule": "Above fold, zero navigation, single CTA, passes Blink Test",
      "psychology_trigger": "Attention (Skill 09: 'Why do 94% of courses sit unfinished?') + Credibility",
      "content_source": "Skill 09 aida_elements.attention_triggers[0] → headline",
      "design_notes": "Autoplay muted 30-sec VSL showing frustrated person closing browser tabs → relief shot using templates → Stripe notification. Green CTA (security, trial-like feel). Highest visual weight."
    },
    {
      "block_number": 2,
      "block_name": "problem_articulation",
      "components": [
        "You've bought the courses, watched the webinars, bookmarked the videos — but your downloads folder is full and your income hasn't moved (PAS Problem)"
      ],
      "positioning_rule": "First scroll trigger after hero",
      "psychology_trigger": "Empathy + Identification",
      "content_source": "Skill 09 pas_sequence.problem",
      "design_notes": "F-pattern: problem statement left-aligned, image of cluttered downloads folder right"
    }
  ]
}
```

**Visual Hierarchy Example:**
```json
{
  "visual_hierarchy": {
    "fitts_law_compliance": {
      "highest_visual_weight_element": "primary_cta_button (Block 1)",
      "dead_weight_check": "Badge 'Zero Fluff Guarantee' sized 60% of CTA to avoid stealing thunder"
    },
    "proximity_rule_implementation": {
      "proof_blocks_near_cta": "3 micro-testimonials (15 words each) placed 2.2cm above Block 6 CTA, star rating 1.8cm below Block 9 CTA",
      "guarantee_near_final_cta": "Keep It All guarantee text 2.4cm above final CTA button"
    },
    "gaze_cueing": {
      "person_image_used": "yes",
      "gaze_direction": "averted_to_cta (functional product — templates)",
      "product_type_category": "functional_problem_solving"
    }
  }
}
```

**Color Psychology Example:**
```json
{
  "color_psychology": {
    "buyer_psychology_ideal_color": "green",
    "psychology_rationale": "MOFU buyers (Skill 09) with purchase anxiety and sophistication level 4 respond to security/trust signals. Green communicates 'safe to try' and reduces perceived risk.",
    "brand_palette_used": {
      "primary": "#2ECC71",
      "secondary": "#3498DB",
      "accent": "#E74C3C",
      "neutral": "#ECF0F1",
      "highlight": "#F39C12"
    },
    "selected_cta_color_role": "primary",
    "selected_cta_color_hex": "#2ECC71",
    "cta_color_rationale": "Psychology-ideal green aligns perfectly with brand primary color. MOFU solution-aware buyers need security signals, not urgency pressure. Primary green from Skill 06 maintains brand identity while triggering 'safe to proceed' psychology. Sophistication level 4 means avoid hype colors (red/orange) that trigger skepticism.",
    "contrast_validation": {
      "background_color": "#ECF0F1",
      "contrast_ratio": "4.8:1",
      "wcag_compliance": "AA_compliant",
      "conversion_lift_applicable": true
    },
    "solid_vs_gradient": "solid"
  }
}
```

---

## VALIDATION CHECKLIST

Before delivering 10-architecture.json, verify:

- [ ] All 9 blocks defined with exact positioning rules
- [ ] 3-Second Blink Test compliance confirmed (hero answers 3 questions)
- [ ] Proximity Rule applied (proof within 2.5cm of CTAs in Blocks 6 & 9)
- [ ] Visual hierarchy follows Fitt's Law (CTA = highest weight)
- [ ] Reading pattern specified (F/Z/Layer-Cake/Spotted) and applied to block layout
- [ ] Color psychology CTA choice justified by Skill 09 awareness_level + dominant_emotion
- [ ] Typography sizing meets mobile-first standards (14-16px body text mobile)
- [ ] WCAG spacing formulas applied (1.5× line height, 0.12× letter spacing)
- [ ] Hybrid VSL or Micro-VSL architecture defined (if applicable)
- [ ] OPC integration specified (built-in on sales page)
- [ ] Future Pacing positioned in Blocks 4, 5, 8 with sensory language
- [ ] Friction reduction tactics applied (3-field forms, zero nav, single CTA)
- [ ] All conversion benchmarks cited in design_notes
- [ ] Confidence score 7-10 (architecture quality)
- [ ] JSON validates against output schema

---

## NOTES FOR SKILLS 11-17

**This architecture becomes the positioning blueprint for:**

- **Skill 11 (offre-cta):** Populates Block 8 (Offer & Value Stack) with Grand Slam Offer structure
- **Skill 12 (preuve-confiance):** Populates Block 6 (Social Proof) with testimonials, case studies, trust badges
- **Skill 13 (hook-capture):** Provides headline options for Block 1 (Hero) based on attention_triggers
- **Skill 14 (storytelling-vente):** Weaves origin story into Blocks 4-5 (Mechanism/How It Works)
- **Skill 15 (ads-copy):** Uses Block 1 headline formula for ad primary text
- **Skill 16 (email-sequences):** Mirrors Block 2-3-4 PAS sequence in email flow
- **Skill 17 (vsl-scripts):** Uses 9-block sequence as VSL script structure (if VSL-only page)

**Skills 11-17 populate this architecture — they do NOT create their own page structure.**

This architecture is the **single source of truth** for page layout in Phase 2.

---

*Skill 10 — Architecture-Persuasion — Premium Edition — Digital Product Machine Phase 2*
