import requests


class HeadHunterAPI:
    """
    Класс для работы с API запросами c сайта hh.ru
    """

    def __init__(self):
        """
        Конструктор по умолчанию имеет url адрес для работы с API запросом для вакансий с сайта hh.ru
        """
        self.__base_url = "https://api.hh.ru/vacancies"

    def get_vacancies(self, employer_id):
        """
        Функция возвращает данные с сайта по введенному ключу
        :param employer_id:
        :return: json object
        """
        try:
            params = {"per_page": 100,
                      "employer_id": employer_id,
                      "only_with_salary": True,
                      "area": 113,
                      "only_with_vacancies": True}
            response = requests.get(self.__base_url, params=params)
            response.raise_for_status()  # Проверяем статус ответа
            return response.json()["items"]

        except requests.exceptions.HTTPError as error:
            raise ConnectionError(f"Не удалось получить доступ к сайту: {error}")


hh = HeadHunterAPI()
vacancies = hh.get_vacancies('3127')
print(len(vacancies))
for vacancy in vacancies:
    print(vacancy)
