from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from category.models import Category
from budget.models import Budget

# Create your views here.

@login_required
def add_budget(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    if  request.method == "POST":
        montant = request.POST["montant"]
        category = request.POST["category"]
        date_fin = request.POST["date"]
        if Budget.objects.filter(category=category).exists():
            messages.info(request, "Cette catégorie existe")
            return redirect("add-budget")
        if not montant:
            messages.error(request, "Le montant est obligatoire")
            return redirect("add-budget")
        if not category:
            messages.error(request, "La catégorie est obligatoire")
            return redirect("add-budget")
        if not date_fin:
            messages.error(request, "La date de fin est obligatoire")
            return redirect("add-budget")
        Budget.objects.create(owner=request.user, montant=montant, category=category, date_fin=date_fin)
        messages.success(request, "Le budget a été ajouté avec succès")
        return redirect('budgets')
    return render(request, "budget/add-budget.html", context)

@login_required
def budgets(request):
    budgets = Budget.objects.filter(owner=request.user)      
    context = {'budgets': budgets}
    return render(request, "budget/budgets.html", context)

@login_required
def update_budget(request, id):
    budget = Budget.objects.get(id=id)
    date_fin = budget.date_fin.strftime("%Y-%m-%d") if budget.date_fin else ""
    categories = Category.objects.all()
    if request.method == "POST":
        montant = request.POST.get("montant").replace(",", ".")
        category = request.POST["category"]
        date_fin = request.POST["date"]
        if Budget.objects.filter(category=category).exists():
            messages.info(request, "Cette catégorie existe")
            return redirect("add-budget")
        if not montant:
            messages.error(request, "Le montant est obligatoire")
            return redirect("update-budget", budget.id)
        if not category:
            messages.error(request, "La catégorie est obligatoire")
            return redirect("update-budget", budget.id)
        if not date_fin:
            messages.error(request, "La date de fin est obligatoire")
            return redirect("update-budget", budget.id)
        budget.montant = montant
        budget.category = category
        budget.date_fin = date_fin
        budget.save()
        messages.info(request, "Votre budget a été modifié")
        return redirect('budgets')
    context = {
        'budget': budget,
        'categories': categories,
        "date_fin": date_fin,
        'id': id
    }
    return render(request, "budget/update-budget.html", context)

@login_required
def delete_budget(request, id):
    budget = Budget.objects.get(id=id)
    budget.delete()
    messages.info(request, "Votre budget a été supprimé")
    return redirect('budgets')

@login_required
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
                f"Vous avez dépassé le budget    pour {budget.category}", #Message
                "settings.EMAIL_HOST_USER",
                ['khalifacoders@gmail.com'], #receiver email
                fail_silently=False
            )

    context = {
        "suivi": suivi,
    }
    return render(request, "budget/suivi_budget.html", context)