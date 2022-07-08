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
# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

yt = None
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
    yt.get_channel_statistics()
    text = yt.channel_statistics
    channel_name = text['items'][0]['snippet']['title']
    json.dumps(channel_name)
    channel_name = channel_name[:len(channel_name)]
    channel_logo = text['items'][0]['snippet']['thumbnails']['default']['url']
    channel_descp = text['items'][0]['snippet']['description']
   # channel_descp = channel_descp[:len(channel_descp)]
    total_subs = text['items'][0]['statistics']['subscriberCount']
    total_views = text['items'][0]['statistics']['viewCount']
    total_videos = text['items'][0]['statistics']['videoCount']
    return render(request, "home.html", {'s1':channel_name, 'link':channel_logo, 'desc':channel_descp, 'subs':total_subs, 'views':total_views, 'videos':total_videos})

def videos(requests):
    yt.get_channel_video_data()
    text = yt.video_data
    