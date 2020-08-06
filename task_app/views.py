import json
from django.http import HttpResponse
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.middleware.csrf import get_token
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from .serializers import UserSerializer
from rest_framework import viewsets

# from django.shortcuts import render_to_response
User = get_user_model()
#from django.core.context_processors import csrf
from django.template import RequestContext


def logged_in_view(request):
    print(request.user)
    if request.user.is_authenticated:
        username = request.user.username
        content = {'user': username}
        return JsonResponse(content)
    else:
        return JsonResponse({'message': "Not logged in"}, status=403)


@csrf_protect
def index(request):
    csrfContext = RequestContext(request).__dict__
    return render(request, 'index.html', csrfContext)

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

def sign_up_view(request):
    post_data = json.loads(request.body)
    print(post_data)
    form = CustomUserCreationForm(post_data)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return JsonResponse({'message': 'logged in!','user':user.username}, status=200)
    return JsonResponse({'message': 'Username/password invalid or already registered.'}, status=400)


def logout_view(request):
    username = request.user.username
    content = {'logged_out_user': username}
    logout(request)
    print(request.user)
    return JsonResponse(content)

def login_view(request):
    post_data = json.loads(request.body)
    username = post_data['username']
    password = post_data['password']
    #print("credintials",username,password)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        # Redirect to a success page.
        return JsonResponse({'message': 'logged in!','user':user.username}, status=200)
    else:
        # Return an 'invalid login' error message.
        return JsonResponse({'message': 'Eror'}, status=401)

def user_info(request):
    current_user = request.user
    print(current_user)
    serializer = UserSerializer(current_user)
    return JsonResponse(serializer.data)

def user_edit(request):
    data = json.loads(request.body)
    non_empty_data = {}
    for key in data:
        if data[key]:
            non_empty_data[key] = data[key]
    serializer = UserSerializer(request.user, data=non_empty_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data)