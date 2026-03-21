from rest_framework import serializers
from depenses.models import Categorie, Depense, Monnaie


class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ["id", "nom", "compte", "created"]
        read_only_fields = ["id", "compte", "created"]

    def get_extra_kwargs(self):
        extra = super().get_extra_kwargs()
        
        if self.instance is not None:
            extra.update({"nom": {"read_only": True}})
        return extra


class DepenseSerializer(serializers.ModelSerializer):
    monnaie = serializers.SlugRelatedField(slug_field="code", queryset=Monnaie.objects.all(), required=False)
    categorie = serializers.SlugRelatedField(slug_field="nom", queryset=Categorie.objects.all(), required=False)

    class Meta:
        model = Depense
        fields = ["id", "compte", "utilisateur", "categorie", "monnaie", "avoir", "description", "date_depense", "created"]
        read_only_fields = ["id", "compte", "utilisateur", "created"]