---
SKILL 06 — visual-identity
Role : Convert validated Phase 1 niche data into a complete visual brand system calibrated on buyer psychology — not aesthetic preference.
Input : phase-1/outputs/PHASE-1-OUTPUT.md → parsed per input-schema.json
Output : phase-1-5/outputs/06-visual-identity.json
---

## OBJECTIVE
Generate a full visual identity system (colors, typography, platform templates, emotional journey, trust visuals, and competitive differentiation) by mapping the niche's dominant emotion and persona to documented conversion psychology principles. Every decision must be traceable to a conversion metric, not subjective taste.

## INPUT SCHEMA
Required fields from input-schema.json:
- validated_niche (string)
- dominant_persona.age_range / .gender / .psychographic (string)
- dominant_emotion (enum: fear | desire | frustration | aspiration | trust | exclusivity)
- positioning (string — from Skill 05)
- price_point (enum: 17 | 27 | 37 | 47)
- top_3_uvp (array of 3 strings)
- competitor_names (array, min 1)

HALT if dominant_emotion is missing → [BLOCKING ERROR: visual-identity — dominant_emotion required]
HALT if dominant_persona is missing → [BLOCKING ERROR: visual-identity — dominant_persona required]

---

## CORE LOGIC — COLOR SYSTEM (60-30-10)

Data points (cite in output rationale):
- Up to 90% of snap purchase judgments are based on color alone
- 85% of consumers cite color as their primary purchase driver
- 60% dominant = emotional base — sets the room's mood
- 30% secondary = trust and structure layer (backgrounds, cards, dividers)
- 10% CTA accent = ONLY occurrence of this color on the page — never repeat
- WCAG contrast minimum 4.5:1 — target 7:1 (7:1 = +23% readability, +15% conversion)
- Violating 60-30-10 ratio = -28% user retention, -22% add-to-cart rate

## EMOTION → COLOR MAPPING TABLE

| Emotion            | Dominant 60%              | CTA 10%                  | Avoid          |
|--------------------|---------------------------|--------------------------|----------------|
| Fear / Urgency     | #1A1A40 deep midnight     | #EC5800 persimmon        | Green          |
| Desire / Aspiration| #A78BFA digital lavender  | #FFD700 sunset gold      | Grey           |
| Frustration→Solution| #0A1128 midnight         | #00E5E5 vibrant cyan     | Red            |
| Trust / Safety     | #1F3A68 navy              | #2E7D32 deep green       | Neons          |
| Transformation     | #F5E9DD sand warm         | #B5651D spiced cider     | Pure black     |
| Exclusivity/Premium| #0C0C0C near-black        | #F7E7CE champagne        | Primary basics |

Map input dominant_emotion to table row. Use exact hex values unless competitor audit mandates a disruptor swap.

---

## TYPOGRAPHY SYSTEM

| Price Tier       | Title Font                    | Body Font   | Signal              |
|------------------|-------------------------------|-------------|---------------------|
| $37–$47 Premium  | Playfair Display Bold         | Inter Regular | Quiet luxury       |
| $17–$27 Mass     | Bebas Neue / Oswald           | Open Sans   | Speed, clarity      |
| Tech / B2B       | Space Grotesk                 | Inter       | Logic, precision    |
| Gen Z            | Bricolage Grotesque           | Poppins     | Anti-design         |
| Personal Dev     | Lora / Libre Baskerville      | DM Sans     | Warmth, safety      |

Rules (non-negotiable):
- Max 2 font families, 3 weights only: 400 Regular / 600 Medium / 700 Bold
- Ebook body: 16–18px, line-height 1.5x, max 75 characters per line
- Social title: min 80px at 1080px canvas width
- Alignment: left ONLY — never justify (justified text creates dyslexia rivers)

---

## EMOTIONAL JOURNEY — COLOR SHIFTS ACROSS FUNNEL

**AWARENESS (TikTok / IG Reels)**
Apply +15–20% saturation boost to dominant_60 color. Use dopamine-coded colors. Kinetic or bold text overlays. No long copy.

**CONSIDERATION (Landing Page / Email)**
Shift to 60-30-10 Elevated Neutrals. secondary_30 dominates layout. Body text 16–18px, line-height 1.5x, 50–75 chars/line.

**DECISION (Sales Page / Checkout)**
Deploy cta_accent_10 in isolation — it must be the ONLY occurrence of this color on the page. Red/orange CTA = +34% CTR vs green (documented). Add countdown timer and risk-reversal badge adjacent to button.

**POST-PURCHASE (Confirmation / Upsell)**
Switch to parasympathetic palette (deep navy or calming green). This reduces post-purchase anxiety before presenting the upsell offer. Required before any upsell is shown.

---

## TRUST VISUALS — REQUIRED FOR $17–$47

1. **Hero 3D Mockup**: 300 DPI, 15-degree perspective, book spine visible, hard drop shadow. Surround with device frames (laptop, tablet, mobile) showing real content pages.
2. **Value Stack Labels**: "$97 Value" text adjacent to each bonus. "Total Value: $XXX" crossed out, real price below. Anchoring effect.
3. **Proof Wall**: Floor-to-ceiling raw screenshots (DMs, comments, emails). Never polish or crop. Raw > designed — imperfection signals authenticity.
4. **Risk-Reversal Badge**: Shield icon + "30-Day Money-Back Guarantee" text. Placed DIRECTLY adjacent to CTA button — never below the fold.

---

## TACTILE REALISM (2025–2026 Anti-AI-Detection)

- Grain overlay: 3–8% opacity noise layer on all background sections
- Texture: paper or fabric texture in Multiply blending mode at 6–8% opacity
- Handwriting accent: messy script font (Caveat or SA Washington Ink) exported as PNG image — NOT editable text. Arrow pointing to CTA with text "Start here!" or similar.
- Never center-align all elements — slight asymmetry = human signal

---

## PLATFORM SAFE ZONES

| Platform        | Constraint                                              |
|-----------------|---------------------------------------------------------|
| TikTok          | Text-free zone: top 250px / bottom 300px                |
| Instagram Feed  | 80px margins all sides, 1:1 ratio                       |
| Pinterest       | Strict 2:3 ratio — high contrast title min 80px         |

---

## COMPETITIVE AUDIT PROTOCOL

1. Pull competitor list from input field competitor_names (min 1 required).
2. For each competitor document: primary color, CTA color, font style category.
3. Identify the dominant visual pattern across competitors (e.g., "All use navy + orange on white with bold sans-serif").
4. Select ONE disruptor element: different dominant color OR different typography family OR opposite style (dark vs light).
5. Apply disruptor to CTA accent only — keep neutral base safe and recognizable.
6. Record disruptor hex and differentiation axis (color | typography | style) in output.

---

## FATAL ERRORS — HALT OUTPUT IF ANY IS TRUE

❌ CTA color appears more than once on the page
❌ Body text set below 16px
❌ More than 2 font families or more than 5 total colors used
❌ Any text/background combination with contrast ratio below 4.5:1 (WCAG AA)
❌ Chromostereopsis combinations used: red on blue, red on green (causes eye vibration, raises bounce)
❌ Pure white #FFFFFF used as main background (causes eye fatigue on long-form sales pages)
❌ Ebook cover not tested at 160px thumbnail size before delivery

---

## OUTPUT

Write a single JSON file — no markdown fences — to:
`phase-1-5/outputs/06-visual-identity.json`

All fields from output-schema.json must be populated. No null values except accent_font. Confirm WCAG contrast ratio for cta_accent_10 before writing. Include full Canva/Midjourney prompts for all 4 platforms.

---

## HALT CONDITIONS

- HALT if dominant_emotion field is missing from input
  → [BLOCKING ERROR: visual-identity — dominant_emotion required]

- HALT if competitor_names is empty or not provided
  → [BLOCKING ERROR: visual-identity — competitor audit requires min 1 name]

- HALT if generated palette contrast_ratio < 4.5:1 on any text/background pair
  → [BLOCKING ERROR: visual-identity — WCAG violation on palette]

- HALT if price_point is not one of [17, 27, 37, 47]
  → [BLOCKING ERROR: visual-identity — invalid price_point]

---

## EXAMPLE OUTPUT

```json
{
  "color_system": {
    "dominant_60": { "hex": "#1A1A40", "emotion_rationale": "Deep midnight activates authority and urgency for fear-driven ADHD buyers" },
    "secondary_30": { "hex": "#2B2D42", "role": "Section backgrounds, card surfaces, dividers" },
    "cta_accent_10": { "hex": "#EC5800", "contrast_ratio": "7.4:1" }
  },
  "typography_system": {
    "title_font": "Bebas Neue",
    "body_font": "Open Sans",
    "accent_font": "Caveat",
    "price_tier_rationale": "$27 mass-market tier — Bebas Neue signals speed and urgency for anxious overachievers"
  },
  "competitive_differentiation": {
    "competitors_audited": ["Focus@Will", "Focusmate"],
    "dominant_pattern_in_niche": "All use navy + orange on white backgrounds",
    "our_disruptor_color": "#EC5800",
    "differentiation_axis": "color"
  }
}
```
