# SKILL 12 — OFFRE-CTA
## Digital Product Machine — Phase 2 | Pivot de Monétisation

**Role:** Transform validated buyer psychology (09), LP architecture (10), and funnel design (11)
into a complete monetized offer with CTAs, value stack, AOV engineering, and scarcity timeline.

**This skill is the monetization pivot.** It does not invent psychology — it converts
existing data from skills 09/10/11 into a structured offer engine.

**Output:** `outputs/12-offre.json` — parsed directly by `analyst.py`

---

## PRE-FLIGHT — BLOCKING CONDITIONS

Run this check BEFORE any generation. HALT immediately on any failure.

```python
from os.path import exists

REQUIRED = [
    "outputs/09-buyer-psychology.json",
    "outputs/10-architecture.json",
    "outputs/11-funnel-architecture.json"
]

for f in REQUIRED:
    if not exists(f):
        raise SystemExit(
            f"[BLOCKING ERROR: {f} missing — sequential dependency violation. "
            f"Run the corresponding skill before Skill 12.]"
        )
```

**Field-level blocking (validate after loading):**

From `09-buyer-psychology.json` — HALT if missing:
- `buyer_state_analysis.awareness_level` → drives CTA tone
- `persona_primary.pain_points` (min 3) → anchors big_domino_claim
- `verbatims_bank` (min 10) → MANDATORY source for all CTA VoC copy
- `advanced_tactics.big_domino_shift` → feeds grand_slam_offer.big_domino_claim

From `10-architecture.json` — HALT if missing:
- `lp_blocks` (min 9 blocks) → CTA matrix mapping
- `blink_test_hero` → hero CTA must extend this, never contradict

From `11-funnel-architecture.json` — HALT if missing:
- `price_point` (must be $17-$47) → calibrates stack ratio
- `order_bump_price` (must be $12-$19) → AOV engineering
- `oto_price` (must be $51-$100) → AOV engineering
- `value_stack_ratio_target` (minimum 10) → stack validation gate

**If `outputs/00-persuasion-intel.json` exists** → load it for competitor differentiation.
Not blocking if absent — skip competitor contrast step only.

---

## NON-NEGOTIABLE RULES

These rules apply to every output regardless of niche, price, or awareness level.
Violating any of these = output rejected.

| # | Rule | Source |
|---|------|--------|
| R1 | Stack ratio ≥ 10:1. Ideal 16.9:1 for $47. | Hormozi |
| R2 | Guarantee minimum 60 days. Never less. | Hormozi (60d = +23% vs 30d) |
| R3 | ONE CTA per LP block. No exceptions. | Unbounce CTA research |
| R4 | All CTAs in first person ("Je", "Mon", "Oui je"). | Unbounce (+90% clicks) |
| R5 | Zero generic CTA text: "Submit", "Buy", "Register". | CXL Institute |
| R6 | Micro-copy under EVERY CTA button. | Copyhackers (+9-15%) |
| R7 | Big Domino from skill 09 only — never invented. | Evidence-first doctrine |
| R8 | All CTA copy anchored on verbatims_bank. | VoC rule |
| R9 | Zero fake scarcity — FTC 2026 compliance. | FTC enforcement |
| R10 | JSON output only — zero markdown fences. | analyst.py parsing |
| R11 | Core promise must contain: number + time unit + "without [obstacle]". | Believability threshold |
| R12 | Guest checkout always enabled. | -24% abandonment data |

---

## EXECUTION SEQUENCE

### PHASE 1 — DATA INGESTION (load before any generation)

```
Step 1.1: Load outputs/09-buyer-psychology.json
  → Extract: awareness_level, pain_points, core_desires, top_objections,
             verbatims_bank, big_domino_shift, bab_positioning, buyer_needs_analysis

Step 1.2: Load outputs/10-architecture.json
  → Extract: lp_blocks (all 9), blink_test_hero, brand_palette

Step 1.3: Load outputs/11-funnel-architecture.json
  → Extract: funnel_type, price_point, order_bump_price, oto_price,
             bonus_depletion_timeline, value_stack_ratio_target

Step 1.4 (optional): Load outputs/00-persuasion-intel.json if exists
  → Extract: competitor_offers, market_hooks

Step 1.5: Validate all required fields are present (blocking conditions above)
```

### PHASE 2 — GRAND SLAM OFFER
**Reference:** `references/grand-slam-framework.md` — LOAD this file before this phase.

```
Step 2.1: UNIQUE MECHANISM
  → Inspect: product positioning from skill 11, mechanism hints from skill 10 blink_test
  → Name the proprietary mechanism (2-5 words, non-generic, proprietary feel)
  → If 00-intel loaded: verify name not used by any competitor

Step 2.2: BIG DOMINO
  → Source EXCLUSIVELY from: 09.advanced_tactics.big_domino_shift
  → Format: "[Result] isn't about [common assumption] — it's about [real mechanism]"
  → Zero invention — cite the exact belief from skill 09

Step 2.3: CORE PROMISE
  → Formula: "[Specific Result] in [Precise Time] without [Primary Obstacle]"
  → Result: anchored on 09.persona_primary.core_desires[0]
  → Time: must be achievable, reference Quick Win delivery in < 24h
  → Obstacle: extracted from 09.persona_primary.pain_points[0]
  → Believability check: bold promise → add "documented by [N] students" framing

Step 2.4: VALUE EQUATION
  → dream_outcome: from 09.bab_positioning.after_state + verbatim language
  → perceived_probability: list three levers (guarantee + proximity proof + ICP testimonials)
  → time_delay: specify exact chapter/module delivering first win in < 24h
  → effort_sacrifice: list plug-and-play assets included (templates, scripts, checklists)
```

### PHASE 3 — VALUE STACK
**Reference:** `references/grand-slam-framework.md` — Section 2-3.

```
Step 3.1: CORE OFFER
  → Title, format, list of 3+ modules/chapters
  → Module 1 MUST be the Quick Win (< 24h result)
  → Perceived value: consultant equivalent pricing (not inflated)

Step 3.2: BONUS HIERARCHY (Rank 1 → 4 priority order)
  → Bonus 1 (Rank 1 — plug-and-play): templates, scripts, or checklists
    Perceived value: hours saved × freelancer rate
  → Bonus 2 (Rank 2 — speed): 7-day plan, quick-start, shortcuts
    Perceived value: time savings × opportunity cost
  → Bonus 3 optional (Rank 3 — accountability): community or Q&A
    Include only if 09 persona values certainty/accountability

Step 3.3: FAST-ACTION BONUS
  → Type: exclusivity or accountability (Rank 3-4)
  → Deadline: 48 hours from opt-in (Deadline Funnel tracking)
  → Rule: bonus disappears, core offer stays

Step 3.4: GUARANTEE
  → Select type based on awareness level and sophistication score:
    TOFU/MOFU → keep-product (lowest barrier, highest perceived safety)
    BOFU → better-than-money-back (signals premium quality)
    Sophistication 4-5 → conditional (forces implementation, filters refunders)
  → Duration: 60 days (non-negotiable)
  → Write full copy: duration + conditions + what customer keeps

Step 3.5: CALCULATE RATIO
  → total_perceived_value = sum(all elements)
  → stack_ratio = total_perceived_value / price_point
  → If ratio < 10: increase perceived_value on existing elements (justified revaluation)
  → If ratio < 10 after revaluation: add one more bonus (Rank 3 or 4)
  → Target: 16.9:1 for $47, proportionally for other prices

Step 3.6: LEAD MAGNET
  → Free entry-point asset tied to funnel_type from skill 11
  → Must connect directly to core offer (not a separate topic)
  → Perceived value: minimal ($0 — free asset, no monetary value attribution)
```

### PHASE 4 — AOV STACK
**Reference:** `references/guarantee-scarcity.md` — Section 3.

```
Step 4.1: ORDER BUMP ($12-$19)
  → Price: use order_bump_price from skill 11
  → Logical extension of core offer (not a separate product)
  → Headline: "Add [Name] for only $[Price] — [Immediate benefit today]"
  → Write 2-3 dynamic variants:
    Variant A (Meta/paid): visual-heavy, benefit-first
    Variant B (email/organic): context-aware, story-led
  → target_take_rate: 37.8%

Step 4.2: OTO ($51-$100)
  → Price: use oto_price from skill 11
  → Opening: "Before you close this page…" (non-negotiable opening)
  → Positioned on thank_you_page (immediate post-purchase)
  → target_acceptance_rate: 15-25%
  → If offer includes recurring: bundle setup + first month into single transaction

Step 4.3: DOWNSELL
  → Select type based on awareness_level from skill 09:
    TOFU/MOFU → payment_plan (lower commitment threshold)
    BOFU → lite_version (knows the value, just price-sensitive)
  → Never arbitrary discount on identical product
```

### PHASE 5 — CTA MATRIX
**Reference:** `references/cta-playbook.md` — Load for full rules + formulas.

```
Step 5.1: LOAD verbatims_bank from skill 09
  → Extract 5 highest-emotion phrases
  → These are the raw material for CTA VoC copy

Step 5.2: MAP CTAs to LP blocks (from skill 10)
  → Block 1 (Hero): "Oui, je veux [dream_outcome mirror] →"
    Source: verbatims_bank most aspirational phrase
  → Block 4 (Solution): "Voir comment [unique_mechanism_name] fonctionne →"
    Source: unique_mechanism_name from grand_slam_offer
  → Block 5 (How It Works): optional mid-page engagement CTA
  → Block 6 (Proof): "Rejoindre [N] personnes qui ont [specific result] →"
    Source: if N exists in skill 10 proof blocks, use exact number
  → Block 8 (Offer): "Oui ! Je veux [core offer name] + [bonus count] bonus pour $[price] →"
    Source: value_stack.core_offer.title, price_point from skill 11
  → Block 9 (Risk Reversal): "Essayer sans risque pendant 60 jours →"
    Source: guarantee.duration_days

Step 5.3: MICRO-COPY for each CTA
  → Format: "✓ [Immediate access/delivery] · ✓ Garantie [N] jours · ✓ [Friction removal]"
  → Hero micro-copy: emphasize zero-risk + instant access
  → Offer micro-copy: emphasize value stack + fast-action deadline if active
  → Risk Reversal micro-copy: emphasize keep-product clause (if applicable)

Step 5.4: VoC VALIDATION
  → Read each CTA button text aloud — could a real buyer have said this?
  → If CTA contains: "transform", "unlock", "journey", "potential" → REWRITE
  → If CTA could appear unchanged on 3 competitors' pages → REWRITE
```

### PHASE 6 — SCARCITY TIMELINE
**Reference:** `references/guarantee-scarcity.md` — Section 2.

```
Step 6.1: Load bonus_depletion_timeline from skill 11
  → Map available bonuses per phase

Step 6.2: BUILD 3-PHASE SCHEDULE
  → j1_j2: full stack available. Copy references Fast-Action Bonus deadline.
  → j3_j4: Fast-Action Bonus expired. Copy names the specific bonus lost.
  → j5_plus: Bonus 2 also removed. Core + Bonus 1 + Guarantee remain always.
  → Core offer NEVER removed in any phase.

Step 6.3: COPY FOR EACH PHASE
  → Must name specific bonus that expired (never generic "some bonuses removed")
  → Must state what remains (not just what's gone)
  → Tone: matter-of-fact, not manipulative
```

### PHASE 7 — IDENTITY ALIGNMENT

```
Step 7.1: DESIRED IDENTITY
  → Source: 09.bab_positioning.after_state — extract who the buyer wants to BECOME
  → Frame as identity claim, not feature: "You become [Identity], not someone who bought [Product]"

Step 7.2: RATIONAL ALIBI
  → Calculate ROI: price_point / hours_saved_per_month = cost per hour
  → Compare to alternative: "[Product] costs less than one [comparison] per [time unit]"
  → Frame: "The logical reason this purchase makes sense"

Step 7.3: STATUS SIGNAL
  → Source: 09.buyer_needs_analysis.dominant_need — social or psychological dimension
  → Frame: "By owning this, the buyer signals [identity] to their peers"

Step 7.4: FEEL SMART STATEMENT
  → The post-purchase reassurance that reduces buyer's remorse
  → Frame: "Someone who [identity claim] doesn't pay for [alternative cost]"
  → Reduces refund demand by making buyer feel like a rational decision-maker
```

### PHASE 8 — CHECKOUT FRICTION REDUCTION

```
Step 8.1: Express checkout → always include Apple Pay + Google Pay
Step 8.2: BNPL check → if price_point > 37: add Klarna + Afterpay
Step 8.3: Trust badges → SSL + payment processor + guarantee seal (in this order)
Step 8.4: Guarantee reminder copy → short (≤ 20 words) for placement at card fields
Step 8.5: guest_checkout → always true
```

### PHASE 9 — OUTPUT & VALIDATION

```
Step 9.1: Compile complete 12-offre.json matching output-schema.json exactly
Step 9.2: Run internal validation checklist (below)
Step 9.3: Calculate confidence_score based on evidence density
Step 9.4: Output pure JSON — zero markdown, zero commentary, zero fences
```

---

## VALIDATION CHECKLIST

Before emitting any output, verify:

- [ ] Stack ratio ≥ 10:1 — calculated and shown
- [ ] Core promise contains: specific number + time unit + "without [obstacle]"
- [ ] All CTA button texts in first person ("Je", "Mon", "Oui je")
- [ ] Zero banned CTAs: "Submit", "Buy", "Register", "Learn More", "Click Here"
- [ ] Micro-copy under EVERY button (5 CTAs × 2 fields = 10 micro-copy lines minimum)
- [ ] Guarantee duration = 60 days (or justified exception documented)
- [ ] Big Domino sourced from 09.advanced_tactics.big_domino_shift
- [ ] Unique Mechanism name is original (not generic)
- [ ] Scarcity timeline has 3 distinct phases — core never removed
- [ ] Order bump price $12-$19
- [ ] OTO price $51-$100 on thank_you_page
- [ ] Downsell is lite_version OR payment_plan (not arbitrary discount)
- [ ] identity_alignment.desired_identity sourced from 09 bab_positioning
- [ ] checkout_friction_reduction.guest_checkout = true
- [ ] JSON validates against output-schema.json
- [ ] Zero markdown fences in output
- [ ] confidence_score justified

---

## CONFIDENCE SCORE CALIBRATION

| Score | Condition |
|-------|-----------|
| 9-10 | All verbatim anchors present, min 15 verbatims in skill 09, stack ratio ≥ 14:1, all CTAs sourced from VoC |
| 7-8 | Most anchors present, some inferences made, ratio ≥ 10:1, CTAs mostly VoC-sourced |
| 5-6 | Several fields inferred without verbatim evidence — flag for human review |
| < 5 | HALT — insufficient input data quality. Return error with missing fields list. |

---

## REFERENCE FILES

| File | Load when generating |
|------|---------------------|
| `references/grand-slam-framework.md` | Phases 2 and 3 (grand_slam_offer + value_stack) |
| `references/cta-playbook.md` | Phase 5 (cta_matrix) |
| `references/guarantee-scarcity.md` | Phases 4, 6, and 8 (aov_stack, scarcity_timeline, checkout) |

**Loading rule:** Load each reference file at the START of its corresponding phase.
Do not load all three upfront — progressive loading keeps context focused.

---

## OUTPUT FORMAT REMINDER

```
Respond with pure JSON only.
No markdown fences (no ```json).
No explanatory text before or after the JSON.
No comments inside the JSON.
The entire response = the JSON object and nothing else.
```

The output-schema.json is the authoritative contract.
When in doubt about a field → re-read the schema before generating.

---

## ERROR MESSAGES — Standard Format

```
[BLOCKING ERROR: outputs/09-buyer-psychology.json missing]
[BLOCKING ERROR: verbatims_bank has only {N} entries — minimum 10 required]
[BLOCKING ERROR: price_point {value} is outside $17-$47 range]
[BLOCKING ERROR: stack_ratio {value} < 10 — cannot generate compliant offer]
[WARNING: 00-persuasion-intel.json not found — competitor contrast step skipped]
[WARNING: confidence_score {X}/10 below 7 — human review recommended]
```

---

*Skill 12 — offre-cta — Digital Product Machine Phase 2 v1.0*
*Sequential dependency: Skills 09 → 10 → 11 → 12*
*Output consumed by: Skills 13 (hooks), 14 (storytelling), 15 (ads), 16 (email), 17 (VSL)*
