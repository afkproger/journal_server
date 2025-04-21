from rest_framework import serializers
from server.models import Friendship
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class FriendshipSerializer(serializers.ModelSerializer):
    friend = serializers.CharField() 
    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        user = self.context['request'].user
        friend_nickname = validated_data['friend']  # предполагаем, что приходит ник друга как строка

        # Ищем пользователя по нику
        try:
            friend = User.objects.get(username=friend_nickname)
        except ObjectDoesNotExist:
            raise serializers.ValidationError("Пользователь с таким ником не существует.")

        # Проверка, что пользователь не пытается добавить самого себя
        if user == friend:
            raise serializers.ValidationError("Нельзя добавить самого себя в друзья.")
        
        # Проверка, существует ли уже такая связь дружбы
        if Friendship.objects.filter(user=user, friend=friend).exists():
            raise serializers.ValidationError("Вы уже в друзьях.")

        return Friendship.objects.create(user=user, friend=friend)