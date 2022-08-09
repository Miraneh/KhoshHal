from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models.user import User
from .models.patient import Patient
from .models.counselor import Counselor


class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = "Patient"
        user.save()
        # patient = Patient.objects.create(user=user)
        return user


class CounselorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('first_name', 'last_name', 'email', 'password', 'phone', 'specialty')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "Counselor"
        user.save()
        return user
