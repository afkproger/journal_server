from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework import status

class WorkspaceAPIView(APIView):  # Опечатка в названии класса исправлена (было Worskspace)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,  # Используем строковое поле, а не объект
            'email': user.email,        # Другие поля, если нужны
            'id': user.id               # Пример числового поля
        })