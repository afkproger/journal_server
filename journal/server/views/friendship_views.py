from rest_framework.views import APIView
from server.serializers.friendship_serializers import FriendshipSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 
from server.models import Friendship

class FriendshipAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self , request):
        print(request.data)
        serializer = FriendshipSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Ошибки сериализатора:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self , request):
        user = request.user
        friendships = Friendship.objects.filter(user=user)
        friend_usernames = [friendship.friend.username for friendship in friendships]
        return Response({"friend_usernames": friend_usernames})