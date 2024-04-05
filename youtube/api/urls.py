from django.urls import path
from .views import *
urlpatterns = [
    path("test/",test,name="test"), #Test View
    path("",GetVideosView.as_view(),name="home"), #Get Latest Videos
    path("search/",SearchVideosView.as_view(),name="search")# Search Stored Videos
]
