from django.conf import settings
from kavenegar import KavenegarAPI


sms_sender = KavenegarAPI(settings.KAVENEGAR_SECRET_KEY)
