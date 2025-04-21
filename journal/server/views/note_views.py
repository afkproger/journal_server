from server.serializers.note_serializers import NoteSerializer
from server.models import Note
from server.utils.save_base64 import save_base64_images_from_content

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 


class NoteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user).order_by('-date')
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        print(request.user)
        note_id = request.data.get('id')
        content = request.data.get('content', '')

        content = save_base64_images_from_content(content)
        data = request.data.copy()
        data['content'] = content

        if note_id:
            try:
                note = Note.objects.get(id=note_id, user=request.user)
            except Note.DoesNotExist:
                return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)

            serializer = NoteSerializer(note, data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = NoteSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()  # user подтянется из контекста через HiddenField
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        note_id = request.data.get('note_id')
        if not note_id:
            return Response({'error': 'note_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            note = Note.objects.get(id=note_id, user=request.user)
            note.delete()
            return Response({'message': 'Note deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Note.DoesNotExist:
            return Response({'error': 'Note not found'}, status=status.HTTP_404_NOT_FOUND)
