from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import requests
import json
import os

app = FastAPI()

# 📁 Chemins
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 📄 Dossier de sortie PDF
os.makedirs("output", exist_ok=True)


# ==============================================================
# 🔹 Fonction : Appel à Ollama (modèle llama3:latest)
# ==============================================================
def call_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}

    payload = {
        "model": "llama3:latest",
        "prompt": f"""
Tu es un assistant d'analyse marketing. 
Réponds UNIQUEMENT en JSON, sans texte avant ni après.
Format strict :
{{
  "produits": [
    {{
      "nom": "Nom du produit",
      "prix": 0,
      "tendances": ["motclé1", "motclé2"]
    }}
  ]
}}

Analyse le marché pour cette demande :
{prompt}
"""
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            return {"produits": [{"nom": "Erreur API", "prix": "N/A", "tendances": ["Échec de la requête vers Ollama"]}]}

        # Ollama renvoie souvent la réponse en plusieurs morceaux JSONL
        text = ""
        for line in response.text.splitlines():
            try:
                part = json.loads(line)
                if "response" in part:
                    text += part["response"]
            except json.JSONDecodeError:
                continue

        # Nettoyage du texte pour s'assurer qu'il est bien JSON
        text = text.strip()
        if not text.startswith("{"):
            start = text.find("{")
            if start != -1:
                text = text[start:]

        # Tentative de parsing JSON
        data = json.loads(text)
        return data

    except Exception as e:
        return {"produits": [{"nom": "Erreur JSON", "prix": "N/A", "tendances": [f"Impossible de parser : {str(e)}"]}]}


# ==============================================================
# 🔹 Génération du PDF
# ==============================================================
def generate_pdf(data):
    pdf_path = "output/etude_marche.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 80, "Étude de marché automatique")

    y = height - 130
    c.setFont("Helvetica", 12)

    for produit in data.get("produits", []):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, f"Produit : {produit.get('nom', 'Inconnu')}")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(60, y, f"Prix moyen : {produit.get('prix', 'N/A')}")
        y -= 15

        tendances = produit.get("tendances", [])
        if isinstance(tendances, list):
            tendances = ", ".join(tendances)
        c.drawString(60, y, f"Tendances : {tendances}")
        y -= 25

        if y < 100:
            c.showPage()
            y = height - 100

    c.save()
    return pdf_path


# ==============================================================
# 🔹 Routes FastAPI
# ==============================================================

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/analyse", response_class=HTMLResponse)
def analyse_market(
    request: Request,
    produits: str = Form(...),
    secteur: str = Form(...)
):
    prompt = f"""
Tu es un expert en études de marché. Compare les produits suivants :
{produits}
dans le secteur {secteur}.

Présente :
- Le positionnement de chaque produit,
- Les tendances du marché,
- Les avantages et inconvénients de chacun,
- Un résumé global.

Retourne STRICTEMENT un JSON sous le format :
{{
  "produits": [
    {{
      "nom": "Nom du produit",
      "prix": "valeur indicative",
      "tendances": ["motclé1", "motclé2"],
      "points_forts": ["..."],
      "points_faibles": ["..."]
    }}
  ]
}}
    """
    result = call_ollama(prompt)
    pdf_file = generate_pdf(result)
    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result,
        "pdf_path": pdf_file
    })


# ==============================================================
# ✅ Lancement (si tu veux exécuter directement)
# ==============================================================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
