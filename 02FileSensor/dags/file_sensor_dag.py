from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash import BashOperator
from airflow.sensors.filesystem import FileSensor

from datetime import datetime

with DAG(
    dag_id='file_sensor_dag',
    start_date=datetime(2022, 5, 28),
    schedule_interval='@daily',
    catchup=False
) as dag:

    start_task = EmptyOperator(
        task_id='start'
    )

    wait_for_file_arrival = FileSensor(
        task_id='wait_for_file_arrival',
        fs_conn_id='fp_data',
        filepath='log_{{ds}}.txt',
        mode='poke',
        poke_interval=10
    )

    print_file_content = BashOperator(
        task_id='print_file_content',
        bash_command='cat /opt/airflow/data/log_{{ds}}.txt'
    )

    stop_task = EmptyOperator(
        task_id='stop'
    )

start_task >> wait_for_file_arrival
wait_for_file_arrival >> print_file_content
print_file_content >> stop_task