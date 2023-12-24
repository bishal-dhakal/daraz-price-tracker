from django.urls import path
from tracker.views import LoginView,RegistrationView,UserProfileView

urlpatterns = [
    path("login",LoginView.as_view(),name='login'),
    path("signin",RegistrationView.as_view(),name='signin'),
    path("profile",UserProfileView.as_view(),name='profile'),
]
