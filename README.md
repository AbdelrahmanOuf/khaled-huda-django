# Abdelrahman & Omnia — Django Celebration Website

A polished Django version of a modern engagement / wedding celebration landing page.

## Features

- Responsive luxury one-page design
- Cinematic emerald, antique-gold and warm-ivory visual system
- Event profile editable from Django Admin
- Complete section copy, visibility and navigation controls
- Desktop/mobile hero, social preview and browser icon uploads
- Countdown timer
- Story timeline with ordering and visibility controls
- Gallery with image title, caption, crop position, ordering and visibility controls
- Safe color pickers for the public website palette
- Event venue + Google Maps link
- Fully configurable RSVP copy, guest limit and response messages
- Background music upload/URL, autoplay-first playback, volume and cinematic intro controls
- CSRF protection + honeypot anti-spam
- WhiteNoise static files
- PostgreSQL-ready via `DATABASE_URL`
- Docker + Gunicorn production setup
- GitHub Actions CI
- SEO / Open Graph metadata
- Accessibility and reduced-motion support

## Local setup

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/` and admin at `http://127.0.0.1:8000/admin/`.

## Customization

1. Create a superuser.
2. Open Django Admin.
3. Open the single **Event Site** record. It is the website control center and is intentionally limited to one record.
4. Edit the event date, venue, section titles, buttons, RSVP wording, music, colors and section visibility in the numbered panels.
5. Add **Gallery Photos** and **Story Timeline** items at the bottom of the same page, or manage them from their dedicated admin lists.
6. Use `Order` to rearrange an item and `Is visible` to publish or hide it without deleting it.

For music, enable **Music enabled**, upload an audio file (or add a direct URL), and keep
**Music autoplay** enabled. The website attempts audible playback immediately; when a browser
blocks it, visitors see the configurable one-tap music entry prompt.

The **View on site** button in the Event Site editor opens the public page so changes can be checked immediately after saving.

The visual system is driven by the six color controls in **14. Appearance**. Borders,
surfaces, highlights, buttons and dark sections are derived from that palette so custom
colors remain consistent across the full website.

## Production

Set:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=your-domain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com`
- `DATABASE_URL=postgresql://...`
- `SECURE_SSL_REDIRECT=True`
- `DJANGO_SUPERUSER_USERNAME=your-admin-name`
- `DJANGO_SUPERUSER_EMAIL=you@example.com`
- `DJANGO_SUPERUSER_PASSWORD=use-a-long-unique-password`

The project is ready for Railway / Render / any container hosting provider.
