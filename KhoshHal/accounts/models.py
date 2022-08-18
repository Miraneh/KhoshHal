from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone

from utils import random64


class Email(models.Model):
    address = models.EmailField()
    verified = models.BooleanField(
        default=False,
    )
    last_sent = models.DateTimeField(
        null=True,
        default=None,
    )
    token = models.CharField(
        max_length=64,
        null=False,
        blank=False,
        default=random64,
    )

    def normalize(self):
        try:
            email_name, domain_part = self.address.strip().rsplit("@", 1)
        except ValueError:
            pass
        self.address = email_name + "@" + domain_part.lower()

    def refresh_token(self):
        self.token = random64()

    def send_activation_email(self):
        assert self.can_send_email()
        user = get_user_model()
        message = render_to_string(
            'accounts/activation_email.html',
            {
                'user': user.objects.get(email=self),
                'token': self.token,
            },
        )
        email = EmailMessage(
            settings.ACTIVATION_EMAIL_SUBJECT,
            message,
            to=[self.address],
        )
        email.send()
        self.last_sent = timezone.now()

    def send_forget_password_email(self):
        assert self.can_send_email()
        user = get_user_model()
        message = render_to_string(
            'accounts/forget_password_email.html',
            {
                'user': user.objects.get(email=self),
                'token': self.token,
            },
        )
        email = EmailMessage(
            settings.ACTIVATION_EMAIL_SUBJECT,
            message,
            to=[self.address],
        )
        email.send()
        self.last_sent = timezone.now()

    def can_send_email(self):
        if self.last_sent is None:
            return True
        cooldown = settings.ACTIVATION_EMAIL_COOLDOWN
        return timezone.now() - self.last_sent >= cooldown


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
    medial_information = models.FileField(blank=True, null=True)
    verified = models.BooleanField(default=False)


class Patient(models.Model):
    objects = models.Manager()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, primary_key=True)


class File(models.Model):
    upload = models.FileField(upload_to='counselor_information_uploads/')


class Appointment(models.Model):
    counselor = models.OneToOneField(Counselor, on_delete=models.CASCADE, primary_key=True)
    date = models.DateTimeField()
    time = models.TimeField()
    price = models.PositiveIntegerField()
    reserved = models.BooleanField(default=False)


class Reservation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, primary_key=True)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)


