from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('characters/', views.characters, name='characters'),
    path('characters/<str:character_name>/', views.character_detail, name='character_detail'),
    path('races/', views.races, name='races'),
    path('races/<str:race_name>/', views.race_detail, name='race_detail'),
    path('afflictations/', views.afflictations, name='afflictations'),
    path('afflictations/<str:afflictation_name>/', views.affliction_detail, name='affliction_detail'),
    path('domains/', views.domains, name='domains'),
    path('domains/<str:domain_name>/', views.domain_detail, name='domain_detail'),
    path(
        'domains/<str:domain_name>/<str:territory_name>/',
        views.territory_detail,
        name='territory_detail',
    ),
]