# your_app/models.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from app1.models import camera_alerts

@receiver(post_save, sender=camera_alerts)
def alert_handler(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "alerts",
            {
                "type": "send_alert",
                "alert": instance.alert_message,  # Adjust based on your model fields
            }
        )
