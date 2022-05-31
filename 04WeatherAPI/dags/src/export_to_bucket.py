def _write_file_to_bucket(ti) -> tuple:
    from airflow.providers.amazon.aws.hooks.s3 import S3Hook
    
    filename = ti.xcom_pull(task_ids='fetch_data')
    key = filename.split('/')[-1]
    bucket = 'my-weather-data'

    s3 = S3Hook('local_minio')

    s3.load_file(
        filename=filename,
        key=key,
        bucket_name=bucket
    )

    return (key, bucket)