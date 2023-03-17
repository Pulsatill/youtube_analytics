import os

from googleapiclient.discovery import build, HttpError


class Video:

    def __init__(self, id):
        self.id = id
        # переменная для вызова метода класса с API
        youtube = self.get_service()
        # переменная для сбора статистики канала
        video = youtube.videos().list(id=self.id, part='snippet,statistics').execute()
        self.video_title = video["items"][0]["snippet"]["title"]
        self.video_views = video["items"][0]["statistics"]["viewCount"]
        self.video_likes = video["items"][0]["statistics"]["likeCount"]

    @classmethod
    def get_service(cls):
        # перехват ключа из окружения, для работы с API
        api_key: str = os.getenv('API_YouTube')
        # специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video):

    def __init__(self, id, playlist_id):
        super().__init__(id)
        self.playlist_id = playlist_id
        self.playlist_title = self.get_playlist()

    def get_playlist(self):
        try:
            youtube = super().get_service()
            playlist = youtube.playlists().list(id=self.playlist_id, part='snippet,contentDetails, status').execute()
            return playlist['items'][0]['snippet']['title']
        except HttpError:
            raise Exception("Ошибка id плейлиста")

    def __str__(self):
        return f"{self.video_title} ({self.playlist_title})"


video1 = Video('9lO06Zxhu88')
video2 = PLVideo('BBotskuyw_M', 'PL7Ntiz7eTKwrqmApjln9u4ItzhDLRtPuD')
print(video1.video_views)
print(video1.video_likes)
print(video2.video_views)
print(video2.video_likes)
