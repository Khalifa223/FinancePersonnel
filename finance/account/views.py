from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Sum

from revenu.models import Revenu
from depense.models import Depense

from .utils import authenticate

# Create your views here.

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        pass1 = request.POST["password"]
        
        User.objects.create_user(username=username, email=email, password=pass1)
        return redirect('login')
        # messages.info(request, "user created")
    return render(request, "account/register.html")


def loginView(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            # messages.info(request, "user connecté !!!")
            return redirect("home")
        else:
            messages.error(request, 'user non connecté...')
    return render(request, "account/login.html")

def log_out(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    solde = 0
    montant_depense = Depense.objects.all().aggregate(total=Sum("montant"))
    montant_revenu = Revenu.objects.all().aggregate(total=Sum("montant"))
    revenu = montant_revenu["total"]
    depense = montant_depense["total"]
    if depense is not None and revenu is not None:
        solde = revenu - depense
    context = {
        # 'revenus': revenus,
        'montant_revenu': montant_revenu,
        # 'depenses': depenses,
        'montant_depense': montant_depense,
        # 'montant_revenu': montant_revenu,
        'solde': solde
    }
    # send_mail(
    #     "Accueil", #Title
    #     "Bienvenue FinancePersonnel", #Message
    #     "settings.EMAIL_HOST_USER",
    #     ['khalifacoders@gmail.com'], #receiver email
    #     fail_silently=False
    # )
    return render(request, "account/home.html", context)