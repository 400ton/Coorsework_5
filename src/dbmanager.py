import re
import psycopg2


class DBManager:
    """Класс для работы с базой данных"""
    def __init__(self, params):
        self.params = params

    def create_bd(self, database_name):
        """Cоздание базы данных"""
        if not re.match(r'^[a-zA-Z0-9_]+$', database_name):
            raise ValueError("Имя базы данных должно содержать только буквы, цифры и подчеркивания.")

        try:
            conn = psycopg2.connect(dbname='postgres', **self.params_db)
            conn.autocommit = True
            cur = conn.cursor()

            cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
            cur.execute(f'CREATE DATABASE {database_name}')

            cur.close()
            conn.close()
        except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
            print(f"Ошибка при создании базы данных: {e}")

    def create_tables(self, database_name):
        """Создание таблиц companies и vacancies в созданной базе данных HH_vacancy"""

        try:
            with psycopg2.connect(dbname=database_name, **self.params_db) as conn:
                with conn.cursor() as cur:
                    cur.execute("SELECT true FROM pg_catalog.pg_database WHERE datname = %s", (database_name,))
                    if not cur.fetchone():
                        raise Exception(f"База данных {database_name} не найдена.")

                    cur.execute("""
                        CREATE TABLE companies (
                        company_id SERIAL PRIMARY KEY,
                        company_name VARCHAR UNIQUE
                        )
                        """)

                    cur.execute("""
                            CREATE TABLE vacancies (
                            vacancy_id serial,
                            vacancy_name text not null,
                            salary int,
                            company_name text REFERENCES companies(company_name) NOT NULL,
                            vacancy_url varchar not null,
                            foreign key(company_name) references companies(company_name)
                            )
                            """)
        except psycopg2.Error as e:
            print(f"Ошибка при создании таблиц: {e}")
        finally:
            conn.close()

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и
        количества вакансий у каждой компании"""
        pass

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям"""
        pass

    def get_vacancies_with_higher_salary(self):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям"""
        pass

    def get_vacancies_with_keyword(self):
        """получает список всех вакансий,
        в названии которых содержатся переданные в метод слова, например python"""
        pass
