from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SimpleAPIView(APIView):
    def get(self, request):
        data = {
            "message": "Привет, Николай!",
            "status": "ok"
        }
        return Response(data, status=status.HTTP_200_OK)