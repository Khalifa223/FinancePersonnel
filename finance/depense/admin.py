from django.contrib import admin
from .models import Depense
# Register your models here.

class DepenseAdmin(admin.ModelAdmin):
    list_display = ('categorie', 'montant', 'description', 'date')
    
admin.site.register(Depense, DepenseAdmin)