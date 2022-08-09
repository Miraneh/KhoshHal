# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view
from django.shortcuts import render
from .models import User, Patient, Counselor
from .serializers import UserSerializer, CounselorSerializer, PatientSerializer
from .forms import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import HttpResponse

# class LogoutAPIView(APIView):
#     # permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(
#             data={'message': f'Bye {request.user.username}!'},
#             status=status.HTTP_204_NO_CONTENT
#         )


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create(serializer)
            return render(request, template_name='registration/signup.html')


# class SignUpView(APIView):
#     permission_classes = (AllowAny,)
#     template_name = "registration/signup.html"
#



class LogInView(APIView):  # TODO
    template_name = "registration/login.html"


class PatientSignUpView(APIView):
    model = Patient
    form_class = PatientSignUpForm
    template_name = 'registration/signup_form.html'

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)


class CounselorSignUpView(APIView):
    model = Counselor
    form_class = CounselorSignUpForm
    template_name = 'registration/signup_form.html'  # TODO

    def post(self, request):
        serializer = CounselorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)
