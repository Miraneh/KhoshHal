from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.db import models
from django.template.loader import render_to_string
from django.utils import timezone

from utils import random64 #TODO


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
        User = get_user_model()
        message = render_to_string(
            'accounts/activation_email.html',
            {
                'user': User.objects.get(email=self),
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
        User = get_user_model()
        message = render_to_string(
            'accounts/forget_password_email.html',
            {
                'user': User.objects.get(email=self),
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
