from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='staff_dashboard'),
    path('logout/', views.logout_staff, name='logout_staff'),
    
    path('ajouter/<str:type_media>/', views.ajouter_media, name='ajouter_media'),
    path("modifier/<int:pk>/", views.modifier_media, name="modifier_media"),
    path("supprimer/<int:pk>/", views.supprimer_media, name="supprimer_media"),
    path("retour/<int:pk>/", views.retour_media, name="retour_media"),
    
    path("emprunteurs/", views.liste_emprunteurs, name="liste_emprunteurs"),
    path("emprunteurs/ajouter/", views.ajouter_emprunteur, name="ajouter_emprunteur"),
    path("emprunteurs/modifier/<int:pk>/", views.modifier_emprunteur, name="modifier_emprunteur"),
    path("emprunteurs/supprimer/<int:pk>/", views.supprimer_emprunteur, name="supprimer_emprunteur"),
    
]
