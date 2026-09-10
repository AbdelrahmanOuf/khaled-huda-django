from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator
from django.db import models
from django.urls import reverse


hex_color_validator = RegexValidator(
    regex=r"^#[0-9A-Fa-f]{6}$",
    message="Enter a valid six-digit HEX color, for example #BB7D72.",
)


class EventSite(models.Model):
    """The single content and appearance configuration for the public website."""

    # Identity and SEO
    couple_names = models.CharField(max_length=120, default="Abdelrahman & Omnia")
    event_title = models.CharField(
        max_length=160,
        default="Engagement Celebration",
        help_text="The public celebration title used in the page title and throughout the site.",
    )
    brand_symbol = models.CharField(
        max_length=8,
        default="♡",
        help_text="A short decorative symbol used in the header, hero and footer.",
    )
    seo_description = models.CharField(
        max_length=300,
        blank=True,
        help_text="Search and social description. Leave empty to use the hero subtitle.",
    )
    social_share_image = models.ImageField(
        upload_to="branding/social/",
        blank=True,
        help_text="Optional image used when the website is shared. Recommended: 1200 × 630 px.",
    )
    site_icon = models.ImageField(
        upload_to="branding/icon/",
        blank=True,
        help_text="Optional browser icon. A square PNG or WebP works best.",
    )

    # Navigation
    navigation_enabled = models.BooleanField(default=True)
    nav_story_label = models.CharField(max_length=40, default="Our story")
    nav_gallery_label = models.CharField(max_length=40, default="Moments")
    nav_details_label = models.CharField(max_length=40, default="Details")
    nav_rsvp_label = models.CharField(max_length=40, default="RSVP")

    # Hero
    eyebrow = models.CharField(max_length=120, default="Together, always")
    hero_title = models.CharField(max_length=180, default="Our Forever Begins Here")
    hero_subtitle = models.CharField(
        max_length=240,
        default="We would be delighted to celebrate this beautiful chapter with you.",
    )
    hero_primary_button_label = models.CharField(max_length=70, default="Confirm attendance")
    hero_secondary_button_label = models.CharField(max_length=70, default="View celebration details")
    discover_label = models.CharField(max_length=40, default="Discover")
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

    # Date and venue
    event_datetime = models.DateTimeField(help_text="Date and time used across the site and countdown.")
    venue_name = models.CharField(max_length=180, default="The Celebration Venue")
    venue_address = models.CharField(max_length=255, default="Cairo, Egypt")
    maps_url = models.URLField(blank=True)

    # Cinematic intro
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
    intro_skip_label = models.CharField(max_length=30, default="Skip")

    # Save the date
    save_date_enabled = models.BooleanField(default=True)
    save_date_kicker = models.CharField(max_length=80, default="Save the date")
    save_date_title = models.CharField(max_length=120, default="One beautiful day,")
    save_date_title_accent = models.CharField(max_length=120, default="one forever.")
    invitation_note = models.TextField(
        blank=True,
        default="Your presence will make our day even more memorable.",
    )
    countdown_enabled = models.BooleanField(default=True)
    countdown_days_label = models.CharField(max_length=24, default="Days")
    countdown_hours_label = models.CharField(max_length=24, default="Hours")
    countdown_minutes_label = models.CharField(max_length=24, default="Minutes")
    countdown_seconds_label = models.CharField(max_length=24, default="Seconds")

    # Story
    story_enabled = models.BooleanField(default=True)
    story_kicker = models.CharField(max_length=100, default="A story worth keeping")
    story_title = models.CharField(max_length=120, default="Our story")
    story_intro = models.TextField(
        max_length=500,
        default=(
            "Some chapters begin quietly. Ours became the kind of story we wanted "
            "to celebrate with the people we love most."
        ),
    )

    # Quote
    quote_enabled = models.BooleanField(default=True)
    quote_text = models.CharField(
        max_length=300,
        default="And suddenly, every love song made sense.",
    )

    # Gallery
    gallery_enabled = models.BooleanField(default=True)
    gallery_kicker = models.CharField(max_length=100, default="Captured with love")
    gallery_title = models.CharField(max_length=120, default="Our favorite")
    gallery_title_accent = models.CharField(max_length=120, default="moments.")
    gallery_intro = models.TextField(
        max_length=500,
        default="A collection of the memories we love most.",
    )

    # Event details
    details_enabled = models.BooleanField(default=True)
    details_kicker = models.CharField(
        max_length=120,
        blank=True,
        help_text="Leave empty to use the event title.",
    )
    details_title = models.CharField(max_length=120, default="Where forever")
    details_title_accent = models.CharField(max_length=120, default="begins.")
    details_intro = models.TextField(
        max_length=500,
        default="Everything you need for an effortless arrival and a beautiful evening with us.",
    )
    date_card_label = models.CharField(max_length=60, default="Date & time")
    venue_card_label = models.CharField(max_length=60, default="Venue")
    maps_button_label = models.CharField(max_length=80, default="Open in Google Maps")
    note_card_label = models.CharField(max_length=60, default="A little note")
    note_card_title = models.CharField(max_length=140, default="Come ready to celebrate")
    note_card_text = models.TextField(
        max_length=500,
        default="Your presence is the only gift we need. Bring your smile and stay for the memories.",
    )

    # RSVP
    rsvp_section_enabled = models.BooleanField(default=True)
    is_rsvp_open = models.BooleanField(default=True)
    rsvp_kicker = models.CharField(max_length=80, default="Kindly reply")
    rsvp_title = models.CharField(max_length=120, default="Will you")
    rsvp_title_accent = models.CharField(max_length=120, default="join us?")
    rsvp_intro = models.TextField(
        max_length=500,
        default=(
            "We would be delighted to celebrate this chapter with you. Please send "
            "your response so we can prepare everything beautifully."
        ),
    )
    rsvp_form_title = models.CharField(max_length=60, default="RSVP")
    rsvp_form_subtitle = models.CharField(max_length=160, default="Please complete the form below.")
    rsvp_name_label = models.CharField(max_length=60, default="Your name")
    rsvp_phone_label = models.CharField(max_length=60, default="Phone")
    rsvp_guests_label = models.CharField(max_length=60, default="Guests")
    rsvp_attendance_label = models.CharField(max_length=80, default="Will you attend?")
    rsvp_message_label = models.CharField(max_length=80, default="A message for us")
    rsvp_optional_label = models.CharField(max_length=40, default="Optional")
    rsvp_submit_label = models.CharField(max_length=80, default="Send RSVP")
    rsvp_name_placeholder = models.CharField(max_length=100, default="Your name")
    rsvp_phone_placeholder = models.CharField(max_length=100, default="+20 ...")
    rsvp_message_placeholder = models.CharField(
        max_length=160,
        default="Write a note for the couple…",
    )
    rsvp_attending_option = models.CharField(max_length=100, default="Joyfully attending")
    rsvp_declining_option = models.CharField(max_length=100, default="Regretfully declining")
    rsvp_max_guests = models.PositiveSmallIntegerField(
        default=8,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        help_text="Maximum guests allowed in one response (1–20).",
    )
    rsvp_success_message = models.CharField(
        max_length=240,
        default="Thank you — your RSVP has been received.",
    )
    rsvp_closed_message = models.CharField(
        max_length=240,
        default="RSVP is currently closed. Thank you for celebrating with us.",
    )

    # Background music
    music_enabled = models.BooleanField(
        default=False,
        help_text="Enable background music and the visitor music controls.",
    )
    music_autoplay = models.BooleanField(
        default=True,
        help_text=(
            "Try to start music as soon as the website opens. If the browser blocks "
            "audible autoplay, an elegant one-tap entry prompt is shown."
        ),
    )
    music_volume = models.PositiveSmallIntegerField(
        default=55,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Initial music volume from 0 to 100.",
    )
    music_start_prompt = models.CharField(
        max_length=160,
        default="Tap to begin the celebration with music",
        help_text="Shown only when the visitor's browser blocks automatic sound.",
    )
    music_start_button_label = models.CharField(max_length=60, default="Enter with music")
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

    # Footer and social links
    footer_enabled = models.BooleanField(default=True)
    footer_left_label = models.CharField(max_length=60, default="With love")
    footer_right_label = models.CharField(max_length=60, default="Forever")
    footer_note = models.CharField(
        max_length=240,
        default="Thank you for being part of our story.",
    )
    instagram_url = models.URLField(blank=True)
    instagram_label = models.CharField(max_length=60, default="Instagram")

    # Appearance
    text_color = models.CharField(max_length=7, default="#211C19", validators=[hex_color_validator])
    page_background_color = models.CharField(max_length=7, default="#FBF7F2", validators=[hex_color_validator])
    soft_background_color = models.CharField(max_length=7, default="#F3E9E1", validators=[hex_color_validator])
    accent_color = models.CharField(max_length=7, default="#BB7D72", validators=[hex_color_validator])
    accent_dark_color = models.CharField(max_length=7, default="#895B52", validators=[hex_color_validator])
    dark_section_color = models.CharField(max_length=7, default="#2D2724", validators=[hex_color_validator])

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def music_source(self):
        if self.music_file:
            return self.music_file.url
        return self.music_url

    @property
    def page_description(self):
        return self.seo_description or self.hero_subtitle

    @property
    def share_image(self):
        return self.social_share_image or self.hero_image

    @property
    def details_kicker_text(self):
        return self.details_kicker or self.event_title

    def clean(self):
        super().clean()
        if EventSite.objects.exclude(pk=self.pk).exists():
            raise ValidationError("Only one Event Site configuration can exist.")

    def get_absolute_url(self):
        return reverse("home")

    class Meta:
        verbose_name = "Event Site"
        verbose_name_plural = "Event Site"

    def __str__(self):
        return self.couple_names


class StoryMoment(models.Model):
    event = models.ForeignKey(EventSite, on_delete=models.CASCADE, related_name="story_moments")
    is_visible = models.BooleanField(default=True)
    order = models.PositiveSmallIntegerField(default=0, db_index=True)
    date_label = models.CharField(max_length=80, blank=True)
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=600)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class GalleryItem(models.Model):
    class ImagePosition(models.TextChoices):
        CENTER = "center center", "Center"
        TOP = "center top", "Top"
        BOTTOM = "center bottom", "Bottom"
        LEFT = "left center", "Left"
        RIGHT = "right center", "Right"

    event = models.ForeignKey(EventSite, on_delete=models.CASCADE, related_name="gallery_items")
    is_visible = models.BooleanField(default=True)
    image = models.ImageField(
        upload_to="gallery/",
        help_text="Use a high-resolution JPG, PNG or WebP image.",
    )
    image_position = models.CharField(
        max_length=20,
        choices=ImagePosition.choices,
        default=ImagePosition.CENTER,
        help_text="Controls which part of the image remains visible when it is cropped.",
    )
    title = models.CharField(
        max_length=140,
        blank=True,
        help_text="Main title displayed on the photo.",
    )
    caption = models.TextField(
        max_length=500,
        blank=True,
        help_text="Optional sentence displayed below the photo title and in the lightbox.",
    )
    alt_text = models.CharField(
        max_length=180,
        default="Celebration photo",
        help_text="A short image description for accessibility and search engines.",
    )
    order = models.PositiveSmallIntegerField(
        default=0,
        db_index=True,
        help_text="Lower numbers appear first.",
    )

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title or self.caption or self.alt_text


class RSVP(models.Model):
    class Attendance(models.TextChoices):
        YES = "yes", "Joyfully attending"
        NO = "no", "Regretfully declining"

    name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    attendance = models.CharField(max_length=3, choices=Attendance.choices)
    guests = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
    )
    message = models.TextField(max_length=800, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_attendance_display()}"
