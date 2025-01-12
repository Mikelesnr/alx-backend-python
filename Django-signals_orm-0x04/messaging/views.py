from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required
def delete_user(request):
    user = request.user
    user.delete()
    return redirect('home')  # Redirect to the home page or any other page after deletion
