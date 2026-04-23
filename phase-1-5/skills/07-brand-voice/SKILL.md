# SKILL: brand-voice

## ROLE
Convert niche data + persona verbatims into a complete brand voice system calibrated on direct response psychology.
Output is the voice bible for all Phase 2 copy (ads, emails, VSL, sales page).
Single responsibility: voice only.
Never produces hooks or Value Stack — that belongs to Skill 05.

---

## INPUT
Fields from `input-schema.json`.

**HALT if `verbatim_samples` < 3 items**
→ `[BLOCKING ERROR: brand-voice — minimum 3 verbatim samples required from Skill 04]`

**HALT if `06-visual-identity.json` not found at `visual_identity_ref`**
→ `[BLOCKING ERROR: brand-voice — 06-visual-identity.json required as input]`

---

## STEP 1 — VOICE ARCHETYPE SELECTION

Map `dominant_emotion` + `psychographic` to the correct archetype:

| Emotion / Psychographic      | Archetype                         |
|------------------------------|-----------------------------------|
| Fear + anxious overachiever  | Scientific Authority (Caples)     |
| Desire + aspirational        | Results-Oriented Mentorship       |
| Frustration + burnt-out      | Conversational Intimacy (Halbert) |
| Trust + cautious buyer       | Poetic / Sensory Realism          |
| Exclusivity + status seeker  | Results-Oriented Mentorship       |
| Gen Z + anti-conformist      | Playful & Energetic               |

Select ONE archetype. Write `niche_rationale` explaining why this archetype fits this niche.

---

## STEP 2 — NESB VOICE CALIBRATION ($17–$47 MANDATORY)

Frame every claim through NESB:

- **NEW:** "Here's the mechanism I stumbled on" — never "revolutionary"
- **EASY:** Use Not-Statements — "It's not X. It's not Y. It's [mechanism]."
- **EASY:** Use Even-If — "[Goal] — even if [biggest objection]"
- **SAFE:** Assurance adjacent to every risk claim
- **BIG:** Match transformation scale to `price_point`
  - $17 = quick win
  - $27 = habit shift
  - $37 = system change
  - $47 = identity-level transformation

---

## STEP 3 — BANNED WORDS (40 total — 10 per category)

**Corporate Verbs — never use:**
delve, leverage, foster, ignite, empower, uncover, unleash, underscore, optimize, streamline

**Abstract Nouns — never use:**
tapestry, landscape, beacon, symphony, realm, journey, roadmap, synergy, ecosystem, paradigm

**Vague Adjectives — never use:**
cutting-edge, seamless, robust, future-ready, multifaceted, pivotal, dynamic, transformative, revolutionary, game-changer

**Transition Fillers — never use:**
furthermore, moreover, additionally, "in today's digital age", "let's dive in", "but here's the kicker", "it is important to note", "ultimately", "in conclusion", "generally speaking"

**FIX RULE:** Replace every banned word with its Anglo-Saxon equivalent.
- "optimize" → fix / clean
- "leverage" → use / take advantage of
- "transformative" → useful / works

---

## STEP 4 — POWER WORDS BY EMOTION

**URGENCY:** now, today, ends, limited, fast, immediate, final, expiring, quick, deadline

**TRUST:** guaranteed, safe, predictable, proven, secure, exact, verified, authentic, certified, official

**CURIOSITY:** secret, discover, reveal, little-known, truth, hidden, behind-the-scenes, why, confession, uncover

**EXCLUSIVITY:** only, exclusive, proprietary, private, insider, elite, restricted, invitation, member, patented

**TRANSFORMATION:** breakthrough, imagine, shift, grow, turn, build, fix, escape, rebuild, master

Apply `dominant_emotion` power words at 3x frequency in all generated copy.

---

## STEP 5 — SENTENCE ARCHITECTURE

**Rhythm:** Alternate short (1–5 words) and long sentences. Short = impact. Long = emotional runway. Never 3+ same-length in a row.

**Paragraphs:** Max 3 sentences. Single-sentence paragraphs = emphasis.

**Vocabulary:** Anglo-Saxon first.
- get > procure | burn > incinerate | see > perceive
- Use Latinate only for premium price justification ($37–$47).

**Emphasis:** Bold emotional trigger words only. Italics for internal dialogue / reader's inner speech. Never bold full sentences.

**Alignment:** Left only. No center-align body copy.

---

## STEP 6 — TACTILE REALISM (Anti-AI Markers)

10 micro-opinion openers to inject into copy:

1. "Honestly, I didn't expect this to work, but..."
2. "Here's the part most people don't say out loud:"
3. "If we're being real for a second..."
4. "This might sound weird, but..."
5. "Let me show you what this actually looks like in real life:"
6. "Here's the uncomfortable truth:"
7. "The part nobody puts on their sales page is..."
8. "I'm not going to pretend this is magic — here's the deal:"
9. "On paper, this looks simple. But in reality..."
10. "Here's where most people lose months without realizing it:"

**Specificity rule:** Always use exact numbers.
- "48,245 customers" not "nearly 50,000"
- "Last Tuesday at 11:47 PM" not "recently"

**Sensory translation rule:** Every abstract benefit → tactile scene under 15 words.
- "Save time" → "Closing your laptop while the sun is still up"
- "Reduce stress" → "Feeling your shoulders drop as you exhale, phone face down"
- "Make money" → "Watching the screen blink with a new payment notification"

---

## STEP 7 — PLATFORM VOICE ADAPTATION

**TIKTOK:** Raw, 1–3 second hook. Bold on-screen text. First-person direct. Relatable micro-story.
Structure: `[Uncomfortable truth] → [micro-story] → [pitch]`

**INSTAGRAM CAPTION:** Polished but human. Conversational tone. Natural-language keywords for social SEO. End with actionable lesson + save/share prompt.

**EMAIL SUBJECT:** 4–6 words max. Curiosity without clickbait.
Structure: "Idea for [specific pain]" / "Quick question about [challenge]"
Body: 1-to-1 friend letter. Verbal bridges between paragraphs: "That said," / "But here's the thing," / "The upshot is..."

**SALES PAGE HEADLINE:** 4 U's — Urgent, Unique, Useful, Ultra-Specific.
Template: "Get [Ultra-Specific Benefit] in [Urgent Timeframe] with [Unique Mechanism] — Even If [Biggest Objection]."

---

## STEP 8 — HEADLINE FORMULAS

Generate one filled `niche_example` per formula using `validated_niche`. All 10 required:

1. **"They Laughed"** — Caples story lead
   Template: `They laughed when I [action] — until [result]`

2. **"How I"** — N.E.S.B. personal proof
   Template: `How I [result] in [timeframe] without [objection]`

3. **"Even If" Destroyer** — inclusion emotion
   Template: `You can [goal] — even if [biggest objection]`

4. **Direct "How To" Promise** — pure usefulness
   Template: `How to [specific result] in [timeframe]`

5. **"Little-Known Secret"** — exclusivity + curiosity
   Template: `The little-known [mechanism] that [result] for [persona]`

6. **"Better Than" Comparison** — competitor invalidation
   Template: `Why [mechanism] works better than [familiar solution] for [persona]`

7. **WARNING / FOMO** — urgency + scarcity
   Template: `WARNING: [painful consequence] if you [inaction] past [specific date/event]`

8. **"Who Else Wants"** — social proof + belonging
   Template: `Who else wants to [desirable outcome] by [specific timeframe]?`

9. **Mechanism Reveal** — "new" emotion
   Template: `New [mechanism] lets you [result] without [sacrifice]`

10. **4 U's Direct Offer** — bottom-of-funnel
    Template: `Get [ultra-specific benefit] in [urgent timeframe] with [unique mechanism] — even if [biggest objection]`

---

## STEP 9 — CTA COPY

**Button text (first-person declaration only):**
- "Get my [specific outcome]"
- "Send me the [deliverable]"
- "Grab your [product name]"
- "See the [transformation]"
- "Give me access"

**NEVER USE ON BUTTON:** Submit / Sign Up / Learn / Buy / any pun

**Halo copy** (adjacent to button, not below fold):
"100% Secure Checkout" + "Instant Access" + "30-Day Guarantee"

**Urgency framing:** Time-bound + specific quantity.
"Only [X] copies at this price" / "Offer ends [specific day]"

---

## FATAL ERRORS — HALT IF ANY IS TRUE

❌ Any banned word present in generated copy
→ `[BLOCKING ERROR: brand-voice — banned word detected: {word}]`

❌ Paragraph > 3 sentences without a line break
→ `[BLOCKING ERROR: brand-voice — paragraph exceeds 3-sentence limit]`

❌ CTA button uses "Submit", "Sign Up", "Buy", or "Learn"
→ `[BLOCKING ERROR: brand-voice — prohibited CTA button text detected]`

❌ Any claim without specific data or tactile translation
→ `[BLOCKING ERROR: brand-voice — abstract claim without data or tactile anchor]`

❌ Verbatim samples not referenced in voice calibration
→ `[BLOCKING ERROR: brand-voice — verbatim samples unused in voice calibration]`

❌ Hooks or Value Stack produced (belongs to Skill 05 only)
→ `[BLOCKING ERROR: brand-voice — hooks/Value Stack out of scope. Delegate to Skill 05]`

❌ headline_formulas array contains fewer than 10 items
→ `[BLOCKING ERROR: brand-voice — 10 headline formulas required]`

---

## OUTPUT

Write output to: `phase-1-5/outputs/07-brand-voice.json`

- Pure JSON only — no markdown fences
- All fields populated — no null values
- `headline_formulas` array: exactly 10 items, each with `niche_example` filled
- `tactile_realism_copy.sensory_benefits`: minimum 5 items
- `banned_words`: exactly 10 per category (40 total)
- `power_words_by_emotion`: exactly 10 per emotion (50 total)
- `tactile_realism_markers`: exactly 10 items
- All 4 platform voice adaptations present with filled examples

---

## HALT CONDITIONS

| Condition | Error Message |
|---|---|
| `verbatim_samples` < 3 | `[BLOCKING ERROR: brand-voice — minimum 3 verbatim samples required from Skill 04]` |
| `visual_identity_ref` file not found | `[BLOCKING ERROR: brand-voice — 06-visual-identity.json required as input]` |
| Banned word in any output field | `[BLOCKING ERROR: brand-voice — banned word detected: {word}]` |
| `headline_formulas` < 10 items | `[BLOCKING ERROR: brand-voice — 10 headline formulas required]` |
