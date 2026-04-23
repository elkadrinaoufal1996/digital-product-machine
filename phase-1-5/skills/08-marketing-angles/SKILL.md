# SKILL: marketing-angles
**Skill ID:** 08 | **Phase:** 1.5 | **Status:** FINAL SKILL OF PHASE 1.5
**Inputs:** Skills 01–07 outputs | **Output:** 08-marketing-angles.json + PHASE-1.5-OUTPUT.md

---

## ROLE

Convert a validated niche and full brand system into a complete marketing angle arsenal:
10 ranked angles + 30-angle library + 1→7 recycling system + 30-day launch sequence.

This is the **final skill of Phase 1.5**. Its output feeds directly into `PHASE-1.5-OUTPUT.md`.
Single responsibility: **angles only**.
Never produces hooks bank or Value Stack — that belongs to Skill 05.

---

## INPUT

All fields from `input-schema.json`. Load `07-brand-voice.json` at `brand_voice_ref` before proceeding.

**HALT if `market_awareness_level` missing**
→ `[BLOCKING ERROR: marketing-angles — market_awareness_level required]`

**HALT if `07-brand-voice.json` not found at `brand_voice_ref`**
→ `[BLOCKING ERROR: marketing-angles — 07-brand-voice.json required]`

**HALT if `new_mechanism_name` missing**
→ `[BLOCKING ERROR: marketing-angles — new_mechanism_name required]`

**HALT if Skills 06 or 07 outputs not found**
→ `[BLOCKING ERROR: Skill 08 requires Skills 06+07 outputs]`

---

## STEP 1 — NAME THE NEW MECHANISM

Every $17–$47 product needs a proprietary mechanism.
Generic features cannot be sold at impulse speed.
A named mechanism shifts the question from "which product?" to "how does this process work?"

**5 Naming Structures** (select based on niche feel):

| Structure | Feel |
|---|---|
| Protocol [Name] | Scientific, clinical |
| System [Name] | Predictable machine, no skill needed |
| Technology / Algorithm [Name] | Innovation, technical edge |
| Formula / Equation [Name] | Mathematical certainty |
| Matrix / Framework [Name] | Visual roadmap, clear steps |

**Positioning statement (mandatory):**
> "[Mechanism Name]: the only method that [desired result] without [main pain point] — even if [biggest objection]."

**NESB Validation** — all four must pass:

- **New:** Does it feel unlike anything they've tried?
- **Easy:** Does it remove the dominant friction?
- **Safe:** Does it eliminate the biggest perceived risk?
- **Big:** Does the result match the price point?
  - $17 = quick win | $27 = repeatable system | $37 = identity shift | $47 = business transformation

---

## STEP 2 — SELECT TOP 10 ANGLES

**Map each angle to awareness level first.** Never use a Most Aware angle on cold traffic. Never use an Unaware angle on hot traffic.

**Awareness → Angle Mapping:**

| Awareness Level | Valid Archetypes |
|---|---|
| Unaware | Enemy / Contrarian / Discovery (curiosity-led) |
| Problem Aware | Root Cause Revelation / Pain Agitation |
| Solution Aware | New Mechanism / Transformation / Identity |
| Product Aware | Social Proof / Speed / Risk-Free Fast Track |
| Most Aware | FOMO / Urgency / Crazy Deal |

**10 Core Archetypes** (rank by fit to `dominant_emotion`):

1. **Root-Cause Revelation** — "Not your fault" + mechanism reveal
2. **Effortless Shortcut** — System 1, friction removal, 15 min/day
3. **Proprietary Mechanism** — Novelty, pattern interruption
4. **Anybody Can Blueprint** — Even-if, incompetence relief
5. **Predictable Formula** — Mathematical certainty, risk elimination
6. **Done-For-You Vault** — Convenience, effort = zero
7. **Prove Them Wrong** — Resentment, redemption, status
8. **Insider Secret** — Exclusivity, curiosity gap
9. **Micro-Constraint** — Accessibility, overwhelm relief
10. **Risk-Free Fast Track** — Cognitive safety, instant gratification

For each angle generate **3 hooks** (Question / Statement / Negative Constraint) filled with the exact `validated_niche` and persona. No placeholders — all hooks are niche-specific.

**Proof Pairing (mandatory per angle):**

| Angle | Required Proof Asset |
|---|---|
| Root-Cause | Before/After visual contrast graph |
| Effortless | Screen recording, time-stamped demo |
| Bandwagon | Testimonial stack + logos |
| Vengeance | Raw SMS/email screenshots |
| FOMO | Live sales notification recording |
| Curiosity | Reaction video, first discovery moment |
| Exclusivity | Private community peek (Skool/Slack) |
| Safety | Meta ad metrics screenshot |

---

## STEP 3 — 30-ANGLE LIBRARY

Generate exactly **30 angles** in **6 categories × 5**. All `core_hook_sentence` fields filled for this niche.

**IDENTITY (5):** Elite Club · Future Self · Insider Shift · Transformation · Vengeance Arc

**ENEMY (5):** System Rigged · Fake Guru · Hidden Saboteur · Root Cause · Obsolete Method

**DISCOVERY (5):** Weird Hack · Secret Vault · Missing Piece · Untapped Mine · Quiet Shift

**SPEED (5):** 15-Minute Fix · Lazy Shortcut · Overnight Switch · Skip-the-Line · Instant ROI

**CONTRARIAN (5):** Unpopular Take · Hard Truth · Opposite Rule · Hustle Myth · Counter-Logic

**SOCIAL PROOF (5):** Mass Exodus · Client Win · Blueprint Stolen · Community Wave · Undeniable Math

For each: `core_hook_sentence` (fill-in-the-blank, niche-filled) + `primary_emotion` + `best_platform`.

---

## STEP 4 — 1→7 RECYCLING SYSTEM

Take the **#1 ranked angle**. Transform into 7 platform-native formats:

**1. TIKTOK HOOK**
Raw, face-to-camera, under 60s. Text overlay.
Structure: `[Old way] is dead → [New mechanism] → [Result in 7 days]`

**2. INSTAGRAM CAPTION**
PAS structure: `[Problem] → [Agitate] → [Solution + link in bio]`
Social SEO keywords in natural language.

**3. EMAIL SUBJECT**
4–6 words. Curiosity gap. e.g. "The weird reason your [goal] is failing..."
Never clickbait — always deliverable on the subject line promise.

**4. EMAIL BODY**
300-word story arc: Discovery of mechanism → Root cause → Product as easy button → CTA.
Verbal bridges: *"That said,"* / *"But here's the thing,"*

**5. SALES PAGE HEADLINE**
NESB formula:
> "The Only [Mechanism] That Lets [Persona] Achieve [Result] Without [Pain] in Just [Timeframe]."

**6. META AD COPY**
AIDA: `[Attention: stop old way]` `[Interest: 10k+ switched]` `[Desire: benefit + price]` `[Action: tap Learn More]`

**7. PINTEREST PIN**
Visual listicle: `"3 Steps to [Result] Using the [Mechanism] Method"`
High contrast, 2:3 ratio, links to sales page.

---

## STEP 5 — 30-DAY LAUNCH SEQUENCE

### Phase 1 — DISRUPTION (Days 1–10) — Cold Traffic
Deploy: Enemy + Contrarian + Discovery angles.
Platform: TikTok organic + Meta TOF ads.
Goal: Invalidate existing beliefs, reveal root cause.
**Never pitch the product in Phase 1.**

### Phase 2 — INDOCTRINATION (Days 11–20) — Warm Traffic
Deploy: Identity + New Mechanism + Social Proof (client wins).
Platform: Email sequence + retargeting ads.
Goal: Introduce mechanism as the logical solution.
One case study per email. Identity shift framing.

### Phase 3 — 4-DAY CASH MACHINE (Days 21–30) — Hot Traffic
Deploy: Speed + Bandwagon + FOMO.

| Day | Content |
|---|---|
| Day 27 | Crazy Deal announcement — price + urgency anchor |
| Day 28 | Value stack reveal — all bonuses with individual values |
| Day 29 | Mass Exodus — "500 joined yesterday" social proof |
| Day 30 | Final Warning — "price doubles at midnight" |

---

## STEP 6 — COMPETITIVE GAP AUDIT

1. Pull `competitor_names` from input.
2. Document their `competitor_dominant_angle` pattern.
3. Identify which **Blue Ocean angle** they ignore — choose from:
   - **Radical Transparency** — raw metrics, failures, behind-the-scenes
   - **Taboo / Mistake Reveal** — calling out an accepted practice as fraud
   - **Identity Stage 5** — no outcome promise, pure elite status signal
4. Select **ONE** blue ocean angle as primary differentiator.
5. Confirm the chosen angle matches brand voice from `07-brand-voice.json`. Check against banned word list.

---

## STEP 7 — ANGLE TESTING PROTOCOL

5 hook variants → deploy organic (TikTok / IG Reels) → 72-hour window.

**Track ONLY:** 3-second hold rate + average watch time.
**Ignore:** likes, comments, follower count.

| Threshold | Decision |
|---|---|
| Hold rate < 40% | Angle dead — pivot immediately |
| Hold rate > 60% | Validated — move to paid traffic |

**4 Pivot Options if angle fatigues:**
1. New audience callout (same angle, new demographic)
2. Flip tension (gain → loss aversion)
3. Name the mechanism (make generic feature proprietary)
4. Escalate proof tier (founder story → UGC → expert endorsement)

---

## STEP 8 — TIKTOK FLASH SCRIPT (23 seconds)

Generate one complete script filled for this niche:

| Segment | Duration | Instruction |
|---|---|---|
| **Hook** | 0–3s | Pattern interrupt → old method is dead |
| **Agitate** | 3–8s | Not their fault → hidden root cause |
| **Value Demo** | 8–18s | System demo → result + timeframe |
| **CTA** | 18–23s | Price anchor → link in bio → now |

All four fields filled for this specific niche. No placeholders.

---

## FATAL ERRORS — HALT IF ANY IS TRUE

- ❌ Any angle deployed at wrong awareness level
- ❌ Mechanism name uses a banned word from `07-brand-voice.json`
- ❌ Recycling system has fewer than 7 formats
- ❌ 30-angle library has fewer than 30 angles
- ❌ Launch sequence missing Day 27–30 specifics
- ❌ Angle stacking uses more than 2 hooks in first 3 seconds
- ❌ Hooks or Value Stack produced (belongs to Skill 05 only)

---

## ANGLE STACKING RULES

- **Max hooks per opening:** 2 (never more in first 3 seconds)
- **Order:** `pattern_interrupt → curiosity_gap`
- **Example stack:** Filled for niche — no placeholders in output

---

## OUTPUT — TWO FILES

### FILE 1: `phase-1-5/outputs/08-marketing-angles.json`
All fields from `output-schema.json` populated.
Pure JSON only — no markdown fences.
- `top_10_angles`: exactly 10 items, all hooks filled for niche
- `angle_library_30`: exactly 30 items across 6 categories

### FILE 2: `phase-1-5/outputs/PHASE-1.5-OUTPUT.md`
Structured markdown summary:
1. New Mechanism — name + positioning statement
2. Top 10 Angles — ranked table with hooks
3. 1→7 Recycling System — all 7 formats filled
4. 30-Day Launch Sequence — phase by phase
5. Competitive Gap — blue ocean angle selected
6. Testing Protocol — thresholds and pivot rules
7. TikTok Flash Script — ready to shoot

---

## HALT CONDITIONS

| Condition | Error Message |
|---|---|
| `market_awareness_level` missing | `[BLOCKING ERROR: marketing-angles — market_awareness_level required]` |
| `07-brand-voice.json` not found at `brand_voice_ref` | `[BLOCKING ERROR: marketing-angles — 07-brand-voice.json required]` |
| `new_mechanism_name` missing | `[BLOCKING ERROR: marketing-angles — new_mechanism_name required]` |
| `top_10_angles` < 10 | `[BLOCKING ERROR: marketing-angles — 10 angles required]` |
| `angle_library_30` < 30 | `[BLOCKING ERROR: marketing-angles — 30 angles required]` |
| `PHASE-1.5-OUTPUT.md` not generated | `[BLOCKING ERROR: marketing-angles — final output file missing]` |
| Skills 06 or 07 outputs not found | `[BLOCKING ERROR: Skill 08 requires Skills 06+07 outputs]` |
