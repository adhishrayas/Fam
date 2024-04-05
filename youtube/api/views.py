from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views import View
from .tasks import test_func
from .models import YouTubeVideos
from django.core.paginator import Paginator, Page
from datetime import datetime
from django.utils import timezone as tz
# Create your views here.
#for testing
def test(request):
    test_func.delay()
    return HttpResponse("Done")


#Generic function to paginate and render data
def paginate_and_render(request,data_list):
    per_page = 15 #15 videos per page
    paginator = Paginator(data_list, per_page) #Make the Paginator
    page_number = request.GET.get('page', 1) #Get the required page, or default to the first one
    page_obj = paginator.get_page(page_number) #Get the required Page
    return render(request,'frontend.html',{'page_obj':page_obj})# Render the page

#View to Display Data
class GetVideosView(View):

    def get(self,request):
        arrangement = request.GET.get('ar')#Arrange data according to the sort
        start_datetime_str = request.GET.get('start_datetime')#Fetch Start date
        end_datetime_str = request.GET.get('end_datetime')#Fetch End Date

        #convert to correct format for querying
        if start_datetime_str:
           start_datetime = tz.make_aware(datetime.strptime(start_datetime_str, '%Y-%m-%dT%H:%M'))
        else:
           start_datetime = None
           
        if end_datetime_str:
           end_datetime = tz.make_aware(datetime.strptime(end_datetime_str, '%Y-%m-%dT%H:%M'))
        else:
           end_datetime = None
        queryset = YouTubeVideos.objects.all()

        if start_datetime: #Get all Videos published after the given start date
           video_list = queryset.filter(publish_time__gte=start_datetime)
        if end_datetime:#Get all Videos published before the given date
           video_list = queryset.filter(publish_time__lte=end_datetime)
        
        if start_datetime or end_datetime:
              return paginate_and_render(request,video_list)
        #Arrange on given sorting criteria
        if arrangement is None or arrangement=="publish_time":
           video_list = queryset.order_by("-publish_time")
        elif arrangement == "publish_timeasc":
           video_list = queryset.order_by("publish_time")
        elif arrangement =="video_title":
           video_list = queryset.order_by("video_title")
        else:
            video_list = queryset.order_by("-video_title")
        return paginate_and_render(request,video_list)
    

class SearchVideosView(View):
    
    def get(self,request):
        return render(request,'search_frontend.html')

    def post(self,request):
        query = request.POST.get('q')#Check for Search Query
        if query is not None:
            queries = YouTubeVideos.objects.filter(video_title__icontains = query).values('video_title','description','publish_time','thumbnail_url','channel_title')#Filtering on based of queried title
            video_list = [dict(query) for query in queries] #Making a list of dictionaries to be consumed by the javascript
            return JsonResponse({"videos":video_list}) #Return Json for the Javascript to render
        else:
            return JsonResponse({})#Return Empty Response if query empty 



