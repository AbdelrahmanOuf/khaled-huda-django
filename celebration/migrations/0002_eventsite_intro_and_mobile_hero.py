from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("celebration", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventsite",
            name="hero_mobile_image",
            field=models.ImageField(
                blank=True,
                help_text="Optional mobile hero image. Recommended: portrait 4:5 or 9:16.",
                upload_to="hero/mobile/",
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="intro_enabled",
            field=models.BooleanField(
                default=True,
                help_text="Show the cinematic opening once per browser session.",
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="intro_subtitle",
            field=models.CharField(
                blank=True,
                default="A celebration of love, family & forever",
                max_length=180,
            ),
        ),
        migrations.AddField(
            model_name="eventsite",
            name="intro_title",
            field=models.CharField(
                blank=True,
                default="",
                help_text="Leave empty to use the couple names.",
                max_length=120,
            ),
        ),
        migrations.AlterField(
            model_name="eventsite",
            name="hero_image",
            field=models.ImageField(
                blank=True,
                help_text="Desktop hero image. Recommended: landscape image, at least 2000px wide.",
                upload_to="hero/",
            ),
        ),
        migrations.AlterField(
            model_name="galleryitem",
            name="image",
            field=models.ImageField(
                help_text="Use high-resolution JPG/WebP images. The site loads gallery images lazily.",
                upload_to="gallery/",
            ),
        ),
    ]
