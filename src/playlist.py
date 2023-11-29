import os
import datetime

import isodate
from googleapiclient.discovery import build


class PlayList:
    """
    Класс для представления плейлиста, который инициализируется по id плейлиста
    """
    api_key: str = os.getenv('YT_API_KEY')
    youtube = build('youtube', 'v3', developerKey=api_key)

    def __init__(self, id_playlist):
        """
        инициация класса
        """
        self.id_playlist = id_playlist
        playlists = self.youtube.playlists().list(id=self.id_playlist,
                                             part='contentDetails,snippet',
                                             maxResults=50,
                                             ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.id_playlist}'

        playlist_videos = self.youtube.playlistItems().list(playlistId=self.id_playlist,
                                                            part='contentDetails',
                                                            maxResults=50,
                                                            ).execute()

        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        self.video_response = self.youtube.videos().list(part='contentDetails,statistics',
                                                    id=','.join(video_ids)
                                                    ).execute()

    @property
    def total_duration(self):
        """
        метод, как атрибут для отображения общей длительности плейлиста
        """

        total_time = datetime.timedelta(0)
        for video in self.video_response['items']:

            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_time += duration
        return total_time

    def show_best_video(self):
        """
        метод для возврата ссылки на лучшее видео из плейлиста
        """

        for video in self.video_response['items']:
            like = 0
            video_id = ''
            if like < int(video['statistics']['likeCount']):
                like = int(video['statistics']['likeCount'])
                video_id = video['id']
        return f'https://youtu.be/{video_id}'
