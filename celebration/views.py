from datetime import timedelta
from types import SimpleNamespace

from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import RSVPForm
from .models import EventSite


def _default_event():
    return SimpleNamespace(
        couple_names="Abdelrahman & Omnia",
        eyebrow="Together, always",
        hero_title="Our Forever Begins Here",
        hero_subtitle="We would be delighted to celebrate this beautiful chapter with you.",
        event_datetime=timezone.now() + timedelta(days=90),
        venue_name="The Celebration Venue",
        venue_address="Cairo, Egypt",
        maps_url="https://maps.google.com/?q=Cairo,Egypt",
        hero_image=None,
        hero_mobile_image=None,
        intro_enabled=True,
        intro_title="",
        intro_subtitle="A celebration of love, family & forever",
        invitation_note="Your presence will make our day even more memorable.",
        instagram_url="",
        is_rsvp_open=True,
        story_moments=SimpleNamespace(all=lambda: []),
        gallery_items=SimpleNamespace(all=lambda: []),
    )


def home(request):
    event = EventSite.objects.prefetch_related("story_moments", "gallery_items").first() or _default_event()

    if request.method == "POST":
        if not event.is_rsvp_open:
            messages.error(request, "RSVP is currently closed.")
            return redirect("home")

        form = RSVPForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — your RSVP has been received.")
            return redirect("home")
    else:
        form = RSVPForm()

    return render(request, "celebration/home.html", {"event": event, "form": form})


def healthcheck(request):
    return JsonResponse({"status": "ok"})
