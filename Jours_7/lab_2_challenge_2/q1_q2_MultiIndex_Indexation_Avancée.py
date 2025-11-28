"""
Q1-Q2: Broadcasting Avancé
Q1: Structure Hiérarchique Complexe
Q2: Sélection Multi-Niveaux
"""

import pandas as pd
import numpy as np
import os
import time

# Load dataset with correct path
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'advanced_employees.csv')
df = pd.read_csv(csv_path)

# Inspect columns
print("Available columns:")
print(df.columns.tolist())
print()

# Extract year from hire_date
df['Année d\'embauche'] = pd.to_datetime(df['hire_date']).dt.year

# Create MultiIndex: region → main_department → grade → Année d'embauche
df_indexed = df.set_index(['region', 'main_department', 'grade', 'Année d\'embauche'])

# Q1: Calculate salary statistics at each level
print("=== Salary Statistics by MultiIndex Level ===\n")

# By region
print("By region:")
print(df_indexed.groupby(level='region')['base_salary'].agg(['mean', 'median', 'std', 'count']))
print()

# By region → main_department
print("By region → main_department:")
print(df_indexed.groupby(level=['region', 'main_department'])['base_salary'].agg(['mean', 'median', 'std', 'count']))
print()

# By region → main_department → grade
print("By region → main_department → grade:")
print(df_indexed.groupby(level=['region', 'main_department', 'grade'])['base_salary'].agg(['mean', 'median', 'std', 'count']))
print()

# By all levels
print("By all levels (region → main_department → grade → Année d'embauche):")
print(df_indexed.groupby(level=['region', 'main_department', 'grade', 'Année d\'embauche'])['base_salary'].agg(['mean', 'count']))
print()

# Q1: Extract Managers from Europe hired after 2020 using xs()
print("=== Managers in Europe Hired After 2020 ===\n")
try:
    managers_europe = df_indexed.xs(('Europe', slice(None), 'Manager', slice(2021, None)), 
                                     level=['region', 'main_department', 'grade', 'Année d\'embauche'])
    print(f"Found {len(managers_europe)} Managers")
    print(managers_europe[['base_salary', 'first_name']].head(10))
except KeyError:
    # Alternative approach if exact values don't match
    print("Filtering using alternative method:")
    managers_europe = df_indexed.xs('Europe', level='region').xs('Manager', level='grade')
    managers_europe = managers_europe[managers_europe.index.get_level_values('Année d\'embauche') > 2020]
    print(f"Found {len(managers_europe)} Managers")
    print(managers_europe[['base_salary', 'first_name']].head(10) if 'first_name' in managers_europe.columns else managers_europe.head(10))

print("\n" + "="*60)
print("Q2: Multi-Level Selection with IndexSlice")
print("="*60 + "\n")

# Start timing
start_time = time.time()

# Reset index to work with columns
df_work = df.reset_index(drop=True)

# Filter for departments and grades
dept_filter = df_work['main_department'].isin(['Technology', 'Finance'])
grade_filter = df_work['grade'].isin(['Senior', 'Lead'])
perf_filter = df_work['performance_score'] > 7.5

# Combine filters
result = df_work[dept_filter & grade_filter & perf_filter]

end_time = time.time()
elapsed_time = end_time - start_time

print(f"Employees in (Technology OR Finance) & (Senior OR Lead) & Performance > 7.5:")
print(f"Found {len(result)} employees")
print(f"Selection time: {elapsed_time:.4f} seconds\n")

print(result[['first_name', 'last_name', 'main_department', 'grade', 'base_salary', 'performance_score']].head(15))
print()

# Show breakdown by department and grade
print("Breakdown by Department and Grade:")
print(result.groupby(['main_department', 'grade']).size())
print()

# Show salary statistics for selected employees
print("Salary Statistics for Selected Employees:")
print(result.groupby(['main_department', 'grade'])['base_salary'].agg(['mean', 'min', 'max', 'count']))
