from rest_framework import serializers
from comptes.models import Compte


class CompteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Compte
        fields = ["id", "nom", "utilisateur", "created"]
        read_only_fields = ["id", "created"]