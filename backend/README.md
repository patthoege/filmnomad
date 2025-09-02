# FilmNomad – Backend (Django REST API)

This folder contains the backend for **FilmNomad**, a movie location finder web application. It provides a RESTful API built with Django and Django REST Framework (DRF) to search for movies and filming locations, plan trips, and submit suggestions. It also includes user authentication via JSON Web Tokens (JWT), admin moderation tools, and support for future features like saved trips and ratings.

## Features

- **Search**: Look up movies/series by title, filter by type (movie/series), or search locations by city.
- **Locations**: Retrieve filming locations associated with a movie or find all locations in a given city.
- **Trip planner**: Create and manage custom trip plans with an ordered list of locations.
- **Suggestions**: Submit new filming location suggestions for review by an administrator.
- **Accommodation & Flights**: Query recommended lodging and flight links for a city.
- **Authentication**: Obtain and refresh JWT tokens; admin interface for moderation and data management.
- **Extensible**: Easily add additional models (e.g. user ratings, trip sharing) and APIs as needed.

## Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/yourusername/filmnomad.git
   cd filmnomad/backend

2.	Create a virtual environment and activate it

   ``` python3 -m venv .venv
       source .venv/bin/activate  # On Windows use: .venv\Scripts\Activate.ps1

3.	Install dependencies

    pip install -r requirements.txt

4.	Create an environment file

    Copy .env from the example below, then customize it to suit your environment (never commit secrets):
    SECRET_KEY=your-secret-key
    DEBUG=True
    ALLOWED_HOSTS=localhost,127.0.0.1
    # Use SQLite by default; for PostgreSQL set this to `postgres://user:password@localhost:5432/dbname`
    DATABASE_URL=sqlite:///db.sqlite3
    OMDB_API_KEY=your-omdb-api-key

5.	Apply database migrations

    python manage.py makemigrations
    python manage.py migrate

6.	Create an admin user

    python manage.py createsuperuser

7.  Run the development server

    python manage.py runserver

The API will be available at http://127.0.0.1:8000/api/, and the Django admin interface at http://127.0.0.1:8000/admin/.


## API Overview

All endpoints are prefixed with /api/. Authentication is required for write operations; read operations are public.

## Authentication
	•	POST /api/auth/token/ – Obtain access and refresh tokens. Send JSON with {"username": "...", "password": "..."}.
	•	POST /api/auth/refresh/ – Refresh an access token. Send JSON with {"refresh": "<refresh_token>"}.

### Movies
	•	GET /api/movies/ – List all movies and series.
	•	GET /api/movies/<imdb_id>/ – Retrieve a single movie.
	•	POST /api/movies/ – Create a new movie (requires auth).
	•	PUT/PATCH/DELETE /api/movies/<imdb_id>/ – Update or delete a movie (requires auth).
	•	GET /api/movies/search/?q=<query>&type=<movie|series> – Search movies/series.

### Cities
	•	GET /api/cities/ – List all cities.
	•	GET /api/cities/<id>/ – Retrieve a city.
	•	POST /api/cities/ – Create a city (requires auth).
	•	GET /api/cities/search/?q=<query> – Search cities by name.

### Locations
	•	GET /api/locations/ – List all filming locations.
	•	GET /api/locations/<id>/ – Retrieve a location.
	•	POST /api/locations/ – Create a location (requires auth).
	•	GET /api/locations/search/?city=<city>&movie=<title> – Search by city or movie title.

### Trip Plans
	•	GET /api/trips/ – List the authenticated user’s trip plans.
	•	POST /api/trips/ – Create a new trip plan with ordered locations.
	•	GET /api/trips/<id>/ – Retrieve a trip.
	•	PUT/PATCH/DELETE /api/trips/<id>/ – Update or delete a trip (owner only).

### Suggestions
	•	GET /api/suggestions/ – List all suggestions (public).
	•	POST /api/suggestions/ – Submit a new suggestion (authenticated or anonymous).
	•	POST /api/suggestions/<id>/review/ – Approve or reject a suggestion (admin only).

### Accommodations & Flights
	•	GET /api/accommodations/ – List accommodation links.
	•	GET /api/flights/ – List flight source links.

### Environment Variables
	•	SECRET_KEY: Django secret key (required).
	•	DEBUG: Set True for development; False in production.
	•	ALLOWED_HOSTS: Comma-separated list of hostnames allowed to serve the app.
	•	DATABASE_URL: Database connection URL. Defaults to SQLite; use PostgreSQL for production.
	•	OMDB_API_KEY: API key for OMDb API to look up movie details.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change. Run linting and tests before submitting PRs.

## License

This project does not yet specify a license. Consider adding one to define permitted uses.