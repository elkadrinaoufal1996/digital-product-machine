#!/usr/bin/env python3
"""
phase1.py — Orchestrateur Principal Phase 1
============================================
Lance le pipeline complet d'analyse de marché digital US en 5 étapes séquentielles.

Usage:
    python phase1.py --market=US

Dépendances requises:
    pip install anthropic apify-client firecrawl-py tavily-python python-dotenv

Variables d'environnement requises (voir .env.example):
    ANTHROPIC_KEY, APIFY_TOKEN, FIRECRAWL_KEY, TAVILY_KEY
"""

import argparse
import os
import sys
import subprocess
import time
from pathlib import Path
from dotenv import load_dotenv

# ─── Chemins ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.resolve()
OUTPUTS_DIR = BASE_DIR / "outputs"
AGENTS_DIR = BASE_DIR / "agents"

# ─── Couleurs terminal ───────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def log_step(step: int, message: str):
    """Log d'étape réussie."""
    print(f"{GREEN}{BOLD}[STEP {step} — OK]{RESET} {message}")


def log_error(message: str):
    """Log d'erreur bloquante."""
    print(f"{RED}{BOLD}[BLOCKING ERROR: {message}]{RESET}")


def log_info(message: str):
    """Log informatif."""
    print(f"{CYAN}[INFO]{RESET} {message}")


def log_warn(message: str):
    """Log avertissement non-bloquant."""
    print(f"{YELLOW}[WARN]{RESET} {message}")


def check_env_vars() -> bool:
    """
    Vérifie que toutes les variables d'environnement requises sont définies.
    Retourne True si tout est OK, False sinon.
    """
    required_vars = ["ANTHROPIC_KEY", "APIFY_TOKEN", "FIRECRAWL_KEY", "TAVILY_KEY"]
    missing = [v for v in required_vars if not os.getenv(v)]

    if missing:
        log_error(f"Variables d'environnement manquantes: {', '.join(missing)}")
        print(f"  → Créez un fichier .env basé sur .env.example et renseignez les clés manquantes.")
        return False

    log_info("Toutes les variables d'environnement sont présentes.")
    return True


def wait_for_output(filepath: Path, timeout_seconds: int = 300, poll_interval: int = 5) -> bool:
    """
    Attend qu'un fichier output soit créé (produit par un agent).
    Timeout par défaut : 5 minutes.
    Retourne True si le fichier est trouvé, False en cas de timeout.
    """
    log_info(f"Attente du fichier: {filepath.name} (timeout: {timeout_seconds}s)")
    elapsed = 0
    while elapsed < timeout_seconds:
        if filepath.exists() and filepath.stat().st_size > 10:
            return True
        time.sleep(poll_interval)
        elapsed += poll_interval
        if elapsed % 30 == 0:
            log_info(f"  ... toujours en attente de {filepath.name} ({elapsed}s écoulées)")
    return False


def run_agent(script: str, args: list[str], step: int, description: str) -> subprocess.CompletedProcess | None:
    """
    Lance un script agent en subprocess avec les arguments fournis.
    Retourne le CompletedProcess ou None en cas d'erreur.
    """
    agent_path = AGENTS_DIR / script
    cmd = [sys.executable, str(agent_path)] + args

    log_info(f"Lancement: {script} {' '.join(args)}")
    print(f"  {'─' * 60}")

    try:
        result = subprocess.run(
            cmd,
            cwd=str(BASE_DIR),
            check=True,            # Lève une exception si returncode != 0
            text=True,
        )
        log_step(step, description)
        return result

    except subprocess.CalledProcessError as e:
        log_error(f"Agent {script} a terminé avec code {e.returncode}")
        return None

    except FileNotFoundError:
        log_error(f"Script introuvable: {agent_path}")
        return None


def parse_args() -> argparse.Namespace:
    """Parse les arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Phase 1 — Pipeline d'analyse marché digital US",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples:
  python phase1.py --market=US
  python phase1.py --market=US --skip-scraper   # Si 01-market-discovery.json existe déjà
        """
    )
    parser.add_argument(
        "--market",
        default="US",
        choices=["US"],
        help="Marché cible (default: US — seul marché supporté en Phase 1)"
    )
    parser.add_argument(
        "--skip-scraper",
        action="store_true",
        help="Sauter l'étape scraper (utilise outputs/01-market-discovery.json existant)"
    )
    return parser.parse_args()


def main():
    """
    Pipeline principal Phase 1.

    Étapes :
        1. Chargement de l'environnement
        2. Scraping (scraper.py) → outputs/01-market-discovery.json
        3. Scoring des niches (analyst.py --skill=02) → outputs/02-scored.json
        4. Competitor X-Ray (analyst.py --skill=03) → outputs/03-xray.json
        5. Buyer Intelligence (analyst.py --skill=04) → outputs/04-personas.json
        6. Positioning & Launch (analyst.py --skill=05) → outputs/PHASE-1-OUTPUT.md
    """
    args = parse_args()

    print(f"\n{BOLD}{'═' * 65}{RESET}")
    print(f"{BOLD}  PHASE 1 — Digital Product Market Intelligence{RESET}")
    print(f"{BOLD}  Marché: {args.market}{RESET}")
    print(f"{BOLD}{'═' * 65}{RESET}\n")

    # ── ÉTAPE 0 : Chargement .env ────────────────────────────────────────────
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)
        log_info(".env chargé.")
    else:
        log_warn(".env introuvable — les variables d'environnement doivent être définies système.")

    if not check_env_vars():
        sys.exit(1)

    OUTPUTS_DIR.mkdir(exist_ok=True)

    # ── ÉTAPE 1 : Scraping ───────────────────────────────────────────────────
    output_01 = OUTPUTS_DIR / "01-market-discovery.json"

    if args.skip_scraper:
        if not output_01.exists():
            log_error("--skip-scraper demandé mais outputs/01-market-discovery.json introuvable")
            sys.exit(1)
        log_info("Scraper ignoré (--skip-scraper). Utilisation du fichier existant.")
    else:
        log_info("─── ÉTAPE 1 : Collecte de données marché (scraper.py) ───")
        result = run_agent(
            script="scraper.py",
            args=[f"--market={args.market}"],
            step=1,
            description="Données marché collectées → outputs/01-market-discovery.json"
        )
        if result is None:
            log_error("scraper.py a échoué — pipeline interrompu")
            sys.exit(1)

        if not wait_for_output(output_01, timeout_seconds=300):
            log_error("outputs/01-market-discovery.json non trouvé après timeout — halt")
            sys.exit(1)

    print()

    # ── ÉTAPE 2 : Scoring des niches ─────────────────────────────────────────
    output_02 = OUTPUTS_DIR / "02-scored.json"
    log_info("─── ÉTAPE 2 : Scoring des niches (analyst.py --skill=02) ───")

    result = run_agent(
        script="analyst.py",
        args=["--skill=02"],
        step=2,
        description="Niches scorées → outputs/02-scored.json"
    )
    if result is None:
        log_error("analyst.py --skill=02 a échoué — pipeline interrompu")
        sys.exit(1)

    if not wait_for_output(output_02, timeout_seconds=300):
        log_error("outputs/02-scored.json non trouvé après timeout — halt")
        sys.exit(1)

    print()

    # ── ÉTAPE 3 : Competitor X-Ray ───────────────────────────────────────────
    output_03 = OUTPUTS_DIR / "03-xray.json"
    log_info("─── ÉTAPE 3 : Competitor X-Ray (analyst.py --skill=03) ───")

    result = run_agent(
        script="analyst.py",
        args=["--skill=03"],
        step=3,
        description="Analyse concurrentielle → outputs/03-xray.json"
    )
    if result is None:
        log_error("analyst.py --skill=03 a échoué — pipeline interrompu")
        sys.exit(1)

    if not wait_for_output(output_03, timeout_seconds=300):
        log_error("outputs/03-xray.json non trouvé après timeout — halt")
        sys.exit(1)

    print()

    # ── ÉTAPE 4 : Buyer Intelligence ─────────────────────────────────────────
    output_04 = OUTPUTS_DIR / "04-personas.json"
    log_info("─── ÉTAPE 4 : Buyer Intelligence (analyst.py --skill=04) ───")

    result = run_agent(
        script="analyst.py",
        args=["--skill=04"],
        step=4,
        description="Personas acheteurs → outputs/04-personas.json"
    )
    if result is None:
        log_error("analyst.py --skill=04 a échoué — pipeline interrompu")
        sys.exit(1)

    if not wait_for_output(output_04, timeout_seconds=300):
        log_error("outputs/04-personas.json non trouvé après timeout — halt")
        sys.exit(1)

    print()

    # ── ÉTAPE 5 : Positioning & Launch ───────────────────────────────────────
    output_final = OUTPUTS_DIR / "PHASE-1-OUTPUT.md"
    log_info("─── ÉTAPE 5 : Positioning & Launch (analyst.py --skill=05) ───")

    result = run_agent(
        script="analyst.py",
        args=["--skill=05"],
        step=5,
        description="Stratégie de positionnement → outputs/PHASE-1-OUTPUT.md"
    )
    if result is None:
        log_error("analyst.py --skill=05 a échoué — pipeline interrompu")
        sys.exit(1)

    if not wait_for_output(output_final, timeout_seconds=300):
        log_error("outputs/PHASE-1-OUTPUT.md non trouvé après timeout — halt")
        sys.exit(1)

    # ── RÉSUMÉ FINAL ─────────────────────────────────────────────────────────
    print(f"\n{BOLD}{'═' * 65}{RESET}")
    print(f"{GREEN}{BOLD}  PHASE 1 COMPLÈTE ✓{RESET}")
    print(f"{BOLD}{'═' * 65}{RESET}")
    print(f"\n  Fichiers produits dans {OUTPUTS_DIR.relative_to(BASE_DIR)}/:")
    for f in sorted(OUTPUTS_DIR.iterdir()):
        if f.name != ".gitkeep":
            size_kb = f.stat().st_size / 1024
            print(f"  {GREEN}✓{RESET}  {f.name} ({size_kb:.1f} KB)")
    print(f"\n  Livrable principal: {GREEN}outputs/PHASE-1-OUTPUT.md{RESET}\n")


if __name__ == "__main__":
    main()
