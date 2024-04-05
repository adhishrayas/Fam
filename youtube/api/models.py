from django.db import models

# Create your models here.

class YouTubeVideos(models.Model):
    video_id = models.TextField(default="")
    video_title = models.TextField(default="")
    description = models.TextField(default="")
    publish_time = models.DateTimeField(default="")
    thumbnail_url = models.TextField(default="")
    channel_title = models.TextField(default="")

    def __str__(self):
        return self.video_title
    
    class Meta:
        #Adding an Index for quicker queries
        indexes= [ 
            models.Index(fields=['publish_time']),
            models.Index(fields=['video_title']),
        ]

#to keep track of the index
class KeyIndex(models.Model):
    key_index = models.IntegerField(default = 0)