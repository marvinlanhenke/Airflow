from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from src.export_to_bucket import _write_file_to_bucket
from src.export_to_db import _write_to_database
from src.clean_tmp import _clean_up_tmp
from datetime import datetime

with DAG(
    dag_id='weather_api',
    start_date=datetime(2022, 5, 30),
    schedule_interval='@hourly',
    catchup=False
) as dag:

    fetch_data = BashOperator(
        task_id='fetch_data',
        bash_command='curl -o \
            /tmp/weatherapi_{{ts}}.json \
            -X GET "http://api.weatherapi.com/v1/current.json?key=$key&q=$city&aqi=no"; \
            echo "/tmp/weatherapi_{{ts}}.json"',
        env={'city': 'Ahlen', 'key': 'daec3b7f11714df7958145849223005'}
    )

    write_file_to_bucket = PythonOperator(
        task_id='write_file_to_bucket',
        python_callable=_write_file_to_bucket,
        provide_context=True
    )

    write_to_database = PythonOperator(
        task_id='write_to_database',
        python_callable=_write_to_database,
        provide_context=True
    )

    clean_up_tmp = PythonOperator(
        task_id='clean_up_tmp',
        python_callable=_clean_up_tmp,
        provide_context=True
    )

fetch_data >> write_file_to_bucket
write_file_to_bucket >> write_to_database
write_to_database >> clean_up_tmp