import pandas as pd
import os
from airflow.utils.dates import days_ago
from airflow.models import Variable
from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator


def read_csv_file():
    df = pd.read_csv('/Users/loonycorn/airflow/datasets/car_data.csv')
    print(df)
    return df.to_json()


def determine_branch():
    final_output = Variable.get("transform", default_var=None)

    if final_output == 'filter_two_seaters':
        return 'filter_two_seaters_task'
    elif final_output == 'filter_fwds':
        return 'filter_fwds_task'


def filter_two_seaters(ti):
    json_data = ti.xcom_pull(task_ids='read_csv_file_task')
    df = pd.read_json(json_data)
    two_seater_df = df[df['Seats'] == 2]
    
    ti.xcom_push(key='transform_result', value=two_seater_df.to_json())
    ti.xcom_push(key='transform_filename', value='two_seaters')


def filter_fwds(ti):
    json_data = ti.xcom_pull(task_ids='read_csv_file_task')
    df = pd.read_json(json_data)
    fwd_df = df[df['PowerTrain'] == 'FWD']
    
    ti.xcom_push(key='transform_result', value=fwd_df.to_json())
    ti.xcom_push(key='transform_filename', value='fwds')


def write_csv_result(ti): 
    json_data = ti.xcom_pull(key='transform_result')
    file_name = ti.xcom_pull(key='transform_filename')

    output_dir = os.path.join(os.getcwd(), 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    df = pd.read_json(json_data)
    csv_path = os.path.join(output_dir, f'{file_name}.csv')
    df.to_csv(csv_path, index=False)
    print(f"Saved csv to {csv_path}")


with DAG(
    dag_id = 'branching_using_operators',
    description = 'Branching using operators',
    default_args = default_args,
    start_date = days_ago(1),
    schedule_interval = '@once',
    tags = ['branching', 'python', 'operators']
) as dag:
    read_csv_file_task = PythonOperator(
        task_id = 'read_csv_file_task',
        python_callable = read_csv_file
    )

    determine_branch_task = BranchPythonOperator(
        task_id='determine_branch_task',
        python_callable=determine_branch
    )

    filter_two_seaters_task = PythonOperator(
        task_id='filter_two_seaters_task',
        python_callable=filter_two_seaters
    )

    filter_fwds_task = PythonOperator(
        task_id='filter_fwds_task',
        python_callable=filter_fwds
    )

    write_csv_result_task = PythonOperator(
        task_id = 'write_csv_result_task',
        python_callable = write_csv_result,
        trigger_rule='none_failed'
    )


read_csv_file_task >> determine_branch_task >> \
    [filter_two_seaters_task, filter_fwds_task] >> write_csv_result_task
