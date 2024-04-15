from src.config import config
from src.hh_api import HeadHunterAPI
from src.dbmanager import DBManager


def main():

    # Создаем обьект класса HeadHunterAPI для получения данных по api
    hh_response = HeadHunterAPI()

    # Получаем список доступных компаний
    company = hh_response.list_company()

    # Получаем список доступных вакансий
    vacancy = hh_response.list_vacancies()

    # Создаем обьект класса DBManager для работы с базой данных PostgreSQL
    db_manager = DBManager(config(), 'HH_company')

    # Создаем базу данных
    db_manager.create_bd()

    # Создаем таблицы в базе данных
    db_manager.create_tables()

    # Заполняем таблицы в базе данных
    db_manager.save_info_db(company, vacancy)

    # Получение списка всех компаний и количества вакансий у каждой компании
    all_comp_vac = db_manager.get_companies_and_vacancies_count()

    print("Получение списка всех компаний и количества вакансий у каждой компании: ")
    for value in all_comp_vac:
        print(f"{value}")

    # Получение списка всех вакансий
    all_vacancies = db_manager.get_all_vacancies()

    print("\nПолучение списка всех вакансий: ")
    for value in all_vacancies:
        print(f"{value}\n")

    # Получение средней зарплаты по вакансиям
    avg_salary = db_manager.get_avg_salary()

    print("\nПолучение средней зарплаты по вакансиям: ")
    for value in avg_salary:
        print(f"{value}\n")

    # Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям
    higher_salary = db_manager.get_vacancies_with_higher_salary()

    print("\nПолучение списка всех вакансий, у которых зарплата выше средней по всем вакансиям: ")
    for value in higher_salary:
        print(f"{value}")

    # Получение списка всех вакансий, в названии которых содержатся переданные в метод слова, например 'водитель'
    with_keyword = db_manager.get_vacancies_with_keyword('водитель')
    print("\nПолучение списка всех вакансий, по ключевому слову: ")
    for value in with_keyword:
        print(f"{value}")


if __name__ == "__main__":
    main()
