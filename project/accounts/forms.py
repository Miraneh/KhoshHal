from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, Patient, Counselor


class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = "Patient"
        user.save()
        patient = Patient.objects.create(user=user)
        return user


class CounselorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "Counselor"
        if commit:
            user.save()
        return user
