from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers.reg_serializers import RegisterSerializer
from rest_framework.permissions import AllowAny

class RegAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self , request):
        print(request.data)
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