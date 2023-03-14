import os
import json

from googleapiclient.discovery import build


# класс YouTube, который позволяет узнать название канала, автора и другую информацию о канале
class YouTube:

    def __init__(self, id):
        self.__id = id
        # переменная для вызова метода класса с API
        youtube = self.get_service()
        # переменная для сбора статистики канала
        channel = youtube.channels().list(id=self.id, part='snippet,statistics').execute()
        # атрибуты экземпляра инициализируются через полученую переменную
        self.title = channel["items"][0]["snippet"]["title"]
        self.description = channel["items"][0]["snippet"]["description"]
        self.country = channel["items"][0]["snippet"]["country"]
        self.subs_count = channel["items"][0]["statistics"]["subscriberCount"]
        self.video_count = channel["items"][0]["statistics"]["videoCount"]
        self.view_count = channel["items"][0]["statistics"]["viewCount"]
        self.custom_url = 'https://www.youtube.com/' + channel["items"][0]["snippet"]["customUrl"]

    @property
    def id(self):
        return self.__id

    @classmethod
    def get_service(cls):
        # перехват ключа из окружения, для работы с API
        api_key: str = os.getenv('API_YouTube')
        # специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def to_json(self):
        data = {"title": self.title,
                "id": self.id,
                "description": self.description,
                "country": self.country,
                "Url": self.custom_url,
                "video count": self.video_count,
                "view count": self.view_count,
                "subscribers count": self.subs_count}
        file_name = self.id
        with open(f"{file_name}.json", "w", encoding="UTF-8") as file:
            json.dump(data, file, indent=2, ensure_ascii=False)
        return print(f"Файл {self.title} создан")

    def __str__(self) -> str:
        return f"Youtube-канал: {self.title}"

    def __add__(self, other) -> int:
        return self.subs_count + other.subs_count

    def __lt__(self, other):
        return self.subs_count < other.subs_count

    def __gt__(self, other):
        return self.subs_count > other.subs_count
