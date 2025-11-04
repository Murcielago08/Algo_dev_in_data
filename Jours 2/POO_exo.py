from typing import Optional
import uuid

class Personne:
    def __init__(self, nom: str, age: int, ident: Optional[str] = None):
        self.nom = nom
        self.age = age
        self.id = ident or str(uuid.uuid4())

    def presentation(self) -> str:
        return f"Je m'appelle {self.nom} et j'ai {self.age} ans."

class CompteBancaire:
    def __init__(self, titulaire: Personne, solde_initial: float = 0.0):
        self.titulaire = titulaire
        self.solde = solde_initial

    def deposer(self, montant: float):
        if montant <= 0:
            raise ValueError("Le montant du dépôt doit être positif.")
        self.solde += montant
        return montant

    def retirer(self, montant: float):
        if montant <= 0:
            raise ValueError("Le montant du retrait doit être positif.")
        if montant > self.solde:
            raise ValueError("Fonds insuffisants pour ce retrait.")
        self.solde -= montant
        return montant

    def afficher_solde(self) -> str:
        return f"Le solde du compte de {self.titulaire.nom} est de {self.solde:.2f} euros."

class Etudiant(Personne):
    def __init__(self, nom: str, age: int, ident: Optional[str] = None):
        super().__init__(nom, age, ident)
        self.niveau = []

    def print_niveau(self) -> str:
        return ", ".join(self.niveau) if self.niveau else "Aucun niveau d'étude défini."
    
    def etudier(self, niveau: str) -> str:
        """Ajoute un niveau d'étude valide et renvoie une confirmation."""
        if not isinstance(niveau, str) or not niveau.strip():
            raise ValueError("Le niveau doit être une chaîne non vide.")
        
        niveau_clean = niveau.strip()
        
        # Vérifie si le niveau existe déjà et incrémente ou ajoute
        for i in range(len(self.niveau)):
            if self.niveau[i].startswith(niveau_clean):
                current_level = int(self.niveau[i].split()[-1])
                if current_level < 10:
                    self.niveau[i] = f"{niveau_clean} Niveau {current_level + 1}"
                    return f"{self.nom} a maintenant {niveau_clean} Niveau {current_level + 1}"
                else:
                    return f"{niveau_clean} est déjà au niveau maximum."
        
        # Si le niveau n'existe pas, l'ajoute avec le niveau 1
        self.niveau.append(f"{niveau_clean} Niveau 1")
        return f"{self.nom} étudie maintenant : {niveau_clean} Niveau 1"

# Ajout des classes pour l'exercice 4 : Polymorphisme
class Animal:
    def parler(self) -> str:
        """Méthode de base à redéfinir par les sous-classes."""
        raise NotImplementedError("La méthode parler() doit être implémentée par la sous-classe.")

class Chien(Animal):
    def parler(self) -> str:
        return "Wouf!"

class Chat(Animal):
    def parler(self) -> str:
        return "Miaou!"

class Voiture:
    def __init__(self, marque: str, vitesse: float = 0.0):
        # Attributs privés
        self.__marque = marque
        self.__vitesse = vitesse

    # --- Accesseurs (getters) ---
    def get_marque(self) -> str:
        """Retourne la marque de la voiture."""
        return self.__marque

    def get_vitesse(self) -> float:
        """Retourne la vitesse actuelle de la voiture."""
        return self.__vitesse

    # --- Mutateurs (setters) ---
    def set_marque(self, nouvelle_marque: str):
        """Modifie la marque de la voiture."""
        if not nouvelle_marque or not isinstance(nouvelle_marque, str):
            raise ValueError("La marque doit être une chaîne non vide.")
        self.__marque = nouvelle_marque

    def set_vitesse(self, nouvelle_vitesse: float):
        """Modifie la vitesse, avec validation."""
        if not isinstance(nouvelle_vitesse, (int, float)) or nouvelle_vitesse < 0:
            raise ValueError("La vitesse doit être un nombre positif.")
        self.__vitesse = nouvelle_vitesse

    # --- Méthodes d’action ---
    def accelerer(self, gain: float):
        """Augmente la vitesse de la voiture."""
        if gain <= 0:
            raise ValueError("Le gain de vitesse doit être positif.")
        self.__vitesse += gain
        return f"La voiture accélère à {self.__vitesse} km/h."

    def freiner(self, perte: float):
        """Réduit la vitesse sans descendre sous zéro."""
        if perte <= 0:
            raise ValueError("La perte de vitesse doit être positive.")
        self.__vitesse = max(0, self.__vitesse - perte)
        return f"La voiture ralentit à {self.__vitesse} km/h."

    def afficher_infos(self) -> str:
        """Affiche les informations principales de la voiture."""
        return f"Voiture : {self.__marque}, Vitesse actuelle : {self.__vitesse} km/h."

if __name__ == "__main__":
    print("\n----- Personne -----")
    p = Personne("Alice", 30)
    print(p.presentation())
    print(f"ID unique: {p.id}")
    
    print("\n----- Compte Bancaire -----")
    c = CompteBancaire(p, 100.0)
    print(c.afficher_solde())
    print(f"Dépôt de : {c.deposer(50.0)}")
    print(c.afficher_solde())
    print(f"Retrait de : {c.retirer(30.0)}")
    print(c.afficher_solde())

    print("\n----- Étudiant -----")
    e = Etudiant("Bob", 20)
    print(e.presentation())
    print(e.print_niveau())
    print(e.etudier("Informatique"))
    print(e.etudier("Mathématiques"))
    print(e.etudier("Informatique"))
    print(e.print_niveau())

    print("\n----- Animaux (Polymorphisme) -----")
    animaux = [Chien(), Chat(), Chien()]
    for a in animaux:
        print(f"{a.__class__.__name__} : {a.parler()}")

    print("\n----- Voiture (Encapsulation) -----")
    v = Voiture("Tesla", 50)
    print(v.afficher_infos())
    print(v.accelerer(20))
    print(v.freiner(30))
    print(v.afficher_infos())

    # Test des getters et setters
    v.set_marque("BMW")
    v.set_vitesse(120)
    print(f"Nouvelle marque : {v.get_marque()}")
    print(f"Nouvelle vitesse : {v.get_vitesse()} km/h")
    print(v.afficher_infos())

