# Word Count

Проект с DAG для Apache Airflow & Docker Compose, который читает текст из файла, считает слова и выводит результат.



## Содержимое

```
itmo-2sem-devops/
├── dags/
│   ├── word_count_dag.py  
│   ├── input/             
│   └── output/            
├── Dockerfile             
├── docker-compose.yml     
└── README.md              
```


## Описание DAG

1. **`read_input_text_task`:** Читает текст из `input/input.txt`.
2. **`print_input_text_task`:** Выводит текст в лог.
3. **`count_words_task`:** Считает слова, выводит кол-во в лог и записывает его в `output/output.txt`.


## Как запустить

1. Клонируйте репозиторий:
   ```bash
   git clone https://gitlab.com/countercurrent1/itmo-2sem-devops.git
   cd itmo-2sem-devops
   ```

2. Добавьте текст в файл:
   ```bash
   echo "Например, это текст из шести слов." > dags/input/input.txt
   ```

3. Запустите контейнеры, проверьте что у всех статус healthy:
   ```bash
   docker-compose up -d
   docker ps
   ```

4. Откройте Airflow: `http://localhost:8080` (логин: `airflow`, пароль: `airflow`).

5. Запустите DAG `word_count` и проверьте логи + вывод в output файле.


## Скриншоты | Screenshots

1.  Запущенные контейнеры | Running Containers
    ![docker](/dags/images/containers.png)

2.  Список DAG-ов | DAGs List
    ![dags](/dags/images/dags.png)

3.  Информация о DAG | DAG Info
    ![dag](/dags/images/dag_info.png)


## Остановка

```bash
docker-compose down
```

