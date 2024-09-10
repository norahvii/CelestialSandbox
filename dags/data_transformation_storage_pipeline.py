import pandas as pd
import json, csv, os

from airflow.operators.sqlite_operator import SqliteOperator
from airflow.utils.dates import days_ago
from airflow.decorators import dag, task

from airflow.models import Variable
from datetime import datetime, timedelta
from airflow.models import Variable

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}


dataset_dir = os.path.join(os.getcwd(), 'datasets')
output_dir = os.path.join(os.getcwd(), 'output')


@dag(dag_id='data_transformation_storage_pipeline',
    description = 'Data transformation and storage pipeline',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['sqlite', 'python', 'taskflow_api', 'xcoms'])

def data_transformation_storage_pipeline():

    @task
    def read_dataset():
        df = pd.read_csv(os.path.join(dataset_dir, 'car_data.csv'))
        return df.to_json()
    
    @task
    def create_table():
        sqlite_operator = SqliteOperator(
            task_id="create_table",
            sqlite_conn_id="my_sqlite_conn",
            sql="""CREATE TABLE IF NOT EXISTS car_data (
                        id INTEGER PRIMARY KEY,
                        brand TEXT NOT NULL,
                        model TEXT NOT NULL,
                        body_style TEXT NOT NULL,
                        seat INTEGER NOT NULL,
                        price INTEGER NOT NULL);""",
        )

        sqlite_operator.execute(context=None)

    @task
    def insert_selected_data(**kwargs):
        ti = kwargs['ti']
        json_data = ti.xcom_pull(task_ids='read_dataset')
        df = pd.read_json(json_data)
        df = df[['Brand', 'Model', 'BodyStyle', 'Seats', 'PriceEuro']]
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        insert_query = """
            INSERT INTO car_data (brand, model, body_style, seat, price)
            VALUES (?, ?, ?, ?, ?)
        """

        parameters = df.to_dict(orient='records')

        for record in parameters:
            sqlite_operator = SqliteOperator(
                task_id="insert_data",
                sqlite_conn_id="my_sqlite_conn",
                sql=insert_query,
                parameters=tuple(record.values()),
            )

            sqlite_operator.execute(context=None)

    read_dataset() >> create_table() >> insert_selected_data()


data_transformation_storage_pipeline()
