from rest_framework import viewsets, permissions
from rest_framework.generics import DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from comptes.services import obtenir_compte_utilisateur, obtenir_role_utilisateur
from comptes.models import RoleUtilisateur
from depenses.models import Categorie, Depense, Monnaie
from depenses.serializers import CategorieSerializer, DepenseSerializer
from depenses.services import (
    construire_requete_depense,
    depense_totale_par_categorie,
    depense_totale_par_devise,
    depense_totale_par_utilisateur,
    periode_depense,
    exporter_rapport
)


MONNAIES = {
    "XOF": {"nom": "Francs CFA", "symbole": "FCFA"},
    "EUR": {"nom": "Euro", "symbole": "€"},
    "USD": {"nom": "Dollars", "symbole": "$"},
}


class CategorieViewSet(viewsets.ModelViewSet):
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        compte = obtenir_compte_utilisateur(self.request.user)
        return Categorie.objects.filter(compte=compte)

    def perform_create(self, serializer):
        compte = obtenir_compte_utilisateur(self.request.user)
        role = obtenir_role_utilisateur(self.request.user, compte)

        if role == RoleUtilisateur.INVITER:
            raise PermissionDenied("Un invité ne peut créer des catégories")
        serializer.save(compte=compte)


class CategorieSuppressionView(DestroyAPIView):
    serializer_class = CategorieSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        compte = obtenir_compte_utilisateur(self.request.user)
        return Categorie.objects.filter(compte=compte)


class DepenseViewSet(viewsets.ModelViewSet):
    serializer_class = DepenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return construire_requete_depense(self.request.user, self.request.query_params)

    def perform_create(self, serializer):
        compte = obtenir_compte_utilisateur(self.request.user)

        code_monnaie = self.request.data.get("monnaie")
        infos_monnaie = MONNAIES.get(code_monnaie, {"nom": code_monnaie, "symbole": ""})
        monnaie, _ = Monnaie.objects.get_or_create(
            code=code_monnaie,
            defaults={"nom": infos_monnaie["nom"], "symbole": infos_monnaie["symbole"]}
        )

        categorie = get_object_or_404(
            Categorie,
            nom=self.request.data.get("categorie"),
            compte=compte
        )

        serializer.save(
            compte=compte,
            utilisateur=self.request.user,
            categorie=categorie,
            monnaie=monnaie
        )


class DepenseSuppressionView(DestroyAPIView):
    serializer_class = DepenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Depense.objects.filter(compte=obtenir_compte_utilisateur(self.request.user))


class RapportDepenseParCategorie(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        requete_depense = construire_requete_depense(self.request.user, request.query_params)
        donnee = depense_totale_par_categorie(requete_depense)
        return Response(donnee)


class RapportDepenseParUtilisateur(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        compte = obtenir_compte_utilisateur(self.request.user)
        role = obtenir_role_utilisateur(self.request.user, compte)
        requete_depense = construire_requete_depense(self.request.user, request.query_params)
        donnee = depense_totale_par_utilisateur(requete_depense, self.request.user, role)
        return Response(donnee)


class RapportDepenseParPeriode(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        periode = request.query_params.get("periode")
        requete_depense = construire_requete_depense(self.request.user, request.query_params)
        donnee = periode_depense(requete_depense, periode)
        return Response(donnee)


class RapportDepenseParMonnaie(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        requete_depense = construire_requete_depense(self.request.user, request.query_params)
        donnee = depense_totale_par_devise(requete_depense)
        return Response(donnee)


class RapportDepenseExporter(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        requete_depense = construire_requete_depense(self.request.user, request.query_params)
        fichier = exporter_rapport(requete_depense, type_rapport="csv")
        reponse = HttpResponse(fichier, content_type="text/csv")
        reponse["Content-Disposition"] = "attachment; filename='rapport_depenses.csv'"
        return reponse