from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from server.serializers.auth_serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

class LoginApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            res = Response({
                "id": user.id,
                "status": True,
                'access':access_token,
                "refresh": refresh_token
                            }, status=status.HTTP_200_OK)
            # res.set_cookie('access', str(refresh.access_token), httponly=True,secure=False, samesite='None')
            # res.set_cookie('refresh', str(refresh), httponly=True, secure=False, samesite='None')
            return res
        return Response({
            "status": False,
            "message": "Tokens error",
        },status=status.HTTP_401_UNAUTHORIZED)