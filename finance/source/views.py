from django.shortcuts import redirect, render
from .models import Source
from django.contrib import messages

# Create your views here.

def sources(request):
    sources = Source.objects.all()
    context = {'sources': sources}
    return render(request, "source/sources.html", context)

def add_source(request):
    if request.method == "POST":
        name = request.POST["name"]
        if Source.objects.filter(name=name).exists():
            messages.error(request, "Cet nom de source existe déjà")
            return redirect("add-source")
        if not name:
            messages.error(request, "Le nom de la source est obligatoire")
            return redirect("add-source")
        source = Source(name=name)
        source.save()
        return redirect('sources')
    return render(request, "source/add-source.html")

def update_source(request, id):
    source = Source.objects.get(id=id)
    if request.method == "POST":
        name = request.POST["name"]
        if not name:
            messages.error(request, "Le nom de la source est obligatoire")
            return redirect("update-source", source.id)
        source.name = name
        source.save()
        messages.info(request, "Votre source a été modifié")
        return redirect('sources')
    context = {"source": source, "id": id}
    return render(request, "source/update-source.html", context)

def delete_source(request, id):
    source = Source.objects.get(id=id)
    source.delete()
    return redirect('sources')
