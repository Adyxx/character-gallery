from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('codex/', views.codex, name='codex'),
    path('atlas/', views.atlas, name='atlas'),
    path('characters/', views.characters, name='characters'),
    path('characters/<slug:slug>/', views.character_detail, name='character_detail'),
    path('characters/<slug:character_slug>/<slug:story_slug>/', views.character_story_detail, name='character_story_detail'),

    path('races/', views.races, name='races'),
    path('races/<slug:slug>/', views.race_detail, name='race_detail'),
    path('submerges/', views.submerges, name='submerges'),
    path('affiliations/', views.affiliations, name='affiliations'),
    path('affiliations/<slug:slug>/', views.affiliation_detail, name='affiliation_detail'),
    path('domains/', views.domains, name='domains'),
    path(
    "domains/<slug:slug>/",
    views.domain_detail,
    name="domain_detail",
    ),
    path('regions/<slug:slug>/', views.region_detail, name='region_detail'),
    path('chronicles/', views.chronicles, name='chronicles'),
    path('chronicles/<slug:slug>/', views.chronicle_detail, name='chronicle_detail'),
    path('story/<slug:slug>/', views.storyfragment_detail, name='storyfragment_detail'),
]