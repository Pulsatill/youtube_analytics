import os
import json

from googleapiclient.discovery import build

# перехват ключа из окружения, для работы с API
api_key: str = os.getenv('API_YouTube')

# специальный объект для работы с API
youtube = build('youtube', 'v3', developerKey=api_key)


# класс YouTube, который позволяет узнать название канала, автора и другую информацию о канале
class YouTube:

    def __init__(self, id):
        self.id = id
        self.title = None
        self.description = None
        self.country = None
        self.custom_url = None

    def print_info(self):
        """

        :return: возвращает информацию о канале в формате json
        и выводит на экран эту информацию
        """
        json_info = []
        channel = youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        channel_information = json.dumps(channel, indent=2, ensure_ascii=False)
        json_info.append(channel_information)
        print(channel_information)

        return json_info

    def channel_title(self, json_info=None):
        """
        :param json_info: извлекается с помощью модуля print_info()
        :return: извлекает объявленные атрибуты класса
        """
        if json_info is None:
            json_info = self.print_info()
        for i in json_info:
            self.title = i.get("title")
            self.description = i.get("description")
            self.country = i.get("country")
            self.custom_url = i.get("customUrl")
        return self.title, self.description, self.country, self.custom_url
