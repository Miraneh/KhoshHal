from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

from ..utils import random_phone_token
from utils import sms_sender


class Phone(models.Model):
    number = PhoneNumberField(
        null=False,
        blank=False,
    )
    verified = models.BooleanField(
        default=False,
    )
    last_sent = models.DateTimeField(
        null=True,
        default=None,
    )
    token = models.IntegerField(
        validators=[
            MinValueValidator(settings.PHONE_VERIFICATION_TOKEN_MIN_VALUE),
            MaxValueValidator(settings.PHONE_VERIFICATION_TOKEN_MAX_VALUE),
        ],
        default=random_phone_token,
        null=False,
        blank=False,
    )
    chances = models.IntegerField(
        null=False,
        blank=False,
        default=0,
    )

    def refresh_token(self):
        self.token = random_phone_token()
        self.chances = 3

    def send_activation_sms(self):
        assert self.can_send_activation_sms()
        params = {
            'receptor': str(self.number),
            'message': settings.PHONE_VERIFICATION_SMS_FORMAT.format(
                code=self.token,
            ),
        }
        if settings.KAVENEGAR_ENABLED:
            sms_sender.sms_send(params)
        self.last_sent = timezone.now()

    def can_send_activation_sms(self):
        if self.verified:
            return False
        if self.last_sent is None:
            return True
        cooldown = settings.VERIFY_PHONE_COOLDOWN
        return timezone.now() - self.last_sent >= cooldown

    def check_token(self, token):
        if self.chances <= 0:
            return False
        self.chances -= 1
        self.verified = self.token == token
        return self.verified
