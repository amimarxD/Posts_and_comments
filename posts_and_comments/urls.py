from django.urls import path
from . import views 

app_name = 'post'

urlpatterns = [
    path('', views.index, name = 'index'),
    path('create_post', views.create_post, name = 'create_post')
]