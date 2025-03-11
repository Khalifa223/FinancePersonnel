from django.urls import path
from epargne import views

urlpatterns = [
    path("", views.epargnes, name="epargnes"),
    path("add/", views.add_epargne, name="add-epargne"),
    path("suivi/", views.suivi_epargne, name="suivi-epargne"),
    path("definir/", views.definir_epargne, name="definir-epargne"),
    path("update/<int:id>/", views.update_epargne, name="update-epargne"),
    path("delete/<int:id>/", views.delete_epargne, name="delete-epargne")
]