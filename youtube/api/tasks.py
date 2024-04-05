from celery import shared_task
from django.db import transaction
from datetime import datetime,timedelta,timezone
from django.conf import settings
from googleapiclient.discovery import build
from .models import YouTubeVideos,KeyIndex

api_keys = settings.YOUTUBE_API_KEYS

#function to get the current active key
def get_current_key():

    index = KeyIndex.objects.all()
    if index.exists():
       idx = index.first()
       return api_keys[idx.key_index]
    else:
       obj = KeyIndex.objects.create(key_index=0)
       return api_keys[obj.key_index]

#funtion to shift to the next key if current key is exhausted
def next_key():
   idx = KeyIndex.objects.all().first()
   idx.key_index = (idx.key_index + 1)%len(api_keys)



@shared_task(bind = True)
def test_func(self):
    for i in range(10):
        print(i)
    return "Done"



@transaction.atomic
def create_youtube_videos(video_data):
    YouTubeVideos.objects.bulk_create([
        YouTubeVideos(**data) for data in video_data
    ])

#main function
@shared_task(bind = True)
def search_youtube(*args, **kwargs):
    try:
           api_key =get_current_key()#Fetch the Currently Active Key
           client = build('youtube','v3',developerKey = api_key) #Building the client object
           now_utc = datetime.now(timezone.utc)

           # Subtract 10 seconds from the current time
           ten_seconds_ago = now_utc - timedelta(seconds=10)

#          Format the publishedAfter parameter
           published_after = (ten_seconds_ago - timedelta(hours=10)).isoformat(timespec='seconds')
           youtube_response = client.search().list(
               q='football',  #Search keyword (Manchester United all the way!!)
               part='snippet', #Snippet is the only required part for saving into the DB
               type='video',
               order='date',
               publishedAfter=published_after
            ).execute() #Make the request and get the response
           video_data = []
           for video in youtube_response.get('items', []):
                data = {} #Get the object data
                data["video_id"] = video['id']['videoId']
                data["video_title"] = video['snippet']['title']
                data["description"] = video['snippet']['description']
                data["publish_time"] = video['snippet']['publishedAt']
                data["thumbnail_url"] = video['snippet']['thumbnails']['default']['url']
                data["channel_title"] = video['snippet']['channelTitle']
                video_data.append(data)
           create_youtube_videos(video_data)
           print("haha")
           return "hehe"
    except:
        next_key()