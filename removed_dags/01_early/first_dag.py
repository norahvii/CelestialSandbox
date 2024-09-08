from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _start():
    print('hi')

def _stop():
    print('bye')

# Define the DAG
with DAG('first_dag', start_date=datetime(2024, 1, 1),
         tags=['test','tutorial'],
         schedule_interval='@daily', catchup=False) as dag:

    start_task = PythonOperator(
        task_id='start_task',
        python_callable=_start
    )

    stop_task = PythonOperator(
        task_id='stop_task',
        python_callable=_stop
    )

    start_task >> stop_task