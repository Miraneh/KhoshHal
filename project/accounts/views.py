# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic
from .models import User
from .models import Counselor
from .models import Patient
from .forms import PatientSignUpForm, CounselorSignUpForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class LogInView(generic.CreateView):
    template_name = "registration/login.html"


class PatientSignUpView(generic.CreateView):
    model = Patient
    form_class = PatientSignUpForm
    template_name = 'registration/signup_form.html'  # TODO

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = "Patient"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('patients:profile')  # TODO


class CounselorSignUpView(generic.CreateView):
    model = Counselor
    form_class = CounselorSignUpForm
    template_name = 'registration/signup_form.html'  # TODO

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = "Counselor"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('counselor:profile')  # TODO
