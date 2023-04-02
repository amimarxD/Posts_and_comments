from django.urls import path
from . import views
from django.contrib.auth import views as v
# from django.contrib.auth import login

app_name = "auth"
urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('login', v.LoginView.as_view(), name='login'),
    path('logout', v.LogoutView.as_view(), name="logout"),
    path('sign-up', views.sign_up, name="sign-up")
]