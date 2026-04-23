# Scoring Protocols — Skill 02

Reference for the three non-negotiable scoring rules applied in Skill 02.
These protocols are scoped to Skill 02 only. Do not duplicate in adjacent skills.

---

## Protocol 1 — Zero-Error Calculation (Chain of Thought)

Every matrix calculation must be shown step by step before displaying any score table.

**Required format:**
```
NICHE: [Name]
MATRIX A CALCULATION:
- Proven Demand: [raw_score] × 4 = [weighted]
- Monetization:  [raw_score] × 3 = [weighted]
- Virality:      [raw_score] × 2 = [weighted]
- Accessibility: [raw_score] × 1 = [weighted]
SUM CHECK: [w1] + [w2] + [w3] + [w4] = [total]
VERIFICATION: [total] ✓ or ❌ RECALCULATE
```

Rules:
- Never display a score table before completing the chain of thought
- If sum ≠ displayed total → STOP → recalculate → restart the matrix
- Apply identically for Matrix B (4 criteria × weights 4/3/2/1)

---

## Protocol 2 — Payment Reality Filter (Demand Tier Assignment)

Every niche receives a Tier before any score is assigned to Proven Demand.

**Tier hierarchy:**

| Tier | Evidence Required | Demand Score Ceiling |
|------|------------------|----------------------|
| TIER 1 | Transaction confirmation: Gumroad ≥500 sales OR Kindle BSR <10K with recent reviews OR active paid enrollment | No cap (8-10 possible) |
| TIER 2 | Demand proxy: TikTok >500K views OR SEO >10K/month OR Reddit engagement | Capped at 7/10 |
| TIER 3 | No payment evidence found | Capped at 5/10 |

**Blocking rule:**
- Score > 7 on Demand with Tier 2 or Tier 3 = SCORING ERROR
- Verdict 🟢 GO with Tier 2 or Tier 3 = BLOCKED → auto-downgrade to 🟡 CONDITIONAL GO

**Documentation required in output:**
```json
"tier_demand": "TIER_1",
"tier_evidence": "Gumroad product 'X' shows 1,247 sales — URL: https://..."
```

---

## Protocol 3 — VC Pessimism (Mandatory Counter-Arguments)

For any raw score ≥ 7/10 on any criterion in either matrix:

**Required format:**
```
⚠️ VC Challenge [Criterion name]:
[Specific reason why this score could be 1-2 points lower]
```

Valid counter-argument types:
- Seasonality risk: "Sales spike may be tied to Q4 gifting cycle"
- Recency risk: "BSR rank observed once — no rank history available to confirm stability"
- Supply risk: "Content gap exists today but 3 well-funded competitors announced products in this angle"
- Platform risk: "TikTok reach depends on algorithm that may not favor this niche type"
- Competition risk: "Differentiation is marginal — top competitor could copy this angle in <30 days"

Invalid counter-arguments (too vague):
- ❌ "Competition might increase"
- ❌ "Market could change"
- ❌ "There are risks"

A score ≥ 7 without a specific, sourced VC Challenge = incomplete scoring. Do not deliver.
