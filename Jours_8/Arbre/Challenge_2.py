data = [
    {"age": 25, "ville": "Paris", "achat": "oui"},
    {"age": 35, "ville": "Lyon", "achat": "oui"},
    {"age": 45, "ville": "Paris", "achat": "non"},
    {"age": 28, "ville": "Marseille", "achat": "non"},
    {"age": 31, "ville": "Lyon", "achat": "oui"},
    {"age": 40, "ville": "Paris", "achat": "non"}
]


def predict(client: dict) -> str:
    """Prédit 'oui' ou 'non' selon les règles :
    - Si ville == 'Lyon' -> 'oui'
    - Sinon si age < 30 -> 'oui'
    - Sinon -> 'non'
    """
    ville = client.get("ville", "")
    age = client.get("age", 0)

    if ville == "Lyon":
        return "oui"
    if age < 30:
        return "oui"
    return "non"


def accuracy(dataset: list) -> float:
    correct = sum(1 for d in dataset if predict(d) == d.get("achat"))
    return correct / len(dataset) if dataset else 0.0


if __name__ == "__main__":
    # Tests demandés
    tests = [
        {"age": 27, "ville": "Paris"},
        {"age": 38, "ville": "Marseille"}
    ]

    print("Predictions tests :")
    for c in tests:
        print(f"Client age={c['age']}, ville={c['ville']} -> prédiction: {predict(c)}")

    acc = accuracy(data)
    print(f"\nAccuracy sur les données d'entraînement: {acc*100:.2f}% ({int(acc*len(data))}/{len(data)})")
