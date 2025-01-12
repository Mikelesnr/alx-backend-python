from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message

def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver').prefetch_related('replies')
    return render(request, 'chat/conversation.html', {'messages': messages})

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # Redirect to the home page or any other page after deletion
