from multiprocessing import context
from django.shortcuts import redirect, render
from .models import Category
from django.contrib import messages

# Create your views here.

def allCategory(request):
    categorys = Category.objects.all()
    context = {'categorys': categorys}
    return render(request, "category/categorys.html", context)

def addCategory(request):
    if request.method == "POST":
        name = request.POST["name"]
        if Category.objects.filter(name=name).exists():
            messages.error(request, "Cet nom de catégorie existe déjà")
            return redirect("add-category")
        if not name:
            messages.error(request, "Le nom de la catégorie est obligatoire")
            return redirect("add-category")
        category = Category(name=name)
        category.save()
        messages.success(request, "Votre catégorie a été ajouté")
        return redirect('categorys')
    return render(request, "category/add-category.html")

def updateCategory(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        name = request.POST["name"]
        if not name:
            messages.error(request, "Le nom de la catégorie est obligatoire")
            return redirect("update-category", category.id)
        category.name = name
        category.save()
        messages.info(request, "Votre catégorie a été modifié")
        return redirect('categorys')
    context = {"category": category, "id": id}
    return render(request, "category/update-category.html", context)

def deleteCategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    messages.info(request, "Votre catégorie a été supprimé")
    return redirect('categorys')
 
def category(request, id):
    category = Category.objects.get(id=id)
    context = {
        'category': category,
        'id': id
    }
    return render(request, "category/category.html", context)