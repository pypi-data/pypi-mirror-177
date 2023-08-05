import requests
from requests_ntlm import HttpNtlmAuth
import os
import warnings

warnings.filterwarnings("ignore")

class SharePoint:
    def __init__(self, username, password):
        self.auth = HttpNtlmAuth(username, password)
        self.headers = {'Accept': 'application/json;odata=verbose'}

    def __make_request(self, request_url):
        """
        Создает запрос на сервер с учетными данными
        :param request_url: string
        :return: Response
        """
        return requests.get(request_url, verify=False, auth=self.auth, headers=self.headers)

    def get_request_json(self, request_url):
        """
        Создает запрос на сервер, возращает ответ в виде json
        :param request_url: string
        :return: json
        """
        return self.__make_request(request_url).json()

    @staticmethod
    def get_data_from_lists_type(response_json):
        """
        Получение доступных страниц для типа List SharePoint
        Возвращает список вида
        [
            {
                "title": Title,
                "link" : "Lists(guid'9c095153-274d-4c73-9b8b-4e3dd6af89e5')/Items(16)"
            }
        ]
        :param response_json: json result of get_request_json()
        :return: []
        """
        name_url_list = []
        for k in response_json['d']['results']:
            name_url_list.append({'title': k['Title'], 'link': k['__metadata']['id']})
        return name_url_list

    @staticmethod
    def get_data_from_attachment_files_type(response_json):
        """
        Получение доступных файлов на страние
        Возвращает список вида
        [
            {
                "FileName": FileName,
                "ServerRelativeUrl" : "/Lists/2014/Attachments/16/01_преп_текущие_01.09-11.09.xlsx"
            }
        ]
        :param response_json: json result of get_request_json()
        :return: []
        """
        name_url_list = []
        for k in response_json['d']['results']:
            name_url_list.append({'FileName': k['FileName'], 'ServerRelativeUrl': k['ServerRelativeUrl']})
        return name_url_list

    def save_file_by_url(self, api_url_with_web, server_relative_url, file_name, to_path=''):
        """
        Сохранение файла по его ServerRelativeUrl
        :param server_relative_url: ServerRelativeUrl ex.
        :param api_url_with_web: ex. https://portal.petrocollege.ru/_api/web/
        :param file_name: FileName
        :param to_path: path to save
        :return:
        """
        if not os.path.exists(to_path):
            os.makedirs(to_path)
        full_path = to_path + "/" + file_name
        response = self.__make_request(
            api_url_with_web + "/GetFileByServerRelativeUrl('" + server_relative_url + "')/$value")
        open(full_path, 'wb').write(response.content)
        print("File " + file_name + " added to path " + to_path)
        return os.path.isfile(full_path)
