from django.db import models

# Create your models here.

class YtData:
    id = int
    video_title = str
    date = str
    thumbnails = str
    views = int
    likes = int
    comments = int
    duration = int
    video_link = int