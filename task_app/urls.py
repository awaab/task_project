from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.sign_up_view, name='signup'),
    path('csrf/', views.csrf, name='csrf'),
    path('', views.index, name='index'),
]
