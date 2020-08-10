import json
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.exceptions import StopConsumer
from .views import  DISCONNECTED_MSG

class StatusConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close()
        else:
            self.user_room_name = f'user-status-{str(self.user.id)}'
            await self.channel_layer.group_add(self.user_room_name, self.channel_name)
            await self.accept()

    async def receive_json(self, content, **kwargs):
        """
        This handles data sent over the wire from the client.
        """
        pass



    async def notify(self, event):
        if event.get("content") == DISCONNECTED_MSG:
            await self.disconnect({'message': event.get("content")})
        else:
            await self.send_json({'message': event.get("content")})
    
    async def disconnect(self, content):
        try:
            await self.channel_layer.group_discard(
                self.user_room_name,
                self.channel_name
            )
        except AttributeError:
            print(AttributeError.__str__)
        await self.close()
        raise StopConsumer()