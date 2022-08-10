# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Patient, Counselor
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, CounselorSerializer, PatientSerializer
from .forms import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token


# class LogoutAPIView(APIView):
#     # permission_classes = (IsAuthenticated,)
#
#     def post(self, request):
#         request.user.auth_token.delete()
#         return Response(
#             data={'message': f'Bye {request.user.username}!'},
#             status=status.HTTP_204_NO_CONTENT
#         )


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


# class SignUpView(APIView):
#     permission_classes = (AllowAny,)
#     template_name = "registration/signup.html"
#


class LogInView(APIView):  # TODO
    template_name = "registration/login.html"

    def post(self, request, *args, **kwargs):
        # serializer = LoginSerializers(data=request.data, context={'request': request})
        # serializer.is_valid(raise_exception=True)
        # user = serializer.validated_data['user']
        # token, created = Token.objects.get_or_create(user=user)
        # return Response({"status": status.HTTP_200_OK, "Token": token.key})

        email = request.POST.get('email')  # Get email value from form
        password = request.POST.get('password')  # Get password value from form
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
        # t   ype_obj = user_type.objects.get(user=user)
        else:  # Invalid email or password. Handle as you wish
            return redirect('home')


class PatientSignUpView(APIView):
    model = Patient
    template_name = 'registration/signup_form.html'

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)


class CounselorSignUpView(APIView):
    model = Counselor
    template_name = 'registration/signup_form.html'

    def post(self, request):
        serializer = CounselorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(status=status.HTTP_201_CREATED)
