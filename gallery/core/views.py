from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.urls import reverse

from .models import Affiliation, Character, Domain, Fauna, Flora, Race, Region, StoryFragment, Submerge, Landmark


def home(request):
  return render(request, 'index.html')


def codex(request):
  return render(request, 'codex.html')


def atlas(request):
  return render(request, 'atlas.html')


def characters(request):
    character_list = (
        Character.objects.select_related('race', 'birthplace', 'affiliation')
        .prefetch_related('stories', 'trivia_entries')
        .order_by('name')
    )
    return render(request, 'characters/list.html', {'characters': character_list})


def character_detail(request, slug):
    character = get_object_or_404(
        Character.objects.select_related('race', 'birthplace__domain', 'affiliation')
        .prefetch_related('stories', 'trivia_entries', 'gallery_images'),
        slug=slug,
    )
    return render(request, 'characters/detail.html', {'character': character})


def races(request):
  race_list = Race.objects.prefetch_related('regions').order_by('name')
  return render(request, 'races/list.html', {'races': race_list})

def race_detail(request, slug):
    race = get_object_or_404(
        Race.objects.prefetch_related('regions__domain', 'stories', 'trivia_entries', 'gallery_images'),
        slug=slug
    )

    representatives = Character.objects.filter(
        race=race
    ).select_related('affiliation').order_by('name')

    context = {
        'race': race,
        'representatives': representatives,
    }
    return render(request, 'races/detail.html', context)


def affiliations(request):
  domains = Domain.objects.prefetch_related('regions__affiliations').order_by('name')
  grouped_affiliations = []
  seen_affiliation_ids = set()

  for domain in domains:
    affiliations = (
      Affiliation.objects.filter(regions__domain=domain)
      .distinct()
      .order_by('name')
    )
    grouped_affiliations.append({'domain': domain, 'affiliations': affiliations})
    seen_affiliation_ids.update(affiliation.id for affiliation in affiliations)

  unassigned_affiliations = (
    Affiliation.objects.exclude(id__in=seen_affiliation_ids)
    .order_by('name')
  )

  return render(
    request,
    'affiliations/list.html',
    {
      'grouped_affiliations': grouped_affiliations,
      'unassigned_affiliations': unassigned_affiliations,
    },
  )


def affiliation_detail(request, slug):
    affiliation = get_object_or_404(
        Affiliation.objects.prefetch_related('regions__domain', 'stories', 'trivia_entries', 'gallery_images'),
        slug=slug
    )

    members = Character.objects.filter(
        affiliation=affiliation
    ).select_related('birthplace').order_by('name')

    context = {
        'affiliation': affiliation,
        'members': members,
    }
    return render(request, 'affiliations/detail.html', context)

def domains(request):
  domain_list = Domain.objects.prefetch_related('regions').order_by('name')
  return render(request, 'domains/list.html', {'domains': domain_list})


def chronicles(request):
  story_fragments = StoryFragment.objects.filter(is_world_story=True).order_by('title', 'id')
  return render(request, 'chronicles/list.html', {'story_fragments': story_fragments})


def submerges(request):
    submerge_list = Submerge.objects.prefetch_related('flora_set', 'fauna_set').order_by('name')
    return render(request, 'submerges/submerges.html', {'submerges': submerge_list})

def documented_submerges(request):
    submerge_list = Submerge.objects.prefetch_related('discovered_in').order_by('name')
    return render(request, 'submerges/list.html', {'submerges': submerge_list})

def submerge_detail(request, slug):
    submerge = get_object_or_404(
        Submerge.objects.select_related('category', 'discovered_in__domain')
        .prefetch_related('stories', 'trivia_entries', 'gallery_images'),
        slug=slug
    )

    exclusive_flora = submerge.flora_set.all()
    exclusive_creatures = submerge.fauna_set.all()

    context = {
        'submerge': submerge,
        'exclusive_flora': exclusive_flora,
        'exclusive_creatures': exclusive_creatures,
    }
    return render(request, 'submerges/detail.html', context)

def flora(request):
    flora_list = Flora.objects.prefetch_related('exclusive_to_submerge', 'found_in_regions').order_by('name')
    return render(request, 'flora/flora.html', {'flora': flora_list})

def fauna(request):
    fauna_list = Fauna.objects.prefetch_related('exclusive_to_submerge', 'found_in_regions').order_by('name')
    return render(request, 'fauna/fauna.html', {'fauna': fauna_list})

def flora_detail(request, slug):
    flora = get_object_or_404(
        Flora.objects.select_related('exclusive_to_submerge')
        .prefetch_related('traits', 'found_in_regions__domain', 'stories', 'trivia_entries', 'gallery_images'),
        slug=slug
    )

    context = {
        'flora': flora,
    }
    return render(request, 'flora/detail.html', context)

def fauna_detail(request, slug):
    fauna = get_object_or_404(
        Fauna.objects.select_related('exclusive_to_submerge')
        .prefetch_related('found_in_regions__domain', 'stories', 'trivia_entries', 'gallery_images'),
        slug=slug
    )

    context = {
        'fauna': fauna,
    }
    return render(request, 'fauna/detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Domain, Character, Landmark

def domain_detail(request, slug):
    domain = get_object_or_404(
        Domain.objects.select_related('ruler')
        .prefetch_related('regions', 'stories', 'trivia_entries', 'gallery_images'),
        slug=slug
    )
    
    capital = Landmark.objects.filter(
        region__domain=domain, 
        type='CITY',
        is_capital=True
    ).select_related('region').first()

    notable_people = Character.objects.filter(
        affiliation__regions__domain=domain
    ).select_related('affiliation').distinct()[:6]

    context = {
        'domain': domain,
        'capital': capital,
        'notable_people': notable_people,
    }
    return render(request, 'domains/detail.html', context)


def region_detail(request, domain_slug, region_slug):
    region = get_object_or_404(
        Region.objects.select_related('domain')
        .prefetch_related('affiliations', 'stories', 'trivia_entries', 'gallery_images'),
        slug=region_slug,
        domain__slug=domain_slug
    )
    

    landmarks = Landmark.objects.filter(region=region)
    
    local_capital = landmarks.filter(type='CITY', is_capital=True).first()

    local_submerges = Submerge.objects.filter(discovered_in=region).select_related('category')

    local_flora = Flora.objects.filter(found_in_regions=region)
    local_creatures = Fauna.objects.filter(found_in_regions=region)

    local_people = Character.objects.filter(
        affiliation__regions=region
    ).select_related('affiliation').distinct()

    context = {
        'region': region,
        'landmarks': landmarks,
        'local_capital': local_capital,
        'local_submerges': local_submerges,
        'local_flora': local_flora,
        'local_creatures': local_creatures,
        'local_people': local_people,
    }
    return render(request, 'domains/region_detail.html', context)


def landmark_detail(request, domain_slug, region_slug, landmark_slug):
    landmark = get_object_or_404(
        Landmark.objects.select_related('region__domain')
        .prefetch_related('stories', 'trivia_entries', 'gallery_images'),
        slug=landmark_slug,
        region__slug=region_slug,
        region__domain__slug=domain_slug
    )
    

    context = {
        'landmark': landmark,
    }
    return render(request, 'domains/landmark_detail.html', context) 

def character_story_detail(request, character_slug, story_slug):
    character = get_object_or_404(Character, slug=character_slug)
    fragment = get_object_or_404(
        StoryFragment,
        slug=story_slug,
        character=character,
    )
    
    return_to = request.GET.get('return_to')
    return render(
        request,
        'characters/story_detail.html',
        {'fragment': fragment, 'character': character, 'return_to': return_to},
    )


def chronicle_detail(request, slug):
    fragment = get_object_or_404(StoryFragment, slug=slug, is_world_story=True)
    return_to = request.GET.get('return_to')
    return render(request, 'chronicles/detail.html', {
        'fragment': fragment, 
        'return_to': return_to
    })





def not_found(request, unused=None):
  return render(request, '404.html', status=404)


def global_search_api(request):
  query = request.GET.get('q', '').strip()
  results = []

  def add_result(title, subtitle, url):
    results.append({'title': title, 'subtitle': subtitle, 'url': url})

  #if len(query) < 2:
   # return JsonResponse({'results': results})

  character_matches = (
    Character.objects.filter(Q(name__icontains=query) | Q(title__icontains=query))
    .order_by('name')[:5]
  )
  for character in character_matches:
    character_url = character.get_absolute_url()
    character_name = character.name or 'Character'
    add_result(character_name, 'Character', character_url)
    add_result(f'{character_name} / Resonance', 'Character Tab', f'{character_url}#resonance')
    add_result(f'{character_name} / Logbook', 'Character Tab', f'{character_url}#logbook')
    add_result(f'{character_name} / Trivia', 'Character Tab', f'{character_url}#trivia')

  race_matches = Race.objects.filter(name__icontains=query).order_by('name')[:5]
  for race in race_matches:
    add_result(f'{race.name}', 'Race', race.get_absolute_url())

  affiliation_matches = Affiliation.objects.filter(name__icontains=query).order_by('name')[:5]
  for affiliation in affiliation_matches:
    add_result(f'{affiliation.name}', 'Affiliation', affiliation.get_absolute_url())

  domain_matches = Domain.objects.filter(name__icontains=query).order_by('name')[:5]
  for domain in domain_matches:
    add_result(f'{domain.name}', 'Domain', domain.get_absolute_url())

  region_matches = Region.objects.select_related('domain').filter(name__icontains=query).order_by('name')[:5]
  for region in region_matches:
    if not region.domain or not region.slug or not region.domain.slug:
      continue

    region_url = reverse(
      'core:region_detail',
      kwargs={'domain_slug': region.domain.slug, 'region_slug': region.slug},
    )
    add_result(
      f'{region.name}',
      f'Region of {region.domain.name or "Domain"}',
      region_url,
    )

  submerge_matches = Submerge.objects.filter(name__icontains=query).order_by('name')[:5]
  for submerge in submerge_matches:
    add_result(f'{submerge.name}', 'Submerge', submerge.get_absolute_url())

  flora_matches = Flora.objects.filter(name__icontains=query).order_by('name')[:5]
  for flora in flora_matches:
    add_result(f'{flora.name}', 'Flora', flora.get_absolute_url())

  fauna_matches = Fauna.objects.filter(name__icontains=query).order_by('name')[:5]
  for fauna in fauna_matches:
    add_result(f'{fauna.name}', 'Fauna', fauna.get_absolute_url())

  landmark_matches = Landmark.objects.select_related('region__domain').filter(name__icontains=query).order_by('name')[:5]
  for landmark in landmark_matches:
    if not landmark.region or not landmark.region.domain or not landmark.slug or not landmark.region.slug or not landmark.region.domain.slug:
      continue

    landmark_url = reverse(
      'core:landmark_detail',
      kwargs={
        'domain_slug': landmark.region.domain.slug,
        'region_slug': landmark.region.slug,
        'landmark_slug': landmark.slug,
      },
    )
    add_result(
      f'{landmark.name}',
      f'Landmark of {landmark.region.name or "Region"}',
      landmark_url,
    )


  story_matches = (
    StoryFragment.objects.filter(is_world_story=True, title__icontains=query)
    .order_by('title')[:5]
  )
  for fragment in story_matches:
    add_result(f'{fragment.title}', 'Chronicle', fragment.get_absolute_url())

  return JsonResponse({'results': results})