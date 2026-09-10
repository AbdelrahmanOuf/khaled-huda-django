from django.contrib import admin
from django.utils.html import format_html

from .models import EventSite, GalleryItem, RSVP, StoryMoment


class StoryMomentInline(admin.TabularInline):
    model = StoryMoment
    extra = 0
    fields = ("order", "date_label", "title", "description")


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 0
    fields = ("order", "image", "preview", "alt_text", "caption")
    readonly_fields = ("preview",)

    @admin.display(description="Preview")
    def preview(self, obj):
        if not obj or not obj.image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="width:120px;height:80px;object-fit:cover;border-radius:10px;" />',
            obj.image.url,
        )


@admin.register(EventSite)
class EventSiteAdmin(admin.ModelAdmin):
    list_display = ("couple_names", "event_datetime", "venue_name", "is_rsvp_open", "updated_at")
    readonly_fields = ("hero_preview", "hero_mobile_preview")
    fieldsets = (
        (
            "Identity",
            {
                "fields": (
                    "couple_names",
                    "eyebrow",
                    "hero_title",
                    "hero_subtitle",
                )
            },
        ),
        (
            "Cinematic Intro",
            {
                "fields": ("intro_enabled", "intro_title", "intro_subtitle"),
                "description": "The intro appears once per browser session and can be skipped by the visitor.",
            },
        ),
        (
            "Hero Images",
            {
                "fields": (
                    "hero_image",
                    "hero_preview",
                    "hero_mobile_image",
                    "hero_mobile_preview",
                ),
                "description": "Use a wide desktop image and optionally a portrait mobile image for the strongest result.",
            },
        ),
        ("Event", {"fields": ("event_datetime", "venue_name", "venue_address", "maps_url")}),
        ("Content", {"fields": ("invitation_note", "instagram_url", "is_rsvp_open")}),
    )
    inlines = [StoryMomentInline, GalleryItemInline]

    @admin.display(description="Desktop preview")
    def hero_preview(self, obj):
        if not obj or not obj.hero_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="max-width:460px;width:100%;height:220px;object-fit:cover;border-radius:14px;" />',
            obj.hero_image.url,
        )

    @admin.display(description="Mobile preview")
    def hero_mobile_preview(self, obj):
        if not obj or not obj.hero_mobile_image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="width:180px;height:250px;object-fit:cover;border-radius:14px;" />',
            obj.hero_mobile_image.url,
        )


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "attendance", "guests", "created_at")
    list_filter = ("attendance", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


admin.site.site_header = "Khaled & Huda Website Admin"
admin.site.site_title = "Celebration Admin"
admin.site.index_title = "Website Management"
