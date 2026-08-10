from django.shortcuts import get_object_or_404, render

from .models import Affiliation, Character, Domain, Race, StoryFragment, Region


def home(request):
  return render(request, 'index.html')


def codex(request):
  return render(request, 'codex.html')


def atlas(request):
  return render(request, 'atlas.html')


def characters(request):
  character_list = (
    Character.objects.select_related('race', 'birthplace', 'affiliation')
    .prefetch_related('story_fragments', 'trivia_entries')
    .order_by('name')
  )
  return render(request, 'characters/list.html', {'characters': character_list})


def character_detail(request, slug):
  character = get_object_or_404(
    Character.objects.select_related('race', 'birthplace__domain', 'affiliation')
    .prefetch_related('story_fragments', 'trivia_entries', 'gallery_images'),
    slug=slug,
  )
  return render(request, 'characters/detail.html', {'character': character})


def races(request):
  race_list = Race.objects.prefetch_related('regions').order_by('name')
  return render(request, 'races/list.html', {'races': race_list})

def race_detail(request, slug):
  race = get_object_or_404(
    Race.objects.prefetch_related('regions'),
    slug=slug,
  )

  return render(request, 'races/detail.html', {'race': race})


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
    Affiliation.objects.prefetch_related('regions', 'gallery_images'),
    slug=slug,
  )
  return render(request, 'affiliations/detail.html', {'affiliation': affiliation})


def domains(request):
  domain_list = Domain.objects.prefetch_related('regions').order_by('name')
  return render(request, 'domains/list.html', {'domains': domain_list})


def chronicles(request):
  story_fragments = StoryFragment.objects.filter(is_world_story=True).order_by('title', 'id')
  return render(request, 'chronicles/list.html', {'story_fragments': story_fragments})



def submerges(request):
  return render(request, 'submerges.html')


def domain_detail(request, slug):
  domain = get_object_or_404(
    Domain.objects.prefetch_related('regions'),
    slug=slug,
  )

  return render(request, 'domains/detail.html', {'domain': domain})

def character_story_detail(request, character_slug, story_slug):
  character = get_object_or_404(Character, slug=character_slug)
  fragment = get_object_or_404(
    StoryFragment.objects.prefetch_related('characters'),
    slug=story_slug,
    characters=character,
  )
  return_to = request.GET.get('return_to')
  return render(
    request,
    'characters/story_detail.html',
    {'fragment': fragment, 'character': character, 'return_to': return_to},
  )

def chronicle_detail(request, slug):
  fragment = get_object_or_404(
    StoryFragment,
    slug=slug,
    is_world_story=True,
  )
  return_to = request.GET.get('return_to')
  return render(request, 'chronicles/detail.html', {'fragment': fragment, 'return_to': return_to})


def storyfragment_detail(request, slug):
  fragment = get_object_or_404(StoryFragment, slug=slug)
  template = 'chronicles/detail.html'
  return_to = request.GET.get('return_to')
  return render(request, template, {'fragment': fragment, 'return_to': return_to})

def region_detail(request, slug):
  region = get_object_or_404(
    Region.objects.select_related('domain'),
    slug=slug,
  )
  return render(request, 'domains/region_detail.html', {'region': region})


def not_found(request, unused=None):
  return render(request, '404.html', status=404)