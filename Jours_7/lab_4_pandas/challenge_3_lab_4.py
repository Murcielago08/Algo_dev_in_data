import pandas as pd
import numpy as np
from numba import jit

def challenge_optimisation():
    # Dataset massif
    df = pd.DataFrame({
        'A': np.random.rand(1_000_000),
        'B': np.random.rand(1_000_000),
        'C': np.random.rand(1_000_000)
    })

    # 1. Vectorisation
    df['result_vec'] = df['A'] * df['B'] + df['C']

    # 2. Optimisation avec Numba
    @jit(nopython=True)
    def calcul_rapide(a, b, c):
        return a * b + c

    df['result_numba'] = calcul_rapide(df['A'].values, df['B'].values, df['C'].values)

    # 3. Optimisation mémoire
    def optimiser_memoire(df):
        for col in df.columns:
            if df[col].dtype == 'float64':
                df[col] = df[col].astype('float32')
        return df

    df_opt = optimiser_memoire(df.copy())

    # 4. Requêtes complexes
    query_result = df_opt.query("result_vec > 1 and result_numba < 1.5")

    print("\n--- Dataset optimisé ---\n", df_opt.head())
    print("\nRésultat query\n", query_result.head())

challenge_optimisation()