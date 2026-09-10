from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import EventSite, RSVP


class HomeViewTests(TestCase):
    def setUp(self):
        self.event = EventSite.objects.create(
            couple_names="Khaled & Huda",
            event_datetime=timezone.now() + timedelta(days=30),
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Khaled &amp; Huda")

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

    def test_healthcheck(self):
        response = self.client.get(reverse("healthcheck"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"status": "ok"})
