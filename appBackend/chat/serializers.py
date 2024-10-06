# chat/serializers.py

from rest_framework import serializers
from .models import Conversation, Message
from users.models import CustomUser



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'last_seen', 'is_online']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']

# class ConversationSerializer(serializers.ModelSerializer):
#     participants = UserSerializer(many=True, read_only=True)
#     messages = MessageSerializer(many=True, read_only=True)

#     class Meta:
#         model = Conversation
#         fields = ['id', 'participants', 'messages', 'created_at']


# chat/serializers.py

class ConversationSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True)
    last_seen = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = ['id', 'participants', 'messages', 'created_at', 'last_seen']

    def get_last_seen(self, obj):
        # Assuming two participants
        participants = obj.participants.all()
        recipient = participants.exclude(id=self.context['request'].user.id).first()
        return {
            'is_online': recipient.is_online,
            'last_seen': recipient.last_seen
        }
