from django.urls import path
from depense import views

urlpatterns = [
    path("", views.depenses, name="depenses"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_depense, name="add-depense"),
    path("depense-par-categorie-chat/", views.depenses_par_categorie, name="depenses-par-categorie"),
    path("update/<int:id>/", views.update_depense, name="update-depense"),
    path("delete/<int:id>/", views.delete_depense, name="delete-depense")
]