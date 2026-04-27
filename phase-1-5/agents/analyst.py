#!/usr/bin/env python3
"""
agents/analyst.py — Agent 2 : Scorer & Positioning
====================================================
Charge le SKILL.md correspondant au skill passé en argument,
l'injecte dans le system prompt Claude, lit les inputs JSON depuis outputs/,
appelle l'API Anthropic et écrit le fichier output dans outputs/.

Usage (appelé par phase1.py ou directement):
    python agents/analyst.py --skill=02   # Niche Idea Scorer
    python agents/analyst.py --skill=03   # Competitor X-Ray
    python agents/analyst.py --skill=04   # Buyer Intelligence
    python agents/analyst.py --skill=05   # Positioning & Launch

Modèle : claude-sonnet-4-20250514
Max tokens : 8000

Dépendances:
    pip install anthropic python-dotenv
"""

import argparse
import json
import os
import sys
import time
from pathlib import Path

import anthropic
from dotenv import load_dotenv

try:
    import jsonschema
    _JSONSCHEMA_AVAILABLE = True
except ImportError:
    _JSONSCHEMA_AVAILABLE = False

# ─── Chemins ────────────────────────────────────────────────────────────────
BASE_DIR    = Path(__file__).parent.parent.resolve()
SKILLS_DIR  = BASE_DIR / "skills"
OUTPUTS_DIR = BASE_DIR / "outputs"

# ─── Configuration Claude ────────────────────────────────────────────────────
CLAUDE_MODEL      = "claude-sonnet-4-20250514"
CLAUDE_MAX_TOKENS = 8000

# ─── Couleurs terminal ───────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


# ─── Logging ─────────────────────────────────────────────────────────────────

def log_info(msg: str):
    print(f"{CYAN}[INFO]{RESET} {msg}")


def log_ok(msg: str):
    print(f"{GREEN}{BOLD}[OK]{RESET} {msg}")


def log_warn(msg: str):
    print(f"{YELLOW}[WARN]{RESET} {msg}")


def log_error(msg: str):
    print(f"{RED}{BOLD}[BLOCKING ERROR: {msg}]{RESET}")


# ─── Configuration des skills ─────────────────────────────────────────────────

SKILL_CONFIG = {
    "02": {
        "name": "Niche Idea Scorer",
        "skill_dir": "02-niche-idea-scorer",
        "inputs": ["01-market-discovery.json"],
        "output": "02-scored.json",
        "output_format": "json",
        "blocking_check": lambda data: (
            "niche_shortlist" in data and len(data.get("niche_shortlist", [])) >= 3
        ),
        "blocking_msg": "02-scored.json missing 'niche_shortlist' or fewer than 3 niches — re-run Skill 02",
    },
    "03": {
        "name": "Competitor X-Ray",
        "skill_dir": "03-competitor-xray",
        "inputs": ["02-scored.json"],
        "output": "03-xray.json",
        "output_format": "json",
        "blocking_check": lambda data: (
            "final_niche" in data and "uvz_ranked" in data and len(data.get("uvz_ranked", [])) >= 1
        ),
        "blocking_msg": "03-xray.json missing 'final_niche' or 'uvz_ranked' — re-run Skill 03",
    },
    "04": {
        "name": "Buyer Intelligence",
        "skill_dir": "04-buyer-intelligence",
        "inputs": ["03-xray.json"],
        "output": "04-personas.json",
        "output_format": "json",
        "blocking_check": lambda data: (
            "personas" in data and len(data.get("personas", [])) >= 1
        ),
        "blocking_msg": "04-personas.json missing 'personas' array — re-run Skill 04",
    },
    "05": {
        "name": "Positioning & Launch",
        "skill_dir": "05-positioning-launch",
        "inputs": ["02-scored.json", "03-xray.json", "04-personas.json"],
        "output": "PHASE-1-OUTPUT.md",
        "output_format": "markdown",
        "blocking_check": lambda content: (
            isinstance(content, str) and len(content) > 500
        ),
        "blocking_msg": "PHASE-1-OUTPUT.md is empty or too short — re-run Skill 05",
    },
}


# ─── Fonctions utilitaires ────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Parse les arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Analyst Agent — Scorer & Positioning (Phase 1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Skills disponibles:
  --skill=02   Niche Idea Scorer   → outputs/02-scored.json
  --skill=03   Competitor X-Ray    → outputs/03-xray.json
  --skill=04   Buyer Intelligence  → outputs/04-personas.json
  --skill=05   Positioning Launch  → outputs/PHASE-1-OUTPUT.md
        """
    )
    parser.add_argument(
        "--skill",
        required=True,
        choices=["02", "03", "04", "05"],
        help="Numéro du skill à exécuter (02, 03, 04 ou 05)"
    )
    return parser.parse_args()


def load_skill_md(skill_dir_name: str) -> str:
    """
    Charge le contenu du SKILL.md correspondant au skill demandé.
    Lève une SystemExit si le fichier est introuvable.
    """
    skill_path = SKILLS_DIR / skill_dir_name / "SKILL.md"
    if not skill_path.exists():
        log_error(f"SKILL.md introuvable : {skill_path}")
        sys.exit(1)

    content = skill_path.read_text(encoding="utf-8")
    if len(content) > 16000:
        content = content[:16000] + "\n[SKILL TRUNCATED — remaining content omitted to fit context window]"
    log_ok(f"SKILL.md chargé : {skill_path.relative_to(BASE_DIR)}")
    return content


def load_input_files(input_filenames: list[str]) -> dict[str, str]:
    """
    Charge un ou plusieurs fichiers JSON depuis outputs/.
    Retourne un dict {filename: raw_content}.
    Lève une SystemExit si un fichier est manquant.
    """
    loaded = {}
    for filename in input_filenames:
        filepath = OUTPUTS_DIR / filename
        if not filepath.exists():
            log_error(f"Fichier input manquant : {filepath} — vérifiez que l'étape précédente s'est terminée correctement")
            sys.exit(1)
        if filepath.stat().st_size < 10:
            log_error(f"Fichier input vide ou invalide : {filepath}")
            sys.exit(1)
        raw = filepath.read_text(encoding="utf-8")
        loaded[filename] = raw
        log_ok(f"Input chargé : {filename} ({filepath.stat().st_size / 1024:.1f} KB)")
    return loaded


def build_user_prompt(skill_id: str, inputs: dict[str, str]) -> str:
    """
    Construit le prompt utilisateur avec les fichiers input injectés.
    Pour skill 05, injecte les 3 fichiers simultanément.
    """
    config = SKILL_CONFIG[skill_id]

    if skill_id == "05":
        parts = [
            "Execute the skill instructions above using the following input files.\n",
            "Produce the complete PHASE-1-OUTPUT.md deliverable in Markdown format.\n\n",
        ]
        for fname, content in inputs.items():
            parts.append(f"## INPUT FILE: {fname}\n\n```json\n{content}\n```\n\n")
        parts.append(
            "Important: Produce a complete, ready-to-use Markdown document. "
            "All sections must be filled with real, actionable content. "
            "Do not use placeholders or skeleton structures."
        )
        return "".join(parts)
    else:
        # Skills 02, 03, 04 — un seul fichier input
        fname = config["inputs"][0]
        content = inputs[fname]
        return (
            f"Execute the skill instructions above using the following input data.\n"
            f"Produce a valid, well-structured JSON output matching the skill's output schema.\n\n"
            f"## INPUT FILE: {fname}\n\n"
            f"```json\n{content}\n```\n\n"
            f"Important: Return ONLY valid JSON. No markdown code fences, no explanatory text before or after the JSON. "
            f"The response must be parseable directly by json.loads()."
        )


def call_claude_api(system_prompt: str, user_prompt: str, skill_name: str) -> str:
    """
    Appelle l'API Claude avec le system prompt (SKILL.md) et le user prompt (données input).
    Retourne le contenu texte de la réponse.
    Retry exponentiel sur erreurs transitoires (RateLimitError, APIConnectionError, 529).
    Lève une SystemExit en cas d'erreur fatale ou après épuisement des retries.
    """
    api_key = os.getenv("ANTHROPIC_KEY")
    if not api_key:
        log_error("ANTHROPIC_KEY non définie dans l'environnement")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    log_info(f"Appel Claude API — modèle : {CLAUDE_MODEL} — skill : {skill_name}")
    log_info(f"System prompt : {len(system_prompt)} chars | User prompt : {len(user_prompt)} chars")

    _RETRY_DELAYS = [2, 4, 8]  # secondes — backoff exponentiel, 3 tentatives max

    for attempt, delay in enumerate([0] + _RETRY_DELAYS, start=1):
        if delay:
            log_warn(f"Retry {attempt - 1}/3 — attente {delay}s avant nouvel essai...")
            time.sleep(delay)
        try:
            message = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=CLAUDE_MAX_TOKENS,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ],
            )

            # Extraction du contenu texte
            response_text = ""
            for block in message.content:
                if hasattr(block, "text"):
                    response_text += block.text

            log_ok(
                f"Réponse reçue — {len(response_text)} chars | "
                f"Tokens : {message.usage.input_tokens} in / {message.usage.output_tokens} out | "
                f"Stop reason : {message.stop_reason}"
            )

            if message.stop_reason == "max_tokens":
                log_warn("La réponse a atteint la limite max_tokens — le JSON output pourrait être tronqué")

            return response_text

        except anthropic.AuthenticationError:
            log_error("ANTHROPIC_KEY invalide ou expirée — vérifiez votre clé API")
            sys.exit(1)

        except anthropic.RateLimitError:
            if attempt <= len(_RETRY_DELAYS):
                log_warn(f"Rate limit Anthropic atteint (tentative {attempt}/4) — retry dans {_RETRY_DELAYS[attempt - 1]}s")
                continue
            log_error("Rate limit Anthropic persistant après 4 tentatives — arrêt")
            sys.exit(1)

        except anthropic.APIConnectionError as e:
            if attempt <= len(_RETRY_DELAYS):
                log_warn(f"Connexion API échouée (tentative {attempt}/4) : {e} — retry dans {_RETRY_DELAYS[attempt - 1]}s")
                continue
            log_error(f"Connexion à l'API Anthropic impossible après 4 tentatives : {e}")
            sys.exit(1)

        except anthropic.APIStatusError as e:
            if e.status_code == 529 and attempt <= len(_RETRY_DELAYS):
                log_warn(f"API surchargée [529] (tentative {attempt}/4) — retry dans {_RETRY_DELAYS[attempt - 1]}s")
                continue
            log_error(f"Erreur API Anthropic [{e.status_code}] : {e.message}")
            sys.exit(1)

        except Exception as e:
            log_error(f"Erreur inattendue lors de l'appel Claude : {e}")
            sys.exit(1)

    log_error("Échec après 4 tentatives — arrêt du pipeline")
    sys.exit(1)


def parse_json_response(raw: str, skill_id: str) -> dict:
    """
    Parse la réponse Claude comme JSON.
    Tente de nettoyer les artefacts markdown si nécessaire.
    Lève une SystemExit si le JSON est invalide.
    """
    text = raw.strip()

    # Nettoyage des code fences markdown si Claude en a ajouté
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()

    try:
        data = json.loads(text)
        log_ok("JSON parsé avec succès")
        return data
    except json.JSONDecodeError as e:
        log_error(f"La réponse Claude n'est pas un JSON valide : {e}")
        log_warn("Début de la réponse reçue :")
        print(text[:500])
        sys.exit(1)


def check_blocking_conditions(skill_id: str, output_data) -> bool:
    """
    Vérifie les blocking conditions sur l'output produit.
    Retourne True si tout est OK, False sinon.
    """
    config = SKILL_CONFIG[skill_id]
    check_fn   = config["blocking_check"]
    block_msg  = config["blocking_msg"]

    try:
        if check_fn(output_data):
            log_ok("Blocking conditions OK")
            return True
        else:
            log_error(f"Blocking condition non satisfaite : {block_msg}")
            return False
    except Exception as e:
        log_error(f"Erreur lors de la vérification des blocking conditions : {e}")
        return False


def write_output(skill_id: str, content) -> Path:
    """
    Écrit le fichier output dans outputs/.
    - Skills 02/03/04 → JSON pretty-printed + jsonschema validation
    - Skill 05 → Markdown brut

    Retourne le chemin du fichier créé.
    """
    config       = SKILL_CONFIG[skill_id]
    output_name  = config["output"]
    output_path  = OUTPUTS_DIR / output_name
    output_fmt   = config["output_format"]

    OUTPUTS_DIR.mkdir(exist_ok=True)

    try:
        if output_fmt == "json":
            output_path.write_text(
                json.dumps(content, ensure_ascii=False, indent=2),
                encoding="utf-8"
            )
            # ── jsonschema validation ──────────────────────────────────────
            if _JSONSCHEMA_AVAILABLE:
                schema_path = SKILLS_DIR / config["skill_dir"] / "output-schema.json"
                if schema_path.exists():
                    schema = json.loads(schema_path.read_text(encoding="utf-8"))
                    validator = jsonschema.Draft7Validator(schema)
                    errors = list(validator.iter_errors(content))
                    if errors:
                        log_warn(f"Schema validation warnings for {output_name}:")
                        for err in errors[:5]:
                            field = " -> ".join(str(p) for p in err.absolute_path) or "root"
                            log_warn(f"  FIELD '{field}': {err.message}")
                    else:
                        log_ok(f"Schema validation passed — {output_name} conforms to output-schema.json")
                else:
                    log_warn(f"No output-schema.json found for Skill {skill_id} — skipping validation")
            else:
                log_warn("jsonschema not installed — skipping schema validation (run: pip install jsonschema)")
        else:
            # Markdown (skill 05)
            output_path.write_text(content, encoding="utf-8")

        size_kb = output_path.stat().st_size / 1024
        log_ok(f"Output écrit : {output_name} ({size_kb:.1f} KB)")
        return output_path

    except OSError as e:
        log_error(f"Impossible d'écrire {output_path} : {e}")
        sys.exit(1)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    """
    Pipeline analyst.py :
        1. Charger les variables d'environnement
        2. Lire le SKILL.md correspondant au skill demandé
        3. Charger les fichiers input depuis outputs/
        4. Construire le prompt utilisateur
        5. Appeler l'API Claude
        6. Parser / valider l'output
        7. Vérifier les blocking conditions
        8. Écrire l'output dans outputs/
    """
    args = parse_args()
    skill_id = args.skill
    config   = SKILL_CONFIG[skill_id]

    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  ANALYST AGENT — Skill {skill_id}: {config['name']}{RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

    # ── Chargement .env ──────────────────────────────────────────────────────
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        log_info(".env chargé.")
    else:
        log_warn(".env introuvable — variables d'environnement lues depuis le système.")

    api_key = os.getenv("ANTHROPIC_KEY")
    if not api_key:
        log_error("ANTHROPIC_KEY manquante — impossible d'appeler l'API Claude")
        sys.exit(1)

    # ── Chargement SKILL.md → system prompt ──────────────────────────────────
    log_info(f"Chargement du SKILL.md : {config['skill_dir']}/SKILL.md")
    system_prompt = load_skill_md(config["skill_dir"])

    # ── Chargement des fichiers input ─────────────────────────────────────────
    log_info(f"Chargement des inputs : {', '.join(config['inputs'])}")
    inputs = load_input_files(config["inputs"])

    # ── Construction du prompt utilisateur ───────────────────────────────────
    user_prompt = build_user_prompt(skill_id, inputs)

    # ── Appel API Claude ──────────────────────────────────────────────────────
    raw_response = call_claude_api(system_prompt, user_prompt, config["name"])

    # ── Parse et validation de l'output ──────────────────────────────────────
    if config["output_format"] == "json":
        output_data = parse_json_response(raw_response, skill_id)
    else:
        # Skill 05 : output Markdown brut
        output_data = raw_response
        log_ok(f"Réponse Markdown reçue — {len(output_data)} caractères")

    # ── Vérification des blocking conditions ──────────────────────────────────
    if not check_blocking_conditions(skill_id, output_data):
        # On écrit quand même l'output brut pour diagnostic, puis on halt
        diag_path = OUTPUTS_DIR / f"{skill_id}-DIAGNOSTIC-FAILED.txt"
        diag_path.write_text(raw_response, encoding="utf-8")
        log_warn(f"Output brut sauvegardé pour diagnostic : {diag_path.name}")
        sys.exit(1)

    # ── Écriture de l'output ──────────────────────────────────────────────────
    output_path = write_output(skill_id, output_data)

    # ── Résumé ────────────────────────────────────────────────────────────────
    print(f"\n{GREEN}{BOLD}  Skill {skill_id} — {config['name']} : TERMINÉ ✓{RESET}")
    print(f"  Output : {output_path.relative_to(BASE_DIR)}\n")


if __name__ == "__main__":
    main()
