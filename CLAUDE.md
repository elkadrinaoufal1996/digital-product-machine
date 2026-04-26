# CLAUDE.md — Digital Product Machine

---

## 1. CE QU'EST LE SYSTÈME

Le **Digital Product Machine** est un pipeline autonome de création et vente de produits numériques ($17-$47). Il prend en entrée un marché (`--market=US`) et produit en sortie un système complet de positionnement, branding, copy et conversion — sans intervention humaine sauf validation finale.

### Les 3 Phases

```
PHASE 1 — MARKET INTELLIGENCE
Skill 01 → 02 → 03 → 04 → 05
Input: --market=US
Output: PHASE-1-OUTPUT.md

PHASE 1.5 — BRAND FOUNDATION
Skill 06 → 07 → 08
Input: PHASE-1-OUTPUT.md
Output: PHASE-1.5-OUTPUT.md

PHASE 2 — SALES COPY & CONVERSION
Skill 09 → 10 → 11 → 12 → [13-18]
Input: PHASE-1.5-OUTPUT.md + 04-personas.json
Output: Sales page complète + funnel + copy
```

### Architecture Technique

- **Agents:** `scraper.py` (Skill 01) + `analyst.py` (Skills 02-18)
- **Orchestrateur:** `phase1.py` (Phase 1), `phase1-5.py` (Phase 1.5)
- **LLM:** Claude API (`claude-sonnet-4-20250514`)
- **Data sources:** Apify (Gumroad, Amazon, Etsy, TikTok, Instagram), Tavily (Reddit)
- **Env vars:** `ANTHROPIC_KEY`, `APIFY_TOKEN`, `FIRECRAWL_KEY`, `TAVILY_KEY`
- **Format:** JSON-in / JSON-out pour tous les skills sauf Skill 05 (→ markdown)

### Principe fondamental

Chaque skill a **une seule responsabilité**. Aucun skill n'invente de données — tout trace vers une source primaire avec URL+date. Les blocking conditions arrêtent le pipeline plutôt que produire un output faible.

---

## 2. ÉTAT RÉEL DU PROJET

### PHASE 1 — MARKET INTELLIGENCE

| # | Skill | Agent | Input | Output | Statut |
|---|-------|-------|-------|--------|--------|
| 01 | Market Discovery | scraper.py | `--market=US` | `01-market-discovery.json` | ✅ SKILL.md complet + scraper.py 795 lignes |
| 02 | Niche Idea Scorer | analyst.py | `01-market-discovery.json` | `02-scored.json` | ✅ SKILL.md complet + scoring matrix A/B |
| 03 | Competitor X-Ray | analyst.py | `02-scored.json` | `03-xray.json` | ✅ SKILL.md complet + 6 gap types |
| 04 | Buyer Intelligence | analyst.py | `03-xray.json` | `04-personas.json` | ✅ SKILL.md complet + 3 sources primaires |
| 05 | Positioning & Launch | analyst.py | `02+03+04` | `PHASE-1-OUTPUT.md` | ✅ SKILL.md complet + 7 sections |

**Scripts Phase 1:** `scraper.py` (795 lignes), `analyst.py` (435 lignes), `phase1.py` (299 lignes)
**References Phase 1:** `elimination-filters.md`, `scoring-protocols.md`, `gap-framework.md`, `persona-framework.md`, `value-stack-rules.md`

### PHASE 1.5 — BRAND FOUNDATION

| # | Skill | Agent | Input | Output | Statut |
|---|-------|-------|-------|--------|--------|
| 06 | Visual Identity | analyst.py | `PHASE-1-OUTPUT.md` | `06-visual-identity.json` | ✅ SKILL.md complet (185 lignes) |
| 07 | Brand Voice | analyst.py | `input-schema.json` + `06` | `07-brand-voice.json` | ✅ SKILL.md complet (253 lignes) |
| 08 | Marketing Angles | analyst.py | `06+07` + Phase 1 outputs | `08-marketing-angles.json` + `PHASE-1.5-OUTPUT.md` | ✅ SKILL.md complet (287 lignes) |

### PHASE 2 — SALES COPY & CONVERSION

| # | Skill | Agent | Input | Output | Statut |
|---|-------|-------|-------|--------|--------|
| 09 | Buyer Psychology Masterclass | analyst.py | `PHASE-1.5-OUTPUT.md` + `04-personas.json` | `09-buyer-psychology.json` | ✅ SKILL.md complet (659 lignes) |
| 10 | Architecture Persuasion | analyst.py | `09` + `PHASE-1.5-OUTPUT.md` | `10-architecture.json` | ✅ SKILL.md complet (938 lignes) |
| 11 | Funnel Architecture | analyst.py | `09+10` + `PHASE-1.5-OUTPUT.md` | `11-funnel-architecture.json` | ✅ SKILL.md complet (498 lignes) |
| 12 | Offre & CTA | analyst.py | `09+10+11` | `12-offre.json` | ✅ SKILL.md complet (374 lignes) |
| 13 | Preuve & Confiance | analyst.py | TBD | TBD | 🔲 À construire |
| 14 | Hook Capture | analyst.py | TBD | TBD | 🔲 À construire |
| 15 | Storytelling Vente | analyst.py | TBD | TBD | 🔲 À construire |
| 16 | Ads Copy | analyst.py | TBD | TBD | 🔲 À construire |
| 17 | Email Sequences | analyst.py | TBD | TBD | 🔲 À construire |
| 18 | VSL Scripts | analyst.py | TBD | TBD | 🔲 À construire |

**References Phase 2:** `cta-playbook.md`, `grand-slam-framework.md`, `guarantee-scarcity.md`

---

## 3. PROCESSUS STANDARD DE CRÉATION D'UN SKILL

### Step A — Définir le rôle

Avant de toucher un fichier, répondre à ces 4 questions :
1. Quelle est la **responsabilité unique** de ce skill ? (une phrase, pas une liste)
2. Quel est son **input exact** ? (fichier(s) JSON ou markdown, avec chemin)
3. Quel est son **output exact** ? (nom de fichier + structure de premier niveau)
4. Quelle est la **blocking condition** qui doit arrêter le pipeline ?

Le skill ne fait qu'une chose. Si la réponse à Q1 contient "et", le skill est mal découpé.

### Step B — Générer les questions pour NotebookLM

Produire une liste de questions précises à soumettre à NotebookLM pour extraire la matière premium des sources uploadées. Les questions doivent couvrir :
- Les frameworks de conversion applicables à ce skill (ex: PAS, AIDA, JTBD)
- Les métriques de performance mesurables (ex: "+34% lift", "4.8-6.2% CVR")
- Les règles non-négociables issues de la littérature (ex: "CTA first-person +31%")
- Les formules et structures exactes (ex: "60-30-10 color ratio")
- Les mots interdits et les mots de puissance si copy-related

Format des questions : direct, une par ligne, commençant par "Quels sont...", "Quelle est la règle...", "Donne-moi les métriques...", "Liste les..."

### Step C — Générer le SKILL.md

Avec la matière extraite de NotebookLM, générer le SKILL.md directement. Structure obligatoire :

```markdown
# SKILL [N] — [NOM EN MAJUSCULES]

## RÔLE
[Une phrase. Responsabilité unique. Inclure ce que le skill N'EST PAS.]

## INPUTS
[Liste des fichiers requis avec chemin exact]

## OUTPUT
[Nom du fichier + structure JSON de premier niveau]

## AGENT
[scraper.py OU analyst.py]

## EXECUTION STEPS
[Étapes numérotées. Chaque étape = une action atomique.]

## FRAMEWORKS & RÈGLES
[Tous les frameworks avec métriques exactes]

## BLOCKING CONDITIONS
[Conditions qui arrêtent le pipeline avec message d'erreur exact]

## OUTPUT SCHEMA
[Structure JSON complète avec types et exemples]
```

Règles de génération :
- Toutes les métriques sont des chiffres réels (jamais "~" ou "environ")
- Tous les exemples sont dans le vrai niche du projet, pas des placeholders
- Les formules sont écrites en entier, pas résumées
- Zéro placeholder comme "[INSERT HERE]" — le skill est exécutable tel quel

### Step D — Validation et mise à jour CLAUDE.md

Avant de clore le skill :
1. Vérifier que l'output-schema.json est cohérent avec le SKILL.md
2. Vérifier que l'input-schema.json du skill suivant accepte cet output
3. Tester la blocking condition la plus critique manuellement
4. Mettre à jour le tableau de statut dans ce CLAUDE.md (statut → ✅ SKILL.md complet)

---

## 4. RÈGLES DE DEBUG

**Les bugs se règlent au moment du run, pas pendant la construction.**

Pendant la création d'un skill :
- Ne pas anticiper les edge cases non confirmés
- Ne pas ajouter de try/except pour des scénarios hypothétiques
- Ne pas valider les données au-delà des boundaries réelles (input utilisateur, APIs externes)
- Ne pas écrire de fallbacks pour des erreurs qui n'ont pas encore eu lieu

Au moment du run, si un bug apparaît :
1. Lire le message d'erreur exact — ne pas deviner
2. Identifier le fichier et la ligne
3. Corriger la cause racine, pas le symptôme
4. Ne jamais contourner une blocking condition pour faire avancer le pipeline

Les blocking conditions sont des features, pas des bugs. Si le pipeline s'arrête, c'est qu'un input est invalide — corriger l'input, pas la condition.

---

## 5. RÈGLES DE TRAVAIL DE CLAUDE

1. **Mise à jour automatique de ce fichier** — après chaque skill complété (Step D), je mets à jour le tableau de statut en section 2 sans que l'utilisateur ait à le demander.

2. **Un skill à la fois** — je ne commence pas le skill N+1 avant que le skill N soit validé (SKILL.md complet + schemas cohérents + statut mis à jour).

3. **Aucune invention** — si une métrique, un framework ou une règle n'est pas dans le matériau fourni par NotebookLM ou dans les fichiers existants, je la demande. Je ne comble pas les lacunes avec des généralisations.

4. **Output exécutable** — chaque SKILL.md que je génère doit pouvoir être chargé tel quel par analyst.py comme system prompt et produire un output JSON valide. Pas de templates, pas de placeholders.

5. **Schemas d'abord** — avant d'écrire le SKILL.md, je vérifie que l'input-schema.json du skill précédent existe et est cohérent. Si non, je le crée d'abord.

6. **Pas de commentaires dans le code** — sauf pour les invariants non-évidents ou les workarounds documentés (ex: comportement spécifique d'une API Apify).

7. **Aucun fichier de documentation non demandé** — je ne crée pas de README, de diagrammes ou de fichiers d'analyse intermédiaires. Le SKILL.md est la documentation.

8. **Respect de la chaîne de dépendances** — chaque skill consomme exactement les outputs listés. Je ne court-circuite pas la chaîne pour "simplifier".
