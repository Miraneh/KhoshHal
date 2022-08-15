from django.contrib.auth.models import AbstractUser
from django.db import models


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

    email = models.EmailField(unique=True)
    national_ID = models.PositiveIntegerField()
    phone = models.CharField(max_length=15)
    age = models.PositiveSmallIntegerField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=1)
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(max_length=128)
    ME_number = models.PositiveIntegerField()


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.email
