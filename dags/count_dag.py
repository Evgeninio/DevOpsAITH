from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.python import PythonOperator
from airflow.sensors.python import PythonSensor
from datetime import datetime, timedelta
import os, json

OUTPUT_PATH = "/opt/airflow/spark/output/stats_{{ ts_nodash }}.json"

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 10, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def _exists(path: str) -> bool:
    return os.path.exists(path)

def _read_and_log(path: str, ti=None):
    with open(path, "r") as f:
        stats = json.load(f)
    print(f"[Spark stats] file={path} stats={stats}")
    if ti:
        ti.xcom_push(key="spark_stats", value=stats)

with DAG(
    dag_id="count_spark",
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    tags=["spark"],
) as dag:

    spark_job = SparkSubmitOperator(
        task_id="spark_stats",
        application="/opt/airflow/spark/spark_stats.py",
        name="spark_stats_job",
        conn_id="spark_local",
        application_args=[
            "--n", "10000",
            "--seed", "123",
            "--output", OUTPUT_PATH,
        ],
    )

    wait_for_output = PythonSensor(
        task_id="wait_for_output",
        python_callable=_exists,
        op_kwargs={"path": OUTPUT_PATH},
        poke_interval=5,
        timeout=60 * 5,
        mode="reschedule",
    )

    summarize = PythonOperator(
        task_id="summarize_stats",
        python_callable=_read_and_log,
        op_kwargs={"path": OUTPUT_PATH},
    )

    spark_job >> wait_for_output >> summarize
