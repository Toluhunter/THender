import json

from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import get_object_or_404
from django.http import Http404

from channels.generic.websocket import JsonWebsocketConsumer, WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Online, Transmission, Transfer


Account = get_user_model()


class TransmissionConfigConsumer(JsonWebsocketConsumer):

    # Group to broadcast messages
    groups = ["broadcast"]

    def toggle_online_status(self, status: bool):
        if status:
            # Add User to Online Table
            try:
                Online.objects.create(user=self.scope["user"])
            except IntegrityError:
                '''
                Set User To Offline. This Error is caught if a user recently connected
                and has not given enough time for their status to be changed to offline
                '''

                Online.objects.get(user=self.scope["user"]).delete()

                # Set User to anonymous to prevent trying to delete user before cleanup
                self.scope["user"] = AnonymousUser()
                self.websocket_disconnect({"code": 400})

            return

        # Removes User From Online Table once disconnected
        Online.objects.get(user=self.scope["user"]).delete()

    def connect(self):
        if self.scope["user"].is_anonymous:
            return self.websocket_disconnect({"code": 401})

        self.accept()

        self.toggle_online_status(True)
        async_to_sync(self.channel_layer.group_send)("broadcast", {
            "type": "broadcast_online",
        })

    def broadcast_online(self, event):
        '''
        Broadcast user id of peers online
        '''
        user = self.scope["user"]

        online = []
        for peer in user.peer.peers.all():
            if peer.is_online:
                online.append(str(peer.id))

        peers_online = {
            "peers_online": online
        }

        self.send_json(peers_online)

    def disconnect(self, code):
        if not self.scope["user"].is_anonymous:
            self.toggle_online_status(False)

        return self.close()


class TransferDataConsumer(WebsocketConsumer):

    def connect(self):

        # Enforce user authentication
        if self.scope["user"].is_anonymous:
            self.close()

        # Accept connection
        self.accept()

        # retrieve transmission id from url path
        transmission_id = self.scope["url_route"]["kwargs"]["id"]

        try:
            '''
            If transmission id exists get obj, if no disconnect
            '''
            self.transmission = get_object_or_404(Transmission, id=transmission_id)
            if not self.transmission.accepted:
                raise Http404

        except Http404:
            return self.close()

        try:
            '''
            Get instance of transfer which is used for only currently active connections
            '''
            self.transfer = Transfer.objects.get(id=self.transmission)
        except Transfer.DoesNotExist:
            self.transfer = Transfer.objects.create(id=self.transmission)

    def receive(self, text_data=None, bytes_data=None):
        if text_data:
            if text_data == "recieved":
                self.transmission.bytes_sent += (100 * (1024 * 1024))
                self.transmission.save()
                return

            elif text_data == "Done":
                self.disconnect(200)
                return

            elif text_data == "connected":
                # If user is sender or reciever set on transfer instance else disconnect unknown user
                if self.transmission.sender == self.scope["user"]:
                    self.transfer.sender = self.scope["user"]
                elif self.transmission.reciever == self.scope["user"]:
                    self.transfer.reciever = self.scope["user"]
                else:
                    return self.close()

                # Save transfer instance
                self.transfer.save()

                # add two users to unique group names after transmission id
                group_name = str(self.transmission.id)
                async_to_sync(self.channel_layer.group_add)(
                    group_name, self.channel_name)
                if group_name not in self.groups:
                    # Append for group for cleanup on disconnection
                    self.groups.append(group_name)

                print(f"Sender = {self.transfer.sender}")
                print(f"Reciever = {self.transfer.reciever}")
                if self.transfer.sender and self.transfer.reciever:
                    fields = {
                        "total_size": self.transmission.total_size,
                        "file_hash": self.transmission.file_hash,
                        "file_location": self.transmission.file_location,
                        "bytes_sent": self.transmission.bytes_sent
                    }
                    async_to_sync(self.channel_layer.group_send)(self.groups[0], {
                        "type": "send_transmssion_details", "data": fields})
                return

            else:
                bytes_data = text_data.encode()

        if bool(self.transfer.sender) ^ bool(self.transfer.reciever):
            print(not (bool(self.transfer.sender) ^ bool(self.transfer.reciever)))
            print(f"Sender = {self.transfer.sender}")
            print(f"Reciever = {self.transfer.reciever}")
            self.send("You Are The Only One Ready, Please Contact Second Party")
            return

        async_to_sync(self.channel_layer.group_send)(self.groups[0], {
            "type": "forward_bytes", "data": bytes_data})

    def forward_bytes(self, event):
        if self.scope["user"] == self.transmission.reciever:
            self.send(bytes_data=event["data"])

    def send_transmssion_details(self, event):

        # Retreve the updated transfer instance to prevent race condition
        self.transfer = Transfer.objects.get(id=self.transmission)

        event["data"]["type"] = "recieve"
        if self.scope["user"] == self.transmission.sender:

            event["data"]["type"] = "send"
            data = json.dumps(event["data"])
            self.send(data)
            return

        data = json.dumps(event["data"])
        self.send(data)

    def disconnect(self, code):
        if self.scope["user"].is_anonymous:
            return self.close()

        try:
            '''
            If Transmission ID was invalid capture the error
            '''
            if self.groups:
                '''
                If User has been admitted to the group
                '''
                async_to_sync(self.channel_layer.group_send)(self.groups[0], {
                    "type": "disconnect_peer", "code": code, "channel_name": self.channel_name})
                self.transfer.sender = None

                self.transfer.reciever = None

                self.transfer.save()

        except AttributeError:
            pass

        return self.close()

    def disconnect_peer(self, event):
        if event["channel_name"] != self.channel_name:
            print("here")
            self.scope["user"] = AnonymousUser()
            return super().websocket_disconnect(event)
