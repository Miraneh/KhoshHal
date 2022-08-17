from django.conf import settings
from rest_framework.permissions import IsAuthenticated, BasePermission

from .models import Patient, User, Counselor


class IsPatient(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        self.message = 'Not a Patient'
        return Patient.objects.filter(user=request.user).count() > 0


class IsCounselor(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        self.message = 'Not a counselor'
        return Counselor.objects.filter(user=request.user).count() > 0
