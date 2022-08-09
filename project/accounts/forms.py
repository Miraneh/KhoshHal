from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import Patient, Counselor


class PatientSignUpForm(forms.Form):
    class Meta(UserCreationForm.Meta):
        model = Patient
        # fields = ('first_name', 'last_name', 'email', 'password','repeat')#, 'phone')

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.user_type = "Patient"
        user.save()
        # patient = Patient.objects.create(user=user)
        return user


class CounselorSignUpForm(forms.Form):
    class Meta(UserCreationForm.Meta):
        model = Counselor
        fields = ('first_name', 'last_name', 'email', 'password', 'phone', 'specialty')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = "Counselor"
        user.save()
        return user
