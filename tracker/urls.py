from django.urls import path
from tracker.views import *

urlpatterns = [
    path("login", LoginView.as_view(), name='login'),
    path("signin", RegistrationView.as_view(), name='signin'),
    path("profile", UserView.as_view(), name='profile'),
    path("user_product", UserDashboardView.as_view(), name='profile'),
    path("user", UrlDesiredView.as_view(), name='user'),
    path("price/52week/<str:id>", Ayearprice.as_view(), name='user'),
]
