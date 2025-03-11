from datetime import date
import locale
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Sum
from .models import Epargne, ObjectifEpargne

# Create your views here.

def add_epargne(request):
    if  request.method == "POST":
        montant = request.POST["montant"]
        Epargne.objects.create(owner=request.user, montant=montant)
        # messages.info(request, "epargne ajouté")
        return redirect('epargnes')
    return render(request, "epargne/add-epargne.html")

def epargnes(request):
    epargnes = Epargne.objects.filter(owner=request.user)
    current_month = date.today().month
    epargne_mois = Epargne.objects.filter(date__month=current_month)
    total_epargne = epargne_mois.aggregate(Sum("montant"))
    total = total_epargne['montant__sum']
    context = {
        'epargnes': epargnes,
        'epargne_mois': epargne_mois,
        'total_epargne': total,
    }
    return render(request, "epargne/epargnes.html", context)

def update_epargne(request, id):
    epargne = Epargne.objects.get(id=id)
    context = {
        'epargne': epargne
    }
    if request.method == "POST":
        montant = request.POST["montant"]
        epargne.montant = montant
        epargne.save()
        # messages.info(request, "epargne modifié")
        return redirect('epargnes')
    return render(request, "epargne/update-epargne.html", context)

def delete_epargne(request, id):
    epargne = Epargne.objects.get(id=id)
    epargne.delete()
    return redirect('epargnes')

def suivi_epargne(request):
    # Récupérer l'objectif mensuel (ou créer un par défaut)
    objectif, created = ObjectifEpargne.objects.get_or_create(owner=request.user)  # Un seul objectif pour toute l'application
    
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    mois_courant = date.today().strftime("%Y-%m")
    current_month = date.today().strftime("%B")
    epargne_mensuelle = Epargne.objects.filter(owner=request.user, date__startswith=mois_courant).aggregate(Sum('montant'))['montant__sum'] or 0

    message = ""
    if epargne_mensuelle >= objectif.montant:
        send_mail(
            "Finance Personnel", #Title
            "Objectif d'epargne atteint", #Message
            "settings.EMAIL_HOST_USER",
            [request.user.email], #receiver email    
            fail_silently=False
        )
    else :
        send_mail(
            "Finance Personnel", #Title
            "Objectif d'épargne non atteint", #Message
            "settings.EMAIL_HOST_USER",
            [request.user.email], #receiver email
            fail_silently=False
        )
    # if request.method == 'POST':
    #     if 'montant' in request.POST:  # Ajouter une épargne
    #         montant = request.POST.get('montant')
    #         try:
    #             montant = float(montant)
    #             if montant > 0:
    #                 Epargne.objects.create(montant=montant)  # Créer une nouvelle épargne
    #                 message = f"✅ {montant} € ajoutés à votre épargne."
    #                 # return redirect('suivi_epargne')  # Rediriger après l'ajout
    #             else:
    #                 message = "❌ Le montant doit être supérieur à 0."
    #         except ValueError:
    #             message = "❌ Veuillez entrer un montant valide."
    #     elif 'nouvel_objectif' in request.POST:  # Modifier l'objectif
    #         nouvel_objectif = request.POST.get('nouvel_objectif')
    #         try:
    #             nouvel_objectif = float(nouvel_objectif)
    #             if nouvel_objectif > 0:
    #                 objectif.montant = nouvel_objectif
    #                 objectif.save()
    #                 message = f"✅ Nouvel objectif mensuel défini : {nouvel_objectif} €."
    #             else:
    #                 message = "❌ L'objectif doit être supérieur à 0."
    #         except ValueError:
    #             message = "❌ Veuillez entrer un montant valide pour l'objectif."

    context = {
        'epargne_mensuelle': epargne_mensuelle,
        'objectif_mensuel': objectif.montant,
        'mois_courant': current_month,
        'epargnes': Epargne.objects.filter(owner=request.user),
        'message': message,
    }
    return render(request, 'epargne/suivi_epargne.html', context)

def definir_epargne(request):
    objectif, created = ObjectifEpargne.objects.get_or_create(id=1)  # Un seul objectif pour toute l'application
    message = ""
    if request.method == 'POST':
        if 'nouvel_objectif' in request.POST:  # Modifier l'objectif
            nouvel_objectif = request.POST.get('nouvel_objectif')
            try:
                nouvel_objectif = float(nouvel_objectif)
                if nouvel_objectif > 0:
                    objectif.montant = nouvel_objectif
                    objectif.owner = request.user
                    objectif.save()
                    message = f"✅ Nouvel objectif mensuel défini : {nouvel_objectif} €."
                    return redirect('epargnes')
                else:
                    message = "❌ L'objectif doit être supérieur à 0."
            except ValueError:
                message = "❌ Veuillez entrer un montant valide pour l'objectif."
    context = {
        'message': message,
    }
    return render(request, 'epargne/definir_epargne.html', context)
