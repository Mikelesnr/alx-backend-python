from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from .forms import MessageForm

def conversation_view(request, conversation_id):
    messages = Message.objects.filter(conversation_id=conversation_id).select_related('sender', 'receiver').prefetch_related('replies')
    return render(request, 'chat/conversation.html', {'messages': messages})

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # Redirect to the home page or any other page after deletion

@login_required
def create_message(request):
    sender=request.user
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.save()
            return redirect('conversation_view', conversation_id=message.conversation_id)
    else:
        form = MessageForm()
    return render(request, 'messaging/create_message.html', {'form': form})
