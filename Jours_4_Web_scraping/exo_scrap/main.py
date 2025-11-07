import os
import pandas as pd
from serpapi import GoogleSearch
from dotenv import load_dotenv
from openai import OpenAI

# ===============================
# CHARGEMENT DES CLÉS API
# ===============================
".env à créer dans le répertoire racine"
load_dotenv()
print(os.getenv("SERPAPI_KEY"))
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


# ===============================
# ÉTAPE 1 : COLLECTE DES DONNÉES
# ===============================
def fetch_google_play_apps(query="fitness apps"):
    params = {
        "engine": "google_play",
        "q": query,
        "api_key": SERPAPI_KEY
    }
    print("🔎 Test SerpAPI avec paramètres :", params)

    search = GoogleSearch(params)
    results = search.get_dict()

    # Affiche les 2 premières clés de la réponse
    print("🧩 Clés disponibles dans la réponse :", list(results.keys())[:5])
    print("📱 Exemple de résultat brut :", results.get("apps", [])[0:1])

    return pd.DataFrame(results.get("apps", []))


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
