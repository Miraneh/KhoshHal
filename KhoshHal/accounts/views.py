# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics
from .models import User, Patient, Counselor
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, redirect
from . import serializers
from .permissions import IsPatient, IsCounselor
from django.http import HttpResponse


class SignUpView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get(self, request):
        return render(request, 'registration/signup.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        if len(serializer.errors) > 0:
            first_error = list(serializer.errors)[0]
            return render(request, 'registration/signup.html',
                          {'field': first_error, 'error': serializer.errors[first_error][0]})
        serializer.create(validated_data=serializer.validated_data)
        return render(request, 'registration/signup.html')


class LogInView(APIView):  # TODO

    def get(self, request):
        return render(request, "registration/login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Welcome")
        else:
            return HttpResponse("Wrong info")


class ProfileView(APIView):

    def get(self, request):
        print("hey hey")
        return render(request, "registration/profile.html")


class EditFileView(generics.UpdateAPIView):
    serializer_class = serializers.EditFileSerializer
    permission_classes = (IsCounselor,)

    def get_object(self):
        return self.request.user
