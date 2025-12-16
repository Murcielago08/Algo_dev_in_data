import textwrap

class AgentIA:
    """Classe de base pour tous les agents IA."""
    def __init__(self, nom, categorie, description, architecture, caracteristiques, exemples, limitations=None):
        self.nom = nom
        self.categorie = categorie
        self.description = description
        self.architecture = architecture
        self.caracteristiques = caracteristiques
        self.exemples = exemples
        self.limitations = limitations

    def afficher_details(self):
        print(f"\n{'='*60}")
        print(f"AGENT: {self.nom}")
        print(f"CATÉGORIE: {self.categorie}")
        print(f"{'='*60}")
        print(f"\n[DESCRIPTION]\n{textwrap.fill(self.description, width=60)}")
        print(f"\n[ARCHITECTURE]\n{self.architecture}")
        
        print(f"\n[CARACTÉRISTIQUES]")
        for car in self.caracteristiques:
            print(f"- {car}")
            
        print(f"\n[EXEMPLES]")
        for ex in self.exemples:
            print(f"- {ex}")
            
        if self.limitations:
            print(f"\n[LIMITATIONS]")
            if isinstance(self.limitations, list):
                for lim in self.limitations:
                    print(f"- {lim}")
            else:
                print(f"- {self.limitations}")

class AgentReactifSimple(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent Réactif Simple",
            categorie="Basique",
            description="Le plus basique, fonctionnant selon le principe 'perception-action' sans mémoire interne.",
            architecture="Perception -> Action (Règle directe)",
            caracteristiques=[
                "Pas de mémoire des états passés",
                "Actions déterminées uniquement par l'état courant",
                "Réponses rapides mais limitées"
            ],
            exemples=["Thermostats intelligents", "Détecteurs de mouvement"],
            limitations="Incapacité à apprendre ou à s'adapter à de nouvelles situations"
        )

class AgentReactifModele(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent Réactif avec Modèle",
            categorie="Intermédiaire",
            description="Intègre une représentation interne du monde pour mieux prendre des décisions.",
            architecture="Perception -> Modèle du monde -> Action",
            caracteristiques=[
                "Maintient un état interne du monde",
                "Peut gérer des environnements partiellement observables",
                "Plus flexible que les agents purement réactifs",
                "Équation : action = f(perception, etat_interne)"
            ],
            exemples=["Robots de nettoyage autonomes", "Systèmes de navigation basique"]
        )

class AgentBaseObjectifs(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent à Base d'Objectifs",
            categorie="Délibératif",
            description="Prend des décisions en fonction d'objectifs spécifiques à atteindre.",
            architecture="Perception -> État -> Objectifs -> Planification -> Action",
            caracteristiques=[
                "Évalue les actions en fonction de leur contribution aux objectifs",
                "Capacité de planification et de raisonnement",
                "Peut faire des compromis entre objectifs conflictuels",
                "Utilisation d'algorithmes de recherche et d'optimisation"
            ],
            exemples=["Systèmes de recommandation", "Assistants virtuels simples"]
        )

class AgentUtilitaire(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent Utilitaire",
            categorie="Délibératif",
            description="Maximise une fonction d'utilité qui mesure la performance.",
            architecture="Perception -> État -> Utilité -> Décision -> Action",
            caracteristiques=[
                "Évalue les états selon une mesure d'utilité",
                "Peut gérer l'incertitude et les risques",
                "Optimise les décisions en fonction de préférences",
                "Fonction d'utilité : U(s) = Somme(wi * fi(s))"
            ],
            exemples=["Systèmes de trading algorithmique", "Contrôleurs de trafic intelligents"]
        )

class AgentApprenant(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent Apprenant",
            categorie="Adaptatif",
            description="Améliore ses performances grâce à l'expérience et l'apprentissage.",
            architecture="Perception -> Apprentissage -> Connaissances -> Action",
            caracteristiques=[
                "Capacité d'apprentissage à partir des données",
                "Adaptation aux changements environnementaux",
                "Amélioration continue des performances",
                "Méthodes : Supervisé, Non-supervisé, Par renforcement"
            ],
            exemples=["Recommandateurs personnalisés", "Voitures autonomes"]
        )

class AgentCognitif(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent Cognitif",
            categorie="Avancé",
            description="Simule des processus de pensée humains comme le raisonnement et la conscience.",
            architecture="Perception -> Mémoire -> Raisonnement -> Planification -> Action",
            caracteristiques=[
                "Représentation symbolique des connaissances",
                "Capacités de raisonnement déductif et inductif",
                "Mémoire à long terme et apprentissage conceptuel",
                "Prise de décision métacognitive",
                "Composants : Perception avancée, Base de connaissances, Moteur d'inférence, etc."
            ],
            exemples=["Systèmes experts médicaux", "Assistants IA conversationnels avancés"]
        )

class SystemeMultiAgents(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Système Multi-Agents (SMA)",
            categorie="Distribué",
            description="Implique plusieurs agents interagissant pour résoudre des problèmes complexes.",
            architecture="Plusieurs agents + Environnement partagé + Communication",
            caracteristiques=[
                "Architecture distribuée",
                "Types d'interactions : Coopérative, Compétitive, Mixte",
                "Protocoles : ACL, KQML, FIPA",
                "Avantages : Robustesse, scalabilité"
            ],
            exemples=["Marchés électroniques", "Contrôle de trafic aérien", "Simulations sociales"],
            limitations="Coordination complexe"
        )

class AgentEmotionnel(AgentIA):
    def __init__(self):
        super().__init__(
            nom="Agent Émotionnel",
            categorie="Avancé / Interaction",
            description="Intègre des composantes émotionnelles pour des interactions plus naturelles.",
            architecture="Perception -> Modèle émotionnel -> Raisonnement -> Action",
            caracteristiques=[
                "Reconnaissance des émotions (entrée)",
                "Génération d'émotions (simulation)",
                "Expression émotionnelle (sortie)",
                "Modèles : OCC, PAD"
            ],
            exemples=["Companions numériques", "Éducation personnalisée", "Jeux vidéo"]
        )

def main():
    print("CLASSIFICATION ET CARACTÉRISTIQUES DÉTAILLÉES - AGENTS IA")
    print("Basé sur le document du 16 décembre 2025")
    
    # Instanciation des agents
    agents = [
        AgentReactifSimple(),
        AgentReactifModele(),
        AgentBaseObjectifs(),
        AgentUtilitaire(),
        AgentApprenant(),
        AgentCognitif(),
        SystemeMultiAgents(),
        AgentEmotionnel()
    ]
    
    # Affichage
    for agent in agents:
        agent.afficher_details()

if __name__ == "__main__":
    main()
