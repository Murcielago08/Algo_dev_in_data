import random
import csv
import json
import os
import time
from datetime import datetime, timedelta
from functools import wraps

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator
from airflow.utils.trigger_rule import TriggerRule

# Default arguments for all DAGs
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 10),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# =============================================================================
# Challenge 1 : Pipeline de traitement de données
# =============================================================================

def generate_csv_data(**kwargs):
    """Génère un fichier CSV avec 100 lignes de données aléatoires."""
    file_path = '/tmp/challenge1_data.csv'
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'value'])
        for i in range(100):
            writer.writerow([i, random.randint(1, 1000)])
    print(f"File generated at {file_path}")
    return file_path

def calculate_stats(**kwargs):
    """Lit le fichier CSV et calcule des statistiques (moyenne, min, max)."""
    input_path = '/tmp/challenge1_data.csv'
    output_path = '/tmp/challenge1_stats.json'
    
    values = []
    with open(input_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            values.append(int(row['value']))
            
    stats = {
        'count': len(values),
        'mean': sum(values) / len(values) if values else 0,
        'min': min(values) if values else 0,
        'max': max(values) if values else 0,
        'generated_at': datetime.now().isoformat()
    }
    
    with open(output_path, 'w') as f:
        json.dump(stats, f, indent=4)
        
    print(f"Stats written to {output_path}: {stats}")
    return output_path

def cleanup_files(**kwargs):
    """Nettoie les fichiers temporaires."""
    files = ['/tmp/challenge1_data.csv', '/tmp/challenge1_stats.json']
    for f in files:
        if os.path.exists(f):
            os.remove(f)
            print(f"Removed {f}")

with DAG(
    'challenge_1_pipeline',
    default_args=default_args,
    description='Pipeline de traitement de données CSV -> JSON',
    schedule_interval=None,
    catchup=False,
    tags=['challenge1', 'data']
) as dag1:

    task_generate = PythonOperator(
        task_id='generate_csv',
        python_callable=generate_csv_data
    )

    task_stats = PythonOperator(
        task_id='calculate_stats',
        python_callable=calculate_stats
    )

    task_email = BashOperator(
        task_id='send_email_simulation',
        bash_command='echo "Subject: Stats Calculated\n\nStats are ready." # Simulation d\'envoi d\'email'
    )

    task_cleanup = PythonOperator(
        task_id='cleanup_files',
        python_callable=cleanup_files
    )

    task_generate >> task_stats >> task_email >> task_cleanup


# =============================================================================
# Challenge 2 : Système de décision conditionnelle
# =============================================================================

def check_time_branch(**kwargs):
    """Vérifie l'heure d'exécution et choisit la branche."""
    # Simulation de l'heure pour le test (ou utiliser datetime.now().hour)
    # Pour tester les deux branches, vous pouvez changer cette valeur manuellement ou utiliser une Variable Airflow
    current_hour = datetime.now().hour
    print(f"Current hour: {current_hour}")
    
    if 9 <= current_hour < 18:
        return 'business_hours_start'
    else:
        return 'off_hours_start'

with DAG(
    'challenge_2_conditional',
    default_args=default_args,
    description='Décision conditionnelle selon les heures de bureau',
    schedule_interval=None,
    catchup=False,
    tags=['challenge2', 'branching']
) as dag2:

    branching = BranchPythonOperator(
        task_id='check_time',
        python_callable=check_time_branch
    )

    # Branche Heures de Bureau
    business_start = DummyOperator(task_id='business_hours_start')
    business_process = BashOperator(
        task_id='process_business_transactions',
        bash_command='echo "Processing instant transactions..."'
    )
    business_log = BashOperator(
        task_id='log_business_activity',
        bash_command='echo "Logging business hours activity"'
    )

    # Branche Heures Creuses
    off_hours_start = DummyOperator(task_id='off_hours_start')
    off_hours_batch = BashOperator(
        task_id='process_batch_maintenance',
        bash_command='echo "Running heavy batch maintenance..."'
    )
    off_hours_archive = BashOperator(
        task_id='archive_logs',
        bash_command='echo "Archiving daily logs"'
    )

    # Jonction
    join = DummyOperator(
        task_id='join_branches',
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    branching >> business_start >> business_process >> business_log >> join
    branching >> off_hours_start >> off_hours_batch >> off_hours_archive >> join


# =============================================================================
# Challenge 3 : Décorateur avancé
# =============================================================================

def custom_task_monitor(task_id=None, **kwargs):
    """
    Décorateur qui log le début/fin, mesure le temps et gère les exceptions.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            start_time = time.time()
            print(f"[{datetime.now()}] START Task: {func.__name__}")
            
            try:
                result = func(*args, **inner_kwargs)
                
                duration = time.time() - start_time
                print(f"[{datetime.now()}] END Task: {func.__name__} - Duration: {duration:.4f}s")
                return result
            
            except Exception as e:
                print(f"[{datetime.now()}] ERROR in Task: {func.__name__} - {str(e)}")
                # Ici on pourrait relancer l'exception ou décider de masquer l'erreur
                # Pour Airflow, il vaut mieux relancer pour marquer la tâche en échec (retry)
                raise e
        
        # Création automatique de la tâche Airflow
        # Note: Dans une vraie implémentation 'TaskFlow API' (@task), cela serait différent.
        # Ici on simule le wrapper pour utilisation dans PythonOperator classique ou pur python
        return wrapper
    return decorator

# Fonction décorée à utiliser comme callable
@custom_task_monitor()
def risky_operation(**kwargs):
    print("Performing a risky operation...")
    if random.choice([True, False]): # 50% chance failure
        print("Operation succeeded!")
        return "Success"
    else:
        raise ValueError("Random failure simulation")

with DAG(
    'challenge_3_decorator',
    default_args=default_args,
    description='Démonstration décorateur personnalisé',
    schedule_interval=None,
    catchup=False,
    tags=['challenge3', 'decorator']
) as dag3:
    
    # Note: On appelle le wrapper qui exécute la logique de décoration lors de l'exécution
    task_monitored = PythonOperator(
        task_id='monitored_task',
        python_callable=risky_operation,
        retries=2 # Permet de voir le log de retry grâce au décorateur
    )


# =============================================================================
# Challenge 4 : Workflow complexe avec parallélisme
# =============================================================================

def process_type_a(**kwargs):
    time.sleep(1)
    return "Result A"

def process_type_b(**kwargs):
    time.sleep(2)
    return "Result B"

def process_type_c(**kwargs):
    # Cette branche peut échouer, mais on ne veut pas bloquer l'agrégation
    try:
        if random.random() < 0.3:
            raise Exception("Failure in Branch C")
        return "Result C"
    except Exception as e:
        print(f"Handled error in branch C: {e}")
        return "Error in C (Handled)"

def aggregate_results(**kwargs):
    ti = kwargs['ti']
    # Récupération via XCom
    res_a = ti.xcom_pull(task_ids='process_a')
    res_b = ti.xcom_pull(task_ids='process_b')
    res_c = ti.xcom_pull(task_ids='process_c')
    
    print(f"Aggregation Results: A={res_a}, B={res_b}, C={res_c}")
    return {"A": res_a, "B": res_b, "C": res_c}

with DAG(
    'challenge_4_complex',
    default_args=default_args,
    description='Parallélisme et synchronisation',
    schedule_interval=None,
    catchup=False,
    tags=['challenge4', 'parallel']
) as dag4:
    
    start = DummyOperator(task_id='start')
    
    # Branche A
    task_a = PythonOperator(
        task_id='process_a',
        python_callable=process_type_a
    )
    
    # Branche B
    task_b = PythonOperator(
        task_id='process_b',
        python_callable=process_type_b
    )
    
    # Branche C
    task_c = PythonOperator(
        task_id='process_c',
        python_callable=process_type_c
    )
    
    # Agrégation
    # On utilise ALL_DONE pour s'assurer que ça s'exécute même si C échoue (si non géré)
    # Mais ici C gère son erreur, donc ONE_SUCCESS ou ALL_SUCCESS fonctionne aussi si C renvoie toujours quelque chose.
    # Pour la sûreté "Gestion des erreurs sur une seule branche sans arrêter les autres", TRIGGER_RULE=ALL_DONE est souvent utilisé.
    aggregate = PythonOperator(
        task_id='aggregate_results',
        python_callable=aggregate_results,
        trigger_rule=TriggerRule.ALL_DONE
    )
    
    end = DummyOperator(task_id='end')
    
    start >> [task_a, task_b, task_c] >> aggregate >> end
