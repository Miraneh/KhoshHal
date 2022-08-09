# Create your views here.
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.shortcuts import render
from .models import User, Patient, Counselor
from .serializers import UserSerializer, CounselorSerializer, PatientSerializer
from rest_framework.permissions import AllowAny


class SignUpView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return render(request, 'registration/signup.html')

    def post(self, request):
        # request.user.auth_token.delete()
        print(request.data)
        return render(request, 'registration/signup.html')


class LogInView(APIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        return render(request, 'registration/login.html')

    def post(self, request):
        # request.user.auth_token.delete()
        return HttpResponse("YOOHOO!")
        # return render(request, 'registration/signup.html')