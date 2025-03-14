from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
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
        if len(pass1) < 8:
            messages.error(request, "Le mot de passe est doit etre superieur a 8 caracteres.")
            return redirect("register")
        try:
            if User.objects.get(email = email):
                messages.info(request, "Cet email est deja pris")
                return redirect("register")
        except:
            pass
        try:
            if User.objects.get(username = username):
                messages.info(request, "Ce nom d'utilisateur est deja pris")
                return redirect("register")        
        except:
            pass
        User.objects.create_user(username=username, email=email, password=pass1)
        messages.success(request, "L'utilisateur a ete creee avec success")
        return redirect('login')
    return render(request, "account/register.html")


def loginView(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, "L'utilisateur connecte avec succes")
            return redirect("home")
        else:
            messages.error(request, 'Votre email ou mot de passe est incorrect')
    return render(request, "account/login.html")

def log_out(request):
    logout(request)
    return redirect('login')

@login_required
def index(request):
    solde = 0
    montant_depense = Depense.objects.filter(owner=request.user).aggregate(total=Sum("montant"))
    montant_revenu = Revenu.objects.filter(owner=request.user).aggregate(total=Sum("montant"))
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


# class ChangePasswordView(PasswordChangeView):
#     form_class = PasswordChangeForm
#     success_url = reverse_lazy('home')
#     template_name = 'account/change_password.html'

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(user=request.user, data=request.POST)
        print("########################################################")
        print(form)
        print("########################################################")
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "✅ Votre mot de passe a été modifié avec succès !")
            return redirect('change_password')
        else:
            messages.error(request, "❌ Une erreur s'est produite. Vérifiez vos informations.")
    else:
        form = PasswordChangeForm(user=request.user)

    context={'form': form}
    return render(request, 'account/change_password.html', context)
