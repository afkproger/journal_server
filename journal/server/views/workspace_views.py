from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework import status

class WorkspaceAPIView(APIView):  # Опечатка в названии класса исправлена (было Worskspace)
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,  
            'email': user.email, 
            'middle_name': user.middle_name
        })