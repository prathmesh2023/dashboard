from dataclasses import field
from statistics import mode
from rest_framework import serializers

from app1.models import alert_types,camera,capture_video,guard,camera_alerts,camera_settings


from django.contrib.auth.models import User



class alert_typeSerializer(serializers.ModelSerializer):
    class Meta:
        model = alert_types
        fields= "__all__"
        
        # exclude = ('password',)

class cameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = camera
        fields= "__all__"
        
        # exclude = ('password',)


class capture_videoSerializer(serializers.ModelSerializer):
    class Meta:
        model = capture_video
        fields= "__all__"
        
        # exclude = ('password',)


class guardSerializer(serializers.ModelSerializer):
    class Meta:
        model = guard
        fields= "__all__"
        
        # exclude = ('password',)
    
    
    
    
class camera_alertsSerializer(serializers.ModelSerializer):
    class Meta:
        model = camera_alerts
        fields= "__all__"
        
        # exclude = ('password',)
        
        
class camera_settingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = camera_settings
        fields= "__all__"
        
        # exclude = ('password',)
        

class camera_alert_flagSerializer(serializers.ModelSerializer):
    class Meta:
        model = camera_alerts
        fields= "__all__"
        
        # exclude = ('password',)