from rest_framework import serializers
from .models import User, Patient, Counselor, MedicalInformation
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.db import models
from django.contrib.auth import get_user_model

person = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "password", "repeat")
        # extra_kwargs = {
        #     'first_name': {'required': True},
        #     'last_name': {'required': True}
        # }

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        try:
            file = validated_data["file"]
            user.user_type = 2

        except:
            user.user_type = 1

        user.set_password(validated_data['password'])
        user.save()
        return user


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient


class CounselorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Counselor
        fields = ("specialty", "ME_number")


class EditMedicalInfoSerializer(serializers.ModelSerializer):
    upload = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'emails',
        ]

    def update(self, instance, validated_data):
        upload = instance.upload
        upload.save()
        return instance



