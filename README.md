# padel
Developing web application for sport activities

## Docker

Create an environment file if it does not exist yet:

```bash
cp .env.example .env
```

Start the project:

```bash
docker compose up --build
```

Open the app at http://localhost:8000.

Useful commands:

```bash
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py test
docker compose down
```
