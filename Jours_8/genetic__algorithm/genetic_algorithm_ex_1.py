import random
import statistics
from collections import defaultdict

# Paramètres
NUM_COURSES = 30
NUM_ROOMS = 10
NUM_PROFS = 20
DAYS = 5
SLOTS_PER_DAY = 5

# Génération de données d'exemple
random.seed(0)

# Capacités des salles et indication si salle spéciale
capacite_salle = [random.randint(20, 120) for _ in range(NUM_ROOMS)]
salle_speciale = [random.random() < 0.2 for _ in range(NUM_ROOMS)]

# Pour chaque cours: nombre d'étudiants, besoin de salle spéciale, professeur assigné
etudiants_par_cours = [random.randint(10, 100) for _ in range(NUM_COURSES)]
besoin_salle_speciale = [random.random() < 0.15 for _ in range(NUM_COURSES)]
professeur_par_cours = [random.randrange(NUM_PROFS) for _ in range(NUM_COURSES)]

# Préférences simples: pour chaque prof, préférer certains jours (ensemble)
preferences_prof = {p: set(random.sample(range(DAYS), k=random.randint(1, 3))) for p in range(NUM_PROFS)}

# Représentation:
# Un chromosome est une liste de tuples (cours_id, salle_id, creneau_id, jour_id)
# L'ordre dans la liste est par `cours_id` (index i pour cours i)

def generer_emploi_aleatoire():
	chromosome = []
	for cours in range(NUM_COURSES):
		salle = random.randrange(NUM_ROOMS)
		creneau = random.randrange(SLOTS_PER_DAY)
		jour = random.randrange(DAYS)
		chromosome.append((cours, salle, creneau, jour))
	return chromosome

def detecter_conflits(chromosome):
	# conflits: même prof deux cours en même temps OR même salle deux cours même temps
	conflits = []
	occ_prof = defaultdict(list)  # (prof, jour, creneau) -> list cours
	occ_salle = defaultdict(list)
	for cours, salle, creneau, jour in chromosome:
		prof = professeur_par_cours[cours]
		keyp = (prof, jour, creneau)
		keys = (salle, jour, creneau)
		occ_prof[keyp].append(cours)
		occ_salle[keys].append(cours)

	for k, lst in occ_prof.items():
		if len(lst) > 1:
			conflits.append(('prof', k, lst))
	for k, lst in occ_salle.items():
		if len(lst) > 1:
			conflits.append(('salle', k, lst))
	return conflits

def emploi_du_prof(prof, chromosome):
	# retourne liste d'assignements (cours, jour, creneau)
	return [(cours, jour, creneau) for cours, salle, creneau, jour in chromosome if professeur_par_cours[cours] == prof]

def emploi_trop_charge(emploi):
	# simple: plus de 6 cours par semaine considéré trop chargé
	return len(emploi) > 6

def respecte_preferences(prof, emploi):
	# respecte si au moins la moitié des cours du prof sont sur jours préférés
	if not emploi:
		return True
	pref = preferences_prof.get(prof, set())
	if not pref:
		return True
	ok = sum(1 for _, jour, _ in emploi if jour in pref)
	return ok >= (len(emploi) / 2)

def repartition_equilibree(chromosome):
	# équilibre par jour: compte nombre de cours par jour et regarde écart-type
	counts = [0] * DAYS
	for _cours, _salle, _creneau, jour in chromosome:
		counts[jour] += 1
	return statistics.pstdev(counts) < 3.0

def fitness_emploi_du_temps(chromosome):
	score = 1000

	# 1. Conflits graves
	conflits = detecter_conflits(chromosome)
	score -= len(conflits) * 50

	# 2. Salles trop petites ou non-spéciales
	for cours, salle, creneau, jour in chromosome:
		if capacite_salle[salle] < etudiants_par_cours[cours]:
			score -= 30
		if besoin_salle_speciale[cours] and not salle_speciale[salle]:
			score -= 40

	# 3. Préférences et surcharge prof
	for prof in range(NUM_PROFS):
		emploi = emploi_du_prof(prof, chromosome)
		if emploi_trop_charge(emploi):
			score -= 20
		if respecte_preferences(prof, emploi):
			score += 10

	# 4. Répartition équilibrée
	if repartition_equilibree(chromosome):
		score += 50

	return max(0, score)

def crossover_emploi_du_temps(parent1, parent2):
	point = random.randint(1, len(parent1) - 1)
	enfant = parent1[:point] + parent2[point:]
	return enfant

def mutation_emploi_du_temps(chromosome, taux_mutation=0.1):
	chromosome = list(chromosome)
	for i in range(len(chromosome)):
		if random.random() < taux_mutation:
			cours, salle, creneau, jour = chromosome[i]
			if random.random() < 0.5:
				nouvelle_salle = random.randrange(NUM_ROOMS)
				chromosome[i] = (cours, nouvelle_salle, creneau, jour)
			else:
				nouveau_creneau = random.randrange(SLOTS_PER_DAY)
				nouveau_jour = random.randrange(DAYS)
				chromosome[i] = (cours, salle, nouveau_creneau, nouveau_jour)
	return chromosome

def selection_par_tournoi(population, scores, num_parents, tour_size=3):
	parents = []
	pop_idx = list(range(len(population)))
	for _ in range(num_parents):
		aspirants = random.sample(pop_idx, k=tour_size)
		best = max(aspirants, key=lambda i: scores[i])
		parents.append(population[best])
	return parents

def garder_meilleurs(new_population, old_population, old_scores, top_percent=0.05):
	n = max(1, int(len(new_population) * top_percent))
	# prendre les meilleurs de l'ancienne population
	best_indices = sorted(range(len(old_scores)), key=lambda i: old_scores[i], reverse=True)[:n]
	best_solutions = [old_population[i] for i in best_indices]
	# remplacer les pires de la nouvelle population
	new_scores = [fitness_emploi_du_temps(ind) for ind in new_population]
	worst_indices = sorted(range(len(new_scores)), key=lambda i: new_scores[i])[:n]
	for dest_idx, sol in zip(worst_indices, best_solutions):
		new_population[dest_idx] = sol

def pas_damelioration(derniers_scores, window=50):
	if len(derniers_scores) < window:
		return False
	return max(derniers_scores[-window:]) <= min(derniers_scores[-window:])

def algorithme_genetique_emploi_du_temps(pop_size=100, generations=500):
	population = [generer_emploi_aleatoire() for _ in range(pop_size)]
	meilleur_score = 0
	meilleure_solution = None
	derniers_scores = []

	for generation in range(generations):
		scores = [fitness_emploi_du_temps(ind) for ind in population]
		max_score = max(scores)
		derniers_scores.append(max_score)

		if max_score > meilleur_score:
			meilleur_score = max_score
			meilleure_solution = population[scores.index(max_score)]

		if generation > 50 and pas_damelioration(derniers_scores, window=50):
			break

		# Selection
		parents = selection_par_tournoi(population, scores, num_parents=pop_size, tour_size=3)

		# Reproduction
		enfants = []
		while len(enfants) < pop_size:
			parent1, parent2 = random.sample(parents, 2)
			enfant = crossover_emploi_du_temps(parent1, parent2)
			enfant = mutation_emploi_du_temps(enfant, taux_mutation=0.05)
			enfants.append(enfant)

		# Elitisme
		garder_meilleurs(enfants, population, scores, top_percent=0.05)
		population = enfants

	return meilleure_solution, meilleur_score

def afficher_solution(sol):
	if sol is None:
		print('Aucune solution trouvée')
		return
	print('Meilleure solution (cours, salle, creneau, jour):')
	for gene in sol:
		print(gene)

if __name__ == '__main__':
	sol, score = algorithme_genetique_emploi_du_temps(pop_size=100, generations=500)
	print('Score:', score)
	afficher_solution(sol)

