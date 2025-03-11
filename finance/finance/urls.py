from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("account.urls")),
    path("budget/", include("budget.urls")),
    path("category/", include("category.urls")),
    path("depense/", include("depense.urls")),
    path("epargne/", include("epargne.urls")),
    path("revenu/", include("revenu.urls")),
    path("source/", include("source.urls"))
]
