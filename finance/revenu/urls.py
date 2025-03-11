from django.urls import path
from revenu import views

urlpatterns = [
    path("", views.revenus, name="revenus"),
    # path("dashboard/", views.dashboard, name="dashboard"),
    path("add/", views.add_revenu, name="add-revenu"),
    path('revenus-par-source/', views.revenus_par_source, name='revenus_par_source'),
    path("update/<int:id>/", views.update_revenu, name="update-revenu"),
    path("delete/<int:id>/", views.delete_revenu, name="delete-revenu")
]