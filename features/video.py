import datetime
import os
import isodate

from googleapiclient.discovery import build, HttpError


class GetEnv:

    @classmethod
    def get_service(cls):
        # перехват ключа из окружения, для работы с API
        api_key: str = os.getenv('API_YouTube')
        # специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class Video(GetEnv):

    def __init__(self, id):
        self.id = id
        # переменная для вызова метода класса с API
        youtube = self.get_service()
        # переменная для сбора статистики канала
        video = youtube.videos().list(id=self.id, part='snippet,statistics,contentDetails').execute()
        self.video_title = video["items"][0]["snippet"]["title"]
        self.video_views = video["items"][0]["statistics"]["viewCount"]
        self.video_likes = video["items"][0]["statistics"]["likeCount"]
        iso_8601_duration = video["items"][0]["contentDetails"]["duration"]
        self.duration = isodate.parse_duration(iso_8601_duration)
        self.video_url = 'https://youtu.be/' + id

    def __str__(self):
        return f"{self.video_title}"


class PLVideo(Video, GetEnv):

    def __init__(self, id, playlist_id):
        super().__init__(id)
        self.playlist_id = playlist_id
        self.playlist_title = self.get_playlist()

    def get_playlist(self):
        try:
            youtube = super().get_service()
            playlist = youtube.playlists().list(id=self.playlist_id,
                                                part='snippet,contentDetails, status'
                                                ).execute()
            return playlist['items'][0]['snippet']['title']
        except HttpError:
            raise Exception("Ошибка id плейлиста")

    def __str__(self):
        return f"{self.video_title} ({self.playlist_title})"


class PlayList(Video, GetEnv):

    def __init__(self, pl_id):
        """
        Инициализирует плейлист
        :param pl_id: id плейлиста
        """
        self.pl_id = pl_id
        playlist_title = self.get_pl_title(self.pl_id)
        self.pl_title = playlist_title['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + pl_id
        self.video_ids = self.get_data(self.pl_id)

    def __str__(self):
        return f"{self.pl_title} - {self.url}"

    @classmethod
    def get_pl_title(cls, pl_id):
        try:
            youtube = super().get_service()
            playlist_title = youtube.playlists().list(id=pl_id,
                                                      part='snippet,contentDetails, status'
                                                      ).execute()
            return playlist_title
        except HttpError:
            raise Exception("Ошибка id плейлиста")

    @classmethod
    def get_data(cls, pl_id):
        try:
            youtube = super().get_service()
            playlist_videos = youtube.playlistItems().list(playlistId=pl_id,
                                                           part='contentDetails',
                                                           maxResults=50,
                                                           ).execute()
            video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
            return video_ids
        except HttpError:
            raise Exception("Ошибка id плейлиста")

    def total_duration(self):
        total_duration = datetime.timedelta(seconds=0)
        for video in self.video_ids:
            total_duration += Video(video).duration
        return total_duration

    def show_best_video(self):
        max_video_likes = 1
        video_link = None
        for v in self.video_ids:
            if int(Video(v).video_likes) > int(max_video_likes):
                max_video_likes = Video(v).video_likes
                video_link = Video(v).video_url
            else:
                continue
        print(f"{video_link}")
        return f"{video_link}"
