from rest_framework import serializers
from .models import User, Patient, Counselor


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password", "phone")

    def create(self, validated_data):
        user = User(**validated_data)
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
