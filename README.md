# RANL PRINT

Django website and business admin for RANL PRINT.

## Project structure
- `backend/` — Django website, admin, APIs, templates and static assets.
- `start_all.bat` / `start_backend.bat` — optional local Windows development launchers.
- `backend/media/` and `backend/db.sqlite3` — retained from the supplied project. Back them up; do not commit these files to GitHub.

The old standalone `frontend/` preview has been removed because the public website is rendered by Django from `backend/templates/site/index.html` and uses `backend/static/`.

## Run locally on Windows
1. Install Python 3.11+.
2. Run `start_all.bat`.
3. Website: `http://127.0.0.1:8000/`
4. Admin: `http://127.0.0.1:8000/admin/`

## GitHub and Hostinger VPS deployment
1. Upload the project to a **private GitHub repository**. Do not commit `.env`, the SQLite database, or customer-uploaded media.
2. On the Hostinger VPS, install Python, PostgreSQL, Nginx and Git.
3. Clone the repository to the VPS and create a Python virtual environment inside `backend/`.
4. Install dependencies with `pip install -r requirements.txt`.
5. Create a PostgreSQL database and set the production environment variables described in `backend/.env.example` (plus `DATABASE_URL`).
6. Run `python manage.py migrate`, `python manage.py collectstatic --noinput`, and `python manage.py createsuperuser`.
7. Run Django through Gunicorn managed by `systemd`; configure Nginx to proxy requests to Gunicorn and serve `/static/` from `backend/staticfiles/` and `/media/` from `backend/media/`.
8. Point the Namecheap domain's DNS records to the VPS IP, configure Nginx for the domain, then enable HTTPS with Let's Encrypt/Certbot.
9. Set `DEBUG=False`, a strong unique `SECRET_KEY`, `ALLOWED_HOSTS` to your domain(s), and `CSRF_TRUSTED_ORIGINS` to your HTTPS domain(s). Test the website, admin, quote form, uploads and order tracking.

Do not run Django's development server (`runserver`) for the live website. Back up the database and media regularly.
