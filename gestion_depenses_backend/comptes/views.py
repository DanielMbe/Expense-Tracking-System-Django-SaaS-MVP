from rest_framework import viewsets, permissions
from comptes.models import Compte, RoleUtilisateur
from comptes.serializers import CompteSerializer
from comptes.services import obtenir_compte_utilisateur
from utilisateurs.models import Utilisateur
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError


class CompteViewSet(viewsets.ModelViewSet):
    serializer_class = CompteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Compte.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        compte = serializer.save(utilisateur=self.request.user)
        RoleUtilisateur.objects.create(utilisateur=self.request.user, compte=compte, role=RoleUtilisateur.PROPRIETAIRE)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        utilisateur = authenticate(email=email, password=password)
        if not utilisateur:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(utilisateur)
        return Response({"access": str(refresh.access_token), "refresh": str(refresh), "user": "true"})


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"loggedOut": True})
        except TokenError:
            return Response({"error": "Invalid token"}, status=400)


class CompteMoiView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        compte = obtenir_compte_utilisateur(self.request.user)
        serializer = CompteSerializer(compte)
        return Response(serializer.data)


class InviterMembreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email requis"}, status=status.HTTP_400_BAD_REQUEST)

        compte = obtenir_compte_utilisateur(self.request.user)
        inviter = get_object_or_404(Utilisateur, email=email)
        RoleUtilisateur.objects.create(utilisateur=inviter, compte=compte, role=RoleUtilisateur.INVITER)
        return Response({"detail": "Invitation envoyé"}, status=status.HTTP_201_CREATED)


class ListeMembreView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        compte = obtenir_compte_utilisateur(self.request.user)
        membres = RoleUtilisateur.objects.filter(compte=compte).select_related("utilisateur")
        donnee = [
            {"utilisateur": m.utilisateur.email, "role": m.role, "created": m.created}
            for m in membres
        ]
        return Response(donnee)