# Abdelrahman & Omnia — Django Celebration Website

A polished Django version of a modern engagement / wedding celebration landing page.

## Features

- Responsive luxury one-page design
- Event profile editable from Django Admin
- Countdown timer
- Story timeline
- Gallery with image uploads
- Event venue + Google Maps link
- RSVP form persisted to the database
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
3. Add one **Event Site** record.
4. Add **Story Moments** and **Gallery Items**.
5. Replace placeholder images in `static/site/images/` or upload images in Admin.

## Production

Set:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG=False`
- `DJANGO_ALLOWED_HOSTS=your-domain.com`
- `DJANGO_CSRF_TRUSTED_ORIGINS=https://your-domain.com`
- `DATABASE_URL=postgresql://...`
- `SECURE_SSL_REDIRECT=True`

The project is ready for Railway / Render / any container hosting provider.
