"""
Q7-Q9: Einstein Summation
Q7: Contraction de Tensors (département × grade × compétence)
Q8: Projections Multi-Dimensionnelles
Q9: Calculs de Covariance avec einsum
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
print("Q7: CONTRACTION DE TENSORS")
print("=" * 80)
print()

# Create a tensor: département × grade × compétence
# We'll create synthetic skill dimensions
np.random.seed(42)

# Get unique departments and grades
departments = df['main_department'].unique()
grades = df['grade'].unique()
n_skills = 5  # Number of skill dimensions

print(f"Dimensions du tensor:")
print(f"  - Départements: {len(departments)}")
print(f"  - Grades: {len(grades)}")
print(f"  - Compétences: {n_skills}")
print()

# Create tensor: average skill levels per département × grade
tensor_shape = (len(departments), len(grades), n_skills)
dept_grade_skills = np.zeros(tensor_shape)

# Generate realistic skill data based on department and grade
dept_mapping = {dept: i for i, dept in enumerate(departments)}
grade_mapping = {grade: i for i, grade in enumerate(grades)}

# Assign skills based on department and grade
for dept_idx, dept in enumerate(departments):
    for grade_idx, grade in enumerate(grades):
        # Create department-specific skill profile
        base_skills = np.random.rand(n_skills) * 5 + 5  # Range [5, 10]
        
        # Adjust based on grade seniority
        grade_multiplier = 1.0 + (grade_idx * 0.1)
        dept_grade_skills[dept_idx, grade_idx, :] = base_skills * grade_multiplier

print("Tensor shape:", dept_grade_skills.shape)
print("Sample tensor values (first department, all grades):")
print(dept_grade_skills[0, :, :])
print()

# Use einsum to calculate department similarities
# Similarity based on flattened skill profiles across grades
print("Calculating département similarities using einsum...")
start_time = time.time()

# Method 1: Flatten grade×skill dimensions and compute dot products
# Reshape to (dept, grade*skill)
dept_profiles = dept_grade_skills.reshape(len(departments), -1)

# Use einsum for dot product: similarity_ij = sum_k (profile_ik * profile_jk)
dept_similarity = np.einsum('ik,jk->ij', dept_profiles, dept_profiles)

# Normalize by magnitude to get cosine similarity
dept_magnitudes = np.sqrt(np.einsum('ik,ik->i', dept_profiles, dept_profiles))
dept_similarity = dept_similarity / np.outer(dept_magnitudes, dept_magnitudes)

einsum_time = time.time() - start_time
print(f"Calculation time: {einsum_time:.4f} seconds")
print()

print("Matrice de similarité entre départements:")
similarity_df = pd.DataFrame(dept_similarity, 
                             index=departments, 
                             columns=departments)
print(similarity_df)
print()

# Find most similar department pairs
print("Paires de départements les plus similaires:")
similarity_pairs = []
for i in range(len(departments)):
    for j in range(i + 1, len(departments)):
        similarity_pairs.append((departments[i], departments[j], dept_similarity[i, j]))

similarity_pairs.sort(key=lambda x: x[2], reverse=True)
for dept1, dept2, sim in similarity_pairs[:5]:
    print(f"{dept1:20s} ↔ {dept2:20s}: {sim:.4f}")

print("\n" + "=" * 80)
print("Q8: PROJECTIONS MULTI-DIMENSIONNELLES")
print("=" * 80)
print()

# Extract employee features
features = df[['base_salary', 'performance_score', 'satisfaction_score', 
               'tenure_years']].values

# Normalize features
features_norm = (features - features.mean(axis=0)) / features.std(axis=0)

n_samples, n_features = features_norm.shape
n_components = 2  # Project to 2D

# Create random projection matrix
np.random.seed(42)
projection_matrix = np.random.randn(n_features, n_components)

# Orthogonalize using QR decomposition for better projection
projection_matrix, _ = np.linalg.qr(projection_matrix)

print(f"Original dimensions: {n_features}")
print(f"Projected dimensions: {n_components}")
print()

print("Projection matrix:")
print(projection_matrix)
print()

# Use einsum for projection: Projected = Data × ProjectionMatrix
print("Performing projection using einsum...")
start_time = time.time()

# einsum notation: ij,jk->ik (matrix multiplication)
projected_data = np.einsum('ij,jk->ik', features_norm, projection_matrix)

einsum_time = time.time() - start_time
print(f"Projection time (einsum): {einsum_time:.6f} seconds")

# Compare with standard matrix multiplication
start_time = time.time()
projected_standard = features_norm @ projection_matrix
standard_time = time.time() - start_time
print(f"Projection time (standard): {standard_time:.6f} seconds")
print(f"Results match: {np.allclose(projected_data, projected_standard)}")
print()

# Add projected coordinates to dataframe
df['proj_x'] = projected_data[:, 0]
df['proj_y'] = projected_data[:, 1]

print("Statistiques des données projetées:")
print(f"X - Min: {projected_data[:, 0].min():.4f}, Max: {projected_data[:, 0].max():.4f}, "
      f"Mean: {projected_data[:, 0].mean():.4f}")
print(f"Y - Min: {projected_data[:, 1].min():.4f}, Max: {projected_data[:, 1].max():.4f}, "
      f"Mean: {projected_data[:, 1].mean():.4f}")
print()

print("Sample projected data:")
print(df[['first_name', 'last_name', 'main_department', 'proj_x', 'proj_y']].head(10))

print("\n" + "=" * 80)
print("Q9: CALCULS DE COVARIANCE AVEC EINSUM")
print("=" * 80)
print()

# Select numerical features for covariance
feature_names = ['base_salary', 'performance_score', 'satisfaction_score', 
                 'tenure_years', 'age']

# Handle age if not present
if 'age' not in df.columns:
    # Generate synthetic age data
    df['age'] = 25 + df['tenure_years'] + np.random.randint(-5, 5, len(df))

features_cov = df[feature_names].values

# Center the data
features_centered = features_cov - features_cov.mean(axis=0)

n_samples, n_features = features_centered.shape

print(f"Calculating covariance matrix for {n_features} features...")
print()

# Method 1: Using einsum
print("Method 1: einsum implementation")
start_time = time.time()

# Covariance formula: Cov = (1/n) * X^T * X
# einsum notation: ji,jk->ik (transpose first, then multiply)
cov_einsum = np.einsum('ji,jk->ik', features_centered, features_centered) / (n_samples - 1)

einsum_time = time.time() - start_time
print(f"Time: {einsum_time:.6f} seconds")
print()

# Method 2: Using np.cov
print("Method 2: np.cov()")
start_time = time.time()

cov_numpy = np.cov(features_cov, rowvar=False)

numpy_time = time.time() - start_time
print(f"Time: {numpy_time:.6f} seconds")
print()

# Method 3: Manual calculation
print("Method 3: Manual (X^T @ X)")
start_time = time.time()

cov_manual = (features_centered.T @ features_centered) / (n_samples - 1)

manual_time = time.time() - start_time
print(f"Time: {manual_time:.6f} seconds")
print()

# Verify results match
print("Verification:")
print(f"einsum vs numpy: {np.allclose(cov_einsum, cov_numpy)}")
print(f"einsum vs manual: {np.allclose(cov_einsum, cov_manual)}")
print()

# Display covariance matrix
print("Matrice de covariance:")
cov_df = pd.DataFrame(cov_einsum, index=feature_names, columns=feature_names)
print(cov_df)
print()

# Calculate correlation matrix
print("Matrice de corrélation:")
std_devs = np.sqrt(np.diag(cov_einsum))
corr_einsum = cov_einsum / np.outer(std_devs, std_devs)
corr_df = pd.DataFrame(corr_einsum, index=feature_names, columns=feature_names)
print(corr_df)
print()

# Performance comparison
print("Performance Comparison:")
print(f"  einsum:       {einsum_time*1000:.4f} ms ({'Speedup: ' + str(numpy_time/einsum_time) + 'x' if einsum_time < numpy_time else 'Slower'})")
print(f"  np.cov:       {numpy_time*1000:.4f} ms (baseline)")
print(f"  manual:       {manual_time*1000:.4f} ms ({'Speedup: ' + str(numpy_time/manual_time) + 'x' if manual_time < numpy_time else 'Slower'})")

# Find strongest correlations
print("\nTop 5 corrélations (hors diagonale):")
correlation_pairs = []
for i in range(n_features):
    for j in range(i + 1, n_features):
        correlation_pairs.append((feature_names[i], feature_names[j], abs(corr_einsum[i, j])))

correlation_pairs.sort(key=lambda x: x[2], reverse=True)
for feat1, feat2, corr in correlation_pairs[:5]:
    print(f"{feat1:25s} ↔ {feat2:25s}: {corr:.4f}")

print("\n" + "="*80)
print("FIN Q7-Q9")
print("="*80)
