from channels.generic.websocket import JsonWebsocketConsumer
from asgiref.sync import async_to_sync


class TransferConsumer(JsonWebsocketConsumer):

    def connect(self):

        group = self.scope['url_route']['kwargs']['group']
        self.group_name = f'{group}-group'

        async_to_sync(self.channel_layer.group_add)(
            self.group_name, self.channel_name)
        self.accept()
        self.send(text_data=self.scope["user"].username)

    def receive_json(self, text_data=None, bytes_data=None):
        async_to_sync(self.channel_layer.group_send)(
            self.group_name, {"type": "message", "message": text_data})

    def message(self, event):
        self.send(text_data=event["message"])

    def disconnect(self, code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name, self.channel_layer)
        return super().disconnect(code)
