from django.contrib import admin

from .models import EventSite, GalleryItem, RSVP, StoryMoment


class StoryMomentInline(admin.TabularInline):
    model = StoryMoment
    extra = 0
    fields = ("order", "date_label", "title", "description")


class GalleryItemInline(admin.TabularInline):
    model = GalleryItem
    extra = 0
    fields = ("order", "image", "alt_text", "caption")


@admin.register(EventSite)
class EventSiteAdmin(admin.ModelAdmin):
    list_display = ("couple_names", "event_datetime", "venue_name", "is_rsvp_open", "updated_at")
    fieldsets = (
        ("Identity", {"fields": ("couple_names", "eyebrow", "hero_title", "hero_subtitle", "hero_image")}),
        ("Event", {"fields": ("event_datetime", "venue_name", "venue_address", "maps_url")}),
        ("Content", {"fields": ("invitation_note", "instagram_url", "is_rsvp_open")}),
    )
    inlines = [StoryMomentInline, GalleryItemInline]


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "attendance", "guests", "created_at")
    list_filter = ("attendance", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


admin.site.site_header = "Celebration Website Admin"
admin.site.site_title = "Celebration Admin"
admin.site.index_title = "Website Management"
