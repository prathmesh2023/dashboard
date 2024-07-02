from django.db import models
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# Create your models here.
class alert_types(models.Model):
    alert_type_id = models.AutoField(primary_key=True)
    alert_name = models.CharField(max_length=50)
 
    status =  models.IntegerField()
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
 
    def __str__(self):
        return str(self.alert_name)
    

class guard(models.Model):
    name = models.CharField(max_length=50)
    mobile = models.IntegerField()
    area = models.CharField(max_length=255)
    
    def __str__(self):
        return str(self.name)
    
    
class camera(models.Model):
    ip_address = models.CharField(max_length=255)
    camera_name = models.CharField(blank=True, null=True,  max_length=100)
    guard_id = models.ForeignKey(guard, on_delete=models.CASCADE)
    area_id = models.IntegerField()
    tank_name = models.CharField(default="", max_length=255)
    
    def __str__(self):
        return str(self.camera_name)
    
    
   
    
class capture_video(models.Model):
    captured_video_id = models.AutoField(primary_key=True)
    camera_id = models.ForeignKey(camera, on_delete=models.CASCADE)
    
    date_time = models.DateTimeField(auto_now=True)
    url = models.FileField(upload_to="video", max_length=100)
    
    def __str__(self):
        return str(self.camera_id)
    


    
class camera_alerts(models.Model):
    alert_id = models.AutoField(primary_key=True)
    camera_id = models.CharField( max_length=50)
    alert_type = models.CharField( max_length=50)
    status = models.CharField( max_length=50)
    date_time = models.DateTimeField(auto_now=True)
    # time = models.TimeField(auto_now=False)
    
    
    def __str__(self):
        return str(self.alert_id)
   
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     alert_type_name = "face" if self.alert_type_id == 1 else "motion" if self.alert_type_id == 2 else "unknown"
    #     channel_layer = get_channel_layer()
    #     async_to_sync(channel_layer.group_send)(
    #         "alerts",
    #         {
    #             "type": "send_alert",
    #             "alert": {
    #                 'id': self.alert_id,
    #                 'camera_id': self.camera_id_id,
    #                 'alert_type': alert_type_name,
    #                 'date_time': self.date_time.strftime("%Y-%m-%d %H:%M:%S"),
    #             },
    #         }
    #     )

    
class camera_settings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    camera_id = models.ForeignKey(camera, on_delete=models.CASCADE)
    alert_id = models.ForeignKey(alert_types, on_delete=models.CASCADE)
    date_time = models.DateField(auto_now=True)
    
    def __str__(self):
        return str(self.setting_id)