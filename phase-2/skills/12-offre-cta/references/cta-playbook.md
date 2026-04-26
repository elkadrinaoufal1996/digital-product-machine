# CTA PLAYBOOK — Reference for Skill 12
## Source: Unbounce CTA research, Copyhackers, Peep Laja (CXL), Joanna Wiebe
## Load this file when generating: cta_matrix section

---

## 1. THE 6 NON-NEGOTIABLE CTA RULES

### Rule 1 — ONE CTA per page
- Multiple CTAs = decision paralysis = conversion drop
- Research: +70% conversion when single CTA vs multiple competing CTAs
- Exception: Repeat the SAME CTA button multiple times on a long LP (Hero, Offer, Risk Reversal blocks)
- Each repeat = same text, same destination, same button style

### Rule 2 — First Person voice mandatory
- "Start MY trial" vs "Start YOUR trial" → up to +90% clicks (Unbounce data)
- The prospect mentally owns the result BEFORE purchasing
- Implementation: every button_text must start with "Je", "Oui je", "Mon", "Ma", "Mes"

**Conversion comparison:**
| ❌ Generic | ✅ First Person | Lift |
|-----------|----------------|------|
| "Get Access" | "Accéder à mon programme →" | +31% |
| "Start Now" | "Commencer ma transformation →" | +24% |
| "Download" | "Télécharger mon guide gratuit →" | +14% |
| "Buy Now" | "Oui, je veux [résultat] pour $47 →" | +47% |

### Rule 3 — Outcome-driven, never transactional
**Banned words in button text (friction triggers):**
- Submit / Soumettre (-3% minimum)
- Buy / Acheter (-8%)
- Register / S'inscrire (-5%)
- Click Here / Cliquez ici (-11%)
- Learn More / En savoir plus (-7% for primary CTA)
- Sign Up / S'inscrire (-6%)

**Replacement formula:**
`"[Affirmative Particle] + [First Person Verb] + [Specific Outcome] →"`

Examples:
- "Oui, je veux mes 10 heures/semaine libérées →"
- "Accéder à mon système anti-procrastination →"
- "Rejoindre mes 847 membres et perdre 8kg →"

### Rule 4 — Micro-copy under every button (MANDATORY)
Format: `"✓ [Instant benefit] · ✓ [Guarantee] · ✓ [Friction removal]"`

**Micro-copy templates by position:**
| Position | Template | Impact |
|----------|----------|--------|
| Hero CTA | "✓ Accès immédiat · ✓ Garantie 60 jours · ✓ Sans engagement" | +9 to +15% |
| Offer CTA | "✓ Téléchargement immédiat · ✓ Satisfait ou remboursé · ✓ Prix bloqué aujourd'hui" | +12% |
| Risk Reversal | "✓ 60 jours pour tester · ✓ Aucun risque · ✓ [Keep Product clause if applicable]" | +11% |
| Mobile sticky | "🔒 Sécurisé · Accès en 2 min · Garantie 60j" | +9% cart add |

**Research note:** Micro-copy lifts conversions +9% to +15% across device types.
On mobile, adding a lock icon (🔒) adjacent to the sticky button reduces security anxiety.

### Rule 5 — Above the fold (ATF) placement mandatory
- ATF CTA: +17% to +317% conversion depending on page length
- For VSL funnels: ATF CTA appears AFTER video play (not before — creates curiosity gap)
- For direct sales pages: Hero CTA visible without scroll on 1440px desktop AND 390px mobile
- Design constraint: CTA button must be the HIGHEST contrast element in the hero block

### Rule 6 — Sticky button on mobile
- Sticky bottom CTA bar on mobile: +9% cart additions
- Appears after user scrolls past hero block (triggered at 400px scroll depth)
- Content: shortened CTA text + price + lock icon
  → "Accéder pour $47 🔒"
- Must include 1-line micro-copy (fits ~35 chars)
  → "Garantie 60 jours incluse"

---

## 2. CTA MATRIX — 9 LP Blocks (from Skill 10)

Mapping one CTA intent per relevant block. Blocks 2, 3, 7 = no CTA (agitation phase — adding CTA here breaks emotional arc).

### Block 1 — HERO
**CTA Type:** Primary desire — the dream outcome
**Trigger:** Above the fold, highest priority placement
**Formula:** `"Oui, je veux [Résultat Principal spécifique] →"`

**Source data:** Pull dream_outcome from `grand_slam_offer.value_equation.dream_outcome`
**Constraint:** Must match blink_test_hero from skill 10 — same promise, different syntax

**Example outputs by awareness level:**
- BOFU: "Oui, je veux perdre mes 10kg sans régime draconien →"
- MOFU: "Oui, je veux enfin un système qui marche pour moi →"
- TOFU: "Découvrir pourquoi j'accumule les dettes malgré mon salaire →"

---

### Block 2 — PROBLEM
**CTA:** NONE
**Reason:** Buyer is in emotional agitation mode. A CTA here interrupts the PAS sequence and reduces conversion. Let the pain breathe.

---

### Block 3 — AGITATE
**CTA:** NONE
**Reason:** Still in the agitation arc. Adding CTA = breaking the psychological momentum toward Solution block. Trust the sequence.

---

### Block 4 — SOLUTION (Mechanism Reveal)
**CTA Type:** Mechanism curiosity — intermediate commitment
**Formula:** `"Voir comment [Nom Mécanisme Unique] fonctionne →"`
**Trigger:** Below mechanism explanation, before proof blocks

**Source data:** Pull unique_mechanism_name from `grand_slam_offer.unique_mechanism_name`
**Example:** "Voir comment le Système Triple Levier fonctionne →"

---

### Block 5 — HOW IT WORKS
**CTA Type:** Engagement / Progress commitment
**Formula:** `"Je veux accéder à [Mécanisme] maintenant →"`
**Trigger:** After step-by-step breakdown, before testimonials

**Psychology note:** At this point, buyer has mentally engaged with the system.
Commitment/Consistency bias (Cialdini) activates — a CTA here converts well.

---

### Block 6 — PROOF / SOCIAL PROOF
**CTA Type:** Social conformity + FOMO
**Formula:** `"Rejoindre [N] personnes qui ont déjà [Résultat exact] →"`
**Trigger:** Immediately below testimonial grid

**Source data:** Pull actual numbers from proof blocks in skill 10 architecture
**ICP Matching Rule:** N testimonials shown must match persona demographics from skill 09

**Proximity Rule implementation:**
```
[TESTIMONIAL GRID — 3 results-focused testimonials]
[CTA BUTTON — within 2.5cm visual distance of last testimonial]
[MICRO-COPY BELOW BUTTON]
```

---

### Block 7 — OBJECTIONS / FAQ
**CTA:** NONE
**Reason:** This is the trust-restoration phase. Adding a CTA here creates pressure
at the exact moment the buyer needs reassurance. Let FAQ do its work. CTA follows in Block 8.

---

### Block 8 — OFFER / THE STACK
**CTA Type:** PRIMARY — value anchor + price reveal
**Formula:** `"Oui ! Je veux [Offre Complète] pour seulement $[Prix] →"`
**Trigger:** Below full stack revelation, AFTER price is shown

**This is the highest-converting CTA on the page.**
Design note: Button color = highest contrast vs page background.
No competing visual elements within 100px of this button.

**Example:** "Oui ! Je veux tout le pack + mes 3 bonus pour seulement $47 →"

---

### Block 9 — RISK REVERSAL + FINAL CTA
**CTA Type:** Guarantee anchor — eliminates last objection
**Formula:** `"Essayer sans risque pendant [N] jours →"`
**Trigger:** Immediately below guarantee explanation

**Psychology note:** This CTA removes "but what if it doesn't work?" — the final holdout objection.
The word "essayer" (try) reduces commitment perception vs "acheter" (buy).

**Micro-copy for this position:**
"✓ Si vous n'êtes pas satisfait(e) — remboursement total, pas de question posée"

---

## 3. VOICE OF CUSTOMER (VoC) RULES — CTAs from Buyer Language

### The Mirror Principle
CTA copy that mirrors the buyer's own language converts 23-41% better than
copy written from the seller's perspective (Joanna Wiebe, Copyhackers).

**Process:**
1. Load `verbatims_bank` from `09-buyer-psychology.json`
2. Extract the 5 most emotionally charged phrases
3. Reverse-engineer each phrase into a CTA format
4. Select the one with highest specificity + emotional weight

**Example extraction:**
```
Verbatim: "I just want to wake up and not panic about money for once"
↓ Mirror transformation
CTA: "Oui, je veux me réveiller sans panique financière →"
```

```
Verbatim: "I've tried everything and I'm exhausted. I need something that actually sticks."
↓ Mirror transformation
CTA: "Accéder au seul système qui 'colle' même quand on est épuisé →"
```

### Banned patterns — VoC violations
The following patterns indicate LLM-generated generic copy. Any CTA containing
these patterns must be regenerated using actual verbatim data:

**Generic patterns to reject:**
- "Transform your life" → too abstract, no measurable outcome
- "Achieve your goals" → zero specificity
- "Start your journey" → cliché, triggers skepticism
- "Unlock your potential" → banned (sounds like every other product)
- "The ultimate [X]" → hyperbole, no credibility
- "Revolutionary" / "Game-changing" → red flags for 2026 buyers
- "Limited time offer" without specific end date/reason → fake scarcity signal
- Any CTA that could appear on a competitor's page unchanged → not differentiated

**Test:** Can this exact CTA appear on 3 competitors' pages? If yes → rewrite.

---

## 4. CTA COPY FORMULAS — Quick Reference

### By Awareness Level (from skill 09)

**TOFU (Unaware / Problem-Aware):**
- Lead with curiosity, not commitment
- "Découvrir pourquoi [Symptom the persona has] →"
- "Voir ce que [N] personnes ont découvert sur [Problem] →"
- Micro-copy: "✓ Gratuit · ✓ 3 minutes · ✓ Aucune carte requise"

**MOFU (Solution-Aware):**
- Lead with mechanism differentiation
- "Voir comment [Mécanisme] résout [Problem] sans [Friction] →"
- "Comparer ma méthode aux autres approches →"
- Micro-copy: "✓ Résultats en 48h · ✓ Aucune expérience requise · ✓ Garantie incluse"

**BOFU (Product-Aware / Decision-Ready):**
- Lead with value stack and guarantee
- "Oui, je prends le pack complet pour $[Prix] →"
- "Accéder maintenant — garantie 60 jours incluse →"
- Micro-copy: "✓ Accès immédiat · ✓ Garantie satisfait ou remboursé · ✓ [Fast-Action Bonus] inclus jusqu'au [Date]"

---

### By Funnel Type (from skill 11)

**Simple Direct:**
- Hero + Offer + Risk Reversal CTAs (3-CTA structure)
- High urgency language — buyer is warm, ready to decide

**Lead Magnet 5-Day:**
- Lead magnet CTA (Day 0) → nurture → sales CTA (Day 5)
- Day 0 CTA softer: "Accéder à mon guide gratuit →"
- Day 5 CTA direct: "Oui, je veux le programme complet →"

**VSL:**
- CTA appears ONLY after video ends (or at 70% watch point)
- Button hidden until triggered — creates anticipation
- Post-video: "Je suis prêt(e) — accéder au programme →"

---

## 5. BUTTON DESIGN SPECS (for developer handoff)

| Element | Specification |
|---------|---------------|
| Font size | 18-22px, bold |
| Padding | 18px vertical, 36px horizontal |
| Border radius | 6-8px (not pill — looks clickable, not decorative) |
| Arrow | → appended to all primary CTAs (directional cue +7%) |
| Color | Highest contrast to background — typically brand accent color |
| Shadow | Subtle box-shadow — increases perceived clickability +4% |
| Mobile min-height | 56px (touch target accessibility) |
| Hover state | Darken 10%, subtle scale 1.02 |
| Micro-copy distance | 8-12px below button, smaller font (14px), muted color |

---

*File: references/cta-playbook.md — Loaded by SKILL.md when generating cta_matrix section*
*Source doctrine: Unbounce (90% stat), Copyhackers (VoC methodology), CXL Institute, Joanna Wiebe*
