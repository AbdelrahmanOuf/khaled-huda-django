from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from celebration.models import EventSite, StoryMoment


class Command(BaseCommand):
    help = "Create or refresh demo celebration content."

    def handle(self, *args, **options):
        event, _ = EventSite.objects.update_or_create(
            id=1,
            defaults={
                "couple_names": "Khaled & Huda",
                "eyebrow": "A beautiful beginning",
                "hero_title": "Our Forever Begins Here",
                "hero_subtitle": "Join us as we celebrate love, laughter, and the beginning of our next chapter.",
                "event_datetime": timezone.now() + timedelta(days=90),
                "venue_name": "The Celebration Venue",
                "venue_address": "Cairo, Egypt",
                "maps_url": "https://maps.google.com/?q=Cairo,Egypt",
                "invitation_note": "We cannot wait to celebrate with the people who make our story brighter.",
                "is_rsvp_open": True,
            },
        )
        event.story_moments.all().delete()
        StoryMoment.objects.bulk_create([
            StoryMoment(event=event, order=1, date_label="The beginning", title="We Met", description="Some meetings feel ordinary until they become the start of everything."),
            StoryMoment(event=event, order=2, date_label="The promise", title="We Chose Forever", description="A thousand little moments became one beautiful decision: to build the future together."),
            StoryMoment(event=event, order=3, date_label="The celebration", title="And Now, We Celebrate", description="We would love for you to be part of the day we will remember forever."),
        ])
        self.stdout.write(self.style.SUCCESS("Demo content is ready."))
