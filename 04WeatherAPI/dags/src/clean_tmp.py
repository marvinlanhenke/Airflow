def _clean_up_tmp(ti) -> None:
    import os

    filename = ti.xcom_pull(task_ids='fetch_data')
    os.remove(filename)