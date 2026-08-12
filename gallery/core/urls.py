from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('codex/', views.codex, name='codex'),
    path('atlas/', views.atlas, name='atlas'),

    path('characters/', views.characters, name='characters'), # list of characters
    path('characters/<slug:slug>/', views.character_detail, name='character_detail'), # detail of a character
    path('characters/<slug:character_slug>/<slug:story_slug>/', views.character_story_detail, name='character_story_detail'), # detail of a story fragment for a character

    path('races/', views.races, name='races'), # list of races
    path('races/<slug:slug>/', views.race_detail, name='race_detail'), # detail of a race

    path('submerges/', views.submerges, name='submerges_info'), # info about what is a submerge/history
    path('submerges/documented/', views.documented_submerges, name='submerges'), # list of submerges
    path('submerges/documented/<slug:slug>/', views.submerge_detail, name='submerge_detail'), # detail of a submerge

    path('flora/', views.flora, name='flora'), # info about flora basics, categorization, etc.
    path('fauna/', views.fauna, name='fauna'), # info about fauna basics, categorization, etc.
    path('flora/<slug:slug>/', views.flora_detail, name='flora_detail'), # detail of a flora
    path('fauna/<slug:slug>/', views.fauna_detail, name='fauna_detail'), # detail of a fauna
    # list of flora/fauna on its own will not exist, 
    # the lists will be accessible through the submerge detail page, 
    # the region detail page, and possibly some mention domain detail page.

    path('affiliations/', views.affiliations, name='affiliations'), # info about affiliations and lower list of affiliations ordered per domain/region
    path('affiliations/<slug:slug>/', views.affiliation_detail, name='affiliation_detail'), # detail of an affiliation  

    path('domains/', views.domains, name='domains'), # list of domains
    path("domains/<slug:slug>/", views.domain_detail, name="domain_detail",), # detail of a domain
    path('domains/<slug:domain_slug>/<slug:region_slug>/', views.region_detail, name='region_detail'), # detail of a region
    path('domains/<slug:domain_slug>/<slug:region_slug>/<slug:landmark_slug>/', views.landmark_detail, name='landmark_detail'), # detail of a landmark

    path('chronicles/', views.chronicles, name='chronicles'), # list of chronicles - the world stories
    path('chronicles/<slug:slug>/', views.chronicle_detail, name='chronicle_detail'), # detail of a chronicle - the world story
    
    path('api/search/', views.global_search_api, name='global_search_api'),
]