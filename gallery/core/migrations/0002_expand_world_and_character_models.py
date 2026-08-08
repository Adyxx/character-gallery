# Generated manually to expand the core data model.

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Affiliation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                (
                    "symbol",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/affiliation_symbols/",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Domain",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("about", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Race",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                (
                    "symbol",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="media/race_symbols/",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StoryFragment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("text", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Territory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=255, null=True)),
                ("about", models.TextField(blank=True, null=True)),
                (
                    "domain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="territories",
                        to="core.domain",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TriviaEntry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.AddField(
            model_name="race",
            name="territories",
            field=models.ManyToManyField(blank=True, related_name="races", to="core.territory"),
        ),
        migrations.AddField(
            model_name="affiliation",
            name="territories",
            field=models.ManyToManyField(blank=True, related_name="affiliations", to="core.territory"),
        ),
        migrations.AddField(
            model_name="character",
            name="about",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="age",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="affiliation",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="characters",
                to="core.affiliation",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="birthday",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="birthplace",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="birthplace_characters",
                to="core.territory",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="coherence_state",
            field=models.CharField(blank=True, choices=[("anchored", "Anchored / Intact (100%)"), ("frayed", "Frayed / Displaced"), ("fractured", "Fractured / Distorted"), ("dissolved", "Dissolved")], max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="display_image",
            field=models.ImageField(blank=True, null=True, upload_to="media/character_display_images/"),
        ),
        migrations.AddField(
            model_name="character",
            name="expression",
            field=models.CharField(blank=True, choices=[("internal", "Internal / Battery"), ("external", "External / Projector"), ("latent", "Latent / Dormant"), ("harmonic", "Harmonic / Weaver")], max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="gender",
            field=models.CharField(blank=True, choices=[("male", "Male"), ("female", "Female"), ("non_binary", "Non-binary"), ("other", "Other"), ("unknown", "Unknown")], max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="height",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="icon_image",
            field=models.ImageField(blank=True, null=True, upload_to="media/character_icon_images/"),
        ),
        migrations.AddField(
            model_name="character",
            name="importance",
            field=models.CharField(blank=True, choices=[("protagonist", "Protagonist"), ("supporting", "Supporting"), ("npc", "NPC")], max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name="character",
            name="name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="race",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="characters",
                to="core.race",
            ),
        ),
        migrations.AddField(
            model_name="character",
            name="role",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="story_fragments",
            field=models.ManyToManyField(blank=True, related_name="characters", to="core.storyfragment"),
        ),
        migrations.AddField(
            model_name="character",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="character",
            name="trivia_entries",
            field=models.ManyToManyField(blank=True, related_name="characters", to="core.triviaentry"),
        ),
        migrations.CreateModel(
            name="GalleryImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    models.ImageField(blank=True, null=True, upload_to="media/gallery_images/"),
                ),
                ("caption", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "affiliation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="core.affiliation",
                    ),
                ),
                (
                    "character",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="core.character",
                    ),
                ),
                (
                    "domain",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="core.domain",
                    ),
                ),
                (
                    "territory",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="gallery_images",
                        to="core.territory",
                    ),
                ),
            ],
        ),
    ]