def _write_to_database(ti) -> None:
    import json
    import pandas as pd
    from airflow.providers.amazon.aws.hooks.s3 import S3Hook
    from airflow.providers.postgres.hooks.postgres import PostgresHook
    
    key, bucket = ti.xcom_pull(task_ids='write_file_to_bucket')

    json_str = json.loads(
        S3Hook('local_minio')
        .read_key(key=key, bucket_name=bucket)
    )

    indices = ['name', 'region', 'country', 'last_updated', 'temp_c', 'temp_f']

    data = (
        pd
        .concat([
            pd.Series(data=json_str['location']),
            pd.Series(data=json_str['current'])
        ])
        [indices]
        .to_frame()
        .transpose()
    )

    data['last_updated'] = pd.to_datetime(data['last_updated'])

    conn = PostgresHook('local_pg').get_sqlalchemy_engine()

    data.to_sql(
        name='weather_data',
        con=conn,
        if_exists='append',
        index=False
    )