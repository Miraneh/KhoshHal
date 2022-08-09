from django.db import models
from .user import User


class Counselor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField()
    ME_number = models.PositiveIntegerField()
