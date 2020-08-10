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

from django.contrib.auth.models import AnonymousUser

from channels.generic.websocket import JsonWebsocketConsumer
import json
from asgiref.sync import async_to_sync


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
        print(content.get("abcd"))
        # Send message to room group
        async_to_sync(self.send_json({'message': "message"}))
        # async_to_sync(self.channel_layer.group_send)(
        #     self.user_room_name,
        #     {
        #         "type": "notify",
        #         "content": "USER EDIT!!!",
        #     }
        # )


    def notify(self, event):
        print("nope")
        async_to_sync(self.send_json({'message': event.get("content")}))