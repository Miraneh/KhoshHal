# Create your views here.
from .serializers import UserSerializer, CounselorSerializer, PatientSerializer, AppointmentSerializer
from rest_framework.views import APIView
from rest_framework import generics, filters
from .models import User, Patient, Counselor, Appointment
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework import generics, filters
from .models import User, Patient, Counselor
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import render
from . import serializers
from .permissions import IsPatient, IsCounselor
from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import redirect
from datetime import datetime


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
            if user.user_type == 1:
                return redirect("profile/patient")
            elif user.user_type == 2:
                return redirect("profile/counselor")
        else:
            return render(request, "registration/login.html",
                          {"error": "Username or Password isn't correct"})


class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return render(request, "index.html")


class Profileview(APIView):
    def get(self, request):
        print(request.user.user_type)
        if request.user.user_type == 2:
            return redirect('/accounts/login/profile/counselor/')
        else:
            return redirect('/accounts/login/profile/patient/')


class CounselorProfileview(APIView):

    def get(self, request):
        counselor = Counselor.objects.filter(user=request.user)[0]
        appointments = Appointment.objects.filter(counselor=counselor)
        return render(request, "registration/counselor_profile.html"
                      , context={"counselor": counselor,
                                 "appointments": appointments,
                                 "is_user": True})

    def post(self, request):
        counselor = Counselor.objects.filter(user=request.user)[0]
        print("hellllooooooo")
        print(request.data)
        date = request.data['datetime'].split(" ")[0]
        time = request.data['datetime'].split(" ")[1]
        format = request.data['datetime'].split(" ")[2]  # am or pm
        d = datetime(int(date.split('/')[2]), int(date.split('/')[0]), int(date.split('/')[1]),
                     int(time.split(':')[0]),
                     int(time.split(':')[1]))
        appointment = Appointment.objects.create(counselor=counselor, date=d)

        return redirect("/accounts/login/profile/counselor/")
        # return redirect("/accounts/login/profile/counselor/")


class PatientProfileview(APIView):
    def get(self, request):
        return render(request, "registration/patient_profile.html"
                      , context={"username": request.user.username,
                                 "first_name": request.user.first_name,
                                 "last_name": request.user.last_name,
                                 "email": request.user.email
                                 })


class AddAppointment(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data, context={'request': request})
        try:
            serializer.is_valid(raise_exception=True)
        except:
            first_error = list(serializer.errors)[0]
            return render(request, "registration/profile.html",
                          {'field': first_error, 'error': serializer.errors[first_error][0]})

        appointment = serializer.create(validated_data=serializer.validated_data)
        return render(request, 'registration/profile.html')


class CounselorListView(generics.ListAPIView):
    serializer_class = CounselorSerializer
    queryset = Counselor.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialty']
    ordering_fields = ['rating', 'specialty']
    ordering = ['user__last_name']

    def get(self, request):
        doctors = Counselor.objects.all()
        return render(request, "doctors.html", context={'doctors': list(doctors)})

    def post(self, request):
        user = User.objects.filter(username=request.data['doctor'])[0]
        counselor = Counselor.objects.filter(user=user)[0]
        appointments = Appointment.objects.filter(counselor=counselor)
        return render(request, "registration/counselor_profile.html"
                      , context={"counselor": counselor,
                                 "appointments": appointments,
                                 "is_user": False})


class AddCommentView(APIView):
    permission_classes = (IsPatient,)

    def post(self, request, username):
        crit1 = Q(appointment__counselor__username=username)
        crit2 = Q(patient__username=username)
        queryset = Reservation.objects.filter(crit1 & crit2)
        if queryset:
            serializer = CommentSerializer(data=request.data, context={'request': request})
            try:
                serializer.is_valid(raise_exception=True)
            except:
                first_error = list(serializer.errors)[0]
                return render(request, "registration/profile.html",
                              {'field': first_error, 'error': serializer.errors[first_error][0]})
            comment = serializer.create(validated_data=serializer.validated_data)
        else:
            return render(request, "registration/profile.html",
                          {'field': "Comment error", 'error': "You have never had an appointment with this counselor."})
        return render(request, 'registration/profile.html')
