from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("celebration", "0003_rebrand_abdelrahman_omnia"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventsite",
            name="event_title",
            field=models.CharField(
                default="Engagement Celebration",
                help_text="The public title of the celebration shown in the hero and page metadata.",
                max_length=160,
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="music_enabled",
            field=models.BooleanField(
                default=False,
                help_text="Enable background music and the visitor music controls.",
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="music_file",
            field=models.FileField(
                blank=True,
                help_text="Upload an MP3/M4A/OGG file. This takes priority over Music URL.",
                upload_to="music/",
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="music_loop",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="music_title",
            field=models.CharField(
                blank=True,
                default="Our song",
                help_text="Label shown beside the music control.",
                max_length=120,
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="music_url",
            field=models.URLField(
                blank=True,
                help_text="Optional direct audio URL if you do not upload a file.",
            ),
        ),
        migrations.AlterField(
            model_name="eventsite",
            name="event_datetime",
            field=models.DateTimeField(help_text="Date and time used across the site and countdown."),
        ),
        migrations.AlterField(
            model_name="galleryitem",
            name="caption",
            field=models.CharField(
                blank=True,
                help_text="Optional sentence shown with this image and inside the lightbox.",
                max_length=240,
            ),
        ),
        migrations.AlterField(
            model_name="galleryitem",
            name="order",
            field=models.PositiveSmallIntegerField(default=0, help_text="Lower numbers appear first."),
        ),
    ]
