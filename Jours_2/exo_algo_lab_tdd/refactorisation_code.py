import re
from collections import defaultdict
from typing import List


def factoriser_variables_repetees(code: str) -> str:
    """
    Transforme des variables répétées du type solde1, solde2,... en liste.
    """
    lignes = code.splitlines()
    var_pattern = re.compile(r'(\w+?)(\d+)')
    nouvelles_lignes = []
    vars_detectees = defaultdict(list)

    # Détecter les variables répétées
    for ligne in lignes:
        for var, index in var_pattern.findall(ligne):
            vars_detectees[var].append((index, ligne))

    # Créer les lignes refactorisées
    for ligne in lignes:
        new_line = ligne
        for var, occurrences in vars_detectees.items():
            if len(occurrences) > 1:
                # Remplacer varX par var[X-1]
                new_line = re.sub(rf'{var}(\d+)', lambda m: f'{var}[{int(m.group(1)) - 1}]', new_line)
        nouvelles_lignes.append(new_line)

    # Ajouter l'initialisation des listes au début
    init_lignes = []
    for var, occurrences in vars_detectees.items():
        if len(occurrences) > 1:
            count = len(occurrences)
            init_lignes.append(f"{var} = [0]*{count}")

    return '\n'.join(init_lignes + nouvelles_lignes)


def factoriser_if_else(code: str) -> str:
    """
    Transforme les if/else identiques en fonction.
    Limité aux patterns simples : if var <cond> val1 else val2
    """
    lignes = code.splitlines()
    pattern = re.compile(r'if (\w+) ([<>]=?) (\d+):\s+(\w+)\s*=\s*(\d+)\s+else:\s+\4\s*=\s*(\d+)')
    nouvelle_lignes = []
    fonction_creee = False

    for ligne in lignes:
        match = pattern.match(ligne.strip())
        if match and not fonction_creee:
            # Créer la fonction refactorisée
            var, cond, val_cond, var2, val1, val2 = match.groups()
            func = f"""def check_{var}({var}):
    if {var} {cond} {val_cond}:
        return {val1}
    else:
        return {val2}

"""
            nouvelle_lignes.append(func)
            fonction_creee = True
        # Remplacer le bloc original par l'appel fonction
        if match:
            nouvelle_lignes.append(f"{var} = check_{var}({var})")
        else:
            nouvelle_lignes.append(ligne)

    return '\n'.join(nouvelle_lignes)


def detect_doublons_et_refactoriser(code: str) -> str:
    """
    Applique automatiquement :
    1. Factorisation des variables répétées
    2. Factorisation des if/else répétitifs
    Retourne le nouveau code sous forme de str.
    """
    code = factoriser_variables_repetees(code)
    code = factoriser_if_else(code)
    return code


# --- Exemple d'utilisation ---
if __name__ == "__main__":
    code_exemple = """
solde1 = 0
solde2 = 0

if solde1 < 10:
    solde1 = 100
else:
    solde1 = 50

if solde2 < 10:
    solde2 = 100
else:
    solde2 = 50
"""

    code_refactore = detect_doublons_et_refactoriser(code_exemple)
    print(code_refactore)
