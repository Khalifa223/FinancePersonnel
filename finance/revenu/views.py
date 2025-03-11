from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum

from source.models import Source
from .models import Revenu

# Create your views here.

def add_revenu(request):
    sources = Source.objects.all()
    montant_revenu = Revenu.objects.aggregate(total=Sum("montant"))
    context = {
        'sources': sources,
        'montant_revenu': montant_revenu
    }
    if  request.method == "POST":
        montant = request.POST["montant"]
        source = request.POST["source"]
        description = request.POST["description"]
        Revenu.objects.create(owner=request.user, montant=montant, source=source, description=description)
        # messages.info(request, "revenu ajouté")
        return redirect('revenus')
    return render(request, "revenu/add-revenu.html", context)

def revenus(request):
    revenus = Revenu.objects.all()
    montant_revenu = Revenu.objects.aggregate(total=Sum("montant"))
    context = {'revenus': revenus, 'montant_revenu': montant_revenu}
    return render(request, "revenu/revenus.html", context)

def update_revenu(request, id):
    revenu = Revenu.objects.get(id=id)
    sources = Source.objects.all()
    montant_revenu = Revenu.objects.aggregate(total=Sum("montant"))
    context = {
        'sources': sources,
        'revenu': revenu,
        'montant_revenu': montant_revenu
    }
    if request.method == "POST":
        montant = request.POST["montant"]
        source = request.POST["source"]
        description = request.POST["description"]
        revenu.montant = montant
        revenu.source = source
        revenu.description = description
        revenu.save()
        # messages.info(request, "revenu modifié")
        return redirect('revenus')
    return render(request, "revenu/update-revenu.html", context)

def delete_revenu(request, id):
    revenu = Revenu.objects.get(id=id)
    revenu.delete()
    return redirect('revenus')

# def dashboard(request):
#     revenus = Revenu.objects.all()
#     montant_revenu = Revenu.objects.aggregate(total=Sum("montant"))
#     context = {
#         'revenus': revenus,
#         'montant_revenu': montant_revenu
#     }
#     return render(request, "account/home.html", context)

def revenus_par_source(request):
    # Obtenir les revenus par source
    revenus = Revenu.revenus_par_source()

    # Préparer les données pour le graphique
    sources = [item['source'] for item in revenus]
    montants = [item['total'] for item in revenus]

    context = {
        "sources": sources,
        "montants": montants,
    }
    return render(request, "revenu/revenus_chart.html", context)