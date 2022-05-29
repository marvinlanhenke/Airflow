from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from datetime import datetime

def _write_file_to_bucket():
    filename = '/tmp/test-file.txt'

    with open(filename, 'w') as f:
        f.write('Hello Minio!')
    
    s3 = S3Hook('local_minio')
    s3.load_file(
        filename=filename,
        key='my-test-file.txt',
        bucket_name='my-bucket'
    )

# def _read_file_from_bucket():
#     s3 = S3Hook('local_minio')
#     file_content = s3.read_key(
#         key='my-test-file.txt',
#         bucket_name='my-bucket'
#     )
#     print(file_content)

with DAG(
    dag_id='minio_s3_dag',
    start_date=datetime(2022, 5, 28),
    schedule_interval=None
) as dag:

    start_task = EmptyOperator(
        task_id='start'
    )

    write_file_to_bucket = PythonOperator(
        task_id='write_file_to_bucket',
        python_callable=_write_file_to_bucket
    )

    # read_file_from_bucket = PythonOperator(
    #     task_id='read_file_from_bucket',
    #     python_callable=_read_file_from_bucket
    # )

    stop_task = EmptyOperator(
        task_id='stop'
    )

start_task >> write_file_to_bucket >> stop_task
# start_task >> read_file_from_bucket >> stop_task