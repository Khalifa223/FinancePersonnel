from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from category.models import Category
# Create your models here.

class Depense(models.Model):
    montant = models.FloatField()
    categorie = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    
    # def __str__(self):
    #     return f'{self.categorie}'
    
    @classmethod
    def depenses_par_categorie(cls, user):
        """
        Retourne les dépenses totales regroupées par catégorie pour un utilisateur donné.
        """
        return cls.objects.filter(owner=user).values('categorie').annotate(total=Sum('montant')).order_by('categorie')