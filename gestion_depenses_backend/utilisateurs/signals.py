from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import transaction
from comptes.models import Compte, RoleUtilisateur


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def creer_nouveau_compte(sender, instance, created, **kwargs):
    if created:
        def create_compte():
            if not Compte.objects.filter(utilisateur=instance).exists():
                compte = Compte.objects.create(nom=f"Compte de {instance.email}", utilisateur=instance)
                if not RoleUtilisateur.objects.filter(utilisateur=instance, compte=compte).exists():
                    RoleUtilisateur.objects.create(utilisateur=instance, compte=compte, role=RoleUtilisateur.PROPRIETAIRE)

        transaction.on_commit(create_compte)