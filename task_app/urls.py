from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.sign_up_view, name='signup'),
    path('', views.index, name='index'),
    path('logged_in/', views.logged_in_view, name='logged-in'),
    path('user/', views.user_info, name='user-info'),
    path('user/edit/', views.user_edit, name="user-edit"),
]
