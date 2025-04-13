from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers.auth_serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        res = Response({
            "status": True,
            'access':access_token
                        }, status=status.HTTP_200_OK)
        res.set_cookie('access', str(refresh.access_token), httponly=True, secure=True)
        res.set_cookie('refresh', str(refresh), httponly=True, secure=True)
        return res