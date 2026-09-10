# Generated manually for the initial project scaffold.
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="EventSite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("couple_names", models.CharField(default="Khaled & Huda", max_length=120)),
                ("eyebrow", models.CharField(default="Together, always", max_length=120)),
                ("hero_title", models.CharField(default="Our Forever Begins Here", max_length=180)),
                ("hero_subtitle", models.CharField(default="We would be delighted to celebrate this beautiful chapter with you.", max_length=240)),
                ("event_datetime", models.DateTimeField()),
                ("venue_name", models.CharField(default="The Celebration Venue", max_length=180)),
                ("venue_address", models.CharField(default="Cairo, Egypt", max_length=255)),
                ("maps_url", models.URLField(blank=True)),
                ("hero_image", models.ImageField(blank=True, upload_to="hero/")),
                ("invitation_note", models.TextField(blank=True, default="Your presence will make our day even more memorable.")),
                ("instagram_url", models.URLField(blank=True)),
                ("is_rsvp_open", models.BooleanField(default=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={"verbose_name": "Event Site", "verbose_name_plural": "Event Site"},
        ),
        migrations.CreateModel(
            name="RSVP",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30)),
                ("attendance", models.CharField(choices=[("yes", "Joyfully attending"), ("no", "Regretfully declining")], max_length=3)),
                ("guests", models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(8)])),
                ("message", models.TextField(blank=True, max_length=800)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="StoryMoment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("date_label", models.CharField(blank=True, max_length=80)),
                ("title", models.CharField(max_length=120)),
                ("description", models.TextField(max_length=600)),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="story_moments", to="celebration.eventsite")),
            ],
            options={"ordering": ["order", "id"]},
        ),
        migrations.CreateModel(
            name="GalleryItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("image", models.ImageField(upload_to="gallery/")),
                ("alt_text", models.CharField(default="Celebration photo", max_length=180)),
                ("caption", models.CharField(blank=True, max_length=180)),
                ("order", models.PositiveSmallIntegerField(default=0)),
                ("event", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="gallery_items", to="celebration.eventsite")),
            ],
            options={"ordering": ["order", "id"]},
        ),
    ]
