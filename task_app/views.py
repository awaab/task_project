import json
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render
from .serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from django.template import RequestContext
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

User = get_user_model()
DISCONNECTED_MSG = "DISCONNECTED"
CHANGED_DETAILS_MSG = "CHANGED_DETAILS"
CONNECTED_MSG = "CONNECTED"

def logged_in_view(request):
    if request.user.is_authenticated:
        username = request.user.username
        content = {'user': username}
        return JsonResponse(content)
    else:
        return JsonResponse({'message': "Unauthorized"}, status=401)

@ensure_csrf_cookie
def index(request):
    csrfContext = RequestContext(request).__dict__
    return render(request, 'index.html', csrfContext)

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
    if not request.user.is_authenticated:
        return JsonResponse({'message': "Unauthorized"}, status=401)
    send_user_channel(request.user.id, DISCONNECTED_MSG)
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
        return JsonResponse({'message': 'Bad login'}, status=400)

def user_info(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': "Unauthorized"}, status=401)
    current_user = request.user
    print(current_user)
    serializer = UserSerializer(current_user)
    return JsonResponse(serializer.data)

def user_edit(request):
    if not request.user.is_authenticated:
        return JsonResponse({'message': "Unauthorized"}, status=401)
    send_user_channel(request.user.id, CHANGED_DETAILS_MSG)
    data = json.loads(request.body)
    non_empty_data = {}
    for key in data:
        if data[key]:
            non_empty_data[key] = data[key]
    serializer = UserSerializer(request.user, data=non_empty_data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse(serializer.data)

def send_user_channel(user_id, message):
    group_name = f'user-status-{str(user_id)}'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
            group_name,
            {
                "type": "notify",
                "content": message,
            }
    )