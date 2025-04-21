# server/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_string = self.scope['query_string'].decode()
        username = None
        for param in query_string.split('&'):
            if param.startswith('username='):
                username = param.split('=')[1]
                break

        if not username:
            await self.close()
            return

        try:
            self.user = await self.get_user(username)
        except Exception:
            await self.close()
            return

        self.other_username = self.scope['url_route']['kwargs']['other_username']

        if not await self.are_friends():
            await self.close()
            return

        self.room_name = '_'.join(sorted([self.user.username, self.other_username]))
        self.room_group_name = f'chat_{self.room_name}'

        self.chat = await self.get_or_create_chat()

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'room_group_name') and hasattr(self, 'channel_name'):
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.save_message(message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
                'timestamp': str(await self.get_current_timestamp())
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            'timestamp': event['timestamp']
        }))

    @database_sync_to_async
    def get_user(self, username):
        from server.models import User
        return User.objects.get(username=username)

    @database_sync_to_async
    def are_friends(self):
        from server.models import User, Friendship
        try:
            other_user = User.objects.get(username=self.other_username)
            return Friendship.objects.filter(user=self.user, friend=other_user).exists()
        except User.DoesNotExist:
            return False

    @database_sync_to_async
    def get_or_create_chat(self):
        from server.models import User, Chat
        other_user = User.objects.get(username=self.other_username)
        chat = Chat.objects.filter(participants=self.user).filter(participants=other_user).first()
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(self.user, other_user)
        return chat

    @database_sync_to_async
    def save_message(self, content):
        from server.models import Message
        Message.objects.create(
            chat=self.chat,
            sender=self.user,
            content=content
        )

    @database_sync_to_async
    def get_current_timestamp(self):
        from django.utils import timezone
        return timezone.now()