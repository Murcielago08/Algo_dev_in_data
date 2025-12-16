
try:
    from olama import Client
except ImportError:
    # Fallback si la librairie n'est pas installée pour permettre l'exécution du script
    print("Attention: Librairie 'olama' non trouvée. Utilisation d'un MockClient pour la démonstration.")
    class MockResponse:
        def __init__(self, text):
            self.text = text

    class Client:
        def __init__(self, api_key=None):
            self.api_key = api_key
        
        def generate(self, prompt, model=None):
            # Simulation de réponses basées sur le prompt pour tester la logique
            print(f"[LLM CALL] Model: {model} | Prompt: {prompt[:50]}...")
            if "Résumé" in prompt:
                return MockResponse("Ceci est un résumé concis du texte fourni.")
            elif "Traduire" in prompt:
                return MockResponse("This is a concise summary of the provided text.")
            elif "Reformule" in prompt or "style formel" in prompt:
                return MockResponse("Herein lies a succinct synopsis of the aforementioned text.")
            elif "Simplifier" in prompt:
                return MockResponse("Ref: Summary of text.")
            elif "python" in prompt.lower() or "code" in prompt.lower():
                return MockResponse("def trier_liste(l): return sorted(l)")
            else:
                return MockResponse(f"Réponse générée pour: {prompt[:20]}...")

from difflib import SequenceMatcher

# ---------------------------------------------------------
# 1. COMPOSANTS DE L'ARCHITECTURE
# ---------------------------------------------------------

class Router:
    """Décide quel agent doit traiter la requête."""
    @staticmethod
    def route_request(question):
        q_lower = question.lower()
        if "python" in q_lower or "code" in q_lower or "fonction" in q_lower:
            return "CodeLLM"
        elif "texte" in q_lower or "résumé" in q_lower or "traduire" in q_lower:
            return "ChatLLM"
        else:
            return "GeneralLLM"

class Evaluator:
    """Évalue la qualité des réponses."""
    @staticmethod
    def evaluate(reference, generated):
        # Critère 1: Similitude / Fidélité (pour la traduction/résumé)
        similarity = SequenceMatcher(None, reference, generated).ratio()
        
        # Critère 2: Longueur (simplification devrait être plus courte)
        len_score = 1.0 if len(generated) < len(reference) else 0.5
        
        # Score global pondéré
        final_score = (similarity * 0.7) + (len_score * 0.3)
        return round(final_score, 2)

class Architect:
    """Orchestrateur qui gère le workflow complet."""
    def __init__(self):
        self.client = Client(api_key="VOTRE_CLE_API")
        self.router = Router()
        self.evaluator = Evaluator()

    def run_process_chain(self, initial_text):
        """
        Exécute la chaîne: Résumé -> Traduction -> Reformulation -> Simplification
        """
        print("\n--- Démarrage du Prompt Chaining ---")
        
        # Étape 1: Résumé
        res1 = self.client.generate(f"Résumé ce texte : '{initial_text}'", model="ChatLLM")
        print(f"1. Résumé: {res1.text}")
        
        # Étape 2: Traduction
        res2 = self.client.generate(f"Traduire en anglais : '{res1.text}'", model="ChatLLM")
        print(f"2. Traduction: {res2.text}")
        
        # Étape 3: Reformulation Formelle
        res3 = self.client.generate(f"Reformule de manière formelle : '{res2.text}'", model="ChatLLM")
        print(f"3. Reformulation: {res3.text}")
        
        # Étape 4: Simplification (Challenge 1)
        res4 = self.client.generate(f"Simplifie cette phrase pour un enfant : '{res3.text}'", model="ChatLLM")
        print(f"4. Simplification: {res4.text}")
        
        return res4.text, res2.text # On retourne Simplifié et Traduit pour éval

    def run_parallel_orchestration(self, question):
        """
        Challenge Final: Routing -> Génération Parallèle (Simulée) -> Sélection Meilleur
        """
        print("\n--- Démarrage de l'Orchestration Avancée ---")
        
        # 1. Routing
        agent_type = self.router.route_request(question)
        print(f"-> Routing vers: {agent_type}")
        
        # 2. Génération de variantes (Simulation de "plusieurs agents")
        # Dans un cas réel, on appellerait self.client.generate() deux fois avec des params différents (ex: température)
        print("-> Génération de 2 variantes...")
        variant_1 = self.client.generate(f"V1: {question}", model=agent_type).text
        variant_2 = self.client.generate(f"V2 (plus créatif): {question}", model=agent_type).text
        
        # 3. Évaluation et Sélection
        # Pour évaluer sans "Vérité Terrain" (Ground Truth), on utilise souvent un LLM-as-a-Judge
        # Ici pour le TP, on va simuler une préférence basée sur la longueur ou des mots clés.
        score1 = len(variant_1) 
        score2 = len(variant_2)
        
        print(f"   Variante 1: {variant_1} (Score Longueur: {score1})")
        print(f"   Variante 2: {variant_2} (Score Longueur: {score2})")
        
        best_response = variant_1 if score1 < score2 else variant_2 # Préférence pour court ici arbitrairement
        print(f"-> Meilleure réponse sélectionnée: {best_response}")
        return best_response

# ---------------------------------------------------------
# EXECUTION PRINCIPALE
# ---------------------------------------------------------

if __name__ == "__main__":
    app = Architect()
    
    # CAS 1: Traitement de Texte (Prompt Chaining)
    input_text = "Les agents IA peuvent automatiser des tâches complexes en utilisant des chaînes de prompts et des outils externes."
    final_text, reference_trans = app.run_process_chain(input_text)
    
    # Évaluation finale (Comparaison Simplification vs Traduction juste pour démo evaluator)
    score = app.evaluator.evaluate(reference_trans, final_text)
    print(f"\nScore de transformation (Similitude Traduction vs Simplifié): {score}")
    
    # CAS 2: Question Technique (Camping Challenge Final)
    question_tech = "Écrire une fonction Python pour trier une liste"
    app.run_parallel_orchestration(question_tech)