import os
from googleapiclient.discovery import build


class Video():
    """
    класс для видео
    """

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_video):
        """
        Экземпляр инициализируется по id видео. Дальше все данные будут подтягиваться по API
        """
        self.id_video = id_video
        video_response = self.youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=id_video
                                               ).execute()
        self.title = video_response['items'][0]['snippet']['title']
        self.link = f'https://www.youtube.com/watch?v={self.id_video}'
        self.viewCount = video_response['items'][0]['statistics']['viewCount']
        self.likeCount = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        """
        магический метод для отображения информации об объекте класса для пользователей
        """
        return f"{self.title}"


class PLVideo(Video):
    """
    класс для плейлиста
    """

    def __init__(self, id_video, id_playlist):
        """
        Экземпляр инициализируется по id видео из класса Video и id плейлиста
        """
        super().__init__(id_video)
        self.id_playlist = id_playlist
