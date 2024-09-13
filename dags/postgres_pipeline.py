import os

from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
from airflow import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


sql_dir = os.path.join(os.getcwd(), 'sql_statements')


with DAG(
    dag_id = 'postgres_pipeline',
    description = 'Running a pipeline using the Postgres operator',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['operator', 'postgres'],
    template_searchpath = sql_dir
) as dag:

    create_table_customers = PostgresOperator(
        task_id = 'create_table_customers',
        postgres_conn_id = 'postgres_connection',
        sql = 'create_table_customers.sql'
    )

    create_table_customer_purchases = PostgresOperator(
        task_id = 'create_table_customer_purchases',
        postgres_conn_id = 'postgres_connection',
        sql = 'create_table_customer_purchases.sql'
    )

    create_table_customers >> create_table_customer_purchases
