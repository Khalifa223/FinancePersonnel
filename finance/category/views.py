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
        category = Category(name=name)
        category.save()
        return redirect('categorys')
    return render(request, "category/add-category.html")

def updateCategory(request, id):
    category = Category.objects.get(id=id)
    if request.method == "POST":
        name = request.POST["name"]
        category.name = name
        category.save()
        return redirect('categorys')
    context = {"category": category, "id": id}
    return render(request, "category/update-category.html", context)

def deleteCategory(request, id):
    category = Category.objects.get(id=id)
    category.delete()
    return redirect('categorys')
 
def category(request, id):
    category = Category.objects.get(id=id)
    context = {
        'category': category,
        'id': id
    }
    return render(request, "category/category.html", context)