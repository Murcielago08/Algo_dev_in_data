from collections import defaultdict

clients = [
    {"id": 1, "age": 25, "ville": "Paris", "departement": "75"},
    {"id": 2, "age": 35, "ville": "Lyon", "departement": "69"},
    {"id": 3, "age": 28, "ville": "Paris", "departement": "75"},
    {"id": 4, "age": 42, "ville": "Marseille", "departement": "13"},
    {"id": 5, "age": 31, "ville": "Lyon", "departement": "69"}
]

AGE_GROUPS = ["<30", "30-40", ">40"]


def age_group(age):
    if age < 30:
        return "<30"
    if 30 <= age <= 40:
        return "30-40"
    return ">40"


def build_tree(clients_list):
    # tree[departement][ville][age_group] -> list of clients
    tree = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    for c in clients_list:
        dep = c["departement"]
        city = c["ville"]
        ag = age_group(c["age"])
        tree[dep][city][ag].append(c)
    return tree


def counts(tree):
    # Count by department
    count_by_dep = {dep: sum(len(cl) for city in tree[dep].values() for cl in city.values()) for dep in tree}
    # Count by (dep, city)
    count_by_city = {(dep, city): sum(len(cl) for cl in tree[dep][city].values()) for dep in tree for city in tree[dep]}
    # Count by age group (global)
    count_by_age = {ag: sum(len(tree[dep][city].get(ag, [])) for dep in tree for city in tree[dep]) for ag in AGE_GROUPS}
    return count_by_dep, count_by_city, count_by_age


def print_tree(tree):
    print("France")
    for dep in sorted(tree.keys()):
        print(f"{dep} ")
        for city in sorted(tree[dep].keys()):
            print(f"  {dep} ({city})")
            for ag in AGE_GROUPS:
                clients_in_group = tree[dep][city].get(ag, [])
                if clients_in_group:
                    print(f"    {ag} ans")
                    line = ", ".join(f"Client {c['id']}" for c in clients_in_group)
                    print(f"      {line}")


def main():
    tree = build_tree(clients)
    print_tree(tree)
    c_dep, c_city, c_age = counts(tree)

    print("\nComptages:")
    print("- Par département:")
    for dep, cnt in sorted(c_dep.items()):
        print(f"  {dep}: {cnt}")
    print("- Par ville (département, ville):")
    for (dep, city), cnt in sorted(c_city.items()):
        print(f"  {dep} {city}: {cnt}")
    print("- Par groupe d'âge (global):")
    for ag, cnt in c_age.items():
        print(f"  {ag}: {cnt}")


if __name__ == '__main__':
    main()
