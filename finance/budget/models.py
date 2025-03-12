from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from depense.models import Depense

# Create your models here.

class Budget(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255, unique=True)
    montant = models.FloatField()
    date_debut = models.DateField(auto_now_add=True)
    date_fin = models.DateField(auto_now_add=False)
    
    def __str__(self):
        return f'{self.category} - {self.montant}Fcfa'

    def suivre_depenses(self):
        """
        Retourne les détails des dépenses associées à ce budget :
        - Total des dépenses
        - Reste disponible
        - Statut (OK ou DÉPASSÉ)
        """
        depenses = Depense.objects.filter(
            categorie=self.category,
            date__range=[self.date_debut, self.date_fin]
        )
        total_depenses = depenses.aggregate(total=Sum('montant'))['total'] or 0
        reste = self.montant - total_depenses
        statut = "OK" if reste >= 0 else "DÉPASSÉ"
        return {
            "total_depenses": total_depenses,
            "reste": reste,
            "statut": statut,
        }