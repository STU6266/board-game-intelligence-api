# Board Game Intelligence API

Board Game Intelligence API is a backend and data integration portfolio project built with Python, FastAPI and PostgreSQL.

The project imports BoardGameGeek-style XML data, validates and transforms it into relational database records, tracks synchronization runs and exposes documented REST endpoints for games, import history and analytical recommendation reports.

## Live API

Swagger/OpenAPI documentation:

```text
https://board-game-intelligence-api.onrender.com/docs
```

Useful endpoints:

```text
GET /api/v1/health
GET /api/v1/health/db
GET /api/v1/games
GET /api/v1/games/{game_id}
GET /api/v1/reports/family-friendly
GET /api/v1/reports/low-complexity-high-rating
GET /api/v1/import-runs
GET /api/v1/import-runs/{import_run_id}
POST /api/v1/sync/games/{bgg_id}
```

The deployed API includes development seed data and a synchronized local XML fixture, so the documentation and report endpoints can be explored directly.

Real BoardGameGeek synchronization requires an authorized API token configured securely on the server.

## What This Project Shows

- FastAPI application design with versioned API routes
- PostgreSQL data modeling with SQLAlchemy and Alembic migrations
- external XML data parsing and transformation
- service/repository separation for maintainable backend logic
- data quality validation before database writes
- duplicate-safe synchronization by external `bgg_id`
- import history and error tracking
- documented REST API with Swagger/OpenAPI
- analytical report endpoints based on stored data
- Docker Compose local database setup
- automated tests for parsing, validation, sync logic, reports and client behavior
- cloud deployment with environment-based configuration

## Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- HTTPX
- Docker Compose
- Pytest
- Render

## Architecture

```text
BoardGameGeek XML API2
        |
        v
     BggClient
        |
        v
    XML Parser
        |
        v
Data Quality Validation
        |
        v
 Synchronization Service
        |
        v
 PostgreSQL Database
        |
        v
FastAPI REST Endpoints
        |
        v
Games / Import History / Analytical Reports
```

The code is split into focused backend layers:

```text
app/api/           HTTP endpoints and request handling
app/models/        SQLAlchemy database models
app/schemas/       Pydantic request and response structures
app/repositories/  database query logic
app/services/      parsing, validation, sync and report logic
app/db/            database base class and session setup
app/core/          application configuration
tests/             automated unit tests
scripts/           local development scripts
sample_data/       XML fixture for development and testing
```

## Data Model

Core tables:

```text
games
ratings
categories
mechanics
game_categories
game_mechanics
import_runs
import_errors
```

Games store the external BoardGameGeek ID, title, publication year, description, player range, playtime, minimum age and synchronization timestamp.

Ratings are stored separately and include average rating, Bayesian rating, number of ratings, complexity/weight and rank.

Categories and mechanics use many-to-many relationships because a board game can belong to several categories and contain several mechanics.

Import runs and import errors make synchronization attempts reviewable instead of losing errors in terminal output only.

## API Features

### Health

```text
GET /api/v1/health
GET /api/v1/health/db
```

Checks whether the application and PostgreSQL connection are available.

### Games

```text
GET /api/v1/games
GET /api/v1/games/{game_id}
```

Returns stored game records with metadata, rating data, categories and mechanics.

### Analytical Reports

```text
GET /api/v1/reports/family-friendly
GET /api/v1/reports/low-complexity-high-rating
```

The family-friendly report calculates a score from rating, complexity, age recommendation, playtime and player range.

The low-complexity/high-rating report finds games with strong ratings and lower complexity:

```text
average_rating >= 7.0
average_weight <= 2.5
```

### Synchronization and Import History

```text
POST /api/v1/sync/games/{bgg_id}
GET  /api/v1/import-runs
GET  /api/v1/import-runs/{import_run_id}
```

The sync endpoint requests external data, parses XML, validates the result and creates or updates the stored game. Repeated imports update the existing record instead of creating duplicates.

The import history endpoints expose sync status, created/updated/skipped counts, messages and stored errors.

## XML Parsing and Validation

The parser converts BoardGameGeek-style XML into internal data structures. Parsed fields include:

- BoardGameGeek ID
- primary name
- publication year
- description
- player range
- playtime
- minimum age
- rating values
- complexity value
- rank
- categories
- mechanics
- designers and publishers for future expansion

Before writing data to the database, the validation service checks consistency rules such as valid rating ranges, non-negative playtimes, valid player counts and valid complexity values.

## Run Locally

Requirements:

- Python 3.12
- Docker with Docker Compose
- Git

Clone and install:

```bash
git clone https://github.com/STU6266/board-game-intelligence-api.git
cd board-game-intelligence-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create local environment variables:

```bash
cp .env.example .env
```

Start PostgreSQL:

```bash
docker compose up -d
```

Apply migrations:

```bash
alembic upgrade head
```

Add local demo data:

```bash
python -m scripts.seed_games
python -m scripts.sync_sample_game
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open local Swagger docs:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run the automated tests:

```bash
pytest -v
```

Current suite:

```text
36 passing tests
```

The tests cover parser extraction, missing data handling, validation rules, synchronization create/update behavior, error logging, report filtering/sorting and mocked BoardGameGeek client behavior.

Tests do not require real BoardGameGeek network access or a real API token.

## Deployment

The API is deployed as a Render Web Service with PostgreSQL.

Deployment uses:

- Render-managed environment variables
- PostgreSQL connection through `DATABASE_URL`
- Alembic migrations during deployment
- secrets kept outside the repository
- development seed/fixture data for public exploration

## Project Scope

This is a portfolio-ready MVP focused on backend API architecture and external data integration.

Implemented:

- structured XML data processing
- relational database persistence
- validation and error recording
- documented API endpoints
- analytical reports
- automated tests
- live deployment with Swagger documentation

Possible future improvements:

- authorized live BoardGameGeek sync for the deployed API
- persisted designer and publisher tables
- public game-search sync workflow
- pagination and advanced filters
- GitHub Actions CI workflow

## What I Learned

This project strengthened my understanding of API layering, database migrations, external data validation, repeatable synchronization, integration testing with mocked clients, environment-based configuration and deploying a backend API with a hosted PostgreSQL database.
