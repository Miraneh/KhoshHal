from django.urls import path
from .views import *
from django.contrib.auth.decorators import login_required
from django_filters.views import FilterView
from .filters import UserFilter

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", login_required(Profileview.as_view()), name="profile"),
    path("login/profile/counselor/", CounselorProfileview.as_view(), name="counselor_profile"),
    path("login/profile/patient/", PatientProfileview.as_view(), name="patient_profile"),
    # path("medical-info/", EditFileView.as_view(), name="upload medical information"),
    # path("search/", FilterView.as_view(filterset_class=UserFilter, template_name='index.html'), name="search")
    # TODO make a section with search option
    path("search/", login_required(CounselorListView.as_view()), name="search"),
    # path(r"profile/(?P<username>\w+)/comment/.+", AddCommentView.as_view(), name="add_comment")
]
