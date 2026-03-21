from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("comptes/", include("comptes.urls")),
    path("depenses/", include("depenses.urls")),
]
