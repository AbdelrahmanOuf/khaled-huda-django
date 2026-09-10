from datetime import timedelta
from importlib import import_module

from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import RSVPForm
from .models import EventSite, GalleryItem, RSVP, StoryMoment


class HomeViewTests(TestCase):
    def setUp(self):
        self.event = EventSite.objects.create(
            couple_names="Abdelrahman & Omnia",
            event_datetime=timezone.now() + timedelta(days=30),
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Abdelrahman &amp; Omnia")
        self.assertContains(response, "site/css/luxury-theme.css")
        self.assertContains(response, 'class="celebration-site"')
        self.assertContains(response, '<meta name="theme-color" content="#14231F">')

    def test_admin_managed_section_copy_is_rendered(self):
        self.event.gallery_kicker = "Private collection"
        self.event.gallery_title = "Our newest"
        self.event.gallery_title_accent = "memories"
        self.event.gallery_intro = "Every image tells our story."
        self.event.accent_color = "#123456"
        self.event.save()
        GalleryItem.objects.create(
            event=self.event,
            image="gallery/example.jpg",
            title="The first smile",
            caption="A day we will always remember.",
            order=1,
        )

        response = self.client.get(reverse("home"))

        self.assertContains(response, "Private collection")
        self.assertContains(response, "Our newest")
        self.assertContains(response, "The first smile")
        self.assertContains(response, "A day we will always remember.")
        self.assertContains(response, "--rose: #123456")

    def test_hidden_sections_and_items_are_not_rendered(self):
        self.event.story_enabled = False
        self.event.save()
        StoryMoment.objects.create(
            event=self.event,
            title="Hidden story",
            description="This should never appear.",
            is_visible=True,
        )
        GalleryItem.objects.create(
            event=self.event,
            image="gallery/hidden.jpg",
            title="Hidden photo",
            is_visible=False,
        )

        response = self.client.get(reverse("home"))

        self.assertNotContains(response, "Hidden story")
        self.assertNotContains(response, "Hidden photo")

    def test_rsvp_can_be_submitted(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Guest Name",
                "phone": "+201000000000",
                "attendance": "yes",
                "guests": 2,
                "message": "Congratulations!",
                "website": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RSVP.objects.count(), 1)
        self.assertContains(response, "your RSVP has been received")

    def test_honeypot_rejects_spam(self):
        response = self.client.post(
            reverse("home"),
            {
                "name": "Bot",
                "phone": "000",
                "attendance": "yes",
                "guests": 1,
                "message": "spam",
                "website": "https://spam.example",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(RSVP.objects.count(), 0)

    def test_event_guest_limit_is_enforced(self):
        self.event.rsvp_max_guests = 2
        self.event.save()

        response = self.client.post(
            reverse("home"),
            {
                "name": "Guest Name",
                "phone": "+201000000000",
                "attendance": "yes",
                "guests": 3,
                "message": "",
                "website": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(RSVP.objects.count(), 0)
        self.assertContains(response, "Please choose no more than 2 guests.")

    def test_rsvp_form_uses_admin_managed_labels_and_choices(self):
        self.event.rsvp_name_placeholder = "Full guest name"
        self.event.rsvp_attending_option = "Yes, I will be there"
        self.event.rsvp_declining_option = "Sorry, I cannot attend"
        self.event.save()

        form = RSVPForm(event=self.event)

        self.assertEqual(form.fields["name"].widget.attrs["placeholder"], "Full guest name")
        self.assertEqual(
            list(form.fields["attendance"].choices),
            [("yes", "Yes, I will be there"), ("no", "Sorry, I cannot attend")],
        )

    def test_music_autoplay_and_fallback_prompt_are_rendered(self):
        self.event.music_enabled = True
        self.event.music_autoplay = True
        self.event.music_volume = 65
        self.event.music_file = "music/celebration.mp3"
        self.event.music_start_prompt = "Start our celebration with music"
        self.event.music_start_button_label = "Enter celebration"
        self.event.save()

        response = self.client.get(reverse("home"))

        self.assertContains(response, 'data-music-autoplay="true"')
        self.assertContains(response, 'data-music-volume="65"')
        self.assertContains(response, "Start our celebration with music")
        self.assertContains(response, "Enter celebration")
        self.assertContains(response, "data-music-autoplay-gate")

    def test_music_autoplay_can_be_disabled_from_admin(self):
        self.event.music_enabled = True
        self.event.music_autoplay = False
        self.event.music_file = "music/celebration.mp3"
        self.event.save()

        response = self.client.get(reverse("home"))

        self.assertContains(response, 'data-music-autoplay="false"')
        self.assertNotContains(response, "data-music-autoplay-gate")

    def test_custom_success_and_closed_messages_are_used(self):
        self.event.is_rsvp_open = False
        self.event.rsvp_closed_message = "Responses are now closed."
        self.event.save()

        response = self.client.post(reverse("home"), {}, follow=True)

        self.assertContains(response, "Responses are now closed.")
        self.assertEqual(RSVP.objects.count(), 0)

    def test_healthcheck(self):
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})


class EventSiteModelTests(TestCase):
    def test_new_event_uses_luxury_default_palette(self):
        event = EventSite(event_datetime=timezone.now() + timedelta(days=10))

        self.assertEqual(event.text_color, "#1C211E")
        self.assertEqual(event.page_background_color, "#FBF8F2")
        self.assertEqual(event.soft_background_color, "#EFE7DA")
        self.assertEqual(event.accent_color, "#C29A5B")
        self.assertEqual(event.accent_dark_color, "#8A6330")
        self.assertEqual(event.dark_section_color, "#14231F")

    def test_palette_upgrade_changes_only_the_untouched_original_palette(self):
        palette_migration = import_module(
            "celebration.migrations.0007_alter_eventsite_accent_color_and_more"
        )
        event = EventSite.objects.create(
            event_datetime=timezone.now() + timedelta(days=10),
            **palette_migration.OLD_PALETTE,
        )

        palette_migration.apply_luxury_palette(apps, schema_editor=None)
        event.refresh_from_db()
        for field_name, expected_color in palette_migration.NEW_PALETTE.items():
            self.assertEqual(getattr(event, field_name), expected_color)

        custom_palette = {**palette_migration.OLD_PALETTE, "accent_color": "#123456"}
        EventSite.objects.filter(pk=event.pk).update(**custom_palette)
        palette_migration.apply_luxury_palette(apps, schema_editor=None)
        event.refresh_from_db()
        for field_name, expected_color in custom_palette.items():
            self.assertEqual(getattr(event, field_name), expected_color)

    def test_only_one_configuration_validates(self):
        EventSite.objects.create(event_datetime=timezone.now() + timedelta(days=10))
        another_event = EventSite(event_datetime=timezone.now() + timedelta(days=20))

        with self.assertRaises(ValidationError):
            another_event.full_clean()


class EventSiteAdminTests(TestCase):
    def setUp(self):
        self.event = EventSite.objects.create(
            couple_names="Abdelrahman & Omnia",
            event_datetime=timezone.now() + timedelta(days=30),
        )
        self.admin_user = get_user_model().objects.create_superuser(
            username="site-admin",
            email="admin@example.com",
            password="a-secure-test-password",
        )
        self.client.force_login(self.admin_user)

    def test_control_center_renders_with_all_inlines(self):
        response = self.client.get(
            reverse("admin:celebration_eventsite_change", args=(self.event.pk,))
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Identity &amp; SEO")
        self.assertContains(response, "Gallery photos")
        self.assertContains(response, "Story timeline")
        self.assertContains(response, 'name="music_autoplay"')
        self.assertContains(response, 'name="music_volume"')
        self.assertContains(response, 'name="music_start_prompt"')

    def test_second_event_cannot_be_added_from_admin(self):
        response = self.client.get(reverse("admin:celebration_eventsite_add"))

        self.assertEqual(response.status_code, 403)
