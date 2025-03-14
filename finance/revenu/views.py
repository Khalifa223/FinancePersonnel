from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from source.models import Source
from .models import Revenu

# Create your views here.

@login_required
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
        if not source:
            messages.info(request, "La source est obligatoire.")
            return redirect('add-revenu')
        # if Source.objects.filter(name=source).exists():
        #     messages.info(request, "La source existe déjà")
        #     return redirect('add-revenu')
        if not montant:
            messages.info(request, "Le montant est obligatoire. ")
            return redirect('add-revenu')
        if not description:
            messages.info(request, "La description du revenu est obligatoire.")
            return redirect('add-revenu')
        Revenu.objects.create(owner=request.user, montant=montant, source=source, description=description)
        messages.success(request, "Votre revenu a été ajouté")
        return redirect('revenus')
    return render(request, "revenu/add-revenu.html", context)

@login_required
def revenus(request):
    revenus = Revenu.objects.filter(owner=request.user)
    montant_revenu = Revenu.objects.aggregate(total=Sum("montant"))
    context = {'revenus': revenus, 'montant_revenu': montant_revenu}
    return render(request, "revenu/revenus.html", context)

@login_required
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
        if not montant:
            messages.error(request, "Le montant est obligatoire. ")
            return redirect('update-revenu', revenu.id)
        if not description:
            messages.error(request, "La description du revenu est obligatoire.")
            return redirect('update-revenu', revenu.id)
        revenu.montant = montant
        revenu.source = source
        revenu.description = description
        revenu.save()
        messages.info(request, "Votre revenu a été modifié")
        return redirect('revenus')
    return render(request, "revenu/update-revenu.html", context)

@login_required
def delete_revenu(request, id):
    revenu = Revenu.objects.get(id=id)
    revenu.delete()
    messages.info(request, "Votre revenu a été supprimé")
    return redirect('revenus')

@login_required
def revenus_par_source(request):
    # Obtenir les revenus par source
    revenus = Revenu.revenus_par_source(request.user)

    # Préparer les données pour le graphique
    sources = [item['source'] for item in revenus]
    montants = [item['total'] for item in revenus]

    context = {
        "sources": sources,
        "montants": montants,
    }
    return render(request, "revenu/revenus_chart.html", context)