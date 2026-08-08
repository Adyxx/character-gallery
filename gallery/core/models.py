from django.db import models


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


class Territory(models.Model):
  domain = models.ForeignKey(
    "Domain",
    on_delete=models.SET_NULL,
    related_name="territories",
    blank=True,
    null=True,
  )
  name = models.CharField(max_length=255, blank=True, null=True)
  about = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name or "Territory"


class Domain(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
  about = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.name or "Domain"


class Race(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
  about = models.TextField(blank=True, null=True)
  symbol = models.ImageField(upload_to="media/race_symbols/", blank=True, null=True)
  territories = models.ManyToManyField(Territory, blank=True, related_name="races")

  def __str__(self):
    return self.name or "Race"


class Affiliation(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
  about = models.TextField(blank=True, null=True)
  symbol = models.ImageField(upload_to="media/affiliation_symbols/", blank=True, null=True)
  territories = models.ManyToManyField(Territory, blank=True, related_name="affiliations")

  def __str__(self):
    return self.name or "Affiliation"


class StoryFragment(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  text = models.TextField(blank=True, null=True)

  def __str__(self):
    return self.title or "Story Fragment"


class TriviaEntry(models.Model):
  text = models.CharField(max_length=500, blank=True, null=True)

  def __str__(self):
    return self.text or "Trivia Entry"


class Character(models.Model):
  name = models.CharField(max_length=255, blank=True, null=True)
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
    Territory,
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
  territory = models.ForeignKey(
    Territory,
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
