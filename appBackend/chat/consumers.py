import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from users.models import CustomUser
from .models import Conversation, Message
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            await self.accept()
            await self.set_user_online(self.user.id)
            await self.channel_layer.group_add("online_users", self.channel_name)
            await self.channel_layer.group_send(
                "online_users",
                {
                    "type": "user_online",
                    "user_id": self.user.id,
                    "username": self.user.username,
                }
            )

    async def disconnect(self, close_code):
        await self.set_user_offline(self.user.id)
        await self.channel_layer.group_send(
            "online_users",
            {
                "type": "user_offline",
                "user_id": self.user.id,
                "username": self.user.username,
            }
        )
        await self.channel_layer.group_discard("online_users", self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message')
        to_user_id = data.get('to')

        # Validate to_user_id before processing
        if not to_user_id:
            return

        conversation = await self.get_conversation(self.user.id, to_user_id)
        saved_message = await self.create_message(conversation, self.user, message)

        message_data = {
            'id': str(saved_message.id),  # Ensure ID is string
            'sender': self.user.username,
            'content': saved_message.content,
            'timestamp': saved_message.timestamp.isoformat(),
        }

        # Notify both users
        await self.channel_layer.group_send(f"user_{to_user_id}", {
            "type": "chat_message",
            "message": message_data,
        })
        await self.channel_layer.group_send(f"user_{self.user.id}", {
            "type": "chat_message",
            "message": message_data,
        })

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({'message': message}))

    async def user_online(self, event):
        await self.send(text_data=json.dumps({
            'user_online': {
                'user_id': event['user_id'],
                'username': event['username'],
            }
        }))

    async def user_offline(self, event):
        await self.send(text_data=json.dumps({
            'user_offline': {
                'user_id': event['user_id'],
                'username': event['username'],
            }
        }))

    @database_sync_to_async
    def set_user_online(self, user_id):
        user = CustomUser.objects.get(id=user_id)
        user.is_online = True
        user.last_seen = timezone.now()
        user.save()

    @database_sync_to_async
    def set_user_offline(self, user_id):
        user = CustomUser.objects.get(id=user_id)
        user.is_online = False
        user.last_seen = timezone.now()
        user.save()

    @database_sync_to_async
    def get_conversation(self, user1_id, user2_id):
        user1 = CustomUser.objects.get(id=user1_id)
        user2 = CustomUser.objects.get(id=user2_id)
        conversation = Conversation.objects.filter(participants=user1, participants=user2).first()
        if not conversation:
            conversation = Conversation.objects.create()
            conversation.participants.add(user1, user2)
        return conversation

    @database_sync_to_async
    def create_message(self, conversation, sender, content):
        return Message.objects.create(conversation=conversation, sender=sender, content=content)
