from django.contrib import admin

# Register your models here.

from app1.models import alert_types,camera,capture_video,guard,camera_alerts,camera_settings

admin.site.register(alert_types)
admin.site.register(camera)
admin.site.register(capture_video)
admin.site.register(guard)
admin.site.register(camera_alerts)
admin.site.register(camera_settings)
