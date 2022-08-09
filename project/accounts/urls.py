from django.urls import path
from .views import *


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    # path('login/<int:pk>/', LogInView.as_view()),
]