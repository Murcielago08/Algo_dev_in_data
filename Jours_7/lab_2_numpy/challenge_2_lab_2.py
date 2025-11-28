import numpy as np

# Définition du type structuré
dtype_etudiants = [
    ('nom', 'U20'),
    ('matiere', 'U20'),
    ('note', 'f8'),
    ('date_exam', 'datetime64[D]')
]

# Création d'un tableau de notes
notes = np.array([
    ('Alice', 'Maths', 45.0, np.datetime64('2025-11-01')),
    ('Bob', 'Maths', 75.0, np.datetime64('2025-11-01')),
    ('Charlie', 'Physique', 55.0, np.datetime64('2025-11-02')),
    ('Alice', 'Maths', 65.0, np.datetime64('2025-11-15')),
    ('Bob', 'Physique', 40.0, np.datetime64('2025-11-02')),
], dtype=dtype_etudiants)

# ➡️ Calculer la moyenne par matière
def moyenne_par_matiere(notes):
    matieres = np.unique(notes['matiere'])
    moyennes = {}
    for mat in matieres:
        moyennes[mat] = notes[notes['matiere'] == mat]['note'].mean()
    return moyennes

# ➡️ Trouver les étudiants en échec (< 50%)
def etudiants_en_echec(notes):
    return notes[notes['note'] < 50]

# ➡️ Identifier les améliorations entre deux examens
def ameliorations(notes, nom, matiere):
    exams = notes[(notes['nom'] == nom) & (notes['matiere'] == matiere)]
    exams_sorted = np.sort(exams, order='date_exam')
    if len(exams_sorted) >= 2:
        diff = exams_sorted[-1]['note'] - exams_sorted[0]['note']
        return diff
    return None

# Exemple d'utilisation
print("Moyennes par matière:", moyenne_par_matiere(notes))
print("\nÉtudiants en échec:\n", etudiants_en_echec(notes))
print("\nAmélioration d'Alice en Maths:", ameliorations(notes, 'Alice', 'Maths'))