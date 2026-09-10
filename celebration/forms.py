from django import forms

from .models import RSVP


class RSVPForm(forms.ModelForm):
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "tabindex": "-1",
                "autocomplete": "off",
                "aria-hidden": "true",
                "class": "hp-field",
            }
        ),
    )

    class Meta:
        model = RSVP
        fields = ["name", "phone", "attendance", "guests", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name", "autocomplete": "name"}),
            "phone": forms.TextInput(attrs={"placeholder": "+20 ...", "autocomplete": "tel"}),
            "attendance": forms.Select(),
            "guests": forms.NumberInput(attrs={"min": 1, "max": 8}),
            "message": forms.Textarea(attrs={"rows": 4, "placeholder": "Write a note for the couple…"}),
        }

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event
        if not event:
            return

        self.fields["name"].label = event.rsvp_name_label
        self.fields["phone"].label = event.rsvp_phone_label
        self.fields["guests"].label = event.rsvp_guests_label
        self.fields["attendance"].label = event.rsvp_attendance_label
        self.fields["message"].label = event.rsvp_message_label
        self.fields["name"].widget.attrs["placeholder"] = event.rsvp_name_placeholder
        self.fields["phone"].widget.attrs["placeholder"] = event.rsvp_phone_placeholder
        self.fields["message"].widget.attrs["placeholder"] = event.rsvp_message_placeholder
        self.fields["guests"].widget.attrs["max"] = event.rsvp_max_guests
        self.fields["attendance"].choices = (
            (RSVP.Attendance.YES, event.rsvp_attending_option),
            (RSVP.Attendance.NO, event.rsvp_declining_option),
        )

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Invalid submission.")
        if cleaned.get("attendance") == RSVP.Attendance.NO:
            cleaned["guests"] = 1
        elif (
            self.event
            and cleaned.get("guests") is not None
            and cleaned["guests"] > self.event.rsvp_max_guests
        ):
            self.add_error(
                "guests",
                f"Please choose no more than {self.event.rsvp_max_guests} guests.",
            )
        return cleaned
