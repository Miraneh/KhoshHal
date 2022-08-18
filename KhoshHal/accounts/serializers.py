from rest_framework import serializers
from .models import User, Patient, Counselor, File, Appointment, Reservation, Email
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
import logging

person = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(source='email.address')

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password", "repeat")

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        try:
            attrs['email'] = Email(
                **attrs['email'],
            )
            attrs['email'].save()
        except Exception as e:
            print(e)

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        try:
            validated_data['file'] = File(
                **validated_data['file'],
            )
            user.user_type = 2
            user.set_password(validated_data['password'])
            user.save()
            counselor = Counselor.objects.create(user=user, medical_information=validated_data['file'])
            counselor.save()
            email.send_activation_email()
            email.save()
        except KeyError:
            user.user_type = 1
            user.set_password(validated_data['password'])
            user.save()
            patient = Patient.objects.create(user=user)
            patient.save()
            email.send_activation_email()
            email.save()

        return user


class EditFileSerializer(serializers.ModelSerializer):
    upload = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'file',
        ]

    def update(self, instance, validated_data):
        upload = instance.upload
        upload.save()
        return instance


class AppointmentSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(required=True)
    time = serializers.TimeField(required=True)

    class Meta:
        model = Appointment
        fields = ("counselor", "date", "time")

    def validate(self, attrs):
        attrs['Counselor'] = Counselor(
            **attrs['Counselor'],
        )

        return attrs


class VerifyEmailSerializer(serializers.ModelSerializer):
    address = serializers.ReadOnlyField()

    class Meta:
        model = Email
        fields = ['address']

    def update(self, instance, validated_data):
        instance.verified = True
        instance.save()
        return instance
