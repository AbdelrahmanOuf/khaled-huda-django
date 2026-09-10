from datetime import timedelta
from django.contrib import messages
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import RSVPForm
from .models import EventSite, GalleryItem, StoryMoment


def _default_event():
    return EventSite(
        event_datetime=timezone.now() + timedelta(days=90),
        maps_url="https://maps.google.com/?q=Cairo,Egypt",
    )


def home(request):
    event = (
        EventSite.objects.prefetch_related(
            Prefetch(
                "story_moments",
                queryset=StoryMoment.objects.filter(is_visible=True),
                to_attr="visible_story_moments",
            ),
            Prefetch(
                "gallery_items",
                queryset=GalleryItem.objects.filter(is_visible=True),
                to_attr="visible_gallery_items",
            ),
        ).first()
        or _default_event()
    )
    story_moments = getattr(event, "visible_story_moments", [])
    gallery_items = getattr(event, "visible_gallery_items", [])

    if request.method == "POST":
        if not event.rsvp_section_enabled or not event.is_rsvp_open:
            messages.error(request, event.rsvp_closed_message)
            return redirect("home")

        form = RSVPForm(request.POST, event=event)
        if form.is_valid():
            form.save()
            messages.success(request, event.rsvp_success_message)
            return redirect("home")
    else:
        form = RSVPForm(event=event)

    return render(
        request,
        "celebration/home.html",
        {
            "event": event,
            "form": form,
            "story_moments": story_moments,
            "gallery_items": gallery_items,
        },
    )


def healthcheck(request):
    return JsonResponse({"status": "ok"})
