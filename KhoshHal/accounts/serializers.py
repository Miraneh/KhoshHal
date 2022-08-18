from rest_framework import serializers
from .models import User, Patient, Counselor, File
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
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
        fields = ("username", "first_name", "last_name", "email", "phone", "password", "repeat")

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        attrs['email'] = Email(
            **attrs['email'],
        )

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
            counselor = Counselor.objects.create(user=user)
            counselor.save()
        except KeyError:
            user.user_type = 1
            user.set_password(validated_data['password'])
            user.save()
            patient = Patient.objects.create(user=user)
            patient.save()

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



