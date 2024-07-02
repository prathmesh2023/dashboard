from django.contrib import admin
from django.urls import path, include
from django.views import View
from api import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers




urlpatterns = [

  
    
    path('alert_types',views.alert_typesClassBassedView.as_view()),
    path('alert_types/<int:id>',views.alert_typesClassBassedView.as_view()),
    
    path('camera',views.cameraClassBassedView.as_view()),
    path('camera/<int:id>',views.cameraClassBassedView.as_view()),
    
    path('capture_video',views.capture_videoClassBassedView.as_view()),
    path('capture_video/<int:id>',views.capture_videoClassBassedView.as_view()),
    
    path('guard',views.guardClassBassedView.as_view()),
    path('guard/<int:id>',views.guardClassBassedView.as_view()),
    
    path('camera_alerts',views.camera_alertsClassBassedView.as_view()),
    path('camera_alerts/<int:id>',views.camera_alertsClassBassedView.as_view()),
    
    path('camera_settings',views.camera_settingsClassBassedView.as_view()),
    path('camera_settings/<int:id>',views.camera_settingsClassBassedView.as_view()),
    
    path('camera_alert_flag/alert_type_id=<int:alert_type_id>&camera_id=<int:camera_id>',views.camera_alert_flagClassBassedView.as_view()),
    
    
    

    
    
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 