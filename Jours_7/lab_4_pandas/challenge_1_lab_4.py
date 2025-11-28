import pandas as pd
import numpy as np

def challenge_finance():
    # Création d’un MultiIndex : Entreprise, Année, Trimestre
    entreprises = ['A', 'B', 'C']
    annees = ['2023', '2024']
    trimestres = ['Q1', 'Q2', 'Q3', 'Q4']
    index = pd.MultiIndex.from_product([entreprises, annees, trimestres],
                                       names=['Entreprise', 'Année', 'Trimestre'])

    # Données simulées
    df = pd.DataFrame({
        'CA': np.random.randint(1000, 5000, len(index)),
        'Benefice': np.random.randint(100, 1000, len(index)),
        'Depenses': np.random.randint(500, 2000, len(index))
    }, index=index)

    # 1. Croissance trimestrielle par entreprise
    croissance = df.groupby(['Entreprise', 'Année'])['CA'].pct_change() * 100

    # 2. Marges par année
    marges = df.groupby(['Entreprise', 'Année']).apply(
        lambda x: (x['Benefice'].sum() / x['CA'].sum()) * 100
    )

    # 3. Performance relative entre entreprises
    perf_relative = df.groupby('Entreprise')['Benefice'].sum().rank(ascending=False)

    print("\n--- Données ---\n", df.head())
    print("\nCroissance trimestrielle (%)\n", croissance)
    print("\nMarges par année (%)\n", marges)
    print("\nPerformance relative (rang)\n", perf_relative)

challenge_finance()