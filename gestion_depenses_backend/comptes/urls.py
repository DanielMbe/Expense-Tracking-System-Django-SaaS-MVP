from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import LoginView, LogoutView, ListeMembreView, InviterMembreView, CompteMoiView

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("moi/", CompteMoiView.as_view(), name="compte-moi"),
    path("inviter/", InviterMembreView.as_view(), name="inviter-membre"),
    path("membres/", ListeMembreView.as_view(), name="liste-membres"),
]