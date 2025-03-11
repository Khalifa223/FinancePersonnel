from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from category.models import Category
from budget.models import Budget

# Create your views here.

def add_budget(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    if  request.method == "POST":
        montant = request.POST["montant"]
        category = request.POST["category"]
        date_fin = request.POST["date"]
        Budget.objects.create(owner=request.user, montant=montant, category=category, date_fin=date_fin)
        return redirect('budgets')
    return render(request, "budget/add-budget.html", context)

def budgets(request):
    budgets = Budget.objects.all()
    context = {'budgets': budgets}
    return render(request, "budget/budgets.html", context)

def update_budget(request, id):
    budget = Budget.objects.get(id=id)
    categories = Category.objects.all()
    if request.method == "POST":
        montant = request.POST["montant"]
        category = request.POST["category"]
        date_fin = request.POST["date"]
        budget.montant = montant
        budget.category = category
        budget.date_fin = date_fin
        budget.save()
        return redirect('budgets')
    context = {
        'budget': budget,
        'categories': categories,
        'id': id
    }
    return render(request, "budget/update-budget.html", context)

def delete_budget(request, id):
    budget = Budget.objects.get(id=id)
    budget.delete()
    return redirect('budgets')


def suivi_budget(request):
    budgets = Budget.objects.all()
    suivi = []

    for budget in budgets:
        details = budget.suivre_depenses()
        suivi.append({
            "category": budget.category,
            "montant": budget.montant,
            "date_debut": budget.date_debut,
            "date_fin": budget.date_fin,
            "total_depenses": details["total_depenses"],
            "reste": details["reste"],
            "statut": details["statut"]
        })
        if details["reste"] < 0:
            send_mail(
                "Finance Personnel", #Title
                f"Vous avez dépassé le budget établit pour {budget.category}", #Message
                "settings.EMAIL_HOST_USER",
                ['khalifacoders@gmail.com'], #receiver email
                fail_silently=False
            )

    context = {
        "suivi": suivi,
    }
    return render(request, "budget/suivi_budget.html", context)