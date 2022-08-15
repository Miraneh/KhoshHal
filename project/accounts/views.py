# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import User, Patient, Counselor
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer, CounselorSerializer, PatientSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render, redirect
from rest_framework.authtoken.models import Token


class SignUpView(APIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def get(self, request):
        return render(request, 'registration/signup.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.create(validated_data= serializer.validated_data)
        # token, created = Token.objects.get_or_create(user=user)
        print(request.data)
        return render(request, 'registration/signup.html')


class LogInView(APIView):  # TODO
    print("In here")
    template_name = "registration/login.html"

    def post(self, request, *args, **kwargs):
        print(request.data)
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
