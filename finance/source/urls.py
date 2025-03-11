from django.urls import path
from source import views

urlpatterns = [
    path("", views.sources, name="sources"),
    path("add/", views.add_source, name="add-source"),
    path("update/<int:id>/", views.update_source, name="update-source"),
    path("delete/<int:id>/", views.delete_source, name="delete-source")
]