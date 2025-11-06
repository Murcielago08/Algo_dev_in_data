# QCM - Master 1 Algo Lab3 (2025)

## Structures de données

- Q1. Quelle est la complexité moyenne d’accès à un élément dans une liste chaînée ?
  - (a) O(1)
  - (b) O(log n)
  - **<span style="color:green;">(c) O(n)</span>**
  - (d) O(n²)

- Q2. Dans une pile (stack), l’élément inséré en dernier est :
  - **<span style="color:green;">(a) Le premier à sortir</span>**
  - (b) Le dernier à sortir
  - (c) Jamais supprimé
  - (d) Trié automatiquement

- Q3. La différence principale entre une pile et une file est :
  - (a) L’ordre d’insertion
  - **<span style="color:green;">(b) L’ordre de retrait</span>**
  - (c) La taille maximale
  - (d) L’implémentation en mémoire

- Q4. Une file (queue) suit le principe :
  - (a) LIFO
  - **<span style="color:green;">(b) FIFO</span>**
  - (c) FILO
  - (d) Random Access

- Q5. Une liste doublement chaînée permet :
  - (a) De parcourir les éléments dans un seul sens
  - (b) D’accéder directement à la fin sans parcourir
  - **<span style="color:green;">(c) De parcourir dans les deux sens</span>**
  - (d) De stocker uniquement des entiers

- Q6. Quelle structure de données est la plus adaptée pour implémenter un système de backtracking ?
  - **<span style="color:green;">(a) Pile</span>**
  - (b) File
  - (c) Tableau
  - (d) Graphe


## Programmation Orientée Objet (OOP)

- Q7. Une classe définit :
  - (a) Une instance d’objet
  - **<span style="color:green;">(b) Un modèle d’objet</span>**
  - (c) Un espace mémoire réservé
  - (d) Une fonction globale

- Q8. Le polymorphisme permet :
  - **<span style="color:green;">(a) D’utiliser plusieurs classes différentes avec une même interface</span>**
  - (b) D’éviter l’héritage
  - (c) De supprimer les méthodes virtuelles
  - (d) De créer des objets sans constructeur

- Q9. L’héritage multiple est :
  - (a) Toujours autorisé
  - (b) Interdit dans tous les langages
  - **<span style="color:green;">(c) Autorisé selon le langage</span>**
  - (d) Équivalent au polymorphisme

- Q10. Une méthode abstraite :
  - (a) Possède une implémentation par défaut
  - **<span style="color:green;">(b) N’a pas d’implémentation</span>**
  - (c) Est toujours statique
  - (d) Est privée

- Q11. Une interface sert à :
  - **<span style="color:green;">(a) Définir un contrat sans implémentation</span>**
  - (b) Créer des objets
  - (c) Étendre une classe existante
  - (d) Optimiser les performances

- Q12. L’encapsulation permet de :
  - **<span style="color:green;">(a) Cacher les détails internes d’une classe</span>**
  - (b) Supprimer les attributs publics
  - (c) Créer plusieurs constructeurs
  - (d) Empêcher l’héritage

- Q13. Une méthode statique :
  - **<span style="color:green;">(a) Peut être appelée sans instance</span>**
  - (b) Nécessite une instance
  - (c) Est abstraite
  - (d) Ne peut pas retourner de valeur

- Q14. En Python, le mot-clé super() sert à :
  - **<span style="color:green;">(a) Appeler la méthode parente</span>**
  - (b) Créer une nouvelle classe
  - (c) Supprimer une méthode
  - (d) Créer un constructeur


## Clean Architecture

- Q15. Le principe fondamental de la Clean Architecture est :
  - **<span style="color:green;">(a) Séparer les couches métier et infrastructure</span>**
  - (b) Minimiser les tests unitaires
  - (c) Fusionner les contrôleurs et services
  - (d) Éviter les dépendances inversées

- Q16. La dépendance inversée signifie :
  - **<span style="color:green;">(a) Le domaine ne dépend pas des détails techniques</span>**
  - (b) Les modules externes contrôlent la logique métier
  - (c) Les classes filles dépendent des parents
  - (d) Les entités dépendent des frameworks

- Q17. Dans une architecture propre, les entités :
  - **<span style="color:green;">(a) Ne doivent pas dépendre des frameworks</span>**
  - (b) Sont implémentées dans les contrôleurs
  - (c) Dépendent des adaptateurs
  - (d) Font partie de la couche interface

- Q18. Le but des "use cases" est de :
  - **<span style="color:green;">(a) Exprimer les règles métier</span>**
  - (b) Gérer la base de données
  - (c) Contrôler les requêtes HTTP
  - (d) Stocker la configuration


## FastAPI

- Q19. FastAPI est principalement basé sur :
  - (a) Flask
  - (b) Django
  - **<span style="color:green;">(c) Starlette et Pydantic</span>**
  - (d) Tornado

- Q20. Le décorateur @app.get("/") définit :
  - **<span style="color:green;">(a) Une route GET</span>**
  - (b) Une route POST
  - (c) Une route PUT
  - (d) Une fonction interne

- Q21. Pour définir un modèle de données dans FastAPI, on utilise :
  - (a) dataclass
  - (b) pandas.DataFrame
  - **<span style="color:green;">(c) BaseModel de Pydantic</span>**
  - (d) ORMModel

- Q22. FastAPI est connu pour :
  - **<span style="color:green;">(a) Sa rapidité et la validation automatique</span>**
  - (b) Sa lenteur mais stabilité
  - (c) Son intégration unique avec Flask
  - (d) Son absence de typage

- Q23. Pour lancer une application FastAPI, on utilise :
  - (a) python app.py
  - **<span style="color:green;">(b) uvicorn main:app --reload</span>**
  - (c) flask run
  - (d) fastapi run app


## LLM (Large Language Models)

- Q24. Un LLM est principalement entraîné sur :
  - (a) Des images
  - **<span style="color:green;">(b) Du texte</span>**
  - (c) Du code binaire
  - (d) Des données sonores uniquement

- Q25. Le but d’un LLM est de :
  - **<span style="color:green;">(a) Prédire la prochaine séquence de mots</span>**
  - (b) Compiler du code
  - (c) Convertir du texte en image
  - (d) Traduire automatiquement les pages web

- Q26. Les modèles comme GPT utilisent :
  - **<span style="color:green;">(a) Des réseaux de neurones de type Transformer</span>**
  - (b) Des arbres binaires
  - (c) Des réseaux CNN
  - (d) Des machines à vecteurs de support

- Q27. Le prompt engineering consiste à :
  - **<span style="color:green;">(a) Optimiser la formulation d’entrée pour obtenir de meilleures réponses</span>**
  - (b) Modifier le modèle interne
  - (c) Retrainer un modèle LLM
  - (d) Changer le format des données d’entraînement

- Q28. Les API comme OpenAI ou Ollama permettent :
  - **<span style="color:green;">(a) D’intégrer un LLM dans une application</span>**
  - (b) De créer des bases de données
  - (c) D’héberger un site web
  - (d) De gérer des transactions financières
