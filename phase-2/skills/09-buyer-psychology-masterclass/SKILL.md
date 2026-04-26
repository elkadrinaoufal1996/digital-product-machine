# SKILL 09 — BUYER PSYCHOLOGY MASTERCLASS

## ROLE

Extract and map buyer psychology from validated personas to proven persuasion frameworks. This analysis becomes the foundational psychology layer for all Phase 2 marketing assets (skills 10-17).

You are a buyer psychology diagnostician, not a copywriter. Your output is a structured psychological analysis that other skills will use to generate copy.

---

## UNIQUE RESPONSIBILITY

**What this skill DOES:**
- Identify emotional locks (pains/desires) from persona verbatims using JTBD framework
- Map locks to persuasion mechanisms (PAS, AIDA, BAB)
- Extract trigger words and objections from buyer language
- Diagnose buyer awareness level (TOFU/MOFU/BOFU)
- Assess market sophistication and dominant objections
- Define identity positioning (Before-After states)
- Extract risk reversal anchors from verbatim anxieties

**What this skill DOES NOT DO:**
- Generate marketing copy (that's skills 10-17)
- Create hooks or CTAs (that's skills 11, 13)
- Write email sequences (that's skill 16)
- Score or validate the niche (that was Phase 1)

**Critical principle:**
Skills 10-17 will USE this psychology map — they do NOT recreate it. This is the single source of truth for buyer psychology in Phase 2.

---

## INPUT

### Required Files

1. **PHASE-1.5-OUTPUT.md**
   - Fields needed: `validated_niche`, `dominant_emotion`, `brand_voice`, `top_3_uvp`
   - Source: `../phase-1-5/outputs/PHASE-1.5-OUTPUT.md`

2. **04-personas.json**
   - Structure: Array of 3 personas, each with minimum 5 verbatims
   - Required fields per verbatim: `quote`, `source_url`, `date`
   - Source: `../phase-1/outputs/04-personas.json`

### Data Flow

```
PHASE-1.5-OUTPUT.md  →  validated_niche, dominant_emotion, top_3_uvp
04-personas.json     →  verbatims (minimum 15 total across 3 personas)
                             ↓
                      Skill 09 analysis
                             ↓
             09-buyer-psychology.json → used by skills 10-17
```

---

## FRAMEWORKS REFERENCE (NotebookLM Extract)

### 1. LOCK & KEY FRAMEWORK

**Concept:** The emotional lock is the core pain/desire extracted from verbatims. The key is how the product unlocks this. This framework is implicit across JTBD, PAS, and BAB.

**Lock identification (via JTBD):**
- Find the "moment of struggle" in verbatims
- Extract the 4 Forces of Progress:
  - **Push:** Current frustration forcing them to seek change
  - **Pull:** Attraction to the new solution
  - **Anxiety:** Fear of the unknown holding them back
  - **Allegiance:** Old habits they must abandon

**Example (from NotebookLM):**
```
LOCK (verbatim): "I feel like I'm spinning my wheels trying 10 different things but
nothing sticks long enough to see results"
KEY: The 90-Day Focus Framework — one proven system, zero distractions
```

**Key positioning rule:**
The "key" must map to one of the 3 UVPs from Phase 1. Do not invent new positioning.

---

### 2. PAS (PROBLEM-AGITATE-SOLUTION) FRAMEWORK

**Creator:** Industry standard (SaaSFunnelLab, Copyhackers)

**Core mechanism:** Leverages loss aversion — humans are more motivated to avoid pain than seek pleasure.

**3-Step Structure:**

**PROBLEM (The Lock):**
- State a specific, relatable pain point from verbatims
- Use buyer's exact vocabulary, not marketing jargon
- Ground in concrete situations (e.g., "3 PM deadline panic" not "communication challenges")

**AGITATE:**
- Amplify emotional impact by showing negative consequences
- "Pour salt in the wound" — show how the problem ripples into other areas
- Use frustration, anxiety, or embarrassment patterns from verbatims
- **Mistake to avoid:** Over-agitation. "Tired of cluttered closets?" works better than "Your messy home is ruining your life"

**SOLUTION (The Key):**
- Present product as logical, immediate remedy
- Must directly correspond to agitated pain points
- Focus on tangible proof, not vague promises

**Template:**
```
[PROBLEM] Identify pain point → [AGITATE] Make it urgent/worse → [SOLUTION] Product as answer

Example: "Cluttered closet driving you crazy? (Problem) Every morning wastes 15 minutes
searching for clothes. Guests judge your messy bedroom. (Agitate) Our modular system
organizes 300+ items in 2 hours. Transform chaos into calm. (Solution)"
```

**Extraction instructions:**
- Problem: Extract from verbatims where buyers describe current frustration
- Agitate: Extract consequences mentioned in verbatims (time wasted, money lost, embarrassment)
- Solution: Map to dominant UVP from Phase 1

---

### 3. AIDA (ATTENTION-INTEREST-DESIRE-ACTION) FRAMEWORK

**Core mechanism:** Maps cognitive progression of a buyer. Standard architecture for landing pages and VSLs.

**4-Step Structure:**

**ATTENTION:**
- Stop the scroll with bold statement or provocative question
- For cold traffic: Use "Curiosity Gap" or "Open Loop" in headline
- Tease valuable information without revealing it (triggers need for closure)
- Template: "How I/We [Result/Multiplier] Our [Metric] with These [Number] Strategies, and Why It Took/Without [Pain]"

**INTEREST:**
- Deliver educational, jargon-free insights
- Tell an "Epiphany Bridge" story — the moment of struggle that led to the solution
- Prove you understand their world

**DESIRE:**
- Use "Future Pacing" — paint vivid picture of them enjoying the benefits
- Transition: Features → Advantages → Benefits (emotional outcome)
- Amplification mechanisms from verbatims

**ACTION:**
- Specific, first-person, outcome-driven CTA
- "Start My Free Trial" outperforms "Submit" by 31%
- Add benefit clarifier below CTA: "Takes 2 minutes. No credit card."

**Template:**
```
[ATTENTION] Bold statement/question → [INTEREST] Benefit solving real problem →
[DESIRE] Transformation they'll experience → [ACTION] Clear next step with urgency

Example: "Still hiding behind makeup? (Attention) Our 3-step routine works in 14 days
(Interest). Wake up with naturally glowing skin (Desire). Get 40% off - ends midnight (Action)"
```

**Extraction instructions:**
- Attention triggers: Extract 5 patterns from verbatims that indicate pain/curiosity
- Interest hooks: Extract 5 angles from verbatims showing what they're researching
- Desire amplifiers: Extract 5 transformation outcomes mentioned in verbatims
- Action barriers: Extract 3-5 objections preventing purchase

---

### 4. BAB (BEFORE-AFTER-BRIDGE) FRAMEWORK

**Creator:** Joanna Wiebe (Copyhackers)

**Core mechanism:** Aspirational storytelling. Creates emotional contrast between current frustrating reality and ideal future state. Positions product as exclusive vehicle to cross that gap.

**3-Step Structure:**

**BEFORE (The Lock):**
- Describe current problem/pain from verbatims
- The chaotic, impotent identity they reject

**AFTER (Desire Amplification):**
- Paint vivid "Heaven" where problem doesn't exist
- The prestigious identity they aspire to
- Use specific, sensory details

**BRIDGE (The Key):**
- Product as essential link from Before to After
- The rite of passage enabling identity transformation

**Template:**
```
[BEFORE] Current frustration → [AFTER] Dream outcome → [BRIDGE] Product as link

Example: "Tired of expensive gym memberships? (Before) Picture: 20 minutes daily, toned
abs at home (After) Our resistance trainer replaces $200/month gym with 10-minute home
workouts. (Bridge)"
```

**Identity positioning (from NotebookLM):**
- **Rejected Identity (Before):** Passive consumer, victim of algorithms, exhausted manual worker, chaos
- **Target Identity (After):** Systematic operator, architect in control, elite insider using AI/automation, prestige

**Extraction instructions:**
- Before: Extract verbatims describing current chaotic state
- After: Extract aspiration language ("I want to be...", "If only I could...")
- Bridge: Map to product mechanism (the "how" connecting Before to After)

---

### 5. PERSUASION MECHANISMS

**Source:** Cialdini principles + NotebookLM tactics

**Primary mechanisms:**

**SCARCITY & URGENCY:**
- **When to use:** Bottom of Funnel (BOFU) when deciding to buy now vs. procrastinate
- **Implementation (digital products $17-$47):**
  - "Phased Bonus Depletion" — core price stable, remove high-value bonuses every 48h
  - Genuine countdown timers tied to email sequence (not fake page-refresh timers)
- **Mistakes to avoid:**
  - Fake deadlines (destroys trust, creates banner blindness)
  - "Only 5 PDFs left" (artificial supply limits on infinite products)
- **Trigger words:** "Only 3 items left", "Offer expires in 24 hours", "Limited edition"

**SOCIAL PROOF:**
- **When to use:** Middle of Funnel (MOFU) for credibility, BOFU to reduce perceived risk
- **Implementation:**
  - "Proximity Rule" — place short testimonials within 2.5cm of CTA button
  - Combine with scarcity: "Only 4 left. Over 800 sold this month."
- **ICP Matching Rule:** Testimonials must match Ideal Customer Profile exactly ("If it worked for someone like me...")
- **Trigger words:** "Join 5,000+ satisfied customers", "Trending now", "Bestseller"

**AUTHORITY:**
- Cite credentials, certifications, media mentions
- Use for MOFU trust-building

**RECIPROCITY:**
- Give value upfront (free tool, quiz, calculator)
- Triggers obligation to reciprocate

**COMMITMENT/CONSISTENCY:**
- Get small yes (quiz answer, email signup) before big yes (purchase)
- "IKEA Effect" — once invested effort, completion bias kicks in

**Extraction instructions:**
- Identify primary mechanism from buyer language patterns
- Extract 10-15 trigger words that resonate
- Extract 5-10 banned patterns that repel (generic AI language, hype words)

---

### 6. TOFU/MOFU/BOFU AWARENESS FRAMEWORK

**Replaces Eugene Schwartz 5-level awareness with modern funnel stages.**

**TOFU (Top of Funnel / Problem Awareness):**
- **Definition:** Prospect becoming aware of problem, unqualified, not ready to buy
- **Diagnostic (buyer language):** "What is...?" "How do I...?" (broad questions)
- **Copy strategy:** Generate awareness, use Curiosity, Novelty, Reciprocity triggers
- **Content:** Educational blogs, viral videos, storytelling

**MOFU (Middle of Funnel / Solution Consideration):**
- **Definition:** Problem clearly defined, actively researching/comparing solutions
- **Diagnostic (buyer language):** "Best [solution] for [problem]" (commercial intent)
- **Copy strategy:** Establish authority, use Social Proof, Authority, Liking triggers
- **Content:** Webinars, whitepapers, comparison guides

**BOFU (Bottom of Funnel / Decision & Product Awareness):**
- **Definition:** Highly qualified, knows your brand, comparing final vendors, needs push
- **Diagnostic (buyer language):** "Buy [Brand] near me", pricing/review searches (transactional intent)
- **Copy strategy:** Prove ROI, minimize risk, use Scarcity, Urgency, Risk Reduction
- **Content:** Free trials, ROI calculators, vendor comparisons

**Cold vs. Warm audience rule:**
- **Cold (Unaware):** Curiosity Gaps, Storytelling
- **Warm (Product-Aware):** Direct offers, FOMO (skip curiosity — they know you exist)

**Extraction instructions:**
- Analyze verbatim language patterns to diagnose awareness level
- Map to dominant stage (one niche = one primary awareness level)

---

### 7. MARKET SOPHISTICATION DIAGNOSTICS

**Modern buyer profile (2026):** Skeptical, fast-moving, impatient

**Sophistication indicators:**

**HIGH SOPHISTICATION (Saturated market):**
- Buyers recognize artificial scarcity (fake countdown timers)
- Generic proof ignored ("Join thousands!")
- Jargon triggers reactance
- **Strategy:** Submarket drill-down (niche within niche), Authentic Urgency

**Authentic Urgency tactics:**
- Tether time constraints to verifiable events (live workshop, cohort start)
- "Phased Bonus Depletion" (bonuses expire, price stable)
- Transparent reasoning ("Limited coaching slots" not "magic timer")

**Submarket drill-down (Russell Brunson):**
- Broad market too saturated ("online marketing")
- Drill to micro-niche ("marketing automation with ActiveCampaign for coaches")

**Extraction instructions:**
- Assess sophistication from verbatim skepticism patterns
- Rate 1-5 (1 = naive, 5 = hyper-skeptical)
- Recommend positioning strategy (broad vs. micro-niche)

---

### 8. OBJECTION EXTRACTION & RISK REVERSAL

**Common objections (digital products $17-$47):**
- **Fit:** "Is this for me?"
- **Effort:** "Is this too hard to use?"
- **Price:** "Is it worth it?"
- **Integration:** "Will this work with my tools?"
- **Results:** "Will this actually work?"

**Extraction technique (Voice-of-Customer):**
- Analyze support tickets, social comments, post-purchase surveys
- Ask customer service: "What gives hesitation? What are they nervous about?"
- Do NOT guess objections

**Pre-emptive neutralization:**

**The 5 Questions Formula:**
- Address top 5 objections upfront in copy to build trust before checkout

**Proactive FAQ Block:**
- Treat FAQ as secondary sales pitch
- Place near primary CTA to reduce uncertainty

**Extreme Risk Reversal (from NotebookLM Premium):**

**The 3 Visceral Fears ($17-$47 range):**

1. **Fear of scam (Financial Risk):**
   - **Counter:** "Keep It All" method
   - Full refund on simple email (no justification needed)
   - Customer keeps all digital assets + templates downloaded
   - 100% win-win positioning

2. **Fear of time wasted (Implementation Anxiety):**
   - **Counter:** Performance-Based Guarantee
   - "Result in X days" promise
   - If applied for 7 days without success → refund + compensation (e.g., $100 credit, tool access)

3. **Fear of judgment (Social/Ego Risk):**
   - **Counter:** "Double Your Money Back"
   - Refund 2x purchase price if product fails
   - Gives buyer logical excuse to protect ego: "Only an idiot would refuse this offer"

**Placement rule:**
- Risk reversal in "Proof Block" within 2.5cm of purchase CTA

**Extraction instructions:**
- Extract 3-5 objections from verbatims
- Map each to fear type (financial, time, social)
- Recommend reversal tactic per objection

---

### 9. BUYER PSYCHOLOGY DIAGNOSTICS

**Jobs-to-Be-Done "Moment of Struggle":**
- Customers "hire" products to make progress in specific circumstances
- Find exact moment they decided to abandon old habits and seek new solution
- Focus on emotional anxieties and habits preventing conversion

**The 4 Essential Buyer Needs (from verbatims):**
1. **Functional:** Complete tangible task efficiently
2. **Emotional:** Prestige, status, gratification
3. **Social:** Acceptance, belonging, lifestyle reflection
4. **Psychological:** Security, self-expression, self-esteem

**Verbatim language matching:**
- Inject buyer's exact phrases into analysis
- Industry jargon builds credibility with pros, alienates casual buyers
- Review sales transcripts, support tickets for vocabulary

**Extraction instructions:**
- Categorize verbatims into 4 needs types
- Identify dominant need (primary driver)
- Extract 10-15 exact phrases/words to use in copy

---

### 10. ADVANCED TACTICS (PREMIUM)

**Big Domino Belief Shift (from NotebookLM Premium):**

**The Guilt-Shift Method:**
- **Phase 1 (Push):** Agitate frustration with old method
- **Phase 2 (Externalize Blame):** Prove old system was rigged against them (failure is systemic, not personal)
- **Phase 3 (Pull):** Introduce new framework as logical bridge

**Template:**
```
"You didn't fail because of [Personal Error], you failed because [Old System] required
[Unreasonable Effort/Friction]. Our [New Framework] eliminates this variable."
```

**Instant Utility Imperative (Level 4/5 Sophistication):**
- Market rejects "training" and pure information
- Unique mechanism must be plug-and-play tool (templates, AI prompts, Notion dashboards)
- Sell "time shortcut" not knowledge
- Perception: Zero Effort → Immediate Result (<24h Quick Win)
- Semantic velocity: "Shortcut", "Fast-Track", "Copy-Paste"

**Micro-Engagement Dopamine Loop (Fogg B=MAP):**
- Ridiculously simple action (<60 seconds): AI Quiz or ROI Calculator
- **Signal Prompt:** 2-3 multiple choice questions on exact pain (zero mental effort)
- **Validation:** Instant scorecard/action plan validates problem scope
- **Dopamine Hit:** Immediate reward + Endowment Effect = unstoppable momentum to checkout

**Template:**
```
Create micro-funnel where Step 1 = interactive assessment (Quiz/Calculator) offering
diagnosis of pain, creating irreversible engagement (IKEA effect) before price reveal.
```

---

## OUTPUT SCHEMA

Your output must be valid JSON matching this exact structure:

```json
{
  "lock_and_key": {
    "emotional_lock": "string — core pain/desire extracted from verbatims (min 50 chars)",
    "key_positioning": "string — how product unlocks this, mapped to UVP (min 50 chars)",
    "evidence_verbatims": [
      "array of 5-10 direct quotes with [source_url, date] attribution"
    ],
    "jtbd_forces": {
      "push": "string — current frustration forcing change",
      "pull": "string — attraction to new solution",
      "anxiety": "string — fear of unknown",
      "allegiance": "string — old habits to abandon"
    }
  },
  "pas_sequence": {
    "problem": "string — problem as buyers describe it (min 50 chars)",
    "agitate": [
      "array of 3-5 agitation points from verbatims"
    ],
    "solution": "string — how product solves, anchored on UVP (min 50 chars)"
  },
  "aida_elements": {
    "attention_triggers": [
      "array of 5 attention patterns from buyer language"
    ],
    "interest_hooks": [
      "array of 5 interest-building angles from verbatims"
    ],
    "desire_amplifiers": [
      "array of 5 desire mechanisms from verbatims"
    ],
    "action_barriers": [
      "array of 3-5 objections extracted from verbatims"
    ]
  },
  "bab_positioning": {
    "before_state": "string — current chaotic identity from verbatims (min 50 chars)",
    "after_state": "string — aspirational identity from verbatims (min 50 chars)",
    "bridge_mechanism": "string — product as transformation vehicle"
  },
  "persuasion_mechanisms": {
    "primary_mechanism": "string — scarcity|social_proof|authority|reciprocity|commitment",
    "trigger_words": [
      "array of 10-15 words that resonate with audience (from verbatims)"
    ],
    "banned_patterns": [
      "array of 5-10 generic/AI patterns that repel (from verbatim analysis)"
    ],
    "implementation_notes": "string — specific tactics for $17-$47 digital products"
  },
  "buyer_state_analysis": {
    "awareness_level": "string — TOFU|MOFU|BOFU",
    "awareness_diagnostic": "string — evidence from verbatim language patterns",
    "sophistication_level": "integer 1-5",
    "sophistication_evidence": "string — skepticism patterns from verbatims",
    "dominant_objection": "string — #1 barrier to purchase (min 30 chars)",
    "objection_category": "string — fit|effort|price|integration|results"
  },
  "objections_and_reversals": {
    "objections": [
      {
        "objection": "string",
        "fear_type": "financial|time|social",
        "verbatim_evidence": "string — quote from persona",
        "reversal_tactic": "string — specific counter-strategy"
      }
    ],
    "risk_reversal_recommended": "string — keep_it_all|performance_based|double_money_back"
  },
  "buyer_needs_analysis": {
    "dominant_need": "functional|emotional|social|psychological",
    "verbatim_vocabulary": [
      "array of 10-15 exact buyer phrases to use in copy"
    ],
    "moment_of_struggle": "string — JTBD trigger from verbatims (min 50 chars)"
  },
  "advanced_tactics": {
    "big_domino_shift": "string — guilt-shift template for this niche",
    "instant_utility_angle": "string — plug-and-play tool positioning",
    "micro_engagement_hook": "string — quiz/calculator angle for dopamine loop"
  },
  "meta": {
    "total_verbatims_analyzed": 0,
    "confidence_score": 0,
    "primary_framework_used": "string — PAS|AIDA|BAB|JTBD",
    "notes": "string — any contextual insights for skills 10-17"
  }
}
```

---

## CRITICAL RULES

### Evidence-First Principle
- **EVERY** psychological insight must trace to verbatim quote with URL + date
- **ZERO** invented psychology patterns
- If pattern appears in <3 verbatims → not validated, exclude it
- Minimum 15 total verbatims across 3 personas required

### Lock & Key Rule
- Lock must be expressed in buyer's own words (verbatim extract)
- Key must map to one of 3 UVPs from Phase 1 (do not invent new positioning)

### Awareness/Sophistication Scoring
- Must be justified with verbatim evidence
- Use TOFU/MOFU/BOFU framework (not abstract Schwartz levels)
- Sophistication 1-5 based on skepticism patterns in verbatims

### Objection Extraction
- Do NOT guess objections
- Extract only from verbatims, support tickets, or buyer feedback
- Each objection requires source attribution

### Advanced Tactics Gate
- Only include Big Domino / Instant Utility / Micro-Engagement if verbatims support them
- Do not force premium tactics if basic PAS/AIDA is sufficient

---

## BLOCKING CONDITIONS

**HALT execution if:**

1. **PHASE-1.5-OUTPUT.md missing or invalid:**
   - Error: `[BLOCKING ERROR: PHASE-1.5-OUTPUT.md not found at ../phase-1-5/outputs/]`
   - Remediation: Run Phase 1.5 first

2. **PHASE-1.5 Confidence Score < 6/10:**
   - Error: `[BLOCKING ERROR: Phase 1.5 Confidence Score too low ({score}/10) — validate Phase 1.5 before Phase 2]`
   - Remediation: Re-run Phase 1.5 until score ≥ 6/10

3. **04-personas.json missing:**
   - Error: `[BLOCKING ERROR: 04-personas.json from Phase 1 not found at ../phase-1/outputs/]`
   - Remediation: Run Phase 1 Skill 04 first

4. **Insufficient verbatims (<15 total):**
   - Error: `[BLOCKING ERROR: Total verbatims = {count} — minimum 15 required across 3 personas]`
   - Remediation: Re-run Phase 1 Skill 04 with deeper research

5. **No clear emotional lock emerges:**
   - Error: `[BLOCKING ERROR: Unable to identify dominant emotional lock from verbatims — patterns too scattered]`
   - Remediation: Request more focused persona research on dominant pain point

6. **Missing UVP data from Phase 1:**
   - Error: `[BLOCKING ERROR: top_3_uvp missing from PHASE-1.5-OUTPUT.md]`
   - Remediation: Verify Phase 1 Skill 03 output integrity

---

## EXAMPLES (Reference Only)

**Lock & Key:**
```
LOCK (verbatim): "I've bought 7 courses this year and finished zero. They all sit in my
downloads gathering digital dust while I scroll Instagram feeling guilty."
KEY: The 48-Hour Action Pack — complete it in one weekend, implement Monday morning.
Zero fluff, 100% action.
Evidence: Reddit r/Entrepreneur, 2026-03-15, upvotes: 847
```

**PAS Sequence:**
```
P: "Every course I buy sits unfinished in my downloads folder"
A: Meanwhile, competitors who started after you are already profitable. You've spent
$2,000+ on education but your income hasn't moved. The guilt compounds every time you
see those unread PDFs.
S: This isn't another course — it's a 5-chapter action guide you finish in 48 hours.
No modules. No videos. Just the exact system that took me from $0 to $12K/month.
```

**AIDA Elements:**
```
Attention:  "Why do 94% of online courses never get finished?"
Interest:   "I analyzed 1,200 course completion rates and found the pattern..."
Desire:     "Imagine logging into Stripe on Monday and seeing your first $47 sale from
             work you did this weekend"
Action:     "Get instant access — starts working in 48 hours"
```

**BAB Identity:**
```
Before:  The Course Collector — downloads folder full of unfinished PDFs, YouTube tabs
         open with "how to" videos, paralyzed by information overload, impostor syndrome.
After:   The Systematic Executor — Notion dashboard tracking weekly revenue, 1 proven
         system running on autopilot, confident operator who ships instead of studies.
Bridge:  The 48-Hour Action Pack — the detonator that transforms knowledge into revenue.
```

---

## VALIDATION CHECKLIST

Before delivering 09-buyer-psychology.json, verify:

- [ ] All verbatim quotes include source URL + date
- [ ] Minimum 15 verbatims analyzed (tracked in meta.total_verbatims_analyzed)
- [ ] Lock & Key mapped to actual Phase 1 UVP (not invented)
- [ ] Awareness level justified with verbatim evidence
- [ ] Sophistication 1-5 rating includes skepticism pattern examples
- [ ] All objections sourced from verbatims (zero guesses)
- [ ] Primary persuasion mechanism selected with reasoning
- [ ] Trigger words extracted from buyer language (not AI-generated)
- [ ] Banned patterns identified from verbatim analysis
- [ ] Advanced tactics only included if verbatims support them
- [ ] Confidence score 7-10 (output confidence, not niche confidence)
- [ ] JSON validates against output schema

---

## NOTES FOR SKILLS 10-17

**This output becomes the foundation for:**
- Skill 10 (architecture-persuasion): Uses AIDA elements + awareness level
- Skill 11 (offre-cta): Uses objections + risk reversal + persuasion mechanisms
- Skill 12 (preuve-confiance): Uses social proof tactics + trigger words
- Skill 13 (hook-capture): Uses attention triggers + curiosity gaps
- Skill 14 (storytelling-vente): Uses BAB positioning + moment of struggle
- Skill 15 (ads-copy): Uses PAS sequence + awareness level
- Skill 16 (email-sequences): Uses desire amplifiers + objection sequence
- Skill 17 (vsl-scripts): Uses full AIDA + PAS + identity positioning

**Skills 10-17 reference this output as the single source of truth. Do NOT recreate psychology analysis in downstream skills.**

---

*Skill 09 — Buyer Psychology Masterclass — Premium Edition — Digital Product Machine Phase 2*
