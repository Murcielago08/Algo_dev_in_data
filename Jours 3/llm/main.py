from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests
import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- Configuration de l'app FastAPI ---
app = FastAPI()

# --- Dossiers templates et statiques ---
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- Dossier de sortie PDF ---
os.makedirs("output", exist_ok=True)
app.mount("/output", StaticFiles(directory="output"), name="output")


# --- Fonction pour appeler Ollama ---
def call_ollama(prompt: str):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": "llama3:latest",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        data = response.json()
        return data.get("response", "Erreur : aucune réponse reçue du modèle.")
    except Exception as e:
        return f"Erreur lors de l'appel à Ollama : {e}"


# --- Fonction pour générer un PDF ---
def generate_pdf(result_text: str):
    pdf_path = "output/etude_marche.pdf"

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 80, "Étude de marché automatique")
    c.setFont("Helvetica", 12)

    y = height - 120
    for line in result_text.split("\n"):
        if y < 50:
            c.showPage()
            y = height - 80
            c.setFont("Helvetica", 12)
        c.drawString(40, y, line[:1000])
        y -= 18

    c.save()
    return pdf_path


# --- Page d'accueil (formulaire) ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- Traitement du formulaire et affichage du résultat ---
@app.post("/analyse", response_class=HTMLResponse)
def analyse_market(request: Request, produits: str = Form(...), secteur: str = Form(...)):
    prompt = f"""
Tu es un expert en études de marché.
Analyse et compare les produits suivants : {produits}
dans le secteur : {secteur}.
Donne pour chaque produit :
- Le positionnement et la cible
- Le prix moyen estimé
- Les parts de marché (approximatives)
- Les tendances actuelles
- Les forces et faiblesses
Répond dans un style professionnel et structuré.
"""

    result = call_ollama(prompt)
    pdf_path = generate_pdf(result)
    pdf_url = "/output/etude_marche.pdf"

    return templates.TemplateResponse("result.html", {
        "request": request,
        "result": result,
        "pdf_url": pdf_url
    })
