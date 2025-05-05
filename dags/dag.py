from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime
import re

def read_text(**kwargs):
    input_file = "/opt/airflow/dags/input/input.txt"
    try:
        with open(input_file, 'r', encoding='windows-1251') as f:
            text = f.read()

        words = re.findall(r'\b\w+\b', text)

        word_count = len(words)

        kwargs['ti'].xcom_push(key='just_text', value=text)
        kwargs['ti'].xcom_push(key='word_count', value=word_count)

    except Exception as e:
        print(f"Error reading file {input_file}: {e}")
        raise


def print_text(**kwargs):
    text = kwargs['ti'].xcom_pull(task_ids='read_text', key='just_text')
    print(f"Это текст: {text}")

def count_words(**kwargs):
    text = kwargs['ti'].xcom_pull(task_ids='read_text', key='just_text')
    word_count = len(text.split())
    print(f"Слов в этом тексте: {word_count}")
    output_file = "/opt/airflow/dags/output/output.txt"
    with open(output_file, 'w') as f:
        f.write(f"{word_count}")


with DAG(
    dag_id='dag',
    schedule_interval='@daily',  
    start_date=datetime(2023, 10, 1),
    catchup=False,

) as dag:

    read_text_task = PythonOperator(
        task_id="read_text",
        python_callable=read_text,
        provide_context=True,
    )

    print_text_task = PythonOperator(
        task_id="print_text",
        python_callable=print_text,
        provide_context=True,
    )

    count_words_task = PythonOperator(
        task_id="count_words",
        python_callable=count_words,
        provide_context=True,
    )


    read_text_task >> print_text_task >> count_words_task 