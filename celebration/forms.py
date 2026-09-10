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

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("website"):
            raise forms.ValidationError("Invalid submission.")
        if cleaned.get("attendance") == RSVP.Attendance.NO:
            cleaned["guests"] = 1
        return cleaned
