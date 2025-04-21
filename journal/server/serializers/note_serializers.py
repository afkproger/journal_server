from rest_framework import serializers
from server.models import Note


class NoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Note
        fields = '__all__'