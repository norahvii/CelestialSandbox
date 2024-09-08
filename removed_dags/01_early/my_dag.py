from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.decorators import dag
from datetime import datetime

def _start():
        print('hi')

def _stop():
        print('bye')


with DAG('my_dag', start_date=datetime(2024, 1, 1),
         schedule_interval='@daily', catchup=False) as dag:

         start = PythonOperator(
                 task_id='10001110101',
                 python_callable=_start
        )

         start = PythonOperator(
                 task_id='11001110101',
                 python_callable=_stop
        )

         10001110101 >> 11001110101

