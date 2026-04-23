#!/usr/bin/env python3
"""
agents/scraper.py — Agent 1 : Data Collector
=============================================
Collecte en parallèle des signaux de marché sur 6 sources,
applique un filtre binaire d'élimination, et produit
outputs/01-market-discovery.json.

Usage (appelé par phase1.py ou directement):
    python agents/scraper.py --market=US

Sources:
    SOURCE 1 — Gumroad (Apify: muhammetakkurtt/gumroad-scraper)
    SOURCE 2 — Amazon/Kindle Reviews (Apify: getdataforme/amazon-books-reviews-actor)
    SOURCE 3 — Etsy Digital Products (Apify: epctex/etsy-scraper)
    SOURCE 4 — TikTok Hashtags (Apify: clockworks/tiktok-scraper)
    SOURCE 5 — Instagram Hashtags (Apify: apify/instagram-scraper)
    SOURCE 6 — Reddit Pain Signals (Tavily)

Blocking Condition:
    HALT si SOURCE 1 (Gumroad) ET SOURCE 3 (Etsy) sont toutes les deux FAILED.
"""

import argparse
import asyncio
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
from pathlib import Path

from apify_client import ApifyClient
from dotenv import load_dotenv
from tavily import TavilyClient

# ─── Chemins ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent.parent.resolve()
SKILLS_DIR = BASE_DIR / "skills" / "01-market-discovery"
OUTPUTS_DIR = BASE_DIR / "outputs"

# ─── Couleurs terminal ───────────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
RESET  = "\033[0m"
BOLD   = "\033[1m"


def log_source(source_id: str, status: str, message: str = ""):
    """Log le statut d'une source de données."""
    color = GREEN if status == "OK" else (YELLOW if status in ("PARTIAL", "WARNING") else RED)
    label = f"[SOURCE {source_id} — {status}]"
    print(f"{color}{BOLD}{label}{RESET} {message}")


def log_info(message: str):
    print(f"{CYAN}[INFO]{RESET} {message}")


def log_error(message: str):
    print(f"{RED}{BOLD}[BLOCKING ERROR: {message}]{RESET}")


def log_warn(message: str):
    print(f"{YELLOW}[DATA WARNING: {message}]{RESET}")


def load_skill_md() -> str:
    """Charge le SKILL.md de la compétence 01 pour référence dans les logs."""
    skill_file = SKILLS_DIR / "SKILL.md"
    if skill_file.exists():
        return skill_file.read_text(encoding="utf-8")
    log_warn("SKILL.md introuvable dans skills/01-market-discovery/")
    return ""


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 1 — Gumroad Top 200 Digital Bestsellers (Apify)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_gumroad(apify: ApifyClient) -> dict:
    """
    Lance le scraper Gumroad pour récupérer les 200 meilleurs produits digitaux US.
    Retourne un dict avec status et data.
    """
    log_info("SOURCE 1 — Lancement Gumroad scraper...")
    try:
        run = apify.actor("muhammetakkurtt/gumroad-scraper").call(
            run_input={
                "category": "digital_products",
                "limit": 200,
                "sort": "bestseller",
                "market": "US",
            }
        )
        items = list(
            apify.dataset(run["defaultDatasetId"]).iterate_items()
        )

        if not items:
            log_source("1", "FAILED", "Aucun résultat retourné par Gumroad")
            return {"status": "FAILED", "data": []}

        # Extraction des champs requis
        products = []
        for item in items:
            products.append({
                "product_name":       item.get("name") or item.get("title", ""),
                "category":           item.get("category", ""),
                "price_usd":          item.get("price", 0),
                "sales_count":        item.get("sales_count") or item.get("salesCount", 0),
                "creator_followers":  item.get("creator_followers") or item.get("creatorFollowers", 0),
                "description_snippet": (item.get("description") or "")[:300],
            })

        status = "PARTIAL" if len(products) < 100 else "OK"
        if status == "PARTIAL":
            log_source("1", "PARTIAL", f"Seulement {len(products)} résultats (minimum attendu: 100)")
        else:
            log_source("1", "OK", f"{len(products)} produits collectés")

        return {"status": status, "data": products}

    except Exception as e:
        log_source("1", "FAILED", str(e))
        return {"status": "FAILED", "data": [], "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 2 — Amazon/Kindle Books Reviews (Apify)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_amazon_kindle(apify: ApifyClient) -> dict:
    """
    Scrape les avis et métadonnées des livres Kindle sur les niches cibles.
    SOURCE CRITIQUE — si FAILED en même temps que SOURCE 1 → BLOCKING CONDITION.
    """
    log_info("SOURCE 2 — Lancement Amazon/Kindle scraper...")
    keywords = [
        "self-help", "productivity", "personal-finance",
        "fitness", "relationships", "mindset", "business"
    ]
    try:
        run = apify.actor("getdataforme/amazon-books-reviews-actor").call(
            run_input={
                "keywords":           keywords,
                "sort":               "reviews_count",
                "limit_per_keyword":  20,
                "market":             "US",
            }
        )
        items = list(
            apify.dataset(run["defaultDatasetId"]).iterate_items()
        )

        if not items:
            log_source("2", "FAILED", "Aucun résultat retourné par Amazon/Kindle")
            return {"status": "FAILED", "data": []}

        books = []
        for item in items:
            books.append({
                "title":        item.get("title", ""),
                "review_count": item.get("reviewCount") or item.get("reviews_count", 0),
                "avg_rating":   item.get("avgRating") or item.get("avg_rating", 0),
                "price_usd":    item.get("price", 0),
                "category":     item.get("category", ""),
            })

        log_source("2", "OK", f"{len(books)} titres collectés")
        return {"status": "OK", "data": books}

    except Exception as e:
        log_source("2", "FAILED", str(e))
        return {"status": "FAILED", "data": [], "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 3 — Etsy Digital Products (Apify)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_etsy(apify: ApifyClient) -> dict:
    """Scrape les produits digitaux Etsy (téléchargements digitaux, ebooks, guides)."""
    log_info("SOURCE 3 — Lancement Etsy scraper...")
    try:
        run = apify.actor("epctex/etsy-scraper").call(
            run_input={
                "keywords": ["digital download", "ebook", "guide", "printable"],
                "category": "digital_products",
                "market":   "US",
                "limit":    100,
            }
        )
        items = list(
            apify.dataset(run["defaultDatasetId"]).iterate_items()
        )

        if not items:
            log_source("3", "FAILED", "Aucun résultat Etsy")
            return {"status": "FAILED", "data": []}

        products = []
        for item in items:
            products.append({
                "product_name": item.get("title", ""),
                "category":     item.get("category", ""),
                "price_usd":    item.get("price", 0),
                "sales_count":  item.get("salesCount") or item.get("sales_count", 0),
                "seller_info":  item.get("seller") or item.get("shopName", ""),
            })

        log_source("3", "OK", f"{len(products)} produits Etsy collectés")
        return {"status": "OK", "data": products}

    except Exception as e:
        log_source("3", "FAILED", str(e))
        log_warn("Etsy unavailable")
        return {"status": "FAILED", "data": [], "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 4 — TikTok Educational Hashtags (Apify)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_tiktok(apify: ApifyClient) -> dict:
    """Scrape les hashtags TikTok éducatifs pour mesurer la demande virale."""
    log_info("SOURCE 4 — Lancement TikTok hashtag scraper...")
    hashtags = [
        "learnontiktok", "financetok", "moneytips", "selfimprovement",
        "productivity", "sidehustle", "digitalproduct", "passiveincome",
        "healthtips", "mindset"
    ]
    try:
        run = apify.actor("clockworks/tiktok-scraper").call(
            run_input={
                "hashtags":    hashtags,
                "time_window": "30_days",
                "min_views":   100000,
            }
        )
        items = list(
            apify.dataset(run["defaultDatasetId"]).iterate_items()
        )

        if not items:
            log_source("4", "PARTIAL", "Aucun hashtag TikTok retourné")
            return {"status": "PARTIAL", "data": []}

        tiktok_data = []
        for item in items:
            tiktok_data.append({
                "hashtag":              item.get("hashtag", ""),
                "total_views_30d":      item.get("totalViews") or item.get("total_views_30d", 0),
                "growth_rate_percent":  item.get("growthRate") or item.get("growth_rate_percent", 0),
                "top_video_descriptions": item.get("topVideos") or item.get("top_video_descriptions", []),
                "avg_engagement_rate":  item.get("avgEngagementRate") or item.get("avg_engagement_rate", 0),
            })

        log_source("4", "OK", f"{len(tiktok_data)} hashtags collectés")
        return {"status": "OK", "data": tiktok_data}

    except Exception as e:
        log_source("4", "PARTIAL", str(e))
        return {"status": "PARTIAL", "data": [], "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 5 — Instagram Hashtags (Apify)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_instagram(apify: ApifyClient) -> dict:
    """Scrape les hashtags Instagram pour mesurer la présence organique."""
    log_info("SOURCE 5 — Lancement Instagram scraper...")
    hashtags = [
        "selfimprovement", "digitalproduct", "sidehustle",
        "passiveincome", "financetips", "productivitytips"
    ]
    try:
        run = apify.actor("apify/instagram-scraper").call(
            run_input={
                "searchType":       "hashtag",
                "hashtags":         hashtags,
                "limit_per_hashtag": 50,
                "time_window":      "30_days",
            }
        )
        items = list(
            apify.dataset(run["defaultDatasetId"]).iterate_items()
        )

        if not items:
            log_source("5", "FAILED", "Aucun post Instagram retourné")
            log_warn("Instagram unavailable")
            return {"status": "FAILED", "data": []}

        ig_data = []
        for item in items:
            ig_data.append({
                "hashtag":    item.get("hashtag") or item.get("query", ""),
                "post_count": item.get("postsCount") or item.get("post_count", 0),
                "avg_likes":  item.get("avgLikes") or item.get("avg_likes", 0),
                "avg_comments": item.get("avgComments") or item.get("avg_comments", 0),
                "top_captions": item.get("captions") or item.get("top_captions", []),
            })

        log_source("5", "OK", f"{len(ig_data)} hashtags Instagram collectés")
        return {"status": "OK", "data": ig_data}

    except Exception as e:
        log_source("5", "FAILED", str(e))
        log_warn("Instagram unavailable")
        return {"status": "FAILED", "data": [], "error": str(e)}


# ─────────────────────────────────────────────────────────────────────────────
# SOURCE 6 — Reddit Pain Signals (Tavily)
# ─────────────────────────────────────────────────────────────────────────────
def scrape_reddit(tavily: TavilyClient) -> dict:
    """
    Collecte des signaux de douleur Reddit via Tavily.
    Recherche les posts avec des expressions clés de frustration/besoin.
    """
    log_info("SOURCE 6 — Lancement Reddit search via Tavily...")
    subreddits = [
        "r/personalfinance", "r/getdisciplined", "r/entrepreneur",
        "r/productivity", "r/smallbusiness", "r/selfimprovement"
    ]
    search_terms = [
        "how do I", "I struggle with", "anyone else",
        "I can't figure out", "I feel stuck"
    ]

    all_results = []
    errors = []

    for term in search_terms:
        try:
            query = f"site:reddit.com ({' OR '.join(subreddits)}) {term}"
            response = tavily.search(
                query=query,
                search_depth="advanced",
                max_results=30,
                include_answer=False,
            )

            for result in response.get("results", []):
                all_results.append({
                    "post_title":    result.get("title", ""),
                    "body_snippet":  result.get("content", "")[:500],
                    "subreddit":     next(
                        (s for s in subreddits if s.lower() in result.get("url", "").lower()),
                        "[DATA MISSING]"
                    ),
                    "upvotes":       result.get("score", 0),
                    "comment_count": result.get("num_comments", 0),
                    "url":           result.get("url", ""),
                })

        except Exception as e:
            errors.append(str(e))

    if not all_results and errors:
        log_source("6", "PARTIAL", f"Erreurs Tavily: {errors[0]}")
        return {"status": "PARTIAL", "data": [], "errors": errors}

    # Dédupliquer par URL
    seen_urls = set()
    unique_results = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_results.append(r)

    log_source("6", "OK", f"{len(unique_results)} posts Reddit collectés")
    return {"status": "OK", "data": unique_results[:150]}


# ─────────────────────────────────────────────────────────────────────────────
# FILTRE BINAIRE D'ÉLIMINATION
# ─────────────────────────────────────────────────────────────────────────────
ELIMINATION_RULES = {
    "LEGAL": [
        "medical claims", "financial advice", "legal services",
        "supplements", "prescription", "diagnosis", "cure", "treat"
    ],
    "NO-PAY": [],   # Évalué via absence de signaux Gumroad/Kindle
    "SEASONAL": [
        "christmas", "halloween", "thanksgiving", "valentine",
        "new year", "black friday", "easter", "summer only", "winter only"
    ],
    "PLATFORM-DEPENDENT": [
        "only on tiktok", "only on instagram", "only on youtube",
        "only on snapchat", "platform exclusive"
    ],
}

SATURATION_KEYWORDS = [
    "weight loss", "keto diet", "intermittent fasting", "make money online",
    "dropshipping", "amazon fba", "crypto trading", "forex trading",
    "manifestation", "law of attraction",
]


def apply_elimination_filter(cluster_name: str, signals: dict) -> tuple[str, str]:
    """
    Applique le filtre binaire d'élimination à un cluster de niche.

    Args:
        cluster_name: Nom du cluster/niche
        signals: Données agrégées du cluster

    Returns:
        Tuple (status, reason) où status est:
        - "ACTIVE"    : passe tous les filtres
        - "BORDERLINE": passe mais faiblesse sur 2+ critères
        - "ELIMINATED": éliminé avec raison
    """
    cluster_lower = cluster_name.lower()
    weaknesses = []

    # Vérification LEGAL
    for keyword in ELIMINATION_RULES["LEGAL"]:
        if keyword in cluster_lower:
            return "ELIMINATED", f"ELIMINATED: LEGAL — contient '{keyword}'"

    # Vérification SEASONAL
    for keyword in ELIMINATION_RULES["SEASONAL"]:
        if keyword in cluster_lower:
            return "ELIMINATED", f"ELIMINATED: SEASONAL — '{keyword}'"

    # Vérification PLATFORM-DEPENDENT
    for keyword in ELIMINATION_RULES["PLATFORM-DEPENDENT"]:
        if keyword in cluster_lower:
            return "ELIMINATED", f"ELIMINATED: PLATFORM-RISK — '{keyword}'"

    # Vérification SATURATION (heuristique)
    for keyword in SATURATION_KEYWORDS:
        if keyword in cluster_lower:
            weaknesses.append("potentiellement saturé")
            break

    # Vérification NO-PAY — absence de signal Gumroad ou Kindle
    has_gumroad_signal = signals.get("gumroad_count", 0) > 0
    has_kindle_signal = signals.get("kindle_count", 0) > 0
    if not has_gumroad_signal and not has_kindle_signal:
        return "ELIMINATED", "ELIMINATED: NO-PAY — aucun signal de produit payant"

    # BORDERLINE si 2+ faiblesses
    if len(weaknesses) >= 2:
        return "BORDERLINE", f"BORDERLINE — faiblesses: {', '.join(weaknesses)}"

    return "ACTIVE", "Passe tous les filtres"


# ─────────────────────────────────────────────────────────────────────────────
# CLUSTERING DES SIGNAUX
# ─────────────────────────────────────────────────────────────────────────────
NICHE_CLUSTERS = [
    {"name": "Personal Finance & Money Management", "keywords": ["finance", "money", "budget", "debt", "savings", "wealth", "income"]},
    {"name": "Productivity & Time Management", "keywords": ["productivity", "time management", "focus", "routine", "habit", "efficiency"]},
    {"name": "Self-Improvement & Mindset", "keywords": ["mindset", "self-improvement", "confidence", "motivation", "discipline", "growth"]},
    {"name": "Side Hustle & Online Income", "keywords": ["side hustle", "passive income", "freelance", "online income", "digital product"]},
    {"name": "Health & Fitness (Non-Medical)", "keywords": ["fitness", "workout", "exercise", "nutrition basics", "healthy eating"]},
    {"name": "Relationships & Communication", "keywords": ["relationship", "communication", "dating", "social skills", "anxiety"]},
    {"name": "Business & Entrepreneurship", "keywords": ["business", "entrepreneur", "startup", "marketing", "sales"]},
    {"name": "Parenting & Family", "keywords": ["parenting", "family", "kids", "children", "mom", "dad"]},
    {"name": "Career & Job Skills", "keywords": ["career", "job", "interview", "resume", "promotion", "leadership"]},
    {"name": "Mental Wellness (Non-Clinical)", "keywords": ["anxiety", "stress", "burnout", "overwhelm", "mindfulness", "meditation"]},
    {"name": "Journaling & Self-Reflection", "keywords": ["journaling", "self-reflection", "gratitude", "self-discovery", "writing"]},
    {"name": "Digital Skills & Tech Literacy", "keywords": ["digital skills", "tech", "ai tools", "chatgpt", "automation", "no-code"]},
    {"name": "Study Skills & Academic Success", "keywords": ["study", "learning", "academic", "student", "focus", "memorization"]},
    {"name": "Creative Skills & Passion Projects", "keywords": ["creative", "art", "writing", "music", "craft", "hobby"]},
    {"name": "Sustainable Living & Minimalism", "keywords": ["minimalism", "sustainable", "declutter", "eco", "simple living"]},
    {"name": "Pet Care & Training", "keywords": ["pet", "dog training", "cat care", "animal behavior"]},
    {"name": "Cooking & Meal Prep", "keywords": ["meal prep", "cooking", "recipe", "kitchen", "food planning"]},
    {"name": "Travel Planning & Digital Nomad", "keywords": ["travel", "nomad", "remote work", "travel planning", "backpacking"]},
    {"name": "Spirituality & Personal Growth", "keywords": ["spirituality", "energy", "manifestation", "purpose", "meaning"]},
    {"name": "Social Media & Personal Branding", "keywords": ["personal brand", "instagram growth", "content creator", "audience building"]},
]


def cluster_signals(raw_data: dict) -> list[dict]:
    """
    Groupe les signaux bruts des 6 sources en clusters de niches thématiques.
    Retourne une liste de niches candidates avec leurs signaux agrégés.
    """
    log_info("Clustering des signaux en thèmes de niche...")
    niches = []

    gumroad_products = raw_data.get("source_1", {}).get("data", [])
    kindle_books = raw_data.get("source_2", {}).get("data", [])
    etsy_products = raw_data.get("source_3", {}).get("data", [])
    tiktok_tags = raw_data.get("source_4", {}).get("data", [])
    instagram_tags = raw_data.get("source_5", {}).get("data", [])
    reddit_posts = raw_data.get("source_6", {}).get("data", [])

    for cluster in NICHE_CLUSTERS:
        name = cluster["name"]
        kws = cluster["keywords"]

        def matches(text: str) -> bool:
            text_lower = str(text).lower()
            return any(kw in text_lower for kw in kws)

        # Compter les correspondances par source
        gumroad_matches = [p for p in gumroad_products if matches(p.get("product_name", "") + " " + p.get("category", ""))]
        kindle_matches = [b for b in kindle_books if matches(b.get("title", "") + " " + b.get("category", ""))]
        etsy_matches = [p for p in etsy_products if matches(p.get("product_name", ""))]
        tiktok_matches = [t for t in tiktok_tags if matches(t.get("hashtag", ""))]
        instagram_matches = [i for i in instagram_tags if matches(i.get("hashtag", ""))]
        reddit_matches = [r for r in reddit_posts if matches(r.get("post_title", "") + " " + r.get("body_snippet", ""))]

        # Minimum 2 sources actives pour former un cluster valide
        active_sources = sum([
            1 if gumroad_matches else 0,
            1 if kindle_matches else 0,
            1 if etsy_matches else 0,
            1 if tiktok_matches else 0,
            1 if instagram_matches else 0,
            1 if reddit_matches else 0,
        ])

        if active_sources < 2:
            continue

        # Extraire top pain verbatim depuis Reddit
        top_pain = ""
        pain_url = ""
        if reddit_matches:
            best = sorted(reddit_matches, key=lambda x: x.get("upvotes", 0), reverse=True)
            top_pain = best[0].get("post_title", "")
            pain_url = best[0].get("url", "")

        # Top TikTok signal
        top_tiktok = tiktok_matches[0] if tiktok_matches else {}

        # Top Instagram signal
        top_instagram = instagram_matches[0] if instagram_matches else {}

        signals = {
            "gumroad_count":    len(gumroad_matches),
            "kindle_count":     len(kindle_matches),
            "etsy_count":       len(etsy_matches),
            "tiktok_count":     len(tiktok_matches),
            "instagram_count":  len(instagram_matches),
            "reddit_count":     len(reddit_matches),
        }

        status, reason = apply_elimination_filter(name, signals)

        niche_entry = {
            "niche_name":     name,
            "raw_status":     status,
            "filter_reason":  reason,
            "active_sources": active_sources,
            "signal_sources": (
                (["gumroad"] if gumroad_matches else []) +
                (["kindle"] if kindle_matches else []) +
                (["etsy"] if etsy_matches else []) +
                (["tiktok"] if tiktok_matches else []) +
                (["instagram"] if instagram_matches else []) +
                (["reddit"] if reddit_matches else [])
            ),
            "demand_signals": {
                "gumroad":   {
                    "product_count":         len(gumroad_matches),
                    "avg_sales_comparable":  int(sum(p.get("sales_count", 0) for p in gumroad_matches) / max(len(gumroad_matches), 1)),
                    "price_range":           f"${min((p.get('price_usd', 0) for p in gumroad_matches), default=0)}-${max((p.get('price_usd', 0) for p in gumroad_matches), default=0)}",
                },
                "kindle":    {
                    "bsr_range":       "[DATA MISSING]",
                    "review_velocity": f"{sum(b.get('review_count', 0) for b in kindle_matches)} reviews (top {len(kindle_matches)} titres)",
                    "category":        kindle_matches[0].get("category", "[DATA MISSING]") if kindle_matches else "[DATA MISSING]",
                },
                "etsy":      {
                    "product_count": len(etsy_matches),
                    "avg_sales":     int(sum(p.get("sales_count", 0) for p in etsy_matches) / max(len(etsy_matches), 1)),
                    "price_range":   f"${min((p.get('price_usd', 0) for p in etsy_matches), default=0)}-${max((p.get('price_usd', 0) for p in etsy_matches), default=0)}",
                },
                "tiktok":    {
                    "hashtag":             top_tiktok.get("hashtag", "[DATA MISSING]"),
                    "views_30d":           top_tiktok.get("total_views_30d", 0),
                    "growth_rate_percent": top_tiktok.get("growth_rate_percent", 0),
                },
                "instagram": {
                    "hashtag":        top_instagram.get("hashtag", "[DATA MISSING]"),
                    "post_count":     top_instagram.get("post_count", 0),
                    "avg_engagement": top_instagram.get("avg_likes", 0),
                },
                "reddit":    {
                    "pain_posts_count":  len(reddit_matches),
                    "top_pain_verbatim": top_pain or "[DATA MISSING]",
                    "subreddit":         reddit_matches[0].get("subreddit", "[DATA MISSING]") if reddit_matches else "[DATA MISSING]",
                    "url":               pain_url or "[DATA MISSING]",
                },
            },
            "preliminary_uvz": [],   # Sera enrichi ci-dessous
        }

        # Générer 1-2 UVZ préliminaires basés sur signaux Reddit/TikTok
        if reddit_matches:
            best_reddit = sorted(reddit_matches, key=lambda x: x.get("upvotes", 0), reverse=True)[:2]
            for r in best_reddit:
                niche_entry["preliminary_uvz"].append({
                    "uvz_label":    f"Douleur non résolue: {r.get('post_title', '')[:80]}",
                    "signal_anchor": f"Reddit — {r.get('upvotes', 0)} upvotes",
                    "source_url":   r.get("url", "[DATA MISSING]"),
                })

        niches.append(niche_entry)

    return niches


# ─────────────────────────────────────────────────────────────────────────────
# SÉLECTION FINALE — 15 niches
# ─────────────────────────────────────────────────────────────────────────────
def select_top_niches(niches: list[dict]) -> tuple[list[dict], list[dict]]:
    """
    Sépare les niches actives des éliminées.
    Retourne (active_niches[:15], eliminated_niches).
    """
    active = [n for n in niches if n["raw_status"] in ("ACTIVE", "BORDERLINE")]
    eliminated = [n for n in niches if n["raw_status"] == "ELIMINATED"]

    # Trier par nombre de sources actives (plus il y en a, plus le signal est fort)
    active.sort(key=lambda x: x["active_sources"], reverse=True)

    if len(active) < 15:
        log_warn(f"Seulement {len(active)} niches passent les filtres (cible: 15) — seuil de saturation assoupli")

    top_15 = active[:15]

    # Numéroter les niches
    for i, niche in enumerate(top_15, 1):
        niche["niche_id"] = f"N{i:02d}"
        niche["status"] = niche.pop("raw_status")
        niche.pop("filter_reason", None)

    return top_15, eliminated


# ─────────────────────────────────────────────────────────────────────────────
# POINT D'ENTRÉE PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scraper Agent — Phase 1 Market Discovery")
    parser.add_argument("--market", default="US", choices=["US"], help="Marché cible")
    return parser.parse_args()


def main():
    args = parse_args()

    print(f"\n{BOLD}{'─' * 60}{RESET}")
    print(f"{BOLD}  SCRAPER AGENT — Market Discovery (marché: {args.market}){RESET}")
    print(f"{BOLD}{'─' * 60}{RESET}\n")

    # Charger les variables d'environnement
    env_file = BASE_DIR / ".env"
    if env_file.exists():
        load_dotenv(env_file)

    apify_token    = os.getenv("APIFY_TOKEN")
    tavily_api_key = os.getenv("TAVILY_KEY")

    if not apify_token or not tavily_api_key:
        log_error("APIFY_TOKEN ou TAVILY_KEY manquants — impossible de continuer")
        sys.exit(1)

    # Initialiser les clients API
    apify  = ApifyClient(apify_token)
    tavily = TavilyClient(api_key=tavily_api_key)

    # Charger le SKILL.md pour référence
    skill_content = load_skill_md()
    if skill_content:
        log_info("SKILL.md 01-market-discovery chargé.")

    # ── Lancement parallèle des 6 sources ────────────────────────────────────
    log_info("Lancement parallèle des 6 sources de données...")
    raw_data = {}

    source_functions = {
        "source_1": (scrape_gumroad,       [apify]),
        "source_2": (scrape_amazon_kindle, [apify]),
        "source_3": (scrape_etsy,          [apify]),
        "source_4": (scrape_tiktok,        [apify]),
        "source_5": (scrape_instagram,     [apify]),
        "source_6": (scrape_reddit,        [tavily]),
    }

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = {
            executor.submit(fn, *fn_args): source_key
            for source_key, (fn, fn_args) in source_functions.items()
        }
        for future in as_completed(futures):
            source_key = futures[future]
            try:
                raw_data[source_key] = future.result()
            except Exception as e:
                log_warn(f"{source_key} — exception non capturée: {e}")
                raw_data[source_key] = {"status": "FAILED", "data": [], "error": str(e)}

    # ── Log récapitulatif des statuts ─────────────────────────────────────────
    print(f"\n{BOLD}Récapitulatif des sources:{RESET}")
    statuses = {}
    for i in range(1, 7):
        key = f"source_{i}"
        status = raw_data.get(key, {}).get("status", "FAILED")
        statuses[i] = status
        count = len(raw_data.get(key, {}).get("data", []))
        log_source(str(i), status, f"{count} items")

    # ── Blocking Condition ────────────────────────────────────────────────────
    if statuses.get(1) == "FAILED" and statuses.get(3) == "FAILED":
        log_error("primary market data unavailable — SOURCE 1 ET SOURCE 2 toutes deux FAILED — halt and report")
        sys.exit(1)

    log_info("Blocking Condition évaluée — OK pour continuer.\n")

    # ── Clustering + Filtrage ─────────────────────────────────────────────────
    all_clusters = cluster_signals(raw_data)
    log_info(f"{len(all_clusters)} clusters formés avant filtrage.")

    top_niches, eliminated_niches = select_top_niches(all_clusters)
    log_info(f"{len(top_niches)} niches retenues, {len(eliminated_niches)} éliminées.")

    # ── Construction de l'output JSON ─────────────────────────────────────────
    output = {
        "meta": {
            "skill":          "01-market-discovery",
            "market":         args.market,
            "generated_at":   datetime.utcnow().isoformat() + "Z",
            "sources_status": {
                f"SOURCE_{i}": statuses.get(i, "FAILED") for i in range(1, 7)
            },
            "niches_retained":  len(top_niches),
            "niches_eliminated": len(eliminated_niches),
        },
        "niches": top_niches,
        "eliminated_niches_log": [
            {
                "niche_name": n["niche_name"],
                "reason":     n.get("filter_reason", "ELIMINATED"),
            }
            for n in eliminated_niches
        ],
    }

    # Écrire le fichier output
    OUTPUTS_DIR.mkdir(exist_ok=True)
    output_file = OUTPUTS_DIR / "01-market-discovery.json"
    output_file.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")

    log_info(f"Output écrit: {output_file}")
    print(f"\n{GREEN}{BOLD}[SOURCE SCRAPING COMPLETE]{RESET}")
    print(f"  → {len(top_niches)} niches dans outputs/01-market-discovery.json\n")


if __name__ == "__main__":
    main()
