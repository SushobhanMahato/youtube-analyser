from email.mime import image
from mailbox import MaildirMessage
from pyexpat.errors import messages
from django.shortcuts import render, redirect
#from urllib3 import HTTPResponse
from django.http import HttpResponse
from .yt_stats import YTstats
from django.contrib import messages
import json
import requests
from tinydb import TinyDB
from .models import YtData
# Create your views here.

db = TinyDB('db.json')

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def generate(request):
    channel_id = request.POST['string1']
    API_KEY = 'AIzaSyCYWVcFzw2b5AYYvZHFUvxaU7hG-WjWvc4'
    url = f'https://www.googleapis.com/youtube/v3/channels?&id={channel_id}&key=AIzaSyCYWVcFzw2b5AYYvZHFUvxaU7hG-WjWvc4'
    json_url = requests.get(url)
    data = json.loads(json_url.text)
    if data['pageInfo']['totalResults']==0:
        messages.info(request, 'Invalid channel ID')
        return redirect('home')
    yt = YTstats(API_KEY, channel_id)
    db.truncate()
    db.insert({'channel':channel_id})
    yt.get_channel_statistics()
    text = yt.channel_statistics
    channel_name = text['items'][0]['snippet']['title']
   #json.dumps(channel_name)
    channel_name = channel_name[:len(channel_name)]
    channel_logo = text['items'][0]['snippet']['thumbnails']['default']['url']
    channel_descp = text['items'][0]['snippet']['description']
   # channel_descp = channel_descp[:len(channel_descp)]
    if "subscriberCount" in text['items'][0]['statistics']:
        total_subs = text['items'][0]['statistics']['subscriberCount']
    else:
        total_subs = 0
    total_views = text['items'][0]['statistics']['viewCount']
    total_videos = text['items'][0]['statistics']['videoCount']
    return render(request, "home.html", {'s1':channel_name, 'link':channel_logo, 'desc':channel_descp, 'subs':total_subs, 'views':total_views, 'videos':total_videos, 'id':channel_id})

def videos(request):
    yt1 = db.all()
    channel_id = yt1[0]['channel']
    API_KEY = 'AIzaSyCYWVcFzw2b5AYYvZHFUvxaU7hG-WjWvc4'
    yt = YTstats(API_KEY, channel_id)
    yt.get_channel_video_data()
    text = yt.video_data
    ids = yt.video_ids
    all_data = []
    for id in ids:
        gg = YtData()
        gg.video_title = text[id]['title']
        gg.date = text[id]['publishedAt']
        gg.thumbnails = text[id]['thumbnails']['default']['url']
        gg.views = text[id]['viewCount']
        if "likeCount" in text[id]:
            gg.likes = text[id]['likeCount']
        else:
            gg.likes = None
        if "commentCount" in text[id]:
            gg.comments = text[id]['commentCount']
        else:
            gg.comments = None
        gg.duration = text[id]['duration']
        gg.video_link = "https://www.youtube.com/watch?v="+id
        all_data.append(gg)
    return render(request, "videos.html", {'all_videos':all_data})


