from django.urls import path
from .views import *


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("medical-info/", EditFileView.as_view(), name="upload medical information")
]

