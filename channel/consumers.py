import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("alerts", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("alerts", self.channel_name)

    async def receive(self, text_data):
        pass

    async def send_alert(self, event):
        alert = event['alert']
        await self.send(text_data=json.dumps({
            'alert': alert
        }))
