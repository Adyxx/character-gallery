from django.shortcuts import get_object_or_404, render

from .models import Affiliation, Character, Domain, Race, Territory


def home(request):
  return render(request, 'index.html')


def characters(request):
  character_list = (
    Character.objects.select_related('race', 'birthplace', 'affiliation')
    .prefetch_related('story_fragments', 'trivia_entries')
    .order_by('name')
  )
  return render(request, 'characters/list.html', {'characters': character_list})


def character_detail(request, character_name):
  character = get_object_or_404(
    Character.objects.select_related('race', 'birthplace__domain', 'affiliation')
    .prefetch_related('story_fragments', 'trivia_entries', 'gallery_images'),
    name__iexact=character_name,
  )
  return render(request, 'characters/detail.html', {'character': character})


def races(request):
  race_list = Race.objects.prefetch_related('territories').order_by('name')
  return render(request, 'races/list.html', {'races': race_list})


def race_detail(request, race_name):
  race = get_object_or_404(Race.objects.prefetch_related('territories', 'gallery_images'), name__iexact=race_name)
  return render(request, 'races/detail.html', {'race': race})


def afflictations(request):
  domains = Domain.objects.prefetch_related('territories__affiliations').order_by('name')
  grouped_affiliations = []
  seen_affiliation_ids = set()

  for domain in domains:
    affiliations = (
      Affiliation.objects.filter(territories__domain=domain)
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
    'afflictations/list.html',
    {
      'grouped_affiliations': grouped_affiliations,
      'unassigned_affiliations': unassigned_affiliations,
    },
  )


def affliction_detail(request, afflictation_name):
  affiliation = get_object_or_404(
    Affiliation.objects.prefetch_related('territories', 'gallery_images'),
    name__iexact=afflictation_name,
  )
  return render(request, 'afflictations/detail.html', {'affiliation': affiliation})


def domains(request):
  domain_list = Domain.objects.prefetch_related('territories').order_by('name')
  return render(request, 'domains/list.html', {'domains': domain_list})


def domain_detail(request, domain_name):
  domain = get_object_or_404(Domain.objects.prefetch_related('territories'), name__iexact=domain_name)
  return render(request, 'domains/detail.html', {'domain': domain})


def territory_detail(request, domain_name, territory_name):
  territory = get_object_or_404(
    Territory.objects.select_related('domain'),
    domain__name__iexact=domain_name,
    name__iexact=territory_name,
  )
  return render(request, 'domains/territory_detail.html', {'territory': territory})


def not_found(request, unused=None):
  return render(request, '404.html', status=404)