"""
Q3: Agrégation Hiérarchique Dynamique
Pour chaque niveau hiérarchique, calculez automatiquement:
- Effectifs et turnover
- Écart-type des salaires
- Corrélation performance-salaire
"""

import pandas as pd
import numpy as np
import os

# Load dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'advanced_employees.csv')
df = pd.read_csv(csv_path)

# Extract year from hire_date
df['hire_year'] = pd.to_datetime(df['hire_date']).dt.year

# Calculate turnover risk (example: based on satisfaction and performance)
df['turnover_risk'] = ((10 - df['satisfaction_score']) + (10 - df['performance_score'])) / 20

print("=" * 80)
print("Q3: AGRÉGATION HIÉRARCHIQUE DYNAMIQUE")
print("=" * 80)
print()

# Define hierarchical levels
hierarchical_levels = [
    ['region'],
    ['region', 'main_department'],
    ['region', 'main_department', 'grade'],
    ['region', 'main_department', 'grade', 'hire_year']
]

def calculate_hierarchical_metrics(df, levels):
    """Calculate metrics for given hierarchical levels"""
    grouped = df.groupby(levels)
    
    # Calculate metrics
    metrics = grouped.agg({
        'employee_id': 'count',  # Effectifs
        'turnover_risk': 'mean',  # Turnover moyen
        'base_salary': ['std', 'mean'],  # Écart-type et moyenne des salaires
        'performance_score': 'mean'  # Performance moyenne
    })
    
    # Flatten column names
    metrics.columns = ['_'.join(col).strip('_') for col in metrics.columns.values]
    metrics.rename(columns={
        'employee_id_count': 'effectifs',
        'turnover_risk_mean': 'turnover_avg',
        'base_salary_std': 'salary_std',
        'base_salary_mean': 'salary_mean',
        'performance_score_mean': 'performance_avg'
    }, inplace=True)
    
    # Calculate correlation performance-salaire for each group
    correlations = []
    for name, group in grouped:
        if len(group) > 1:  # Need at least 2 points for correlation
            corr = np.corrcoef(group['performance_score'], group['base_salary'])[0, 1]
        else:
            corr = np.nan
        correlations.append(corr)
    
    metrics['perf_salary_corr'] = correlations
    
    return metrics

# Calculate and display metrics for each hierarchical level
for i, levels in enumerate(hierarchical_levels, 1):
    print(f"\n{'='*80}")
    print(f"Niveau {i}: {' → '.join(levels)}")
    print(f"{'='*80}")
    
    metrics = calculate_hierarchical_metrics(df, levels)
    
    print(f"\nNombre de groupes: {len(metrics)}")
    print(f"\nTop 10 groupes par effectifs:")
    print(metrics.nlargest(10, 'effectifs'))
    
    print(f"\nStatistiques globales pour ce niveau:")
    print(metrics.describe())
    
    # Show groups with highest turnover risk
    print(f"\nTop 5 groupes avec le plus haut risque de turnover:")
    print(metrics.nlargest(5, 'turnover_avg')[['effectifs', 'turnover_avg', 'salary_mean']])
    
    # Show groups with strongest correlation
    valid_corr = metrics.dropna(subset=['perf_salary_corr'])
    if len(valid_corr) > 0:
        print(f"\nTop 5 groupes avec la plus forte corrélation performance-salaire:")
        print(valid_corr.nlargest(5, 'perf_salary_corr')[['effectifs', 'perf_salary_corr', 'salary_std']])

print("\n" + "="*80)
print("FIN Q3")
print("="*80)
