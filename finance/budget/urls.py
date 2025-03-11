from django.urls import path
from budget import views

urlpatterns = [
    path("", views.budgets, name="budgets"),
    path("add/", views.add_budget, name="add-budget"),
    path('suivi-budget/', views.suivi_budget, name='suivi_budget'),
    path("update/<int:id>/", views.update_budget, name="update-budget"),
    path("delete/<int:id>/", views.delete_budget, name="delete-budget")
]