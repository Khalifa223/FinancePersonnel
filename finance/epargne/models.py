from pyexpat import model
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Epargne(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    montant = models.FloatField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.montant}'

class ObjectifEpargne(models.Model):
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=500)  # Valeur par défaut = 500 €

    class Meta:
        verbose_name = "Objectif d'épargne"
        verbose_name_plural = "Objectifs d'épargne"

    def __str__(self):
        return f"Objectif mensuel : {self.montant} €"
