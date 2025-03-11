from django.contrib import admin
from .models import Revenu
# Register your models here.

class RevenuAdmin(admin.ModelAdmin):
    list_display = ('source', 'montant', 'description', 'date')
    
admin.site.register(Revenu, RevenuAdmin)