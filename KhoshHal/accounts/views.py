# Create your views here.
import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .serializers import UserSerializer, CounselorSerializer, PatientSerializer
from .models import User, Patient, Counselor, Appointment, Reservation, Comment
from rest_framework.views import APIView
from rest_framework import generics, filters
from django.contrib.auth import authenticate, login, logout
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.shortcuts import redirect
from datetime import datetime
import re
import requests
from .zarinpal import Zarinpal, ZarinpalError

MERCHANT = '11111111-2222-3333-4444-555555555555'
WSDL = "https://sandbox.zarinpal.com/pg/services/WebGate/wsdl"
WEB_GATE = "https://sandbox.zarinpal.com/pg/StartPay/"
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "Please pay for the meeting"  # Required
CallbackURL = 'http://localhost:8000/verify/'

zarin_pal = Zarinpal('XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX',
                     'http://127.0.0.1:8000/accounts/verify',
                     sandbox=True)


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
        comments = Comment.objects.filter(counselor=counselor)
        return render(request, "registration/counselor_profile.html"
                      , context={"counselor": counselor,
                                 "user": request.user,
                                 "appointments": appointments,
                                 "comments": comments,
                                 "is_user": True})

    def post(self, request):
        counselor = Counselor.objects.filter(user=request.user)[0]
        date = request.data['datetime'].split(" ")[0]
        time = request.data['datetime'].split(" ")[1]
        d = datetime(int(date.split('/')[2]), int(date.split('/')[0]), int(date.split('/')[1]),
                     int(time.split(':')[0]),
                     int(time.split(':')[1]))
        price = request.data['price']
        appointment = Appointment.objects.create(counselor=counselor, date=d, price=price)

        return redirect("/accounts/login/profile/counselor/")


class PatientProfileview(APIView):
    def get(self, request):
        try:
            patient = Patient.objects.filter(user=request.user)[0]
            reservations = Reservation.objects.filter(patient=patient)
            return render(request, "registration/patient_profile.html"
                          , context={"patient": patient,
                                     "user": request.user,
                                     "reservations": reservations,
                                     "is_user": True
                                     })
        except:
            return redirect("/accounts/login/")

    def post(self, request):
        appointment = Appointment.objects.get(pk=request.data["appointment"])
        reservation = Reservation.objects.get(appointment=appointment)  # TODO return the money
        reservation.delete()
        appointment.reserved = False
        appointment.save()
        return redirect('/accounts/login/profile/patient/')


class CounselorListView(generics.ListAPIView):
    serializer_class = CounselorSerializer
    queryset = Counselor.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'specialty']
    ordering_fields = ['rating', 'specialty']
    ordering = ['user__last_name']

    def get_username(self, request):
        self.queryset = Counselor.objects.all()
        for i in self.search_fields:
            if i in request.query_params.keys():
                self.queryset = self.queryset.filter(**{i: request.query_params.get(i)})
        return self.queryset                

    def get(self, request):
        # doctors = Counselor.objects.all()
        return render(request, "doctors.html", context={'doctors': self.get_username(request)})

    def post(self, request):
        user = User.objects.filter(username=request.user.username)[0]
        patient = Patient.objects.filter(user=user)
        counselor_card = User.objects.filter(username=request.POST.get('doctor'))[0]
        counselor = Counselor.objects.filter(user=counselor_card)[0]
        if request.data['post'] == "view":
            appointments = Appointment.objects.filter(counselor=counselor)
            comments = Comment.objects.filter(counselor=counselor)
            can_comment = False
            if patient:
                reservations = Reservation.objects.filter(patient=patient[0])
                for r in reservations:
                    if r.appointment.counselor.user.username == counselor.user.username:
                        can_comment = True
                        break
            return render(request, "registration/counselor_profile.html"
                          , context={"counselor": counselor,
                                     "appointments": appointments,
                                     "comments": comments,
                                     "can_comment": can_comment,
                                     "is_user": False})
        elif request.data['post'] == "comment":
            if request.data['comment'] != "":
                comment = Comment.objects.create(writer=patient[0], counselor=counselor, text=request.data['comment'])
                return redirect('/doctors/search/')
        else:
            appointment = Appointment.objects.get(
                pk=int(re.search('Appointment object \((.*)\)', request.data['appointment']).group(1)))
            patient = Patient.objects.filter(user=request.user)[0]
            if not appointment.reserved:
                try:
                    amount = appointment.price
                    redirect_url = zarin_pal.payment_request(amount, description)
                    reservation = Reservation.objects.create(appointment=appointment, patient=patient,
                                                             authority=zarin_pal.authority)
                    return redirect(redirect_url)
                except ZarinpalError as e:
                    return HttpResponse(e)
            return redirect('/accounts/profile/')


def verify(request):
    if request.GET['Status'] == 'OK':
        authority = int(request.GET['Authority'])
        try:
            # try to found transaction
            try:
                reservation = Reservation.objects.get(authority=authority)

            # if we couldn't find the transaction
            except ObjectDoesNotExist:
                return HttpResponse('we can\'t find this reservation')

            code, message, ref_id = zarin_pal.payment_verification(reservation.appointment.price, authority)

            # everything is okey
            if code == 100:
                reservation.appointment.reserved = True
                reservation.appointment.save()
                reservation.reference_id = ref_id
                reservation.save()
                content = {
                    'type': 'Success',
                    'ref_id': ref_id
                }
                return render(request, "registration/patient_profile.html", context=content)
            # operation was successful but PaymentVerification operation on this transaction have already been done
            elif code == 101:
                content = {
                    'type': 'Warning'
                }
                return render(request, "registration/patient_profile.html", context=content)

        # if got an error from zarinpal
        except ZarinpalError as e:
            return HttpResponse(e)
    else:
        authority = int(request.GET['Authority'])
        reservation = Reservation.objects.get(authority=authority)
        reservation.delete()

    return render(request, "registration/patient_profile.html")
