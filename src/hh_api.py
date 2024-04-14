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
        self.__employers_dict = {'МегаФон': '3127',
                                 'МТС': '3776',
                                 'билайн': '4934',
                                 'СБЕР': '3529',
                                 'Банк ВТБ (ПАО)': '4181',
                                 'Тинькофф': '78638',
                                 'АШАН Ритейл Россия': '54979',
                                 '2ГИС': '64174',
                                 'Газпромбанк': '3388',
                                 'Ozon': '2180'}

    def get_request(self, employer_id):
        """
        Функция возвращает данные с сайта по id работодателя
        :param employer_id:
        :return: json object
        """
        try:
            params = {"per_page": 100,
                      "employer_id": employer_id,
                      "only_with_salary": True,
                      "only_with_vacancies": True}
            response = requests.get(self.__base_url, params=params)
            response.raise_for_status()  # Проверяем статус ответа
            return response.json()['items']

        except requests.exceptions.HTTPError as error:
            raise ConnectionError(f"Не удалось получить доступ к сайту: {error}")

    def list_company(self):
        """
        Получает список всех работодателей с указанием названия компании,
        названия вакансии и ссылки на вакансию
        """
        employer_list = []
        for employer in self.__employers_dict:
            employer_info = self.get_request(self.__employers_dict[employer])
            for info in employer_info:
                employer_list.append({'employer': employer,
                                      'url': info['employer']['alternate_url']})
        return employer_list

    def list_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию
        """
        vacancies_list = []
        for employer_id in self.__employers_dict:
            emp_vacancies = self.get_request(self.__employers_dict[employer_id])
            for vacancy in emp_vacancies:
                if vacancy['salary'] is None:
                    salary = 0

                elif vacancy['salary']['from'] is None:
                    salary = vacancy['salary']['to']

                elif vacancy['salary']['to'] is None:
                    salary = vacancy['salary']['from']
                else:
                    salary = (vacancy['salary']['from'] + vacancy['salary']['to']) / 2
                vacancies_list.append({'vacancy_name': vacancy['name'],
                                       'city': vacancy['area']['name'],
                                       'salary': salary,
                                       'currency': vacancy['salary']['currency'],
                                       'responsibility': vacancy['snippet']['responsibility'],
                                       'publish_date': vacancy['published_at'],
                                       'experience': vacancy['experience']['name'],
                                       'vacancy_url': vacancy['alternate_url'],
                                       'company_name': vacancy['employer']['name']})
        return vacancies_list

