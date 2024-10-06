from rest_framework import generics, permissions
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from rest_framework.permissions import IsAuthenticated
class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user.get_conversations()

class MessageListView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        conversation_id = self.kwargs['conversation_id']
        return Message.objects.filter(conversation__id=conversation_id).order_by('timestamp')
