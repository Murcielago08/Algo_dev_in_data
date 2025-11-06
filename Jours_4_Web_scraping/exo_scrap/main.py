import os
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from openai import OpenAI

# ===============================
# CHARGEMENT DES CLÉS API
# ===============================
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ===============================
# ÉTAPE 1 : COLLECTE DES DONNÉES
# ===============================
def fetch_google_play_apps(query="productivity apps"):
    """Récupère une liste d'applications Google Play depuis SerpAPI."""
    params = {
        "engine": "google_play",
        "q": query,
        "api_key": SERPAPI_KEY
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    apps_data = results.get("apps", [])
    if not apps_data:
        print("⚠️ Aucun résultat trouvé. Vérifie ta clé SerpAPI ou essaie un autre mot-clé.")
        return pd.DataFrame()

    apps = []
    for app in apps_data:
        apps.append({
            "title": app.get("title", ""),
            "developer": app.get("developer", ""),
            "score": app.get("score", None),
            "installs": app.get("installs", None),
            "category": app.get("category", ""),
            "description": app.get("description", "")
        })

    return pd.DataFrame(apps)


# ===============================
# ÉTAPE 2 : NETTOYAGE DES DONNÉES
# ===============================
def clean_data(df):
    """Nettoie et prépare le dataset pour l’analyse."""
    if df.empty:
        print("❌ DataFrame vide, rien à nettoyer.")
        return df

    # Suppression des doublons
    df = df.drop_duplicates(subset=["title", "developer"], keep="first")

    # Normalisation des téléchargements si la colonne existe
    def normalize_installs(x):
        if not isinstance(x, str):
            return None
        x = x.replace("+", "").replace(",", "").strip()
        if "K" in x:
            return int(float(x.replace("K", "")) * 1_000)
        elif "M" in x:
            return int(float(x.replace("M", "")) * 1_000_000)
        elif "B" in x:
            return int(float(x.replace("B", "")) * 1_000_000_000)
        elif x.isdigit():
            return int(x)
        return None

    if "installs" in df.columns:
        df["installs"] = df["installs"].apply(normalize_installs)

    # Nettoyage des caractères spéciaux
    for col in ["title", "description"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(r"[^a-zA-Z0-9\s]", "", regex=True)

    return df


# ===============================
# ÉTAPE 3 : ANALYSE AVEC LLM
# ===============================
def generate_llm_report(df):
    """Génère un rapport synthétique via un LLM OpenAI."""
    if df.empty:
        return "Aucune donnée à analyser."

    if not OPENAI_API_KEY:
        return "Clé OpenAI manquante — rapport non généré."

    client = OpenAI(api_key=OPENAI_API_KEY)

    data_preview = df.head(10).to_csv(index=False)
    prompt = f"""
Voici un dataset contenant des informations sur des applications Google Play :

{data_preview}

Analyse-le et génère un rapport synthétique comprenant :
- Les catégories les plus populaires
- Les applications les mieux notées
- Les plus téléchargées
- Des recommandations pour un utilisateur ou un développeur
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


# ===============================
# PROGRAMME PRINCIPAL
# ===============================
if __name__ == "__main__":
    print("🔍 Récupération des applications Google Play...")
    df = fetch_google_play_apps("fitness apps")

    if df.empty:
        print("❌ Aucun résultat récupéré — arrêt du script.")
        exit()

    print(f"✅ {len(df)} applications récupérées.")
    print(df.head())

    print("\n🧹 Nettoyage des données...")
    df_clean = clean_data(df)
    print(f"✅ {len(df_clean)} lignes après nettoyage.")

    # Sauvegarde
    os.makedirs("data", exist_ok=True)
    df_clean.to_csv("data/google_play_apps.csv", index=False)
    print("💾 Données sauvegardées dans data/google_play_apps.csv")

    # Génération du rapport LLM
    print("\n🧠 Génération du rapport avec LLM (si clé OpenAI présente)...")
    report = generate_llm_report(df_clean)
    print("\n===== RAPPORT SYNTHÉTIQUE =====\n")
    print(report)
