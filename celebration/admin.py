from django.contrib import admin
from django.utils.html import format_html

from .models import EventSite, GalleryItem, RSVP, StoryMoment


class StoryMomentInline(admin.StackedInline):
    model = StoryMoment
    extra = 0
    fields = ("order", "date_label", "title", "description")
    classes = ("collapse",)


class GalleryItemInline(admin.StackedInline):
    model = GalleryItem
    extra = 1
    fields = ("order", "image", "preview", "alt_text", "caption")
    readonly_fields = ("preview",)
    show_change_link = True

    @admin.display(description="Image preview")
    def preview(self, obj):
        if not obj or not obj.image:
            return "Upload an image to preview it here."
        return format_html(
            '<img src="{}" alt="" style="width:220px;height:145px;object-fit:cover;border-radius:14px;box-shadow:0 8px 24px rgba(0,0,0,.12);" />',
            obj.image.url,
        )


@admin.register(EventSite)
class EventSiteAdmin(admin.ModelAdmin):
    list_display = ("couple_names", "event_title", "event_datetime", "venue_name", "music_enabled", "is_rsvp_open", "updated_at")
    readonly_fields = ("hero_preview", "hero_mobile_preview", "music_status")
    save_on_top = True
    fieldsets = (
        (
            "Names & Celebration Title",
            {
                "fields": ("couple_names", "event_title", "eyebrow", "hero_title", "hero_subtitle"),
                "description": "Main public wording shown across the website.",
            },
        ),
        (
            "Date, Time & Venue",
            {
                "fields": ("event_datetime", "venue_name", "venue_address", "maps_url"),
                "description": "Changing the date here automatically updates the hero date, Save the Date, countdown and RSVP details.",
            },
        ),
        (
            "Cinematic Intro",
            {
                "fields": ("intro_enabled", "intro_title", "intro_subtitle"),
                "description": "Opening animation shown once per browser session. Leave Intro title empty to use the couple names.",
            },
        ),
        (
            "Hero Images",
            {
                "fields": ("hero_image", "hero_preview", "hero_mobile_image", "hero_mobile_preview"),
                "description": "Desktop: wide landscape image. Mobile: portrait image. You can replace either image at any time.",
            },
        ),
        (
            "Background Music",
            {
                "fields": ("music_enabled", "music_file", "music_url", "music_title", "music_loop", "music_status"),
                "description": "Upload an audio file or add a direct audio URL. Browsers may block sound autoplay until the visitor interacts; the site handles this gracefully with a visible music control.",
            },
        ),
        (
            "Invitation & Social",
            {"fields": ("invitation_note", "instagram_url", "is_rsvp_open")},
        ),
    )
    inlines = [GalleryItemInline, StoryMomentInline]

    @admin.display(description="Desktop hero preview")
    def hero_preview(self, obj):
        if not obj or not obj.hero_image:
            return "No desktop hero image uploaded yet."
        return format_html(
            '<img src="{}" alt="" style="max-width:620px;width:100%;height:270px;object-fit:cover;border-radius:16px;box-shadow:0 10px 32px rgba(0,0,0,.12);" />',
            obj.hero_image.url,
        )

    @admin.display(description="Mobile hero preview")
    def hero_mobile_preview(self, obj):
        if not obj or not obj.hero_mobile_image:
            return "No mobile hero image uploaded yet."
        return format_html(
            '<img src="{}" alt="" style="width:210px;height:300px;object-fit:cover;border-radius:16px;box-shadow:0 10px 32px rgba(0,0,0,.12);" />',
            obj.hero_mobile_image.url,
        )

    @admin.display(description="Music status")
    def music_status(self, obj):
        if not obj:
            return "Save the event first."
        if not obj.music_enabled:
            return "Music is disabled."
        if obj.music_source:
            return format_html('<strong style="color:#2e7d32;">● Ready</strong> — {}', obj.music_title or "Background music")
        return format_html('<strong style="color:#b26a00;">● Enabled, but no audio source has been added.</strong>')


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "caption", "event", "order")
    list_editable = ("order",)
    search_fields = ("caption", "alt_text", "event__couple_names")
    list_filter = ("event",)
    fields = ("event", "order", "image", "thumbnail_large", "alt_text", "caption")
    readonly_fields = ("thumbnail_large",)

    @admin.display(description="Photo")
    def thumbnail(self, obj):
        if not obj.image:
            return "—"
        return format_html('<img src="{}" alt="" style="width:72px;height:52px;object-fit:cover;border-radius:8px;" />', obj.image.url)

    @admin.display(description="Preview")
    def thumbnail_large(self, obj):
        if not obj or not obj.image:
            return "—"
        return format_html('<img src="{}" alt="" style="max-width:520px;width:100%;max-height:360px;object-fit:contain;border-radius:14px;" />', obj.image.url)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "attendance", "guests", "created_at")
    list_filter = ("attendance", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


admin.site.site_header = "Abdelrahman & Omnia — Website Admin"
admin.site.site_title = "Celebration Admin"
admin.site.index_title = "Website Content Management"
