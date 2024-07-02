from django.contrib import admin
from django.urls import path, include
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

# router = routers.DefaultRouter()
# router.register(r'testing', views.TestingViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("cctv/<int:id>", views.cctv,name="cctv"),
    
    
    path("action_chart/<int:alert_id>/<int:id>", views.action_chart,name="action_chart"),
    path("obj_detection/<int:id>", views.obj_detection,name="obj_detection"),
    path("obj_tracking/<int:id>", views.obj_tracking,name="obj_tracking"),
    path("ai_bot/<int:id>", views.ai_bot,name="ai_bot"),
    
    
    path("obj_testing", views.obj_testing,name="obj_testing"),
    
    
  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 