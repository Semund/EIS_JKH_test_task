## Тестовое задание для ЕИС ЖКХ

1. Скачать ПО:
```
git clone https://github.com/Semund/EIS_JKH_test_task.git && cd ./eis_jkh_test_task
```

2. Создаем базу данных MongoDB и заполняем ее фейковыми данными с помощью контейнеров Docker:
```
docker-compose up -d --build
```

3. Запустить программы для выполнения заданий:
```
python ./solution/task1_solution.py
```

```
python ./solution/task2_solution.py
```
