from django.urls import path
from tracker.views import *
# from tracker.views import LoginView,RegistrationView,UserProfileView,TrackerView

urlpatterns = [
    path("login",LoginView.as_view(),name='login'),
    path("signin",RegistrationView.as_view(),name='signin'),
    path("scrape",ScrapeView.as_view(),name='scraper'),
    path("profile",UserProfileView.as_view(),name='profile'),
    path("user",UserView.as_view(),name='user'),
]
