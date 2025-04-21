from rest_framework import serializers
from server.models import Friendship, User, Chat, Message
from server.serializers.user_serializers import UserSerializer

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']