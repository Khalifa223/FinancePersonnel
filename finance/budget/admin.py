from django.contrib import admin
from .models import Budget

# Register your models here.

class BudgetAdmin(admin.ModelAdmin):
    list_display = ('category', 'montant', 'date_debut', 'date_fin')
    
admin.site.register(Budget, BudgetAdmin)