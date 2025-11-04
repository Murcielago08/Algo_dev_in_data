from functools import reduce

def composer (* fonctions ):
    """ Compose ␣ plusieurs ␣ fonctions ␣de␣ droite ␣ ␣ gauche """
    return reduce ( lambda f , g: lambda x : f (g (x) ) , fonctions )

# Fonctions de base
def ajouter_1 (x ): return x + 1
def ajouter_3 (x ): return x + 3
def multiplier_2 (x ): return x * 2
def carre ( x): return x ** 2

# Composition
transformation = composer (ajouter_3 , carre , multiplier_2 , ajouter_1 )
resultat = transformation (3) # ((3+1) *2) ^2 = 64

print (f" Transformation ␣de␣3:␣{ resultat }")

# Alternative avec pipe
def pipe (* fonctions ) :
    """ Pipe ␣ plusieurs ␣ fonctions ␣de␣ gauche ␣ ␣ droite """
    return reduce ( lambda f , g: lambda x : g (f (x) ) , fonctions )

transformation_pipe = pipe ( ajouter_1 , multiplier_2 , carre )
resultat_pipe = transformation_pipe (3) # ((3+1) *2) ^2 = 64
print (f" Transformation ␣ pipe ␣de␣3:␣{ resultat_pipe }")