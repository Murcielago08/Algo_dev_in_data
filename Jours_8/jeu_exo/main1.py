import pygame
import random
import math
import numpy as np
from enum import Enum

# Initialisation de Pygame
pygame.init()

# Constantes du jeu
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Couleurs
BACKGROUND = (15, 15, 35)
HUMAN_COLOR = (70, 170, 255)
ZOMBIE_COLOR = (50, 220, 50)
BULLET_COLOR = (255, 220, 80)
AMMO_COLOR = (255, 80, 80)
TEXT_COLOR = (230, 230, 230)
UI_BG = (25, 25, 55, 220)
EVOLUTION_BG = (40, 40, 80, 240)
GRID_COLOR = (100, 100, 150, 50)

# Classes
class EntityType(Enum):
    HUMAN = 1
    ZOMBIE = 2

class Human:
    def __init__(self, x, y, chromosome=None, generation=1):
        self.x = x
        self.y = y
        self.radius = 10
        self.health = 100
        self.ammo = 20
        self.reload_time = 0
        self.speed = 2.0
        self.vision = 100
        self.accuracy = 0.7
        self.ammo_capacity = 30
        self.alive = True
        self.fitness = 0
        self.kills = 0
        self.damage_dealt = 0
        self.time_alive = 0
        self.generation = generation
        self.id = random.randint(1000, 9999)
        
        # Chromosome: [vitesse, vision, précision, capacité munitions, agressivité]
        if chromosome:
            self.chromosome = chromosome
        else:
            self.chromosome = [
                random.uniform(0.5, 2.5),    # vitesse (0.5-2.5)
                random.uniform(60, 180),     # vision (60-180)
                random.uniform(0.4, 0.9),    # précision (0.4-0.9)
                random.uniform(20, 40),      # capacité munitions (20-40)
                random.uniform(0.2, 0.8)     # agressivité (0.2-0.8)
            ]
        
        self.apply_chromosome()
    
    def apply_chromosome(self):
        self.speed = self.chromosome[0]
        self.vision = self.chromosome[1]
        self.accuracy = self.chromosome[2]
        self.ammo_capacity = int(self.chromosome[3])
        self.aggressiveness = self.chromosome[4]  # 0 = fuyard, 1 = agressif
    
    def move(self, dx, dy, walls):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Collision avec les murs
        for wall in walls:
            if self.collides_with_wall(new_x, new_y, wall):
                # Essayer de se déplacer seulement sur X
                if not self.collides_with_wall(self.x + dx * self.speed, self.y, wall):
                    new_y = self.y
                # Essayer de se déplacer seulement sur Y
                elif not self.collides_with_wall(self.x, self.y + dy * self.speed, wall):
                    new_x = self.x
                else:
                    return
        
        # Garder dans les limites de l'écran
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, new_x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, new_y))
    
    def collides_with_wall(self, x, y, wall):
        return (x + self.radius > wall[0] and x - self.radius < wall[0] + wall[2] and
                y + self.radius > wall[1] and y - self.radius < wall[1] + wall[3])
    
    def update(self, zombies, ammo_packs, walls):
        if not self.alive:
            return
        
        self.time_alive += 1
        
        # Rechargement
        if self.reload_time > 0:
            self.reload_time -= 1
        
        # Recherche de zombies dans le champ de vision
        zombies_in_range = []
        for zombie in zombies:
            if zombie.alive:
                dist = math.sqrt((self.x - zombie.x)**2 + (self.y - zombie.y)**2)
                if dist < self.vision:
                    zombies_in_range.append((zombie, dist))
        
        # Recherche de munitions
        nearest_ammo = None
        min_ammo_distance = float('inf')
        
        for ammo in ammo_packs:
            dist = math.sqrt((self.x - ammo.x)**2 + (self.y - ammo.y)**2)
            if dist < self.vision and dist < min_ammo_distance:
                min_ammo_distance = dist
                nearest_ammo = ammo
        
        # Comportement basé sur l'agressivité
        if zombies_in_range:
            zombies_in_range.sort(key=lambda x: x[1])
            nearest_zombie, distance = zombies_in_range[0]
            
            # Si trop proche -> fuir
            if distance < 40:
                dx = self.x - nearest_zombie.x
                dy = self.y - nearest_zombie.y
                dist = max(0.1, math.sqrt(dx**2 + dy**2))
                self.move(dx/dist, dy/dist, walls)
                
                # Tirer en fuyant si agressif
                if self.aggressiveness > 0.6 and self.ammo > 0 and self.reload_time == 0:
                    return self.shoot(nearest_zombie)
            
            # Distance moyenne -> stratégie
            elif distance < 100:
                # Les plus agressifs s'approchent, les autres maintiennent distance
                if self.aggressiveness > 0.5:
                    dx = nearest_zombie.x - self.x
                    dy = nearest_zombie.y - self.y
                    dist = max(0.1, math.sqrt(dx**2 + dy**2))
                    
                    if distance > 80:  # S'approcher
                        self.move(dx/dist * 0.7, dy/dist * 0.7, walls)
                    else:  # Garder distance
                        self.move(-dx/dist * 0.3, -dy/dist * 0.3, walls)
                    
                    # Tirer selon agressivité
                    if self.reload_time == 0 and random.random() < (self.accuracy * self.aggressiveness):
                        return self.shoot(nearest_zombie)
                else:
                    # Fuite prudente
                    dx = self.x - nearest_zombie.x
                    dy = self.y - nearest_zombie.y
                    dist = max(0.1, math.sqrt(dx**2 + dy**2))
                    self.move(dx/dist * 0.5, dy/dist * 0.5, walls)
            
            else:
                # Zombie loin -> se rapprocher si agressif
                if self.aggressiveness > 0.7:
                    dx = nearest_zombie.x - self.x
                    dy = nearest_zombie.y - self.y
                    dist = max(0.1, math.sqrt(dx**2 + dy**2))
                    self.move(dx/dist * 0.4, dy/dist * 0.4, walls)
        
        # Recherche de munitions si besoin
        elif nearest_ammo and self.ammo < self.ammo_capacity * 0.4:
            dx = nearest_ammo.x - self.x
            dy = nearest_ammo.y - self.y
            dist = max(0.1, math.sqrt(dx**2 + dy**2))
            self.move(dx/dist, dy/dist, walls)
        
        else:
            # Mouvement aléatoire avec tendance selon agressivité
            if random.random() < 0.3:
                if self.aggressiveness > 0.7:
                    # Les agressifs explorent plus
                    self.move(random.uniform(-1, 1), random.uniform(-1, 1), walls)
                else:
                    # Les prudents bougent moins
                    self.move(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), walls)
        
        # Ramasser des munitions
        for ammo in ammo_packs[:]:
            dist = math.sqrt((self.x - ammo.x)**2 + (self.y - ammo.y)**2)
            if dist < self.radius + ammo.radius:
                self.ammo = min(self.ammo_capacity, self.ammo + ammo.amount)
                ammo_packs.remove(ammo)
                break
        
        return None
    
    def shoot(self, target):
        if self.ammo <= 0 or self.reload_time > 0:
            return None
        
        self.ammo -= 1
        self.reload_time = max(8, 15 - int(self.aggressiveness * 10))  # Recharge plus vite si agressif
        
        # Calculer les dégâts avec la précision et l'agressivité
        base_damage = 20 + (self.aggressiveness * 10)  # Plus agressif = plus de dégâts
        if random.random() > self.accuracy:
            base_damage *= 0.6  # Coup moins précis
        
        self.damage_dealt += base_damage
        return Bullet(self.x, self.y, target.x, target.y, base_damage, self.accuracy)
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
        return not self.alive
    
    def draw(self, screen, show_vision=False):
        if not self.alive:
            return
        
        # Corps de l'humain
        color_intensity = min(255, 100 + int(self.aggressiveness * 155))
        pygame.draw.circle(screen, (70, color_intensity, 255), 
                          (int(self.x), int(self.y)), self.radius)
        
        # Indicateur d'agressivité (arc)
        if self.aggressiveness > 0.5:
            start_angle = math.pi * 0.75
            end_angle = start_angle + (math.pi * 0.5 * self.aggressiveness)
            pygame.draw.arc(screen, (255, 100, 100), 
                           (self.x - 15, self.y - 15, 30, 30),
                           start_angle, end_angle, 2)
        
        # Barre de vie
        health_width = 20
        health_height = 3
        health_x = self.x - health_width/2
        health_y = self.y - self.radius - 8
        
        pygame.draw.rect(screen, (255, 40, 40), 
                        (health_x, health_y, health_width, health_height))
        pygame.draw.rect(screen, (50, 255, 50), 
                        (health_x, health_y, health_width * (self.health/100), health_height))
        
        # Champ de vision (optionnel)
        if show_vision:
            vision_surface = pygame.Surface((self.vision*2, self.vision*2), pygame.SRCALPHA)
            pygame.draw.circle(vision_surface, (100, 100, 255, 30), 
                             (self.vision, self.vision), self.vision)
            screen.blit(vision_surface, (self.x - self.vision, self.y - self.vision))

class Zombie:
    def __init__(self, x, y, difficulty=1):
        self.x = x
        self.y = y
        self.radius = 12
        self.base_health = 80
        self.base_speed = 1.0
        self.difficulty = difficulty  # 1-5
        
        # Les zombies évoluent avec la difficulté
        self.health = self.base_health * (1 + (difficulty-1) * 0.3)
        self.speed = self.base_speed * (1 + (difficulty-1) * 0.2)
        self.damage = 5 + (difficulty-1) * 2
        self.attack_cooldown = 0
        self.alive = True
        self.type = random.choice(['normal', 'rusher', 'tank'])[:difficulty]
        
        if self.type == 'rusher':
            self.speed *= 1.5
            self.health *= 0.8
        elif self.type == 'tank':
            self.speed *= 0.8
            self.health *= 1.5
            self.damage *= 1.2
    
    def collides_with_wall(self, x, y, wall):
        return (x + self.radius > wall[0] and x - self.radius < wall[0] + wall[2] and
                y + self.radius > wall[1] and y - self.radius < wall[1] + wall[3])
    
    def move_towards_target(self, target_x, target_y, walls):
        # Calculer la direction vers la cible
        dx = target_x - self.x
        dy = target_y - self.y
        dist = max(0.1, math.sqrt(dx**2 + dy**2))
        
        # Normaliser la direction
        dir_x = dx / dist
        dir_y = dy / dist
        
        # Calculer le nouveau mouvement
        move_x = dir_x * self.speed
        move_y = dir_y * self.speed
        
        # Vérifier la collision avec chaque mur
        new_x = self.x + move_x
        new_y = self.y + move_y
        
        collision = False
        for wall in walls:
            if self.collides_with_wall(new_x, new_y, wall):
                collision = True
                
                # Essayer de contourner le mur
                # Vérifier si on peut se déplacer seulement en X
                if not self.collides_with_wall(self.x + move_x, self.y, wall):
                    new_y = self.y
                    collision = False
                # Vérifier si on peut se déplacer seulement en Y
                elif not self.collides_with_wall(self.x, self.y + move_y, wall):
                    new_x = self.x
                    collision = False
                else:
                    # Essayer une direction alternative
                    if random.random() < 0.5:
                        # Tourner à droite
                        temp_dir_x = -dir_y
                        temp_dir_y = dir_x
                    else:
                        # Tourner à gauche
                        temp_dir_x = dir_y
                        temp_dir_y = -dir_x
                    
                    new_x = self.x + temp_dir_x * self.speed * 0.5
                    new_y = self.y + temp_dir_y * self.speed * 0.5
                    
                    # Vérifier à nouveau la collision
                    for wall2 in walls:
                        if self.collides_with_wall(new_x, new_y, wall2):
                            # Rester sur place si toujours en collision
                            new_x = self.x
                            new_y = self.y
                            break
                
                break
        
        # Appliquer le mouvement
        self.x = new_x
        self.y = new_y
        
        # Garder dans les limites de l'écran
        self.x = max(self.radius, min(SCREEN_WIDTH - self.radius, self.x))
        self.y = max(self.radius, min(SCREEN_HEIGHT - self.radius, self.y))
        
        return not collision
    
    def update(self, humans, walls):
        if not self.alive:
            return None
        
        # Recherche de l'humain le plus proche
        nearest_human = None
        min_distance = float('inf')
        
        for human in humans:
            if human.alive:
                dist = math.sqrt((self.x - human.x)**2 + (self.y - human.y)**2)
                if dist < min_distance:
                    min_distance = dist
                    nearest_human = human
        
        if nearest_human:
            # Se déplacer vers l'humain avec gestion des collisions
            success = self.move_towards_target(nearest_human.x, nearest_human.y, walls)
            
            # Attaquer si proche
            if min_distance < self.radius + nearest_human.radius + 8 and self.attack_cooldown <= 0:
                self.attack_cooldown = 25 - (self.difficulty * 3)
                return nearest_human
        else:
            # Mouvement aléatoire si pas d'humain visible
            if random.random() < 0.1:
                rand_x = random.uniform(-1, 1)
                rand_y = random.uniform(-1, 1)
                norm = max(0.1, math.sqrt(rand_x**2 + rand_y**2))
                self.move_towards_target(self.x + rand_x * 50, self.y + rand_y * 50, walls)
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        return None
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def draw(self, screen):
        if not self.alive:
            return
        
        # Couleur selon le type
        if self.type == 'rusher':
            color = (80, 240, 80)  # Vert vif
        elif self.type == 'tank':
            color = (40, 180, 40)  # Vert foncé
        else:
            color = (60, 220, 60)  # Vert normal
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)
        
        # Yeux de zombie (rouge plus intense pour les difficiles)
        eye_red = 200 + self.difficulty * 10
        eye_offset = 3
        
        # Œil gauche
        pygame.draw.circle(screen, (eye_red, 50, 50), 
                          (int(self.x - eye_offset), int(self.y - eye_offset)), 3)
        # Œil droit
        pygame.draw.circle(screen, (eye_red, 50, 50), 
                          (int(self.x + eye_offset), int(self.y - eye_offset)), 3)
        
        # Barre de santé pour les zombies difficiles
        if self.difficulty > 2:
            health_ratio = self.health / (self.base_health * (1 + (self.difficulty-1) * 0.3))
            bar_width = 20
            bar_height = 3
            bar_x = self.x - bar_width/2
            bar_y = self.y + self.radius + 5
            
            pygame.draw.rect(screen, (255, 40, 40), 
                            (bar_x, bar_y, bar_width, bar_height))
            pygame.draw.rect(screen, (50, 255, 50), 
                            (bar_x, bar_y, bar_width * health_ratio, bar_height))

class Bullet:
    def __init__(self, x, y, target_x, target_y, damage, accuracy):
        self.x = x
        self.y = y
        self.radius = 3
        self.speed = 8 + (accuracy * 4)  # Plus précis = plus rapide
        self.damage = damage
        self.accuracy = accuracy
        self.alive = True
        
        # Calculer la direction avec un peu d'erreur selon la précision
        dx = target_x - x + random.uniform(-10 * (1-accuracy), 10 * (1-accuracy))
        dy = target_y - y + random.uniform(-10 * (1-accuracy), 10 * (1-accuracy))
        dist = max(0.1, math.sqrt(dx**2 + dy**2))
        self.vx = (dx/dist) * self.speed
        self.vy = (dy/dist) * self.speed
    
    def update(self, walls):
        self.x += self.vx
        self.y += self.vy
        
        # Vérifier les collisions avec les murs
        for wall in walls:
            if (self.x > wall[0] and self.x < wall[0] + wall[2] and
                self.y > wall[1] and self.y < wall[1] + wall[3]):
                self.alive = False
                return
        
        # Vérifier les bords de l'écran
        if (self.x < -50 or self.x > SCREEN_WIDTH + 50 or 
            self.y < -50 or self.y > SCREEN_HEIGHT + 50):
            self.alive = False
    
    def draw(self, screen):
        # Taille selon les dégâts
        radius = self.radius + int(self.damage / 30)
        pygame.draw.circle(screen, BULLET_COLOR, (int(self.x), int(self.y)), radius)
        
        # Effet de traînée
        for i in range(1, 4):
            alpha = 100 - i * 25
            if alpha > 0:
                trail_surface = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
                pygame.draw.circle(trail_surface, (255, 220, 80, alpha), 
                                  (radius, radius), radius - i)
                screen.blit(trail_surface, (int(self.x - radius - self.vx * i * 0.3), 
                                          int(self.y - radius - self.vy * i * 0.3)))

class AmmoPack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 8
        self.amount = random.randint(8, 20)
        self.blink_timer = random.randint(0, 60)
    
    def update(self):
        self.blink_timer = (self.blink_timer + 1) % 120
    
    def draw(self, screen):
        # Effet de clignotement
        alpha = 128 + int(math.sin(self.blink_timer * 0.1) * 100)
        color = (255, 80, 80, alpha)
        
        # Créer une surface avec alpha pour le cercle
        circle_surface = pygame.Surface((self.radius*2, self.radius*2), pygame.SRCALPHA)
        pygame.draw.circle(circle_surface, color, (self.radius, self.radius), self.radius)
        screen.blit(circle_surface, (int(self.x - self.radius), int(self.y - self.radius)))
        
        # Dessiner un "+" pour les munitions
        plus_size = 5
        blink_factor = 0.5 + math.sin(self.blink_timer * 0.2) * 0.5
        plus_width = max(1, int(2 * blink_factor))
        
        pygame.draw.line(screen, (255, 255, 255), 
                        (int(self.x - plus_size), int(self.y)), 
                        (int(self.x + plus_size), int(self.y)), plus_width)
        pygame.draw.line(screen, (255, 255, 255), 
                        (int(self.x), int(self.y - plus_size)), 
                        (int(self.x), int(self.y + plus_size)), plus_width)

class GeneticAlgorithm:
    def __init__(self, population_size=20):
        self.population_size = population_size
        self.mutation_rate = 0.4
        self.mutation_strength = 0.6
        self.elitism_count = 2
        self.generation_stats = []

    # ==========================
    # EXERCICE 1 – FITNESS
    # ==========================
    def calculate_fitness(self, human):
        """
        Fitness basé sur :
        - kills
        - temps de survie
        - dégâts infligés
        Normalisé entre 0 et 100
        """
        kills_score = human.kills * 20
        survival_score = min(human.time_alive / 60, 100)   # survie en secondes
        damage_score = human.damage_dealt * 0.1

        raw_fitness = kills_score + survival_score + damage_score

        # Normalisation
        fitness = min(100, raw_fitness)
        human.fitness = fitness
        return fitness

    # ==========================
    # EXERCICE 2 – SÉLECTION
    # ==========================
    def selection(self, humans):
        humans_sorted = sorted(
            [h for h in humans if h.alive],
            key=lambda h: h.fitness,
            reverse=True
        )

        selected = []

        # Elitisme : garder les meilleurs
        selected.extend(humans_sorted[:self.elitism_count])

        # Sélection par rang pour le reste
        ranks = list(range(1, len(humans_sorted) + 1))
        total_rank = sum(ranks)

        while len(selected) < self.population_size:
            pick = random.uniform(0, total_rank)
            current = 0
            for human, rank in zip(humans_sorted, ranks):
                current += rank
                if current >= pick:
                    selected.append(human)
                    break

        return selected

    # ==========================
    # EXERCICE 3 – CROSSOVER
    # ==========================
    def crossover(self, parent1, parent2):
        size = len(parent1.chromosome)

        p1, p2 = sorted(random.sample(range(size), 2))

        child = (
            parent1.chromosome[:p1] +
            parent2.chromosome[p1:p2] +
            parent1.chromosome[p2:]
        )

        return child

    # ==========================
    # EXERCICE 4 – MUTATION
    # ==========================
    def mutate(self, chromosome, generation):
        adaptive_rate = self.mutation_rate * (1.0 - min(generation / 50, 0.5))
        mutated = chromosome.copy()

        for i in range(len(mutated)):
            if random.random() < adaptive_rate:
                mutation = random.uniform(
                    -self.mutation_strength,
                    self.mutation_strength
                )
                mutated[i] += mutation

        # Contraintes des gènes
        mutated[0] = max(0.5, min(2.5, mutated[0]))   # vitesse
        mutated[1] = max(60, min(180, mutated[1]))    # vision
        mutated[2] = max(0.4, min(0.9, mutated[2]))   # précision
        mutated[3] = max(20, min(40, mutated[3]))     # munitions
        mutated[4] = max(0.2, min(0.8, mutated[4]))   # agressivité

        return mutated

    # ==========================
    # EXERCICE 5 – NOUVELLE GÉNÉRATION
    # ==========================
    def create_new_generation(self, humans, generation):
        # Calculer le fitness pour chaque humain
        fitness_values = []
        for human in humans:
            fitness_values.append(self.calculate_fitness(human))

        # Sauvegarde des statistiques de génération
        if fitness_values:
            self.generation_stats.append({
                "generation": generation,
                "max": max(fitness_values),
                "avg": sum(fitness_values) / len(fitness_values),
                "min": min(fitness_values)
            })

        # Sélection
        selected = self.selection(humans)

        new_population = []

        # Elitisme
        for elite in selected[:self.elitism_count]:
            new_population.append(elite.chromosome.copy())

        # Création des enfants
        while len(new_population) < self.population_size:
            parent1, parent2 = random.sample(selected, 2)
            child = self.crossover(parent1, parent2)
            child = self.mutate(child, generation)
            new_population.append(child)

        return new_population



class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Évolution des Survivants - Algorithme Génétique")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont('Arial', 22)
        self.big_font = pygame.font.SysFont('Arial', 40)
        self.small_font = pygame.font.SysFont('Arial', 18)
        
        # Zone de jeu limitée
        self.play_area = pygame.Rect(60, 60, SCREEN_WIDTH - 120, SCREEN_HEIGHT - 120)
        
        # Groupes d'entités
        self.humans = []
        self.zombies = []
        self.bullets = []
        self.ammo_packs = []
        self.walls = []
        
        # Algorithm génétique
        self.ga = GeneticAlgorithm(population_size=40)
        self.max_humans = 40
        self.generation = 1
        self.total_kills = 0
        self.best_fitness_history = []
        self.average_fitness_history = []
        
        # Statistiques
        self.game_time = 0
        self.max_humans = 20
        self.max_zombies = 50  # AUGMENTÉ de 25 à 50
        self.zombie_spawn_timer = 0
        self.ammo_spawn_timer = 0
        self.difficulty_level = 1
        self.zombies_killed_this_gen = 0
        self.wave_number = 2  # Nouveau : système de vagues
        self.zombies_to_spawn = 0  # Zombies restants à spawn dans la vague
        self.wave_in_progress = False
        self.wave_cooldown = 0
        
        # État du jeu
        self.paused = False
        self.show_stats = True
        self.show_vision = False
        self.auto_next_gen = False
        self.manual_generation_control = True
        
        # NOUVEAU : Options de difficulté
        self.difficulty_settings = {
            'easy': {'max_zombies': 30, 'spawn_rate': 120, 'wave_size': 10},
            'normal': {'max_zombies': 50, 'spawn_rate': 90, 'wave_size': 15},
            'hard': {'max_zombies': 80, 'spawn_rate': 60, 'wave_size': 20},
            'insane': {'max_zombies': 500, 'spawn_rate': 30, 'wave_size': 30}
        }
        self.current_difficulty = 'normal'  # 'easy', 'normal', 'hard', 'insane'
        
        # Interface
        self.next_gen_button = pygame.Rect(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 60, 200, 40)
        self.pause_button = pygame.Rect(SCREEN_WIDTH - 220, SCREEN_HEIGHT - 110, 200, 40)
        # NOUVEAU : Boutons de difficulté
        self.difficulty_buttons = {
            'easy': pygame.Rect(20, SCREEN_HEIGHT - 100, 100, 30),
            'normal': pygame.Rect(130, SCREEN_HEIGHT - 100, 100, 30),
            'hard': pygame.Rect(240, SCREEN_HEIGHT - 100, 100, 30),
            'insane': pygame.Rect(350, SCREEN_HEIGHT - 100, 100, 30)
        }
        
        # Appliquer les paramètres de difficulté
        self.apply_difficulty_settings()
        
        # Créer des murs
        self.create_walls()
        
        # Initialiser la population
        self.initialize_population()
        
        # Démarrer la première vague de zombies
        self.start_wave()
    
    def apply_difficulty_settings(self):
        """Applique les paramètres de la difficulté sélectionnée"""
        settings = self.difficulty_settings[self.current_difficulty]
        self.max_zombies = settings['max_zombies']
        self.zombie_spawn_rate = settings['spawn_rate']
        self.base_wave_size = settings['wave_size']
        
        # Ajuster la difficulté initiale des zombies
        self.difficulty_level = {
            'easy': 1.0,
            'normal': 1.5,
            'hard': 2.0,
            'insane': 3.0
        }[self.current_difficulty]
    
    def create_walls(self):
        # Environnement avec des murs qui forment un labyrinthe
        self.walls = [
            # Murs extérieurs épais
            (40, 40, SCREEN_WIDTH - 80, 20),
            (40, SCREEN_HEIGHT - 60, SCREEN_WIDTH - 80, 20),
            (40, 40, 20, SCREEN_HEIGHT - 80),
            (SCREEN_WIDTH - 60, 40, 20, SCREEN_HEIGHT - 80),
            
            # Structures intérieures (labyrinthe)
            (200, 100, 15, 300),
            (400, 150, 200, 15),
            (650, 100, 15, 250),
            (300, 300, 200, 15),
            (500, 350, 15, 150),
            (750, 250, 150, 15),
            (200, 450, 300, 15),
            (600, 450, 200, 15),
            (400, 500, 15, 150),
            (800, 500, 15, 150),
            
            # Blocs isolés
            (150, 200, 80, 80),
            (900, 150, 100, 100),
            (350, 600, 120, 80),
            (800, 350, 100, 80),
            
            # NOUVEAU : Moins de murs pour permettre plus de zombies
            (550, 600, 150, 15),
            (300, 100, 15, 80),
            (900, 400, 15, 150),
        ]
    
    def initialize_population(self):
        # Créer une population initiale d'humains
        spawn_points = self.get_valid_spawn_points(self.ga.population_size)
        
        for i in range(self.ga.population_size):
            if i < len(spawn_points):
                x, y = spawn_points[i]
            else:
                x = random.randint(100, SCREEN_WIDTH - 100)
                y = random.randint(100, SCREEN_HEIGHT - 100)
            
            human = Human(x, y, generation=self.generation)
            human.ammo_used = 0
            self.humans.append(human)
    
    def get_valid_spawn_points(self, count):
        points = []
        attempts = 0
        
        while len(points) < count and attempts < 1000:
            x = random.randint(self.play_area.left, self.play_area.right)
            y = random.randint(self.play_area.top, self.play_area.bottom)
            
            # Vérifier la collision avec les murs
            valid = True
            for wall in self.walls:
                if (x + 25 > wall[0] and x - 25 < wall[0] + wall[2] and
                    y + 25 > wall[1] and y - 25 < wall[1] + wall[3]):
                    valid = False
                    break
            
            if valid:
                # Vérifier la distance avec les autres points
                too_close = False
                for px, py in points:
                    if math.sqrt((x - px)**2 + (y - py)**2) < 60:
                        too_close = True
                        break
                
                if not too_close:
                    points.append((x, y))
            
            attempts += 1
        
        return points
    
    def get_valid_zombie_spawn_point(self):
        """Trouve un point de spawn valide pour un zombie (sur les bords)"""
        attempts = 0
        while attempts < 100:
            # Choisir un bord aléatoire
            side = random.randint(0, 3)
            
            if side == 0:  # Haut
                x = random.randint(self.play_area.left, self.play_area.right)
                y = self.play_area.top - 30
            elif side == 1:  # Droite
                x = self.play_area.right + 30
                y = random.randint(self.play_area.top, self.play_area.bottom)
            elif side == 2:  # Bas
                x = random.randint(self.play_area.left, self.play_area.right)
                y = self.play_area.bottom + 30
            else:  # Gauche
                x = self.play_area.left - 30
                y = random.randint(self.play_area.top, self.play_area.bottom)
            
            # Vérifier que le point n'est pas dans un mur
            valid = True
            for wall in self.walls:
                if (x + 15 > wall[0] and x - 15 < wall[0] + wall[2] and
                    y + 15 > wall[1] and y - 15 < wall[1] + wall[3]):
                    valid = False
                    break
            
            if valid:
                return x, y
            
            attempts += 1
        
        # Fallback: point aléatoire dans la zone de jeu
        return (random.randint(self.play_area.left, self.play_area.right),
                random.randint(self.play_area.top, self.play_area.bottom))
    
    def spawn_zombies(self, count):
        """Spawn un nombre spécifié de zombies"""
        for _ in range(count):
            x, y = self.get_valid_zombie_spawn_point()
            
            # Les zombies deviennent plus forts avec les générations et la vague
            base_difficulty = min(5, max(1, (self.generation // 5) + 1))
            wave_multiplier = 1 + (self.wave_number - 1) * 0.2
            difficulty_multiplier = {
                'easy': 0.8,
                'normal': 1.0,
                'hard': 1.3,
                'insane': 1.8
            }[self.current_difficulty]
            
            difficulty = int(base_difficulty * wave_multiplier * difficulty_multiplier)
            difficulty = max(1, min(8, difficulty))  # Limiter entre 1 et 8
            
            self.zombies.append(Zombie(x, y, difficulty))
    
    def start_wave(self):
        """Démarre une nouvelle vague de zombies"""
        self.wave_in_progress = True
        self.wave_cooldown = 0
        
        # Calculer la taille de la vague
        base_size = self.base_wave_size
        wave_growth = 5 * (self.wave_number - 1)
        gen_growth = self.generation // 2
        total_zombies = base_size + wave_growth + gen_growth
        
        # Limiter le nombre maximum
        total_zombies = min(total_zombies, self.max_zombies // 2)
        
        self.zombies_to_spawn = total_zombies
        print(f"🚀 Début de la vague {self.wave_number} : {total_zombies} zombies à spawner")
    
    def spawn_ammo(self, count=1):
        for _ in range(count):
            valid = False
            attempts = 0
            
            while not valid and attempts < 100:
                x = random.randint(self.play_area.left + 30, self.play_area.right - 30)
                y = random.randint(self.play_area.top + 30, self.play_area.bottom - 30)
                
                # Vérifier qu'il n'y a pas de mur
                valid = True
                for wall in self.walls:
                    if (x + 20 > wall[0] and x - 20 < wall[0] + wall[2] and
                        y + 20 > wall[1] and y - 20 < wall[1] + wall[3]):
                        valid = False
                        break
                
                if valid:
                    # Vérifier la distance avec les autres munitions
                    too_close = False
                    for ammo in self.ammo_packs:
                        if math.sqrt((x - ammo.x)**2 + (y - ammo.y)**2) < 40:
                            too_close = True
                            break
                    
                    if not too_close:
                        self.ammo_packs.append(AmmoPack(x, y))
                        break
                
                attempts += 1
    
    def update(self):
        if self.paused:
            return
        
        self.game_time += 1
        
        # Mettre à jour les munitions (effet visuel)
        for ammo in self.ammo_packs:
            ammo.update()
        
        # Mettre à jour les humains
        for human in self.humans:
            if human.alive:
                bullet = human.update(self.zombies, self.ammo_packs, self.walls)
                if bullet:
                    self.bullets.append(bullet)
                    if not hasattr(human, 'ammo_used'):
                        human.ammo_used = 0
                    human.ammo_used += 1
        
        # Mettre à jour les zombies
        for zombie in self.zombies:
            if zombie.alive:
                target = zombie.update(self.humans, self.walls)
                if target:
                    target.take_damage(zombie.damage)
        
        # Mettre à jour les balles
        for bullet in self.bullets[:]:
            bullet.update(self.walls)
            
            # Vérifier les collisions avec les zombies
            for zombie in self.zombies[:]:
                if (zombie.alive and 
                    math.sqrt((bullet.x - zombie.x)**2 + (bullet.y - zombie.y)**2) < 
                    bullet.radius + zombie.radius):
                    
                    if zombie.take_damage(bullet.damage):
                        self.zombies_killed_this_gen += 1
                        self.total_kills += 1
                        # Trouver l'humain le plus proche pour lui attribuer le kill
                        closest_human = None
                        min_dist = float('inf')
                        for human in self.humans:
                            if human.alive:
                                dist = math.sqrt((human.x - zombie.x)**2 + (human.y - zombie.y)**2)
                                if dist < min_dist and dist < 200:
                                    min_dist = dist
                                    closest_human = human
                        
                        if closest_human:
                            closest_human.kills += 1
                    
                    bullet.alive = False
                    break
            
            if not bullet.alive:
                self.bullets.remove(bullet)
        
        # Nettoyer les entités mortes
        self.humans = [h for h in self.humans if h.alive]
        self.zombies = [z for z in self.zombies if z.alive]
        
        # Gestion des vagues de zombies
        if self.wave_in_progress:
            if self.zombies_to_spawn > 0:
                # Spawn progressif des zombies de la vague
                self.zombie_spawn_timer -= 1
                if self.zombie_spawn_timer <= 0:
                    zombies_alive = len(self.zombies)
                    if zombies_alive < self.max_zombies:
                        # Spawn par groupes
                        spawn_group = min(3, self.zombies_to_spawn, self.max_zombies - zombies_alive)
                        if spawn_group > 0:
                            self.spawn_zombies(spawn_group)
                            self.zombies_to_spawn -= spawn_group
                            self.zombie_spawn_timer = max(10, self.zombie_spawn_rate // 2)
            else:
                # Vague terminée quand tous les zombies sont morts
                if len(self.zombies) == 0:
                    self.wave_in_progress = False
                    self.wave_cooldown = 180  # 3 secondes de répit
                    print(f"✅ Vague {self.wave_number} terminée!")
        
        # Cooldown entre les vagues
        elif self.wave_cooldown > 0:
            self.wave_cooldown -= 1
            if self.wave_cooldown <= 0:
                self.wave_number += 1
                self.start_wave()
        
        # Spawn de munitions périodique
        self.ammo_spawn_timer -= 1
        if self.ammo_spawn_timer <= 0 and len(self.ammo_packs) < 8:
            self.spawn_ammo(1)
            self.ammo_spawn_timer = 150
        
        # Vérifier si la génération est terminée (seulement en mode auto)
        if self.auto_next_gen and all(not human.alive for human in self.humans) and len(self.humans) > 0:
            self.next_generation()
    
    def next_generation(self):
        # Créer une nouvelle génération avec l'algorithme génétique
        new_chromosomes = self.ga.create_new_generation(self.humans, self.generation)
        
        fitness_values = [h.fitness for h in self.humans]

        if fitness_values:
            self.best_fitness_history.append(max(fitness_values))
            self.average_fitness_history.append(
                sum(fitness_values) / len(fitness_values)
            )

        # Réinitialiser le jeu
        self.humans = []
        self.bullets = []
        self.ammo_packs = []
        self.zombies = []
        self.zombie_spawn_timer = 0
        self.ammo_spawn_timer = 0
        self.zombies_killed_this_gen = 0
        self.wave_number = 1
        self.wave_in_progress = False
        self.wave_cooldown = 0
        
        # Créer la nouvelle population
        spawn_points = self.get_valid_spawn_points(len(new_chromosomes))
        
        for i, chromosome in enumerate(new_chromosomes):
            if i < len(spawn_points):
                x, y = spawn_points[i]
            else:
                x = random.randint(self.play_area.left + 30, self.play_area.right - 30)
                y = random.randint(self.play_area.top + 30, self.play_area.bottom - 30)
            
            human = Human(x, y, chromosome, self.generation + 1)
            human.ammo_used = 0
            self.humans.append(human)
        
        # Démarrer une nouvelle vague
        self.start_wave()
        
        # Incrémenter la génération
        self.generation += 1
        print(f"Génération {self.generation} créée!")
        
        last = self.ga.generation_stats[-1]
        print(
            f"G{last['generation']} | "
            f"Max: {last['max']:.1f} | "
            f"Avg: {last['avg']:.1f} | "
            f"Min: {last['min']:.1f}"
        )

    
    def draw_evolution_graph(self, surface, x, y, width, height):
        """Dessine un graphique de l'évolution de la fitness"""
        if len(self.best_fitness_history) < 2:
            return
        
        # Fond du graphique
        pygame.draw.rect(surface, (30, 30, 60), (x, y, width, height))
        pygame.draw.rect(surface, (50, 50, 90), (x, y, width, height), 2)
        
        # Grille
        grid_steps = 5
        for i in range(1, grid_steps):
            grid_y = y + height - (i * height / grid_steps)
            pygame.draw.line(surface, GRID_COLOR, (x, grid_y), (x + width, grid_y), 1)
        
        # Échelle
        max_fitness = max(self.best_fitness_history)
        scale_factor = height / (max_fitness * 1.1)
        
        # Courbe de la meilleure fitness
        points_best = []
        for i, fitness in enumerate(self.best_fitness_history):
            px = x + (i * width / max(1, len(self.best_fitness_history) - 1))
            py = y + height - (fitness * scale_factor)
            points_best.append((px, py))
        
        if len(points_best) > 1:
            pygame.draw.lines(surface, (255, 100, 100), False, points_best, 3)
        
        # Courbe de la fitness moyenne
        if len(self.average_fitness_history) > 1:
            points_avg = []
            for i, fitness in enumerate(self.average_fitness_history):
                px = x + (i * width / max(1, len(self.average_fitness_history) - 1))
                py = y + height - (fitness * scale_factor)
                points_avg.append((px, py))
            
            pygame.draw.lines(surface, (100, 200, 255), False, points_avg, 2)
        
        # Légende
        legend_y = y + 10
        pygame.draw.line(surface, (255, 100, 100), (x + 10, legend_y), (x + 30, legend_y), 3)
        text_best = self.small_font.render("Meilleure fitness", True, TEXT_COLOR)
        surface.blit(text_best, (x + 35, legend_y - 8))
        
        if len(self.average_fitness_history) > 1:
            pygame.draw.line(surface, (100, 200, 255), (x + 10, legend_y + 20), (x + 30, legend_y + 20), 2)
            text_avg = self.small_font.render("Fitness moyenne", True, TEXT_COLOR)
            surface.blit(text_avg, (x + 35, legend_y + 12))
        
        # Titre
        title = self.font.render("Évolution de la Fitness", True, (255, 255, 200))
        surface.blit(title, (x + width//2 - title.get_width()//2, y - 30))
    
    def draw_ui(self):
        # Fond semi-transparent pour l'UI
        ui_height = 200 if self.show_stats else 120
        ui_surface = pygame.Surface((SCREEN_WIDTH, ui_height), pygame.SRCALPHA)
        ui_surface.fill(UI_BG)
        self.screen.blit(ui_surface, (0, 0))
        
        # Statistiques principales
        humans_alive = len([h for h in self.humans if h.alive])
        zombies_alive = len(self.zombies)
        
        main_stats = [
            f"GÉNÉRATION: {self.generation}",
            f"VAGUE: {self.wave_number}",
            f"HUMAINS: {humans_alive}/{len(self.humans)}",
            f"ZOMBIES: {zombies_alive}/{self.max_zombies}",
            f"ZOMBIES TUÉS: {self.zombies_killed_this_gen}",
            f"DIFFICULTÉ: {self.current_difficulty.upper()}"
        ]
        
        for i, text in enumerate(main_stats):
            color = (255, 200, 100) if i == 0 else TEXT_COLOR
            text_surface = self.font.render(text, True, color)
            self.screen.blit(text_surface, (20, 20 + i * 28))
        
        # Informations sur la vague
        if self.wave_in_progress:
            wave_text = f"Zombies restants: {self.zombies_to_spawn}"
        elif self.wave_cooldown > 0:
            wave_text = f"Prochaine vague dans: {self.wave_cooldown//60}s"
        else:
            wave_text = "Préparation..."
        
        wave_surface = self.font.render(wave_text, True, (255, 150, 150))
        self.screen.blit(wave_surface, (SCREEN_WIDTH - 250, 20))
        
        # Bouton pour la génération suivante
        button_color = (80, 180, 80) if self.next_gen_button.collidepoint(pygame.mouse.get_pos()) else (60, 160, 60)
        pygame.draw.rect(self.screen, button_color, self.next_gen_button, border_radius=8)
        pygame.draw.rect(self.screen, (100, 220, 100), self.next_gen_button, 3, border_radius=8)
        
        next_gen_text = self.font.render("NOUVELLE GÉNÉRATION", True, (255, 255, 255))
        text_rect = next_gen_text.get_rect(center=self.next_gen_button.center)
        self.screen.blit(next_gen_text, text_rect)
        
        # Bouton pause
        pause_color = (180, 80, 80) if self.pause_button.collidepoint(pygame.mouse.get_pos()) else (160, 60, 60)
        pause_text = "REPRENDRE" if self.paused else "PAUSE"
        pygame.draw.rect(self.screen, pause_color, self.pause_button, border_radius=8)
        pygame.draw.rect(self.screen, (220, 100, 100), self.pause_button, 3, border_radius=8)
        
        pause_text_surf = self.font.render(pause_text, True, (255, 255, 255))
        pause_rect = pause_text_surf.get_rect(center=self.pause_button.center)
        self.screen.blit(pause_text_surf, pause_rect)
        
        # Boutons de difficulté
        for diff, rect in self.difficulty_buttons.items():
            # Couleur différente selon la difficulté sélectionnée
            if diff == self.current_difficulty:
                color = (100, 200, 100) if diff == 'easy' else \
                       (200, 200, 100) if diff == 'normal' else \
                       (200, 150, 50) if diff == 'hard' else \
                       (200, 50, 50)
            else:
                color = (60, 140, 60) if diff == 'easy' else \
                       (140, 140, 60) if diff == 'normal' else \
                       (140, 100, 30) if diff == 'hard' else \
                       (140, 30, 30)
            
            # Effet de survol
            if rect.collidepoint(pygame.mouse.get_pos()):
                color = tuple(min(255, c + 40) for c in color)
            
            pygame.draw.rect(self.screen, color, rect, border_radius=5)
            pygame.draw.rect(self.screen, (220, 220, 220), rect, 2, border_radius=5)
            
            diff_text = self.small_font.render(diff.upper(), True, (255, 255, 255))
            text_rect = diff_text.get_rect(center=rect.center)
            self.screen.blit(diff_text, text_rect)
        
        # Instructions
        instructions = [
            "CLIC sur le bouton pour nouvelle génération",
            "ESPACE: Mode auto-génération",
            "1-4: Changer difficulté (EASY, NORMAL, HARD, INSANE)",
            "V: Afficher champs de vision",
            "R: Réinitialiser simulation"
        ]
        
        for i, text in enumerate(instructions):
            text_surface = self.small_font.render(text, True, (200, 200, 200))
            self.screen.blit(text_surface, (SCREEN_WIDTH - 320, 50 + i * 22))
        
        # Statistiques détaillées (si affichées)
        if self.show_stats and humans_alive > 0:
            # Trouver le meilleur humain
            alive_humans = [h for h in self.humans if h.alive]
            if alive_humans:
                best_human = max(alive_humans, key=lambda h: h.fitness)
                
                # Section stats du meilleur humain
                stats_bg = pygame.Surface((350, 140), pygame.SRCALPHA)
                stats_bg.fill((40, 40, 80, 200))
                self.screen.blit(stats_bg, (SCREEN_WIDTH // 2 - 175, 30))
                
                best_title = self.font.render(f"MEILLEUR SURVIVANT (G{best_human.generation})", 
                                            True, (255, 220, 100))
                self.screen.blit(best_title, (SCREEN_WIDTH // 2 - best_title.get_width()//2, 35))
                
                best_stats = [
                    f"Vitesse: {best_human.speed:.2f}",
                    f"Vision: {best_human.vision:.0f}",
                    f"Précision: {best_human.accuracy:.2f}",
                    f"Agressivité: {best_human.aggressiveness:.2f}",
                    f"Kills: {best_human.kills}",
                    f"Fitness: {best_human.fitness:.1f}"
                ]
                
                for i, text in enumerate(best_stats[:3]):
                    text_surface = self.small_font.render(text, True, TEXT_COLOR)
                    self.screen.blit(text_surface, (SCREEN_WIDTH // 2 - 160, 70 + i * 22))
                
                for i, text in enumerate(best_stats[3:]):
                    text_surface = self.small_font.render(text, True, TEXT_COLOR)
                    self.screen.blit(text_surface, (SCREEN_WIDTH // 2, 70 + i * 22))
        
        # Graphique d'évolution
        if len(self.best_fitness_history) > 1:
            self.draw_evolution_graph(self.screen, SCREEN_WIDTH - 420, 
                                     SCREEN_HEIGHT - 250, 400, 200)
    
    def draw(self):
        # Fond avec effet de grille subtile
        self.screen.fill(BACKGROUND)
        
        # Grille de fond
        grid_size = 40
        for x in range(0, SCREEN_WIDTH, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT), 1)
        for y in range(0, SCREEN_HEIGHT, grid_size):
            pygame.draw.line(self.screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y), 1)
        
        # Dessiner les murs
        for wall in self.walls:
            pygame.draw.rect(self.screen, (90, 90, 120), wall)
            pygame.draw.rect(self.screen, (70, 70, 100), wall, 3)
        
        # Dessiner les munitions
        for ammo in self.ammo_packs:
            ammo.draw(self.screen)
        
        # Dessiner les balles
        for bullet in self.bullets:
            bullet.draw(self.screen)
        
        # Dessiner les zombies
        for zombie in self.zombies:
            zombie.draw(self.screen)
        
        # Dessiner les humains
        for human in self.humans:
            human.draw(self.screen, self.show_vision)
        
        # Dessiner l'UI
        self.draw_ui()
        
        # Afficher "Pause" si le jeu est en pause
        if self.paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            
            pause_text = self.big_font.render("PAUSE", True, (255, 80, 80))
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        
        # Afficher "Mode Auto" si activé
        if self.auto_next_gen:
            auto_text = self.font.render("MODE AUTO-GÉNÉRATION ACTIF", True, (255, 200, 100))
            self.screen.blit(auto_text, (SCREEN_WIDTH//2 - auto_text.get_width()//2, SCREEN_HEIGHT - 40))
        
        # NOUVEAU : Afficher le nombre de zombies en gros
        if len(self.zombies) > 20:
            zombie_count_text = self.big_font.render(f"ZOMBIES: {len(self.zombies)}", True, (255, 50, 50))
            self.screen.blit(zombie_count_text, (SCREEN_WIDTH//2 - zombie_count_text.get_width()//2, 50))
        
        pygame.display.flip()
    
    def handle_click(self, pos):
        # Gérer les clics sur les boutons
        if self.next_gen_button.collidepoint(pos):
            self.next_generation()
            return True
        
        if self.pause_button.collidepoint(pos):
            self.paused = not self.paused
            return True
        
        # Gérer les clics sur les boutons de difficulté
        for diff, rect in self.difficulty_buttons.items():
            if rect.collidepoint(pos):
                self.change_difficulty(diff)
                return True
        
        return False
    
    def change_difficulty(self, difficulty):
        """Change la difficulté du jeu"""
        if difficulty in self.difficulty_settings:
            self.current_difficulty = difficulty
            self.apply_difficulty_settings()
            print(f"Difficulté changée: {difficulty.upper()}")
            print(f"  - Zombies max: {self.max_zombies}")
            print(f"  - Taux de spawn: {self.zombie_spawn_rate}")
            print(f"  - Taille vague: {self.base_wave_size}")
    
    def run(self):
        running = True
        
        while running:
            mouse_pos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        self.handle_click(event.pos)
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = not self.paused
                    
                    elif event.key == pygame.K_r:
                        # Réinitialiser le jeu
                        self.__init__()
                    
                    elif event.key == pygame.K_v:
                        self.show_vision = not self.show_vision
                    
                    elif event.key == pygame.K_SPACE:
                        self.auto_next_gen = not self.auto_next_gen
                        print(f"Mode auto-génération: {'ACTIVÉ' if self.auto_next_gen else 'DÉSACTIVÉ'}")
                    
                    elif event.key == pygame.K_s:
                        self.show_stats = not self.show_stats
                    
                    # NOUVEAU : Touches pour changer la difficulté
                    elif event.key == pygame.K_1 or event.key == pygame.K_KP1:
                        self.change_difficulty('easy')
                    elif event.key == pygame.K_2 or event.key == pygame.K_KP2:
                        self.change_difficulty('normal')
                    elif event.key == pygame.K_3 or event.key == pygame.K_KP3:
                        self.change_difficulty('hard')
                    elif event.key == pygame.K_4 or event.key == pygame.K_KP4:
                        self.change_difficulty('insane')
                    
                    # NOUVEAU : Touches pour ajouter des zombies manuellement
                    elif event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                        self.spawn_zombies(10)
                        print(f"+10 zombies ajoutés! Total: {len(self.zombies)}")
                    elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                        self.spawn_zombies(5)
                        print(f"+5 zombies ajoutés! Total: {len(self.zombies)}")
                    
                    elif event.key == pygame.K_a:
                        # Ajouter un humain (debug)
                        x = random.randint(self.play_area.left + 30, self.play_area.right - 30)
                        y = random.randint(self.play_area.top + 30, self.play_area.bottom - 30)
                        human = Human(x, y, generation=self.generation)
                        human.ammo_used = 0
                        self.humans.append(human)
                    
                    elif event.key == pygame.K_z:
                        # Ajouter un zombie (debug)
                        self.spawn_zombies(2)
            
            # Mettre à jour la logique du jeu seulement si pas en pause
            if not self.paused:
                self.update()
            
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

# Lancer le jeu
if __name__ == "__main__":
    print("=" * 60)
    print("ÉVOLUTION DES SURVIVANTS - ALGORITHME GÉNÉTIQUE")
    print("=" * 60)
    print("\nCONTROLES:")
    print("- CLIC sur le bouton vert pour passer à la génération suivante")
    print("- ESPACE: Activer/désactiver le mode auto-génération")
    print("- 1-4: Changer la difficulté (EASY, NORMAL, HARD, INSANE)")
    print("- + : Ajouter 10 zombies")
    print("- - : Ajouter 5 zombies")
    print("- P: Pause/Reprise")
    print("- V: Afficher/cacher les champs de vision")
    print("- R: Réinitialiser la simulation")
    print("- S: Afficher/cacher les statistiques")
    print("\nLe jeu devient de plus en plus difficile à chaque génération!")
    print("=" * 60)
    
    game = Game()
    game.run()