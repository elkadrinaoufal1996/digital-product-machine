# Value Stack Rules — Skill 05

Reference for offer construction in Skill 05. This is the single location in the Phase 1 chain where offer structure, Value Stack, and pricing are defined.

---

## Tier Coherence Rule

The 3 tiers must follow a logical "natural next step" sequence:

```
[Lead Magnet] → creates appetite for the problem addressed by the Ebook
[Core Ebook] → delivers the full system
[Upsell] → accelerates OR expands what the Ebook started
```

Invalid upsell examples (do not build these):
- ❌ Upsell is a summary of the ebook → no new value
- ❌ Upsell is a more expensive version of the same content → confusing
- ❌ Upsell addresses a completely unrelated topic → no logical continuity

Valid upsell formats:
- ✅ Template pack: "You now know the system — here are the ready-to-use assets to apply it"
- ✅ Workbook: "Here's the structured practice companion so you never have to think about the steps"
- ✅ Done-for-you asset: "Here's the X already built — you don't have to create it yourself"
- ✅ Advanced extension: "Chapter 5 introduced Level 2 — this goes deeper into Level 2 only"

---

## Pricing Anchor Rules

Pricing must be sourced from Firecrawl competitor data (SOURCE A), not invented.

**Target positioning:**
- Core Ebook: price at 80th percentile of comparable Gumroad/Kindle products
  - Below $10: commodity signal → avoid unless differentiation is extreme
  - $12-$27: standard ebook range — viable if transformation is clear
  - $27-$47: premium ebook range — requires strong proof and transformation depth
  - $47+: course-adjacent range — requires significant depth or bundle
- Lead Magnet: always free (email capture entry point)
- Upsell: target 30% of ebook price OR next natural price point (e.g., ebook $37 → upsell $67)

**Price justification format (required in output):**
```
Core Ebook: $[price]
Competitor range observed: $[min]-$[max]
Positioning rationale: [1 line — why this price vs. competitors]
```

---

## Value Stack Ratio Calculation

Required in PHASE-1-OUTPUT.md Section 4.

**Method:**
1. Assign perceived standalone value to each tier (= what a comparable standalone product sells for)
2. Sum all perceived values
3. Divide by total ask price (ebook + upsell if bundled)
4. Minimum acceptable ratio: 5:1

**Example:**
```
Lead Magnet standalone value: $17 (comparable templates sell for $17)
Core Ebook standalone value: $37 (market price)
Upsell standalone value: $47 (comparable workbooks sell for $47)
Total perceived value: $17 + $37 + $47 = $101
Total ask (ebook + upsell): $37 + $17 = $54
Ratio: $101 / $54 = 1.87:1 ❌ Too low — rework upsell
```

If ratio < 5:1 → rework the upsell format or increase lead magnet perceived value before delivering output.

---

## Chapter 1 Quick Win Rule

Chapter 1 of the Core Ebook must deliver a tangible result in under 20 minutes.

**Valid Quick Win examples:**
- "Reader produces a completed weekly budget template for their specific income situation"
- "Reader identifies their 3 highest-ROI tasks using the Eisenhower Matrix applied to their actual task list"
- "Reader calculates their exact daily caloric baseline and creates a 7-day meal plan outline"

**Invalid Quick Win examples (rework if this is what you've written):**
- ❌ "Reader understands the framework" → no tangible output
- ❌ "Reader feels inspired" → not measurable
- ❌ "Reader gains clarity" → too vague

The Quick Win must match the result described in Skill 02 Matrix B `quick_win_ch1` field. Do not deviate.

---

## Promise Format Validation

All 3 promise versions must conform to:
`[Specific Result] in [Realistic Timeframe] even if [Primary Objection]`

**Valid examples:**
- "Save 2 hours every workday in 5 days even if you've tried every productivity app and failed"
- "Build a monthly budget you actually stick to in one weekend even if numbers make you anxious"
- "Land your first freelance client in 30 days even if you have no portfolio yet"

**Invalid examples (rework):**
- ❌ "Transform your life" → no specific result
- ❌ "Get results fast" → no timeframe
- ❌ "Even if you're busy" → objection too generic
