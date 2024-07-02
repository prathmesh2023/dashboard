from django.shortcuts import render,HttpResponse

# Create your views here.

from django.http import StreamingHttpResponse
from django.views.decorators import gzip

from datetime import datetime




from django.templatetags.static import static

from .models import camera_alerts,camera


def index(request):
    cameras = camera.objects.all().order_by("-id")
    
    data = {
        "cameras":cameras
    }
    
    return render(request, "index.html",data)

def cctv(request,id):
    id=id
    data ={
        "id":id
    }

    return render(request, "cctv.html",data)

def action_chart(request,alert_id,id):
    
    data = {
        "id":id,
        "alert_id":alert_id,
    }
    return render(request, "action_chart.html",data)

def obj_detection(request,id):
    id=id
    data = {
        "id":id,
    }
    return render(request, "object_detection.html",data)

def obj_tracking(request,id):
    id = id
    data = {
        "id":id
    }
    return render(request, "object_tracking.html",data)

def ai_bot(request,id):
    id = id
    
    data = {
        "id":id,
    }
    
    return render(request, "ai_bot.html",data)

def obj_testing(request):
    alerts = camera_alerts.objects.all().order_by('-date_time')
    data = {
        'alerts':alerts
    }
    return render(request, "test.html",data)
    
