from django.db import migrations, models


def rebrand_existing_event(apps, schema_editor):
    EventSite = apps.get_model("celebration", "EventSite")
    EventSite.objects.filter(couple_names="Khaled & Huda").update(
        couple_names="Abdelrahman & Omnia"
    )
    EventSite.objects.filter(intro_title="Khaled & Huda").update(
        intro_title="Abdelrahman & Omnia"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("celebration", "0002_eventsite_intro_and_mobile_hero"),
    ]

    operations = [
        migrations.AlterField(
            model_name="eventsite",
            name="couple_names",
            field=models.CharField(default="Abdelrahman & Omnia", max_length=120),
        ),
        migrations.RunPython(rebrand_existing_event, migrations.RunPython.noop),
    ]
