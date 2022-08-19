from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator


class File(models.Model):
    upload = models.FileField(upload_to='counselor_information_uploads/')


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

    email = models.EmailField()
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
    ME_number = models.PositiveIntegerField(blank=True, null=True)
    medical_information = models.FileField(blank=True, null=True)
    verified = models.BooleanField(default=False)
    rating = models.DecimalField(max_digits=2, decimal_places=1,
                                 validators=[MinValueValidator(0), MaxValueValidator(5)], blank=True, null=True)


class Patient(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)


class Appointment(models.Model):
    objects = models.Manager()
    counselor = models.OneToOneField(Counselor, on_delete=models.CASCADE, primary_key=True)
    date = models.DateTimeField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    price = models.PositiveIntegerField()
    reserved = models.BooleanField(default=False)


class Reservation(models.Model):
    objects = models.Manager()
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, primary_key=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)


class Comment(models.Model):
    writer = models.OneToOneField(Patient, on_delete=models.CASCADE, primary_key=True)
    counselor = models.OneToOneField(Counselor, on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=False)