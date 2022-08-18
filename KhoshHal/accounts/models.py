from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):
    GENDER_CHOICES = (
        ("M", "male"),
        ("F", "female"),
    )
    USER_TYPE_CHOICES = (
        (1, 'Patient'),
        (2, 'Counselor'),
        (3, 'Admin'),
    )

    email = models.OneToOneField(
        Email,
        null=True,
        on_delete=models.SET_NULL,
    )
    national_ID = models.PositiveIntegerField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, blank=True, null=True)


class Counselor(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(max_length=128)
    ME_number = models.PositiveIntegerField()
    medial_information = models.FileField()
    verified = models.BooleanField(default=False)


class Patient(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)


class File(models.Model):
    upload = models.FileField(upload_to='counselor_information_uploads/')
