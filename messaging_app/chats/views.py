from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from .models import Conversation, Message, CustomUser
from .serializers import ConversationSerializer, MessageSerializer


# Create your views here.
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['participants__username']

    def create(self, request, *args, **kwargs):
        participants_ids = request.data.get('participants', [])
        participants = CustomUser.objects.filter(id__in=participants_ids)
        if not participants.exists():
            return Response({'error': 'Participants not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        conversation.save()
        
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'sender__username']

    def create(self, request, *args, **kwargs):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        message_body = request.data.get('message_body')

        try:
            conversation = Conversation.objects.get(id=conversation_id)
            sender = CustomUser.objects.get(id=sender_id)
        except (Conversation.DoesNotExist, CustomUser.DoesNotExist):
            return Response({'error': 'Conversation or sender not found'}, status=status.HTTP_400_BAD_REQUEST)
        
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )
        
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
