from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def app_index(request):
   return render(request, 'chat/index.html')


def room_name(request, name):
   return render(request, 'chat/chatroom.html', {'room_name': name})

