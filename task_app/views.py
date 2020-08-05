import json
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.shortcuts import render

from django.contrib.auth import get_user_model
User = get_user_model()

def index(request):
    return render(request, "index.html")

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def sign_up_view(request):
    post_data = json.loads(request.body)
    print(post_data)
    form = CustomUserCreationForm(post_data)
    print(form)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        email = form.cleaned_data.get('email')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)
        return JsonResponse({'message': 'logged in!','user':user.username}, status=200)
    return JsonResponse({'message': 'Username or password invalid/ already used'}, status=400)

def logout_view(request):
    username = request.user.username
    content = {'logged_out_user': username}
    logout(request)
    return JsonResponse(content)

def login_view(request):
    #if request.method == 'POST':
    #    print("YESS")
    post_data = json.loads(request.body)
    username = post_data['username']
    password = post_data['password']
    print("credintials",username,password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return JsonResponse({'message': 'logged in!','user':user.username}, status=200)
    else:
        # Return an 'invalid login' error message.
        return JsonResponse({'message': 'Eror'}, status=401)