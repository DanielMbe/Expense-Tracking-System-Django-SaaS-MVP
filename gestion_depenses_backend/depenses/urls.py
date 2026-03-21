from django.urls import path
from .views import (CategorieViewSet, DepenseViewSet, CategorieSuppressionView, DepenseSuppressionView,
                    RapportDepenseParCategorie, RapportDepenseParMonnaie,
                    RapportDepenseParPeriode, RapportDepenseParUtilisateur, RapportDepenseExporter)

urlpatterns = [
    path("categorie/creer/", CategorieViewSet.as_view({"post": "create"}), name="categorie-creer"),
    path("categorie/listes/", CategorieViewSet.as_view({"get": "list"}), name="categorie-listes"),
    path("categorie/supprimer/<int:pk>/", CategorieSuppressionView.as_view(), name="categorie-supprimer"),
    path("categorie/rapport/", RapportDepenseParCategorie.as_view(), name="rapport-categorie"),
    path("listes/", DepenseViewSet.as_view({"get": "list"}), name="depense-listes"),
    path("creer/", DepenseViewSet.as_view({"post": "create"}), name="depense-creer"),
    path("supprimer/<int:pk>/", DepenseSuppressionView.as_view(), name="depense-supprimer"),
    path("monnaie/", RapportDepenseParMonnaie.as_view(), name="rapport-monnaie"),
    path("periode/", RapportDepenseParPeriode.as_view(), name="rapport-periode"),
    path("utilisateur/", RapportDepenseParUtilisateur.as_view(), name="rapport-utilisateur"),
    path("rapport/csv/", RapportDepenseExporter.as_view(), name="rapport-csv"),
]