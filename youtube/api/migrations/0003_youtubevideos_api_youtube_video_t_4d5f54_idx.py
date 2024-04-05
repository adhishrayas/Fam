# Generated by Django 5.0.4 on 2024-04-05 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_keyindex'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='youtubevideos',
            index=models.Index(fields=['video_title'], name='api_youtube_video_t_4d5f54_idx'),
        ),
    ]