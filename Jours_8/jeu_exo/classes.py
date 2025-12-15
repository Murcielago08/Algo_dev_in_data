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
        self.mutation_rate = 0.25
        self.mutation_strength = 0.4
        self.elitism_count = 2  # Nombre de meilleurs individus à conserver
        self.generation_stats = []
    
    def calculate_fitness(self, human):
        # Fitness plus sophistiquée
        
        return human.fitness
    
    def selection(self, humans):
        # Sélection par rang (pas par roulette)
        humans_sorted = sorted([h for h in humans if h.alive], 
                              key=lambda h: h.fitness, reverse=True)
        
        selected = []
        

        
        return selected
    
    def crossover(self, parent1, parent2):
        # Crossover à deux points

        
        return child
    
    def mutate(self, chromosome, generation):
        # Mutation adaptative : moins de mutation au fil des générations
        adaptive_rate = self.mutation_rate * (1.0 - min(generation / 50, 0.5))
        
        mutated = chromosome.copy()
        

        
        return mutated
    
    def create_new_generation(self, humans, generation):
        # Calculer le fitness pour chaque humain
       
        
        return new_population