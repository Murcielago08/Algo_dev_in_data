"""Challenge 4 : Segmentation clients avec arbre
Applique des règles simples pour segmenter les clients.
"""

def segment_rule(montant: float, frequence: int) -> str:
    """Retourne le segment ('A','B' ou 'C') selon les règles données.

    Règles:
    - Si montant > 100 ET fréquence > 2 -> 'A'
    - Sinon si montant > 100 OU fréquence > 2 -> 'B'
    - Sinon -> 'C'
    """
    if montant > 100 and frequence > 2:
        return "A"
    if montant > 100 or frequence > 2:
        return "B"
    return "C"


def classify_clients(clients):
    """Ajoute le segment calculé pour chaque client et retourne la liste mise à jour."""
    results = []
    for c in clients:
        montant = c.get("montant")
        frequence = c.get("frequence")
        seg = segment_rule(montant, frequence)
        out = dict(c)
        out["segment_calcule"] = seg
        results.append(out)
    return results


def distribution(klassed_clients):
    """Retourne la répartition en counts et pourcentages par segment."""
    counts = {"A": 0, "B": 0, "C": 0}
    for c in klassed_clients:
        seg = c.get("segment_calcule")
        if seg in counts:
            counts[seg] += 1
    total = sum(counts.values())
    pct = {k: (v, (v / total * 100) if total else 0) for k, v in counts.items()}
    return counts, pct


def main():
    # Données initiales (exemple)
    ventes = [
        {"client": "Alice", "montant": 150, "frequence": 3, "segment": "A"},
        {"client": "Bob", "montant": 80, "frequence": 5, "segment": "B"},
        {"client": "Charlie", "montant": 200, "frequence": 2, "segment": "A"},
        {"client": "Diana", "montant": 50, "frequence": 1, "segment": "C"},
        {"client": "Eve", "montant": 120, "frequence": 4, "segment": "B"},
    ]

    # Nouveaux clients à classer
    nouveaux = [
        {"client": "Client1", "montant": 90, "frequence": 4},
        {"client": "Client2", "montant": 110, "frequence": 1},
        {"client": "Client3", "montant": 60, "frequence": 2},
    ]

    klassed_new = classify_clients(nouveaux)

    print("Classification des nouveaux clients:")
    for c in klassed_new:
        print(f"- {c['client']}: montant={c['montant']}, frequence={c['frequence']} -> Segment {c['segment_calcule']}")

    counts_new, pct_new = distribution(klassed_new)
    print("\nRépartition (nouveaux clients):")
    for seg, (count, pct) in pct_new.items():
        print(f"- Segment {seg}: {count} client(s) ({pct:.1f}%)")

    # Optionnel: répartition globale (anciens + nouveaux) basée sur le calcul
    all_clients = [
        dict(c) for c in ventes
    ]
    # recalculer segments pour anciens selon la même règle
    for c in all_clients:
        c["segment_calcule"] = segment_rule(c["montant"], c["frequence"])
    all_clients.extend(klassed_new)
    counts_all, pct_all = distribution(all_clients)
    print("\nRépartition (tous les clients, calculée):")
    for seg, (count, pct) in pct_all.items():
        print(f"- Segment {seg}: {count} client(s) ({pct:.1f}%)")


if __name__ == "__main__":
    main()
