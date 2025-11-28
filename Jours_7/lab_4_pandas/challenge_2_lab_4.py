import pandas as pd
import numpy as np

def challenge_monitoring():
    # Création de séries temporelles simulées
    dates = pd.date_range('2023-01-01', periods=1000, freq='H')
    metrics = pd.DataFrame({
        'CPU': np.random.rand(len(dates)) * 100,
        'Memoire': np.random.rand(len(dates)) * 32,   # Go
        'Reseau': np.random.rand(len(dates)) * 1000, # Mbps
        'Stockage': np.random.rand(len(dates)) * 500 # Go
    }, index=dates)

    # 1. Détection anomalies (rolling stats)
    rolling_mean = metrics.rolling(window=24).mean()
    anomalies = metrics[(metrics - rolling_mean).abs() > 2 * metrics.std()]

    # 2. Resampling pour rapports quotidiens
    daily_report = metrics.resample('D').agg(['mean', 'max', 'min'])

    # 3. Features engineering pour ML
    features = pd.DataFrame({
        'cpu_trend': metrics['CPU'].rolling(24).apply(lambda x: np.polyfit(range(len(x)), x, 1)[0]),
        'mem_volatility': metrics['Memoire'].rolling(24).std(),
        'net_efficiency': metrics['Reseau'].pct_change().rolling(24).mean()
    })

    print("\n--- Exemple métriques ---\n", metrics.head())
    print("\nAnomalies détectées\n", anomalies.dropna().head())
    print("\nRapport quotidien\n", daily_report.head())
    print("\nFeatures ML\n", features.head())

challenge_monitoring()