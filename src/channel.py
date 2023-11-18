import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.channel = self.youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        self.title = self.channel['items'][0]['snippet']['title']
        self.description = self.channel['items'][0]['snippet']['description']
        self.url = f'https://www.youtube.com/channel/{self.channel_id}'
        self.subscriberCount = self.channel['items'][0]['statistics']['subscriberCount']
        self.video_count = self.channel['items'][0]['statistics']['videoCount']
        self.viewCount = self.channel['items'][0]['statistics']['viewCount']

    def __str__(self):
        """
        магический метод для отображения информации об объекте класса для пользователей
        """
        return f"{self.title} ({self.url})"

    def __add__(self, other):
        """
        магический метод для сложений подписчиков разных экземпляров класса
        """
        return int(self.subscriberCount) + int(other.subscriberCount)

    def __sub__(self, other):
        """
        магический метод для вычитания подписчиков разных экземпляров класса
        """
        return int(self.subscriberCount) - int(other.subscriberCount)

    def __gt__(self, other):
        """
        магический метод сравнивающий, что подписчиков первого указанного экземпляра класса больше чем второго
        """
        return int(self.subscriberCount) > int(other.subscriberCount)

    def __ge__(self, other):
        """
        магический метод сравнивающий, что подписчиков первого указанного экземпляра класса больше или равно чем второго
        """
        return int(self.subscriberCount) >= int(other.subscriberCount)

    def __lt__(self, other):
        """
        магический метод сравнивающий, что подписчиков первого указанного экземпляра класса меньше чем второго
        """
        return int(self.subscriberCount) < int(other.subscriberCount)

    def __le__(self, other):
        """
        магический метод сравнивающий, что подписчиков первого указанного экземпляра класса меньше или равно чем второго
        """
        return int(self.subscriberCount) <= int(other.subscriberCount)

    def __eq__(self, other):
        """
        магический метод сравнивающий, что подписчиков первого указанного экземпляра класса равно второму
        """
        return int(self.subscriberCount) == int(other.subscriberCount)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(channel))

    @classmethod
    def get_service(cls):
        """
        класс метод возвращающий объект для работы с YouTube API
        """
        return cls.youtube

    def to_json(self, file_name):
        """
        метод сохраняющий в файл значения атрибутов экземпляра Channel
        """
        channel_info = {
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriberCount": self.subscriberCount,
            "video_count": self.video_count,
            "viewCount": self.viewCount
        }

        with open(file_name, 'w', encoding='utf-8') as file:
            json.dump(channel_info, file, ensure_ascii=False, indent=4)
