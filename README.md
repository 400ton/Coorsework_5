# Выполнение курсового проекта № 5. Работа с базой данных

В рамках проекта вам необходимо получить данные о компаниях и вакансиях с сайта [hh.ru](hh.ru), спроектировать таблицы в БД PostgreSQL и загрузить полученные данные в созданные таблицы.

# Используемые технологии
![Jokes Card](https://readme-jokes.vercel.app/api)  
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![PyCharm](https://img.shields.io/badge/pycharm-143?style=for-the-badge&logo=pycharm&logoColor=black&color=black&labelColor=green)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)


# Для работы с проектом необходимо:
1. Установить базу данных PostgresSQL по ссылке https://www.postgresql.org/download/
2. Установить интерпретатор Python, допустим https://www.jetbrains.com/pycharm/download/?section=windows

### Используя интрерпритатор:
- В терминале введите команду 
```ini
git clone https://github.com/400ton/Coorsework_5.git
```
- Создайте виртуальное окружение:
```ini
python3 -m venv venv
```
- Активируйте виртуальное окружение:
```ini
source venv/Scripts/activate
```
- В папке проекта ___src___ cоздайте ___database.ini___ конфигурационный файл с вашими параметрами подключения к БД.

Пример содержания файла:
```ini
[postgresql]
host=localhost
user=postgres
password=12345
port=5432
```

Автор:
Кошелев Антон, https://github.com/400ton/
