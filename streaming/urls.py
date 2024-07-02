from django.contrib import admin
from django.urls import path, include
from django.views import View
from . import views
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [

    path("video_feed/<int:id>/", views.video_feed, name="video_feed"),
  
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 