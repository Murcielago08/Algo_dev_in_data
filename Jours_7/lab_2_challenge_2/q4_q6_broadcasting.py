"""
Q4-Q6: Broadcasting Avancé
Q4: Matrice de Similarités 100k×100k
Q5: Normalisation Multi-Dimensionnelle avec weights
Q6: Benchmarks Departmentaux
"""

import pandas as pd
import numpy as np
import os
import time

# Load dataset
script_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(script_dir, 'advanced_employees.csv')
df = pd.read_csv(csv_path)

print("=" * 80)
print("Q4: MATRICE DE SIMILARITÉS")
print("=" * 80)
print()

# For demonstration, we'll use a subset for the similarity matrix
# (100k x 100k would be ~80GB in memory)
# Use first 1000 employees for demo
n_sample = min(1000, len(df))
sample_df = df.head(n_sample)

# Extract features for similarity calculation
features = sample_df[['base_salary', 'performance_score', 'satisfaction_score']].values

# Normalize features
features_normalized = (features - features.mean(axis=0)) / features.std(axis=0)

print(f"Calculating similarity matrix for {n_sample} employees...")
start_time = time.time()

# Method 1: Using broadcasting (memory intensive but fast)
# Calculate Euclidean distances using broadcasting
# Distance formula: sqrt(sum((A - B)^2))
def calculate_similarity_broadcast(data):
    """Calculate pairwise Euclidean distances using broadcasting"""
    # Reshape for broadcasting: (n, 1, features) - (1, n, features)
    diff = data[:, np.newaxis, :] - data[np.newaxis, :, :]
    distances = np.sqrt(np.sum(diff ** 2, axis=2))
    # Convert to similarity (inverse distance)
    similarities = 1 / (1 + distances)
    return similarities

similarity_matrix = calculate_similarity_broadcast(features_normalized)
broadcast_time = time.time() - start_time

print(f"Similarity matrix shape: {similarity_matrix.shape}")
print(f"Calculation time (broadcasting): {broadcast_time:.4f} seconds")
print(f"Memory usage: {similarity_matrix.nbytes / 1024**2:.2f} MB")
print()

# Method 2: Chunked calculation for larger datasets
print("Method 2: Chunked calculation (optimized for memory)...")
start_time = time.time()

chunk_size = 200
n = len(features_normalized)
similarity_matrix_chunked = np.zeros((n, n), dtype=np.float32)

for i in range(0, n, chunk_size):
    end_i = min(i + chunk_size, n)
    chunk_i = features_normalized[i:end_i]
    
    for j in range(0, n, chunk_size):
        end_j = min(j + chunk_size, n)
        chunk_j = features_normalized[j:end_j]
        
        # Calculate distances for this chunk
        diff = chunk_i[:, np.newaxis, :] - chunk_j[np.newaxis, :, :]
        distances = np.sqrt(np.sum(diff ** 2, axis=2))
        similarity_matrix_chunked[i:end_i, j:end_j] = 1 / (1 + distances)

chunked_time = time.time() - start_time
print(f"Calculation time (chunked): {chunked_time:.4f} seconds")
print(f"Memory usage: {similarity_matrix_chunked.nbytes / 1024**2:.2f} MB")
print()

# Show most similar pairs
print("Top 10 most similar employee pairs (excluding self):")
np.fill_diagonal(similarity_matrix, 0)  # Exclude self-similarity
for _ in range(10):
    i, j = np.unravel_index(np.argmax(similarity_matrix), similarity_matrix.shape)
    print(f"Employee {i} ↔ Employee {j}: Similarity = {similarity_matrix[i, j]:.4f}")
    similarity_matrix[i, j] = 0  # Remove to find next

print("\n" + "=" * 80)
print("Q5: NORMALISATION MULTI-DIMENSIONNELLE")
print("=" * 80)
print()

# Extract features
salaries = df['base_salary'].values
performance = df['performance_score'].values
satisfaction = df['satisfaction_score'].values

# Z-score normalization using broadcasting
def z_normalize(data):
    """Z-score normalization"""
    return (data - np.mean(data)) / np.std(data)

z_salary = z_normalize(salaries)
z_performance = z_normalize(performance)
z_satisfaction = z_normalize(satisfaction)

# Calculate weighted score using broadcasting
weights = np.array([0.5, 0.3, 0.2])  # Salaire, Performance, Satisfaction
z_scores = np.column_stack([z_salary, z_performance, z_satisfaction])

# Broadcasting: multiply each column by its weight
weighted_score = np.sum(z_scores * weights, axis=1)

# Add to dataframe
df['weighted_score'] = weighted_score

print("Score Formula: 0.5 × Z_salaire + 0.3 × Z_performance + 0.2 × Z_satisfaction")
print()
print("Top 20 employés par score pondéré:")
top_employees = df.nlargest(20, 'weighted_score')[
    ['first_name', 'last_name', 'main_department', 'base_salary', 
     'performance_score', 'satisfaction_score', 'weighted_score']
]
print(top_employees)
print()

print("Statistiques des scores:")
print(f"Moyenne: {weighted_score.mean():.4f}")
print(f"Écart-type: {weighted_score.std():.4f}")
print(f"Min: {weighted_score.min():.4f}")
print(f"Max: {weighted_score.max():.4f}")

print("\n" + "=" * 80)
print("Q6: BENCHMARKS DEPARTMENTAUX")
print("=" * 80)
print()

# Calculate departmental benchmarks
dept_benchmarks = df.groupby('main_department').agg({
    'base_salary': 'mean',
    'performance_score': 'mean',
    'satisfaction_score': 'mean'
}).reset_index()

dept_benchmarks.columns = ['main_department', 'dept_salary_avg', 'dept_perf_avg', 'dept_sat_avg']

# Merge benchmarks back to main dataframe
df_with_benchmarks = df.merge(dept_benchmarks, on='main_department')

# Calculate deviations using broadcasting
# Convert to department-indexed arrays
dept_salary_avg = df_with_benchmarks['dept_salary_avg'].values
dept_perf_avg = df_with_benchmarks['dept_perf_avg'].values
dept_sat_avg = df_with_benchmarks['dept_sat_avg'].values

# Calculate percentage deviations
salary_deviation = ((salaries - dept_salary_avg) / dept_salary_avg) * 100
perf_deviation = ((performance - dept_perf_avg) / dept_perf_avg) * 100
sat_deviation = ((satisfaction - dept_sat_avg) / dept_sat_avg) * 100

df['salary_vs_dept'] = salary_deviation
df['perf_vs_dept'] = perf_deviation
df['sat_vs_dept'] = sat_deviation

# Identify over/under performers
# Over-performer: salary above dept avg AND performance above dept avg
df['is_overperformer'] = (salary_deviation > 0) & (perf_deviation > 10)
df['is_underperformer'] = (salary_deviation > 0) & (perf_deviation < -10)

print("Benchmarks départementaux:")
print(dept_benchmarks)
print()

print(f"Over-performers (salaire > dept avg ET performance > +10%): {df['is_overperformer'].sum()}")
print(f"Under-performers (salaire > dept avg ET performance < -10%): {df['is_underperformer'].sum()}")
print()

print("Top 10 Over-performers:")
overperformers = df[df['is_overperformer']].nlargest(10, 'perf_vs_dept')[
    ['first_name', 'last_name', 'main_department', 'base_salary', 
     'salary_vs_dept', 'performance_score', 'perf_vs_dept']
]
print(overperformers)
print()

print("Top 10 Under-performers:")
underperformers = df[df['is_underperformer']].nsmallest(10, 'perf_vs_dept')[
    ['first_name', 'last_name', 'main_department', 'base_salary', 
     'salary_vs_dept', 'performance_score', 'perf_vs_dept']
]
print(underperformers)

print("\n" + "="*80)
print("FIN Q4-Q6")
print("="*80)
