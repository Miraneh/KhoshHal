# Create your views here.
from rest_framework.views import APIView
from rest_framework import generics
from .models import User, Patient, Counselor
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer, PatientSerializer, CounselorSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from . import serializers
from .permissions import IsPatient, IsCounselor
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


class SignUpView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get(self, request):
        return render(request, 'registration/signup.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            first_error = list(serializer.errors)[0]
            return render(request, 'registration/signup.html',
                          {'field': first_error, 'error': serializer.errors[first_error][0]})

        user = serializer.create(validated_data=serializer.validated_data)

        if "file" in request.data.keys():
            serializer = CounselorSerializer(data=request.data, context={'request': request})
            serializer.create(validated_data={"user": user, "medical_information": request.data['file']})
        else:
            serializer = PatientSerializer(data=request.data, context={'request': request})
            serializer.create(validated_data={"user": user})

        return render(request, 'registration/signup.html')


class LogInView(APIView):

    def get(self, request):
        return render(request, "registration/login.html")

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, "registration/profile.html")
        else:
            return render(request, "registration/login.html",
                          {"error": "Username or Password isn't correct"})


# @login_required()
class LogoutView(APIView):

    def get(self, request):
        return render(request, "registration/login.html")  # TODO

    def post(self, request):
        logout(request)
        return render(request, "index.html")


class ProfileView(APIView):

    def get(self, request):
        print("hey hey")
        return render(request, "registration/profile.html")

# class EditFileView(generics.UpdateAPIView):
#     serializer_class = serializers.EditFileSerializer
#     permission_classes = (IsCounselor,)
# 
#     def get_object(self):
#         return self.request.user
#
