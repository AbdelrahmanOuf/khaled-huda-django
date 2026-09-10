from django import forms
from django.contrib import admin
from django.utils.html import format_html

from .models import EventSite, GalleryItem, RSVP, StoryMoment


EVENT_COLOR_FIELDS = (
    "text_color",
    "page_background_color",
    "soft_background_color",
    "accent_color",
    "accent_dark_color",
    "dark_section_color",
)


def image_preview(image, *, width=520, height=280, fit="cover"):
    if not image:
        return "No image uploaded yet."
    return format_html(
        '<img src="{}" alt="" style="max-width:{}px;width:100%;height:{}px;object-fit:{};'
        'border-radius:16px;box-shadow:0 10px 32px rgba(0,0,0,.12);background:#f7f2ee;" />',
        image.url,
        width,
        height,
        fit,
    )


class EventSiteAdminForm(forms.ModelForm):
    class Meta:
        model = EventSite
        fields = "__all__"
        widgets = {
            field: forms.TextInput(attrs={"type": "color", "class": "event-color-input"})
            for field in EVENT_COLOR_FIELDS
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("hero_image", "hero_mobile_image", "social_share_image", "site_icon"):
            field = self.fields.get(field_name)
            if field:
                field.widget.attrs["accept"] = "image/jpeg,image/png,image/webp,image/avif"
        music_field = self.fields.get("music_file")
        if music_field:
            music_field.widget.attrs["accept"] = "audio/mpeg,audio/mp4,audio/ogg,audio/wav"


class StoryMomentInline(admin.StackedInline):
    model = StoryMoment
    extra = 0
    fields = ("is_visible", "order", "date_label", "title", "description")
    classes = ("collapse",)
    verbose_name = "Story moment"
    verbose_name_plural = "Story timeline — قصتنا"


class GalleryItemInline(admin.StackedInline):
    model = GalleryItem
    extra = 0
    fields = (
        ("is_visible", "order"),
        "image",
        "preview",
        "image_position",
        "title",
        "caption",
        "alt_text",
    )
    readonly_fields = ("preview",)
    show_change_link = True
    verbose_name = "Gallery photo"
    verbose_name_plural = "Gallery photos — صور الموقع"

    @admin.display(description="Image preview")
    def preview(self, obj):
        if not obj or not obj.image:
            return "Upload an image, save, then its preview will appear here."
        return image_preview(obj.image, width=560, height=320)


@admin.register(EventSite)
class EventSiteAdmin(admin.ModelAdmin):
    form = EventSiteAdminForm
    list_display = (
        "couple_names",
        "event_title",
        "event_datetime",
        "venue_name",
        "music_enabled",
        "is_rsvp_open",
        "updated_at",
    )
    readonly_fields = (
        "hero_preview",
        "hero_mobile_preview",
        "share_image_preview",
        "site_icon_preview",
        "music_status",
        "updated_at",
    )
    save_on_top = True
    view_on_site = True
    inlines = [GalleryItemInline, StoryMomentInline]
    fieldsets = (
        (
            "1. الهوية وبيانات المشاركة — Identity & SEO",
            {
                "fields": (
                    "couple_names",
                    "event_title",
                    "brand_symbol",
                    "seo_description",
                    "social_share_image",
                    "share_image_preview",
                    "site_icon",
                    "site_icon_preview",
                ),
                "description": "Names, browser metadata and the preview used when the link is shared.",
            },
        ),
        (
            "2. القائمة العلوية — Navigation",
            {
                "fields": (
                    "navigation_enabled",
                    ("nav_story_label", "nav_gallery_label"),
                    ("nav_details_label", "nav_rsvp_label"),
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "3. الواجهة الرئيسية — Hero",
            {
                "fields": (
                    "eyebrow",
                    "hero_title",
                    "hero_subtitle",
                    ("hero_primary_button_label", "hero_secondary_button_label"),
                    "discover_label",
                    "hero_image",
                    "hero_preview",
                    "hero_mobile_image",
                    "hero_mobile_preview",
                ),
                "description": "The desktop and mobile opening section. Changes appear after saving.",
            },
        ),
        (
            "4. ميعاد ومكان المناسبة — Date, Time & Venue",
            {
                "fields": ("event_datetime", "venue_name", "venue_address", "maps_url"),
                "description": "The date automatically updates every date card, the countdown and RSVP details.",
            },
        ),
        (
            "5. شاشة الافتتاح السينمائية — Cinematic Intro",
            {
                "fields": ("intro_enabled", "intro_title", "intro_subtitle", "intro_skip_label"),
                "description": "Shown once per browser session. Leave the intro title empty to use the couple names.",
                "classes": ("collapse",),
            },
        ),
        (
            "6. قسم حفظ التاريخ والعد التنازلي — Save the Date",
            {
                "fields": (
                    "save_date_enabled",
                    "save_date_kicker",
                    ("save_date_title", "save_date_title_accent"),
                    "invitation_note",
                    "countdown_enabled",
                    ("countdown_days_label", "countdown_hours_label"),
                    ("countdown_minutes_label", "countdown_seconds_label"),
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "7. قسم قصتنا — Our Story",
            {
                "fields": ("story_enabled", "story_kicker", "story_title", "story_intro"),
                "description": "Add, remove and reorder the story moments at the bottom of this page.",
                "classes": ("collapse",),
            },
        ),
        (
            "8. الاقتباس — Quote",
            {
                "fields": ("quote_enabled", "quote_text"),
                "classes": ("collapse",),
            },
        ),
        (
            "9. معرض الصور — Gallery",
            {
                "fields": (
                    "gallery_enabled",
                    "gallery_kicker",
                    ("gallery_title", "gallery_title_accent"),
                    "gallery_intro",
                ),
                "description": "Manage every photo, title, sentence, crop position and order at the bottom of this page.",
                "classes": ("collapse",),
            },
        ),
        (
            "10. تفاصيل الحفل — Event Details",
            {
                "fields": (
                    "details_enabled",
                    "details_kicker",
                    ("details_title", "details_title_accent"),
                    "details_intro",
                    "date_card_label",
                    "venue_card_label",
                    "maps_button_label",
                    "note_card_label",
                    "note_card_title",
                    "note_card_text",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "11. تأكيد الحضور — RSVP",
            {
                "fields": (
                    ("rsvp_section_enabled", "is_rsvp_open"),
                    "rsvp_kicker",
                    ("rsvp_title", "rsvp_title_accent"),
                    "rsvp_intro",
                    ("rsvp_form_title", "rsvp_form_subtitle"),
                    ("rsvp_name_label", "rsvp_phone_label"),
                    ("rsvp_guests_label", "rsvp_attendance_label"),
                    ("rsvp_message_label", "rsvp_optional_label"),
                    "rsvp_submit_label",
                    ("rsvp_name_placeholder", "rsvp_phone_placeholder"),
                    "rsvp_message_placeholder",
                    ("rsvp_attending_option", "rsvp_declining_option"),
                    "rsvp_max_guests",
                    "rsvp_success_message",
                    "rsvp_closed_message",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "12. موسيقى الخلفية — Background Music",
            {
                "fields": (
                    "music_enabled",
                    "music_autoplay",
                    "music_volume",
                    "music_file",
                    "music_url",
                    "music_title",
                    "music_loop",
                    "music_start_prompt",
                    "music_start_button_label",
                    "music_status",
                ),
                "description": "The uploaded audio file takes priority over the URL. If audible autoplay is blocked, the visitor gets a polished one-tap entry prompt.",
                "classes": ("collapse",),
            },
        ),
        (
            "13. الفوتر والتواصل — Footer & Social",
            {
                "fields": (
                    "footer_enabled",
                    ("footer_left_label", "footer_right_label"),
                    "footer_note",
                    "instagram_url",
                    "instagram_label",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "14. ألوان التصميم — Appearance",
            {
                "fields": (
                    ("text_color", "page_background_color"),
                    ("soft_background_color", "accent_color"),
                    ("accent_dark_color", "dark_section_color"),
                ),
                "description": "These six colors drive the complete luxury theme, including surfaces, borders, highlights, buttons and dark sections.",
                "classes": ("collapse",),
            },
        ),
        ("System information", {"fields": ("updated_at",), "classes": ("collapse",)}),
    )

    class Media:
        css = {"all": ("admin/css/event_admin.css",)}

    def has_add_permission(self, request):
        return not EventSite.objects.exists() and super().has_add_permission(request)

    def has_delete_permission(self, request, obj=None):
        return False

    @admin.display(description="Desktop hero preview")
    def hero_preview(self, obj):
        return image_preview(obj.hero_image if obj else None, width=680, height=330)

    @admin.display(description="Mobile hero preview")
    def hero_mobile_preview(self, obj):
        return image_preview(obj.hero_mobile_image if obj else None, width=260, height=360)

    @admin.display(description="Social image preview")
    def share_image_preview(self, obj):
        return image_preview(obj.social_share_image if obj else None, width=560, height=294)

    @admin.display(description="Browser icon preview")
    def site_icon_preview(self, obj):
        return image_preview(obj.site_icon if obj else None, width=120, height=120, fit="contain")

    @admin.display(description="Music status")
    def music_status(self, obj):
        if not obj:
            return "Save the event first."
        if not obj.music_enabled:
            return "Music is disabled."
        if obj.music_source:
            return format_html(
                '<strong style="color:#2e7d32;">● Ready</strong> — {}',
                obj.music_title or "Background music",
            )
        return format_html(
            '<strong style="color:#b26a00;">● Enabled, but no audio source has been added.</strong>'
        )


@admin.action(description="Show selected photos on the website")
def show_gallery_items(modeladmin, request, queryset):
    queryset.update(is_visible=True)


@admin.action(description="Hide selected photos from the website")
def hide_gallery_items(modeladmin, request, queryset):
    queryset.update(is_visible=False)


@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ("thumbnail", "title", "event", "order", "is_visible")
    list_editable = ("order", "is_visible")
    search_fields = ("title", "caption", "alt_text", "event__couple_names")
    list_filter = ("is_visible", "event")
    ordering = ("order", "id")
    actions = (show_gallery_items, hide_gallery_items)
    fields = (
        "event",
        ("is_visible", "order"),
        "image",
        "thumbnail_large",
        "image_position",
        "title",
        "caption",
        "alt_text",
    )
    readonly_fields = ("thumbnail_large",)

    @admin.display(description="Photo")
    def thumbnail(self, obj):
        if not obj.image:
            return "—"
        return format_html(
            '<img src="{}" alt="" style="width:72px;height:52px;object-fit:cover;border-radius:8px;" />',
            obj.image.url,
        )

    @admin.display(description="Preview")
    def thumbnail_large(self, obj):
        return image_preview(obj.image if obj else None, width=620, height=390, fit="contain")


@admin.action(description="Show selected moments on the website")
def show_story_moments(modeladmin, request, queryset):
    queryset.update(is_visible=True)


@admin.action(description="Hide selected moments from the website")
def hide_story_moments(modeladmin, request, queryset):
    queryset.update(is_visible=False)


@admin.register(StoryMoment)
class StoryMomentAdmin(admin.ModelAdmin):
    list_display = ("title", "date_label", "event", "order", "is_visible")
    list_editable = ("order", "is_visible")
    list_filter = ("is_visible", "event")
    search_fields = ("title", "date_label", "description", "event__couple_names")
    ordering = ("order", "id")
    actions = (show_story_moments, hide_story_moments)


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "attendance", "guests", "created_at")
    list_filter = ("attendance", "created_at")
    search_fields = ("name", "phone", "message")
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)
    date_hierarchy = "created_at"
    list_per_page = 50


admin.site.site_header = "Abdelrahman & Omnia — Website Admin"
admin.site.site_title = "Celebration Admin"
admin.site.index_title = "Website Content Management"
