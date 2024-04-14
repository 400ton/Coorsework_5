import re
import psycopg2
import codecs


class DBManager:
    """Класс для работы с базой данных"""

    def __init__(self, params, db_name):
        self.params = params
        self.db_name = db_name

    def create_bd(self):
        """Cоздание базы данных"""
        if not re.match(r'^[a-zA-Z0-9_]+$', self.db_name):  # Проверка на корректность имени
            raise ValueError("Имя базы данных должно содержать только буквы, цифры и подчеркивания.")

        conn = psycopg2.connect(dbname='postgres', **self.params)
        conn.autocommit = True
        cur = conn.cursor()

        try:
            cur.execute(f"DROP DATABASE {self.db_name}")
            cur.execute(f"CREATE DATABASE {self.db_name}")
            conn.close()

        except (psycopg2.DatabaseError, psycopg2.OperationalError, psycopg2.errors.InvalidCatalogName) as e:
            print(f"Ошибка при создании базы данных: {e}")

    def create_tables(self):
        """Создание таблиц companies и vacancies в созданной базе данных"""

        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    # Проверка на наличие базы данных в PostgreSql
                    cur.execute("SELECT true FROM pg_catalog.pg_database WHERE datname = %s", self.db_name)
                    if not cur.fetchone():
                        raise Exception(f"База данных {self.db_name} не найдена.")

                    cur.execute("""
                        CREATE TABLE companies (
                        company_id SERIAL PRIMARY KEY,
                        company_name VARCHAR(100) UNIQUE
                        company_url VARCHAR(250)
                        )
                        """)

                    cur.execute("""
                        CREATE TABLE vacancies (
                        vacancy_id SERIAL PRIMARY KEY,
                        vacancy_name VARCHAR(100) not null,
                        city VARCHAR(255),
                        salary INT,
                        currency VARCHAR(10),
                        responsibility TEXT,
                        publish_date DATETIME,
                        experience TEXT,
                        vacancy_url VARCHAR(250),
                        company_name VARCHAR(100) REFERENCES companies(company_name) NOT NULL,
                        foreign key(company_name) REFERENCES companies(company_name)
                        )
                        """)
                conn.commit()
                conn.close()
        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")

    def save_info_db(self, company, vacancies):
        """Сохранение информации в таблице базы данных"""
        try:
            with psycopg2.connect(dbname=self.db_name, **self.params) as conn:
                with conn.cursor() as cur:
                    for employer in company:
                        cur.execute(
                            f"INSERT INTO companies(company_name, company_url) "
                            f"VALUES ('{employer['employer']}' {employer['url']}")
                    for vacancy in vacancies:
                        cur.execute(
                            f"INSERT INTO vacancies(vacancy_name, city, salary, currency, responsibility, publish_date, "
                            f"experience, vacancy_url, company_name) values"
                            f"('{vacancy['vacancy_name']}', '{vacancy['city']}', '{int(vacancy['salary'])}', "
                            f"'{vacancy['currency']}', '{vacancy['employer']}', '{vacancy['url']}')")
                        conn.commit()
                        conn.close()
        except psycopg2.Error as e:
            print(f"Ошибка при заполнении таблиц: {e}")

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и
        количества вакансий у каждой компании"""
        try:
            params_encoded = {k: codecs.encode(v, 'utf-8') for k, v in self.params.items()}
            with psycopg2.connect(dbname=self.db_name, **params_encoded) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT company_name, COUNT(vacancy_name) from vacancies GROUP BY company_name')
                    answer = cur.fetchall()
            conn.close()
            return answer
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка всех компаний и количества вакансий у каждой компании: {e}")

    def get_all_vacancies(self):
        """Получение списка всех вакансий"""
        try:
            params_encoded = {k: codecs.encode(v, 'utf-8') for k, v in self.params.items()}
            with psycopg2.connect(dbname=self.db_name, **params_encoded) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT * from vacancies')
                    answer = cur.fetchall()
            conn.close()
            return answer
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка всех вакансий: {e}")

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        try:
            params_encoded = {k: codecs.encode(v, 'utf-8') for k, v in self.params.items()}
            with psycopg2.connect(dbname=self.db_name, **params_encoded) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT avg(salary) from vacancies')
                    answer = cur.fetchall()
            conn.close()
            return answer
        except psycopg2.Error as e:
            print(f"Ошибка при получении средней зарплаты по вакансиям: {e}")

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        try:
            params_encoded = {k: codecs.encode(v, 'utf-8') for k, v in self.params.items()}
            with psycopg2.connect(dbname=self.db_name, **params_encoded) as conn:
                with conn.cursor() as cur:
                    cur.execute('SELECT vacancy_name, salary FROM vacancies'
                                'WHERE salary > (SELECT AVG(salary) FROM vacancies)'
                                'ORDER BY vacancy_name DESC')
                    answer = cur.fetchall()
            conn.close()
            return answer
        except psycopg2.Error as e:
            print(f"Ошибка при получении списка всех вакансий, у которых зарплата выше средней по всем вакансиям: {e}")

    def get_vacancies_with_keyword(self, keyword):
        """Получение списка всех вакансий,
        в названии которых содержатся переданные в метод слова, например python"""

        params_encoded = {k: codecs.encode(v, 'utf-8') for k, v in self.params.items()}
        with psycopg2.connect(dbname=self.db_name, **params_encoded) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT vacancy_name from vacancies WHERE vacancy_name LIKE '%{keyword}%'")
                answer = cur.fetchall()
        conn.close()
        return answer
