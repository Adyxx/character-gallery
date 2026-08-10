from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class SluggedModel(models.Model):
  slug_source_fields = ()
  slug_fallback = None

  class Meta:
    abstract = True

  def _generate_slug(self):
    for field_name in self.slug_source_fields:
      value = getattr(self, field_name, None)
      if value:
        slug = slugify(value)
        if slug:
          return slug

    if self.slug_fallback:
      fallback_slug = slugify(self.slug_fallback)
      if fallback_slug:
        return fallback_slug

    return ""

  def save(self, *args, **kwargs):
    if not self.slug:
      base_slug = self._generate_slug()
      if base_slug:
        slug = base_slug
        suffix = 2
        manager = self.__class__.objects
        while manager.filter(slug=slug).exclude(pk=self.pk).exists():
          slug = f"{base_slug}-{suffix}"
          suffix += 1
        self.slug = slug

    super().save(*args, **kwargs)


class GenderChoices(models.TextChoices):
  MALE = "male", "Male"
  FEMALE = "female", "Female"
  NON_BINARY = "non_binary", "Non-binary"
  OTHER = "other", "Other"
  UNKNOWN = "unknown", "Unknown"


class ImportanceChoices(models.TextChoices):
  PROTAGONIST = "protagonist", "Protagonist"
  SUPPORTING = "supporting", "Supporting"
  NPC = "npc", "NPC"


class ExpressionChoices(models.TextChoices):
  INTERNAL = "internal", "Internal / Battery"
  EXTERNAL = "external", "External / Projector"
  LATENT = "latent", "Latent / Dormant"
  HARMONIC = "harmonic", "Harmonic / Weaver"


class CoherenceStateChoices(models.TextChoices):
  ANCHORED = "anchored", "Anchored / Intact (100%)"
  FRAYED = "frayed", "Frayed / Displaced"
  FRACTURED = "fractured", "Fractured / Distorted"
  DISSOLVED = "dissolved", "Dissolved"


class Region(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "region"

  domain = models.ForeignKey(
    "Domain",
    on_delete=models.SET_NULL,
    related_name="regions",
    blank=True,
    null=True,
  )
  name = models.CharField(max_length=255, blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)
  about = models.TextField(blank=True, null=True)

  def get_absolute_url(self):
    return reverse(
        "core:region_detail",
        kwargs={"slug": self.slug},
    )
  
  def __str__(self):
    return self.name or "Region"


class Domain(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "domain"

  name = models.CharField(max_length=255, blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)
  about = models.TextField(blank=True, null=True)

  def get_absolute_url(self):
    return reverse(
        "core:domain_detail",
        kwargs={"slug": self.slug},
    )

  def __str__(self):
    return self.name or "Domain"

class Race(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "race"

  name = models.CharField(max_length=255, blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)
  about = models.TextField(blank=True, null=True)
  symbol = models.ImageField(upload_to="media/race_symbols/", blank=True, null=True)
  regions = models.ManyToManyField(Region, blank=True, related_name="races")

  def get_absolute_url(self):
      return reverse(
        "core:race_detail",
        kwargs={"slug": self.slug},
  )
  
  def __str__(self):
    return self.name or "Race"


class Affiliation(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "affiliation"

  name = models.CharField(max_length=255, blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)
  about = models.TextField(blank=True, null=True)
  symbol = models.ImageField(upload_to="media/affiliation_symbols/", blank=True, null=True)
  regions = models.ManyToManyField(Region, blank=True, related_name="affiliations")

  def get_absolute_url(self):
      return reverse(
      "core:affiliation_detail",
        kwargs={"slug": self.slug},
  )

  def __str__(self):
    return self.name or "Affiliation"


class StoryFragment(SluggedModel):
  slug_source_fields = ("title",)
  slug_fallback = "story-fragment"

  title = models.CharField(max_length=255, blank=True, null=True)
  image = models.ImageField(upload_to="media/story_images/", blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)
  text = models.TextField(blank=True, null=True)
  is_world_story = models.BooleanField(default=False)

  def get_absolute_url(self):
      return reverse(
        "core:storyfragment_detail",
        kwargs={"slug": self.slug},
  )

  def __str__(self):
    return self.title or "Story Fragment"


class TriviaEntry(SluggedModel):
  slug_source_fields = ("title",)
  slug_fallback = "trivia-entry"

  title = models.CharField(max_length=255, blank=True, null=True)
  text = models.CharField(max_length=500, blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)

  def get_absolute_url(self):
      return reverse(
        "core:triviaentry_detail",
        kwargs={"slug": self.slug},
  )

  def __str__(self):
    return self.text or "Trivia Entry"


class Character(SluggedModel):
  slug_source_fields = ("name", "title")
  slug_fallback = "character"

  name = models.CharField(max_length=255, blank=True, null=True)
  slug = models.SlugField(unique=True, blank=True)
  title = models.CharField(max_length=255, blank=True, null=True)
  gender = models.CharField(
    max_length=32,
    choices=GenderChoices.choices,
    blank=True,
    null=True,
  )
  race = models.ForeignKey(
    Race,
    on_delete=models.SET_NULL,
    related_name="characters",
    blank=True,
    null=True,
  )
  role = models.CharField(max_length=255, blank=True, null=True)
  importance = models.CharField(
    max_length=32,
    choices=ImportanceChoices.choices,
    blank=True,
    null=True,
  )
  age = models.IntegerField(blank=True, null=True)
  height = models.CharField(max_length=255, blank=True, null=True)
  birthday = models.CharField(max_length=255, blank=True, null=True)
  birthplace = models.ForeignKey(
    Region,
    on_delete=models.SET_NULL,
    related_name="birthplace_characters",
    blank=True,
    null=True,
  )
  affiliation = models.ForeignKey(
    Affiliation,
    on_delete=models.SET_NULL,
    related_name="characters",
    blank=True,
    null=True,
  )
  about = models.TextField(blank=True, null=True)
  submerge_mutation_notes = models.TextField(blank=True, null=True)
  display_image = models.ImageField(upload_to="media/character_display_images/", blank=True, null=True)
  icon_image = models.ImageField(upload_to="media/character_icon_images/", blank=True, null=True)
  expression = models.CharField(
    max_length=32,
    choices=ExpressionChoices.choices,
    blank=True,
    null=True,
  )
  coherence_state = models.CharField(
    max_length=32,
    choices=CoherenceStateChoices.choices,
    blank=True,
    null=True,
  )
  story_fragments = models.ManyToManyField(
    StoryFragment,
    blank=True,
    related_name="characters",
  )
  trivia_entries = models.ManyToManyField(
    TriviaEntry,
    blank=True,
    related_name="characters",
  )

  def get_absolute_url(self):
      return reverse(
          "core:character_detail",
          kwargs={"slug": self.slug},
      )
  
  def __str__(self):
    return self.name or "Character"


class GalleryImage(models.Model):
  image = models.ImageField(upload_to="media/gallery_images/", blank=True, null=True)
  caption = models.CharField(max_length=255, blank=True, null=True)
  character = models.ForeignKey(
    Character,
    on_delete=models.CASCADE,
    related_name="gallery_images",
    blank=True,
    null=True,
  )
  affiliation = models.ForeignKey(
    Affiliation,
    on_delete=models.CASCADE,
    related_name="gallery_images",
    blank=True,
    null=True,
  )
  region = models.ForeignKey(
    Region,
    on_delete=models.CASCADE,
    related_name="gallery_images",
    blank=True,
    null=True,
  )
  domain = models.ForeignKey(
    Domain,
    on_delete=models.CASCADE,
    related_name="gallery_images",
    blank=True,
    null=True,
  )

  def __str__(self):
    return self.caption or "Gallery Image"

from django.db import models

class SubmergeCategory(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "submerge-category"

  name = models.CharField(max_length=100)
  slug = models.SlugField(unique=True)

class Submerge(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "submerge"

  HAZARD_CHOICES = [
      ('SAFE', 'Safe / Stable'),
      ('MILD', 'Mild / Unpredictable'),
      ('HIGH', 'High Hazard'),
      ('LETHAL', 'Lethal / Reality Dissolving'),
  ]
  
  INFLUENCE_CHOICES = [
      ('BENEFICIAL', 'Beneficial / Harvestable'),
      ('NEUTRAL', 'Neutral / Distorting'),
      ('DESTRUCTIVE', 'Destructive / Corrosive'),
  ]

  name = models.CharField(max_length=200)
  slug = models.SlugField(unique=True, blank=True)
  category = models.ForeignKey(SubmergeCategory, on_delete=models.PROTECT)
  hazard_level = models.CharField(max_length=10, choices=HAZARD_CHOICES, default='MILD')
  influence_nature = models.CharField(max_length=15, choices=INFLUENCE_CHOICES, default='NEUTRAL')
  description = models.TextField()
  
  discovered_in = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True, blank=True)


class FloraPropertyTag(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "flora-property-tag"

  name = models.CharField(max_length=50)
  slug = models.SlugField(unique=True)

class Flora(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "flora"

  AVAILABILITY_CHOICES = [
      ('YEAR_ROUND', 'Year-round'),
      ('SPRING', 'Spring Bloom'),
      ('SUMMER', 'Summer Bloom'),
      ('AUTUMN', 'Autumn Fade'),
      ('WINTER', 'Winter Cryo'),
      ('ANOMALOUS', 'Anomalous Only (No Season)'),
  ]

  name = models.CharField(max_length=200)
  slug = models.SlugField(unique=True, blank=True)
  about = models.TextField()
  availability = models.CharField(max_length=15, choices=AVAILABILITY_CHOICES, default='YEAR_ROUND')
  is_hazardous = models.BooleanField(default=False)
  
  traits = models.ManyToManyField(FloraPropertyTag, blank=True)
  
  found_in_regions = models.ManyToManyField('Region', blank=True)
  exclusive_to_submerge = models.ForeignKey(Submerge, on_delete=models.SET_NULL, null=True, blank=True)

  def get_absolute_url(self):
    return reverse(
        "core:flora_detail",
        kwargs={"slug": self.slug},
    )
  
  def __str__(self):
    return self.name or "Flora"

class Creature(SluggedModel):
  slug_source_fields = ("name",)
  slug_fallback = "creature"

  BEHAVIOR_CHOICES = [
    ('DOCILE', 'Docile / Passive'),
    ('TERRITORIAL', 'Territorial'),
    ('AGGRESSIVE', 'Aggressive Predator'),
    ('ANOMALOUS', 'Anomalous / Unpredictable (Mimic, Phase-shifter)'),
  ]

  DIET = [
    ('HERBIVORE', 'Herbivore'),
    ('CARNIVORE', 'Carnivore'),
    ('ESSENCE_EATER', 'Essence Eater'),
  ]

  name = models.CharField(max_length=200)
  slug = models.SlugField(unique=True, blank=True)
  behavior = models.CharField(max_length=15, choices=BEHAVIOR_CHOICES, default='DOCILE')
  about = models.TextField()
  diet = models.CharField(max_length=100, choices=DIET, default='HERBIVORE')
  
  found_in_regions = models.ManyToManyField('Region', blank=True)
  exclusive_to_submerge = models.ForeignKey(Submerge, on_delete=models.SET_NULL, null=True, blank=True)

  def get_absolute_url(self):
    return reverse(
        "core:creature_detail",
        kwargs={"slug": self.slug},
    )
  
  def __str__(self):
    return self.name or "Creature"
