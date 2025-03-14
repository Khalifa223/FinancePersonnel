from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages

from category.models import Category
from budget.models import Budget
from revenu.models import Revenu
from .models import Depense

# Create your views here.

@login_required
def add_depense(request):
    categories = Category.objects.all()
    budgets = Budget.objects.all()
    context = {
            'categories': categories,
            'budgets': budgets
    }
    if  request.method == "POST":
        montant = request.POST["montant"]
        description = request.POST["description"]
        categorie = request.POST["categorie"]
        if not categorie:
            messages.info(request, "La categorie est obligatoire.")
            return redirect('add-depense')
        if Budget.objects.get(category=categorie):
            messages.info(request, "La catégorie existe")
            return redirect('add-depense')
        if not montant:
            messages.info(request, "Le montant est obligatoire. ")
            return redirect('add-depense')
        if not description:
            messages.info(request, "La description de la dépense est obligatoire.")
            return redirect('add-depense')
        depense = Depense(owner=request.user, montant=montant, description=description, categorie=categorie)
        depense.save()
        messages.success(request, "Votre dépense a été ajouté avec succè   s")
        return redirect('depenses')
    return render(request, "depense/add-depense.html", context)

@login_required
def depenses(request):
    depenses = Depense.objects.filter(owner=request.user)
    montant_depense = Depense.objects.aggregate(total=Sum("montant"))
    context = {'depenses': depenses, 'montant_depense': montant_depense}
    return render(request, "depense/depenses.html", context)

@login_required
def update_depense(request, id):
    depense = Depense.objects.get(id=id)
    categories = Category.objects.all()
    context = {
        'depense': depense,
        'categories': categories
    }
    if request.method == "POST":
        montant = request.POST["montant"]
        categorie = request.POST["categorie"]
        description = request.POST["description"]
        if not categorie:
            messages.error(request, "La categorie est obligatoire.")
            return redirect("update-depense", depense.id)
        if not montant:
            messages.error(request, "Le montant est obligatoire. ")
            return redirect("update-depense", depense.id)
        if not description:
            messages.error(request, "La description de la dépense est obligatoire.")
            return redirect("update-depense", depense.id)
        depense.montant = montant
        depense.categorie = categorie
        depense.description = description
        depense.save()
        # messages.info(request, "Depense modifié")
        return redirect('depenses')
    return render(request, "depense/update-depense.html", context)

@login_required
def delete_depense(request, id):
    depense = Depense.objects.get(id=id)
    depense.delete()
    return redirect('depenses')

@login_required
def dashboard(request):
    depenses = Depense.objects.all()
    montant_depense = Depense.objects.all().aggregate(total=Sum("montant"))
    montant_revenu = Revenu.objects.all().aggregate(total=Sum("montant"))
    revenu = montant_revenu["total"]
    depense = montant_depense["total"]
    solde = revenu - depense
    context = {
        'depenses': depenses,
        'montant_depense': montant_depense,
        'montant_revenu': montant_revenu,
        'solde': solde
    }
    return render(request, "depense/data.html", context)

@login_required
def depenses_par_categorie(request):
    # Obtenir les dépenses totales par catégorie
    depenses = Depense.depenses_par_categorie(request.user)

    # Préparer les données pour le graphique
    categories = [item['categorie'] for item in depenses]
    valeurs = [item['total'] for item in depenses]
    context = {
        "categories": categories,
        "valeurs": valeurs,
    }
    return render(request, "depense/depenses_chart.html", context)