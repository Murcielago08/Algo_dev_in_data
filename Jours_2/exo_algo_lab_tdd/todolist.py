class TodoList:
    """
    Classe représentant une liste de tâches simple.
    """

    def __init__(self):
        self.taches = []

    def ajouter_tache(self, description: str):
        """Ajoute une tâche non terminée."""
        if not description or not description.strip():
            raise ValueError("La description de la tâche ne peut pas être vide.")
        self.taches.append({"description": description.strip(), "terminee": False})

    def marquer_terminee(self, description: str):
        """Marque une tâche comme terminée."""
        for tache in self.taches:
            if tache["description"] == description:
                tache["terminee"] = True
                return
        raise ValueError(f"Tâche '{description}' introuvable.")

    def supprimer_tache(self, description: str):
        """Supprime une tâche de la liste."""
        for tache in self.taches:
            if tache["description"] == description:
                self.taches.remove(tache)
                return
        raise ValueError(f"Tâche '{description}' introuvable.")

    def lister_taches(self, terminee: bool | None = None):
        """
        Retourne la liste des tâches.
        - terminee=True → uniquement les tâches terminées
        - terminee=False → uniquement les tâches en cours
        - terminee=None → toutes les tâches
        """
        if terminee is None:
            return self.taches
        return [t for t in self.taches if t["terminee"] == terminee]
