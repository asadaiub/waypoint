# Waypoint

A trail-finder and trip-planner: a pure-Python domain engine with a Django site
built around it.

**Md Asaduzzaman - n01190565**
Application Programming (CCGC-5003-RNA), Summer 2026

## Setup

```bash
python -m venv env
source env/bin/activate          # Windows: env\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Then open <http://127.0.0.1:8000/>.

## Layout

```
waypoint_core/   the domain engine - plain Python, no Django
waypoint/        the Django project - settings, URLs, WSGI
```

The engine is an importable package, so the site can reuse it:

```bash
python -c "import waypoint_core"
```
