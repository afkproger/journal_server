from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers.reg_serializers import RegisterSerializer

class RegAPIView(APIView):
    def post(self , request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
            "user": {
                "username": user.username,
                "email": user.email
            },
            "message": "Пользователь успешно зарегистрирован",}, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)