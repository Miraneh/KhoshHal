from django.urls import path
from .views import *


urlpatterns = [
    path("signup/", UserRegistration.as_view(), name="signup"),
    path('signup/<int:pk>/', UserRegistration.as_view()),
    path("signup/patient", PatientSignUpView.as_view(), name="patient_signup"),
    path("signup/counselor", CounselorSignUpView.as_view(), name="counselor_signup"),
    path("login/", LogInView.as_view(), name="login")
]