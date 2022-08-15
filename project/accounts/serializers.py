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


# class LoginSerializers(serializers.Serializer):
#     email = serializers.CharField(max_length=255)
#     password = serializers.CharField(
#         label=_("Password"),
#         style={'input_type': 'password'},
#         trim_whitespace=False,
#         max_length=128,
#         write_only=True
#     )
#
#     def validate(self, data):
#         username = data.get('email')
#         password = data.get('password')
#
#         if username and password:
#             user = authenticate(request=self.context.get('request'),
#                                 username=username, password=password)
#             if not user:
#                 msg = _('Unable to log in with provided credentials.')
#                 raise serializers.ValidationError(msg, code='authorization')
#         else:
#             msg = _('Must include "username" and "password".')
#             raise serializers.ValidationError(msg, code='authorization')
#
#         data['user'] = user
#         return data