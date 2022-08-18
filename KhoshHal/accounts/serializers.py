from rest_framework import serializers
from .models import User, Patient, Counselor, Appointment
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
import logging

person = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "repeat")

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )

        user.set_password(validated_data['password'])

        return user


class CounselorSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        model = Counselor
        fields = ("user", "medical_information")

    def create(self, validated_data):
        user = validated_data['user']
        user.user_type = 2
        user.save()
        counselor = Counselor.objects.create(user=user, medical_information=validated_data['medical_information'])
        counselor.save()
        return user


class PatientSerializer(UserSerializer):
    class Meta:
        model = User
        fields = "user"

    def create(self, validated_data):
        user = validated_data['user']
        user.user_type = 1
        user.save()
        patient = Patient.objects.create(user=user)
        patient.save()
        return user


class AppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    time = serializers.TimeField(required=True)
    price = serializers.IntegerField(min_value=0)

    class Meta:
        model = Appointment
        fields = ("counselor", "date", "time", "price")

    def validate(self, validated_data):
        counselor = validated_data['counselor']
        date = validated_data['date']
        time = validated_data['time']
        price = validated_data['price']
        appointment = Appointment.objects.create(counselor=counselor, date=date, time=time, price=price)
        appointment.save()

        return appointment
