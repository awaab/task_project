# from django.contrib.auth.models import AnonymousUser

# from channels.generic.websocket import AsyncJsonWebsocketConsumer
# import json


# class StatusConsumer(AsyncJsonWebsocketConsumer):
#     async def connect(self):
#         self.user = self.scope["user"]
#         print(self.user,"*****")
#         if not self.user.is_authenticated:
#             await self.close()
#         else:
#             self.user_room_name = f'user-status-{str(self.user.id)}'
#             await self.channel_layer.group_add(self.user_room_name, self.channel_name)
#             print("################")
#             self.accept()

#     async def receive_json(self, content, **kwargs):
#         """
#         This handles data sent over the wire from the client.
#         """


#         # Send message to room group
#         await self.channel_layer.group_send(
#             self.user_room_name,
#             {
#                 'message': "message"
#             }
#         )
        


#     async def notify(self, event):
#         await self.send_json(event["content"])
import json
from django.contrib.auth.models import AnonymousUser
from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from .views import  DISCONNECTED_MSG

class StatusConsumer(JsonWebsocketConsumer):
    def connect(self):
        self.user = self.scope["user"]
        print(self.user,"*****")
        if not self.user.is_authenticated:
            self.close()
        else:
            self.user_room_name = f'user-status-{str(self.user.id)}'
            async_to_sync(self.channel_layer.group_add)(self.user_room_name, self.channel_name)
            self.accept()
            print("################")

    def receive_json(self, content, **kwargs):
        """
        This handles data sent over the wire from the client.
        """
        pass



    def notify(self, event):
        if event.get("content") == DISCONNECTED_MSG:
            self.disconnect({'message': event.get("content")})
        else:
            async_to_sync(self.send_json({'message': event.get("content")}))
    
    def disconnect(self, content):
        try:
            async_to_sync(self.channel_layer.group_discard)(
                self.user_room_name,
                self.channel_name
            )
        except AttributeError:
            print(AttributeError.__str__)
        raise StopConsumer()