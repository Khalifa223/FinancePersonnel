from django.contrib import admin
from .models import Epargne, ObjectifEpargne

# Register your models here.

class EpargneAdmin(admin.ModelAdmin):
    list_display = ('montant', 'date')
    
class ObjectifEpargneAdmin(admin.ModelAdmin):
    list_display = ('montant',)
    
admin.site.register(Epargne, EpargneAdmin)
admin.site.register(ObjectifEpargne, ObjectifEpargneAdmin)