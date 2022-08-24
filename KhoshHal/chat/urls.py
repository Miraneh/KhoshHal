from django.urls import path
from .views import app_index, room_name
app_name = 'chat'

urlpatterns = [
    path('', app_index, name="index"),
]
