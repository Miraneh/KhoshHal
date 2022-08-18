from django.urls import path
from .views import *
from django_filters.views import FilterView
from .filters import UserFilter

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LogInView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    # path("medical-info/", EditFileView.as_view(), name="upload medical information"),
    path("search/", FilterView.as_view(filterset_class=UserFilter, template_name='index.html'), name="search")
    # TODO make a section with search option
    # path("search/", CounselorListView.as_view(), name="search"),
]
