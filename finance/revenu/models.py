from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from source.models import Source
# Create your models here.

class Revenu(models.Model):
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    montant = models.FloatField()
    source = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.source} - {self.montant} €"
    
    
    @classmethod
    def revenus_par_source(cls, user):
        """
        Calcule les revenus totaux regroupés par source.
        """
        return cls.objects.filter(owner=user).values('source').annotate(total=Sum('montant')).order_by('source')