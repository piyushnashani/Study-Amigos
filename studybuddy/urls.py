
from django.contrib import admin
from django.urls import path, include 
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from studybuddy.settings import MEDIA_ROOT

##def home(request):
##    return HttpResponse("Home Page")

urlpatterns = [
    ##path('', home),                  # Example of url calling function
    path('admin/', admin.site.urls), 
    path('', include('base.urls')),     ##Linking the base urls file with our main router url file   
    path('api/', include('base.api.urls')),          ## to let our django know and how we can reach to the APIs

]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
