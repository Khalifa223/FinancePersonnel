from django.urls import path
from category import views

urlpatterns = [
    path("", views.allCategory, name="categorys"),
    path("add/", views.addCategory, name="add-category"),
    path("read/<int:id>/", views.category, name="read-category"),
    path("update/<int:id>/", views.updateCategory, name="update-category"),
    path("delete/<int:id>/", views.deleteCategory, name="delete-category")
]