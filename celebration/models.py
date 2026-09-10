from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class EventSite(models.Model):
    couple_names = models.CharField(max_length=120, default="Abdelrahman & Omnia")
    event_title = models.CharField(
        max_length=160,
        default="Engagement Celebration",
        help_text="The public title of the celebration shown in the hero and page metadata.",
    )
    eyebrow = models.CharField(max_length=120, default="Together, always")
    hero_title = models.CharField(max_length=180, default="Our Forever Begins Here")
    hero_subtitle = models.CharField(
        max_length=240,
        default="We would be delighted to celebrate this beautiful chapter with you.",
    )
    event_datetime = models.DateTimeField(help_text="Date and time used across the site and countdown.")
    venue_name = models.CharField(max_length=180, default="The Celebration Venue")
    venue_address = models.CharField(max_length=255, default="Cairo, Egypt")
    maps_url = models.URLField(blank=True)

    hero_image = models.ImageField(
        upload_to="hero/",
        blank=True,
        help_text="Desktop hero image. Recommended: landscape image, at least 2000px wide.",
    )
    hero_mobile_image = models.ImageField(
        upload_to="hero/mobile/",
        blank=True,
        help_text="Optional mobile hero image. Recommended: portrait 4:5 or 9:16.",
    )

    intro_enabled = models.BooleanField(
        default=True,
        help_text="Show the cinematic opening once per browser session.",
    )
    intro_title = models.CharField(
        max_length=120,
        blank=True,
        default="",
        help_text="Leave empty to use the couple names.",
    )
    intro_subtitle = models.CharField(
        max_length=180,
        blank=True,
        default="A celebration of love, family & forever",
    )

    music_enabled = models.BooleanField(
        default=False,
        help_text="Enable background music and the visitor music controls.",
    )
    music_file = models.FileField(
        upload_to="music/",
        blank=True,
        help_text="Upload an MP3/M4A/OGG file. This takes priority over Music URL.",
    )
    music_url = models.URLField(
        blank=True,
        help_text="Optional direct audio URL if you do not upload a file.",
    )
    music_title = models.CharField(
        max_length=120,
        blank=True,
        default="Our song",
        help_text="Label shown beside the music control.",
    )
    music_loop = models.BooleanField(default=True)

    invitation_note = models.TextField(
        blank=True,
        default="Your presence will make our day even more memorable.",
    )
    instagram_url = models.URLField(blank=True)
    is_rsvp_open = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def music_source(self):
        if self.music_file:
            return self.music_file.url
        return self.music_url

    class Meta:
        verbose_name = "Event Site"
        verbose_name_plural = "Event Site"

    def __str__(self):
        return self.couple_names


class StoryMoment(models.Model):
    event = models.ForeignKey(EventSite, on_delete=models.CASCADE, related_name="story_moments")
    order = models.PositiveSmallIntegerField(default=0)
    date_label = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=600)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    event = models.ForeignKey(EventSite, on_delete=models.CASCADE, related_name="gallery_items")
    image = models.ImageField(
        upload_to="gallery/",
        help_text="Use high-resolution JPG/WebP images. The site loads gallery images lazily.",
    )
    alt_text = models.CharField(max_length=180, default="Celebration photo")
    caption = models.CharField(
        max_length=240,
        blank=True,
        help_text="Optional sentence shown with this image and inside the lightbox.",
    )
    order = models.PositiveSmallIntegerField(default=0, help_text="Lower numbers appear first.")

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.caption or self.alt_text


class RSVP(models.Model):
    class Attendance(models.TextChoices):
        YES = "yes", "Joyfully attending"
        NO = "no", "Regretfully declining"

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    attendance = models.CharField(max_length=3, choices=Attendance.choices)
    guests = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(8)],
    )
    message = models.TextField(max_length=800, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_attendance_display()}"
