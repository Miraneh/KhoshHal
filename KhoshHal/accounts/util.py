import random

from django.conf import settings


def random_phone_token():
    return random.randint(
        settings.PHONE_VERIFICATION_TOKEN_MIN_VALUE,
        settings.PHONE_VERIFICATION_TOKEN_MAX_VALUE,
    )