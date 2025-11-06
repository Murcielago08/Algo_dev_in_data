import unittest
import tempfile
import os
import random
from fibonacci import fibonacci
from todolist import TodoList
from math_utils import MathUtils
from csv_reader import lire_csv_en_dict
from logger import SimpleLogger
from bibliotheque import Livre, Bibliotheque
from rps import rps
from decorators import retry
from personne import Personne
from text_vote import normalize_text_quinettoieuntextepminuscules_suppressionponctuationq, VoteSystem

#Exo 1
class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self.titulaire = titulaire
        self.solde = solde_initial

    def deposer(self, montant: float):
        if montant <= 0:
            print("❌ Le montant du dépôt doit être positif.")
            return 0
        self.solde += montant
        print(f"✅ Dépôt de {montant:.2f} euros effectué.")
        return montant

    def retirer(self, montant: float):
        if montant <= 0:
            print("❌ Le montant du retrait doit être positif.")
            return 0
        if montant > self.solde:
            print(f"⚠️ Retrait refusé : solde insuffisant ({self.solde:.2f} € disponibles).")
            return 0
        self.solde -= montant
        print(f"💸 Retrait de {montant:.2f} euros effectué avec succès.")
        return montant
    
    def afficher_solde(self) -> str:
        return f"💰 Le solde du compte de {self.titulaire} est de {self.solde:.2f} euros."

#Exo 2
class TestFibonacci(unittest.TestCase):
    def test_fibonacci_zero(self):
        self.assertEqual(fibonacci(0), 0)

    def test_fibonacci_un(self):
        self.assertEqual(fibonacci(1), 1)

    def test_fibonacci_classique(self):
        self.assertEqual(fibonacci(5), 5)   # 0,1,1,2,3,5
        self.assertEqual(fibonacci(10), 55) # vérif plus grande valeur

    def test_fibonacci_negatif(self):
        with self.assertRaises(ValueError):
            fibonacci(-3)

#Exo 3
class TestTodoList(unittest.TestCase):

    def setUp(self):
        self.todo = TodoList()

    def test_ajouter_tache(self):
        self.todo.ajouter_tache("Acheter du pain")
        self.assertEqual(len(self.todo.taches), 1)
        self.assertEqual(self.todo.taches[0]["description"], "Acheter du pain")
        self.assertFalse(self.todo.taches[0]["terminee"])

    def test_ajouter_tache_vide(self):
        with self.assertRaises(ValueError):
            self.todo.ajouter_tache("")

    def test_marquer_terminee(self):
        self.todo.ajouter_tache("Faire les devoirs")
        self.todo.marquer_terminee("Faire les devoirs")
        self.assertTrue(self.todo.taches[0]["terminee"])

    def test_marquer_terminee_inexistante(self):
        with self.assertRaises(ValueError):
            self.todo.marquer_terminee("Tâche inconnue")

    def test_supprimer_tache(self):
        self.todo.ajouter_tache("Aller courir")
        self.todo.supprimer_tache("Aller courir")
        self.assertEqual(len(self.todo.taches), 0)

    def test_supprimer_tache_inexistante(self):
        with self.assertRaises(ValueError):
            self.todo.supprimer_tache("Dormir")

    def test_lister_taches(self):
        self.todo.ajouter_tache("Lire un livre")
        self.todo.ajouter_tache("Faire du sport")
        self.todo.marquer_terminee("Lire un livre")

        toutes = self.todo.lister_taches()
        terminees = self.todo.lister_taches(terminee=True)
        en_cours = self.todo.lister_taches(terminee=False)

        self.assertEqual(len(toutes), 2)
        self.assertEqual(len(terminees), 1)
        self.assertEqual(len(en_cours), 1)
        self.assertEqual(terminees[0]["description"], "Lire un livre")

#Exo 4
class TestMathUtils(unittest.TestCase):

    # --- factorial ---
    def test_factorial_zero(self):
        self.assertEqual(MathUtils.factorial(0), 1)

    def test_factorial_positif(self):
        self.assertEqual(MathUtils.factorial(5), 120)

    def test_factorial_negatif(self):
        with self.assertRaises(ValueError):
            MathUtils.factorial(-3)

    # --- is_prime ---
    def test_is_prime_vrai(self):
        self.assertTrue(MathUtils.is_prime(7))
        self.assertTrue(MathUtils.is_prime(2))

    def test_is_prime_faux(self):
        self.assertFalse(MathUtils.is_prime(1))
        self.assertFalse(MathUtils.is_prime(9))
        self.assertFalse(MathUtils.is_prime(0))

    # --- gcd ---
    def test_gcd_valeurs(self):
        self.assertEqual(MathUtils.gcd(54, 24), 6)
        self.assertEqual(MathUtils.gcd(10, 0), 10)
        self.assertEqual(MathUtils.gcd(0, 0), 0)
        self.assertEqual(MathUtils.gcd(-8, 12), 4)

#Exo 5
class TestLireCSVEnDict(unittest.TestCase):

    def setUp(self):
        # Création d'un fichier CSV temporaire pour les tests
        self.tempfile = tempfile.NamedTemporaryFile(mode="w", delete=False, newline='', suffix=".csv")
        self.tempfile.write("nom,age,ville\n")
        self.tempfile.write("Alice,30,Paris\n")
        self.tempfile.write("Bob,25,Lyon\n")
        self.tempfile.close()
        self.chemin = self.tempfile.name

    def tearDown(self):
        # Suppression du fichier après les tests
        os.remove(self.chemin)

    def test_lecture_csv_valide(self):
        resultat = lire_csv_en_dict(self.chemin)
        attendu = [
            {"nom": "Alice", "age": "30", "ville": "Paris"},
            {"nom": "Bob", "age": "25", "ville": "Lyon"}
        ]
        self.assertEqual(resultat, attendu)

    def test_fichier_vide(self):
        fichier_vide = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
        fichier_vide.close()
        resultat = lire_csv_en_dict(fichier_vide.name)
        self.assertEqual(resultat, [])
        os.remove(fichier_vide.name)

    def test_fichier_inexistant(self):
        with self.assertRaises(FileNotFoundError):
            lire_csv_en_dict("fichier_qui_nexiste_pas.csv")

class TestLogger(unittest.TestCase):
    def test_logger_memory_and_file(self):
        tmp = tempfile.NamedTemporaryFile(delete=False)
        tmp.close()
        path = tmp.name

        log = SimpleLogger()
        log.log('info', 'Hello')
        log.log('error', 'Something went wrong')
        self.assertEqual(len(log.records), 2)
        log.write_to_file(path)

        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        os.unlink(path)

        self.assertIn('INFO', content)
        self.assertIn('Hello', content)


class TestBibliotheque(unittest.TestCase):
    def setUp(self):
        self.lib = Bibliotheque()
        self.book1 = Livre('Le Petit Prince', 'Saint-Exupéry', '123')
        self.book2 = Livre('Le Grand Livre', 'Auteur', '456')

    def test_add_and_search(self):
        self.lib.add_book(self.book1)
        self.lib.add_book(self.book2)
        res = self.lib.search_by_title('Petit')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].isbn, '123')

    def test_remove(self):
        self.lib.add_book(self.book1)
        ok = self.lib.remove_by_isbn('123')
        self.assertTrue(ok)
        self.assertEqual(self.lib.count(), 0)


class TestRPS(unittest.TestCase):
    def test_all_combinations(self):
        choices = ['rock', 'paper', 'scissors']
        results = {('rock','scissors'), ('scissors','paper'), ('paper','rock')}
        for a in choices:
            for b in choices:
                res = rps(a,b)
                if a == b:
                    self.assertEqual(res, 'draw')
                elif (a,b) in results:
                    self.assertEqual(res, 'player1')
                else:
                    self.assertEqual(res, 'player2')


class TestRetry(unittest.TestCase):
    def test_retry_success_after_failures(self):
        state = {'calls': 0}

        @retry(max_attempts=4, exceptions=(ValueError,), delay=0)
        def flaky():
            state['calls'] += 1
            if state['calls'] < 3:
                raise ValueError('fail')
            return 'ok'

        self.assertEqual(flaky(), 'ok')
        self.assertEqual(state['calls'], 3)

    def test_retry_raises(self):
        @retry(max_attempts=2, exceptions=(RuntimeError,), delay=0)
        def always_fail():
            raise RuntimeError('boom')
        with self.assertRaises(RuntimeError):
            always_fail()


class TestPersonne(unittest.TestCase):
    def test_personne_properties(self):
        p = Personne('Alice', 30)
        self.assertEqual(p.name, 'Alice')
        self.assertEqual(p.age, 30)
        p.age = 31
        self.assertEqual(p.age, 31)
        with self.assertRaises(ValueError):
            p.age = -5


class TestTextVote(unittest.TestCase):
    def test_normalize_text(self):
        s = " Hello, WORLD!! This is a test... "
        result = normalize_text_quinettoieuntextepminuscules_suppressionponctuationq(s)
        self.assertEqual(result, 'hello world this is a test')

    def test_vote_system(self):
        v = VoteSystem()
        v.add_candidate('Alice')
        v.add_candidate('Bob')
        v.vote('Alice')
        v.vote('Bob')
        v.vote('Alice')
        self.assertEqual(v.counts()['Alice'], 2)
        self.assertEqual(v.winner(), 'Alice')
        with self.assertRaises(ValueError):
            v.vote('Charles')



if __name__ == "__main__":
    print("----- Exo 1 -----")
    c = CompteBancaire("Dupont", 100.0)
    print(c.afficher_solde())
    c.deposer(50.0)
    print(c.afficher_solde())
    c.retirer(30.0)
    print(c.afficher_solde())
    c.retirer(130.0)
    print(c.afficher_solde())
    print("\n----- Exo 2 -----")
    print("Fibonacci(0) =", fibonacci(0))   # 0
    print("Fibonacci(1) =", fibonacci(1))   # 1
    print("Fibonacci(6) =", fibonacci(6))   # 8
    print("Fibonacci(10) =", fibonacci(10)) # 55

    # Test d’erreur
    try:
        fibonacci(-2)
    except ValueError as e:
        print("Erreur capturée :", e)

    print("\n----- Exo 3 -----")
    todo = TodoList()

    # Ajouter des tâches
    todo.ajouter_tache("Faire les courses")
    todo.ajouter_tache("Étudier Python")
    todo.ajouter_tache("Aller courir")

    # Lister toutes les tâches
    print("Toutes les tâches :", todo.lister_taches())

    # Marquer une tâche comme terminée
    todo.marquer_terminee("Faire les courses")
    print("Tâches terminées :", todo.lister_taches(terminee=True))

    # Supprimer une tâche
    todo.supprimer_tache("Aller courir")
    print("Après suppression :", todo.lister_taches())

    # Erreurs attendues
    try:
        todo.marquer_terminee("Dormir")
    except ValueError as e:
        print("Erreur :", e)

    try:
        todo.ajouter_tache("")
    except ValueError as e:
        print("Erreur :", e)

    print("\n----- Exo 4 -----")
    # Factorielle
    print("5! =", MathUtils.factorial(5))  # 120
    print("0! =", MathUtils.factorial(0))  # 1

    try:
        MathUtils.factorial(-2)
    except ValueError as e:
        print("Erreur :", e)

    # Test de primalité
    print("7 est premier ?", MathUtils.is_prime(7))  # True
    print("9 est premier ?", MathUtils.is_prime(9))  # False
    print("1 est premier ?", MathUtils.is_prime(1))  # False

    # PGCD
    print("PGCD(54, 24) =", MathUtils.gcd(54, 24))   # 6
    print("PGCD(10, 0) =", MathUtils.gcd(10, 0))     # 10
    print("PGCD(0, 0) =", MathUtils.gcd(0, 0))       # 0
    print("PGCD(-8, 12) =", MathUtils.gcd(-8, 12))   # 4

    print("\n----- Exo 5 -----")
    # Création d’un fichier CSV temporaire
    temp = tempfile.NamedTemporaryFile(mode="w", delete=False, newline='', suffix=".csv")
    temp.write("nom,age,ville\n")
    temp.write("Alice,30,Paris\n")
    temp.write("Bob,25,Lyon\n")
    temp.close()

    # Lecture du fichier
    resultat = lire_csv_en_dict(temp.name)
    print("Lecture CSV :", resultat)

    # Fichier vide
    temp_vide = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv")
    temp_vide.close()
    print("Lecture fichier vide :", lire_csv_en_dict(temp_vide.name))

    # Fichier inexistant
    try:
        lire_csv_en_dict("fichier_inexistant.csv")
    except FileNotFoundError as e:
        print("Erreur :", e)

    # Nettoyage
    os.remove(temp.name)
    os.remove(temp_vide.name)

    print("----- Exo 7 : Logger -----")

    log = SimpleLogger()
    log.log("info", "Application démarrée")
    log.log("warning", "Attention, mémoire faible")
    log.log("error", "Une erreur s’est produite")

    print("Logs en mémoire :")
    for entry in log.records:
        print("  ", entry)

    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.close()
    log.write_to_file(temp.name)
    print(f"Logs écrits dans : {temp.name}")
    with open(temp.name, 'r', encoding='utf-8') as f:
        print("Contenu du fichier log :")
        print(f.read())
    os.remove(temp.name)

    print("\n----- Exo 8 : Livre & Bibliothèque -----")

    biblio = Bibliotheque()
    livre1 = Livre("1984", "George Orwell", "A1")
    livre2 = Livre("Le Petit Prince", "Saint-Exupéry", "A2")
    livre3 = Livre("Python Facile", "Guido van Rossum", "A3")

    biblio.add_book(livre1)
    biblio.add_book(livre2)
    biblio.add_book(livre3)

    print("Livres contenant 'Python' :", [l.title for l in biblio.search_by_title("Python")])
    print("Livres de Saint-Exupéry :", [l.title for l in biblio.search_by_author("exupéry")])
    print("Nombre total de livres :", biblio.count())

    biblio.remove_by_isbn("A2")
    print("Après suppression (A2), nombre total :", biblio.count())

    print("\n----- Exo 9 : Pierre-Papier-Ciseaux -----")

    choix = [("rock", "scissors"), ("paper", "rock"), ("scissors", "paper"), ("rock", "rock")]
    for a, b in choix:
        print(f"{a} vs {b} → {rps(a, b)}")

    print("\n----- Exo 10 : Décorateur retry -----")

    tentative = {'count': 0}

    @retry(max_attempts=5, exceptions=(ValueError,), delay=0)
    def fonction_instable():
        tentative['count'] += 1
        if random.random() < 0.7:
            print(f"Tentative {tentative['count']} échouée ❌")
            raise ValueError("Erreur aléatoire")
        print(f"Tentative {tentative['count']} réussie ✅")
        return "succès"

    try:
        resultat = fonction_instable()
        print("Résultat :", resultat)
    except ValueError:
        print("Échec après plusieurs tentatives ❌")

    print("\n----- Exo 11 : Classe Personne avec propriétés -----")

    p1 = Personne("Alice", 30)
    print("Nom :", p1.name, "| Âge :", p1.age)
    p1.age = 31
    print("Âge mis à jour :", p1.age)

    try:
        p1.age = -5
    except ValueError as e:
        print("Erreur attendue :", e)

    try:
        p1.name = ""
    except ValueError as e:
        print("Erreur attendue :", e)

    print("\n----- Exo 12 : Normalisation texte & Système de vote -----")

    texte = "Bonjour!!! Le PYTHON, c’est SUPER... :)"
    texte_normalise = normalize_text_quinettoieuntextepminuscules_suppressionponctuationq(texte)
    print("Texte normalisé :", texte_normalise)

    votes = VoteSystem()
    votes.add_candidate("Alice")
    votes.add_candidate("Bob")

    votes.vote("Alice")
    votes.vote("Bob")
    votes.vote("Alice")

    print("Résultats des votes :", votes.counts())
    print("Gagnant :", votes.winner())

    try:
        votes.vote("Charles")
    except ValueError as e:
        print("Erreur attendue :", e)

    print("\n----- unittests -----")
    unittest.main()