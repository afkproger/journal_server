from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from server.models import User, Friendship, Chat
from server.serializers.chat_serializers import ChatSerializer
from rest_framework import status


class ChatAPIView(APIView):
    def get(self, request, other_username):
        # Получаем username из строки запроса
        username = request.GET.get('username')
        if not username:
            return Response({"error": "Username is required"}, status=status.HTTP_400_BAD_REQUEST)

        # Находим пользователя по username
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Находим другого пользователя по other_username
        try:
            other_user = User.objects.get(username=other_username)
        except User.DoesNotExist:
            return Response({"error": "Other user not found"}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем, являются ли пользователи друзьями
        if not Friendship.objects.filter(user=user, friend=other_user).exists():
            return Response({"error": "Users are not friends"}, status=status.HTTP_403_FORBIDDEN)

        # Получаем или создаём чат
        chat = Chat.objects.filter(participants=user).filter(participants=other_user).first()
        if not chat:
            chat = Chat.objects.create()
            chat.participants.add(user, other_user)

        # Возвращаем данные (пример)
        return Response({
            "chat_id": chat.id,
            "participants": [user.username, other_user.username]
        }, status=status.HTTP_200_OK)