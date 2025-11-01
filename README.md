# Django Calorie Calculator

A clean, MIT-licensed Django app that computes BMR/TDEE using Mifflin–St Jeor, sets a daily calorie target by goal, and lets users log foods and meals.

## Features
- User registration/login
- Profile with sex/age/height/weight/activity/goal
- BMR, TDEE, and target calories calculator
- Foods CRUD (kcal/100g, macros)
- Meals CRUD with daily dashboard (consumed vs. remaining)
- Bootstrap 5 UI, src/ layout, GitHub Actions CI, tests

## Tech
- Python ≥ 3.10, Django 5, SQLite (default)

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```
Open http://127.0.0.1:8000

## Project layout
```
src/config  -> Django project (settings, urls, wsgi, asgi)
src/calories -> App (models, views, forms, utils, urls, templates, static)
```

## Tests
```bash
pip install pytest pytest-django
pytest -q
```

## Deployment notes
- Set `DJANGO_DEBUG=False` and a strong `SECRET_KEY` in `.env`.
- Set `ALLOWED_HOSTS` accordingly.
- Use Postgres in production (set `DATABASE_URL` and update settings as needed).

## License
MIT © 2025 Mobin Yousefi

