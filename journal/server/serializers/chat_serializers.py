from rest_framework import serializers
from server.models import Chat
from server.serializers.user_serializers import UserSerializer
from server.serializers.message_serializers import MessageSerializer
class ChatSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True)
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages', 'created_at']