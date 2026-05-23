# Board Game Intelligence API

Board Game Intelligence API is a backend and data integration portfolio project built with Python, FastAPI and PostgreSQL.

The application is designed to retrieve board game data from the BoardGameGeek XML API2, transform XML responses into validated relational data, store synchronization history and expose REST endpoints for browsing games and generating analytical recommendations.

## Why I Built This

I built this project to demonstrate backend development skills beyond simple CRUD operations.

The project focuses on:

- integrating an external XML API
- parsing and transforming third-party data
- validating imported data before storage
- designing a normalized relational database
- handling repeated synchronization without duplicate records
- recording import history and errors
- exposing documented REST endpoints
- calculating analytical recommendation reports
- writing automated tests for important application logic

The board game topic gives the project a practical domain: users can understand whether a stored game is family-friendly, easy to learn, highly rated or suitable for a short game session.

## Current Project Status

Implemented:

- FastAPI application with versioned API routes
- PostgreSQL development database through Docker Compose
- SQLAlchemy database connection and session dependency
- Alembic database migrations
- normalized database models for games, ratings, categories and mechanics
- import tracking models for synchronization runs and errors
- health and database health endpoints
- game list and game detail endpoints
- local development seed script
- local BoardGameGeek-style XML fixture
- XML parser service
- data quality validation service
- local XML synchronization workflow
- duplicate prevention through update-by-`bgg_id` logic
- analytical report service and recommendation endpoints
- BoardGameGeek HTTP client with token configuration, request throttling and error handling
- live synchronization endpoint prepared for authorized BGG API access
- import-run history endpoints
- automated unit test suite with 36 passing tests

A real live BoardGameGeek import requires an authorized API token configured locally. Without a token, the application can still be developed and tested through the local XML fixture and mocked client responses.

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

The project separates responsibilities into dedicated layers:

```text
app/api/           HTTP endpoints and request handling
app/models/        SQLAlchemy database models
app/schemas/       Pydantic request and response structures
app/repositories/  Database query logic
app/services/      Parsing, validation, synchronization and report logic
app/db/            Database base class and session setup
app/core/          Application configuration
tests/             Automated unit tests
scripts/           Local development scripts
sample_data/       XML fixture used during development and testing
```

## Data Model

### Core Game Data

```text
games
ratings
categories
mechanics
game_categories
game_mechanics
```

Each game stores core information such as:

- external BoardGameGeek ID
- name
- publication year
- description
- supported player count
- playtime
- minimum recommended age
- synchronization timestamp

Ratings are separated into their own table and include:

- average rating
- Bayesian average rating
- number of ratings
- average weight / complexity
- overall rank

Categories and mechanics use many-to-many relationships because one game can belong to several categories and contain several mechanics.

### Import Tracking

```text
import_runs
import_errors
```

Each synchronization attempt records:

- source
- status
- start and finish time
- games found
- games created
- games updated
- games skipped
- error count
- descriptive message

Errors are stored separately and linked to the related import run. This makes unsuccessful imports reviewable instead of losing the information in terminal output only.

## API Endpoints

Interactive Swagger documentation is available locally at:

```text
http://127.0.0.1:8000/docs
```

### Health

```text
GET /api/v1/health
GET /api/v1/health/db
```

`GET /api/v1/health` checks whether the FastAPI application is running.

`GET /api/v1/health/db` checks whether the API can reach PostgreSQL.

### Games

```text
GET /api/v1/games
GET /api/v1/games/{game_id}
```

`GET /api/v1/games` returns stored games with core metadata and rating information.

`GET /api/v1/games/{game_id}` returns a detailed game record including categories and mechanics.

### Analytical Reports

```text
GET /api/v1/reports/family-friendly
GET /api/v1/reports/low-complexity-high-rating
```

`GET /api/v1/reports/family-friendly` calculates a transparent family suitability score and returns games ordered by suitability.

`GET /api/v1/reports/low-complexity-high-rating` returns games with:

```text
average_rating >= 7.0
average_weight <= 2.5
```

Results are ordered by rating, complexity and name.

### Synchronization and Import History

```text
POST /api/v1/sync/games/{bgg_id}
GET  /api/v1/import-runs
GET  /api/v1/import-runs/{import_run_id}
```

`POST /api/v1/sync/games/{bgg_id}` requests current game data from BoardGameGeek, validates the parsed record and creates or updates the stored game.

This endpoint requires a valid local `BGG_API_TOKEN`.

`GET /api/v1/import-runs` returns recorded synchronization attempts.

`GET /api/v1/import-runs/{import_run_id}` returns a single import run including stored errors.

## XML Parsing

The project contains a local XML fixture for development and automated testing:

```text
sample_data/bgg_thing_sample.xml
```

The parser service converts XML game details into validated internal data structures:

```text
app/services/bgg_parser.py
```

Parsed information currently includes:

- BoardGameGeek ID
- primary game name
- publication year
- description
- player range
- playtime
- minimum age
- average rating
- Bayesian rating
- user rating count
- complexity value
- overall ranking
- categories
- mechanics
- designers
- publishers

Designers and publishers are already parsed for future expansion, but are not currently persisted as database tables in the MVP.

## Data Quality Validation

Before parsed external data is stored, the synchronization process validates important consistency rules.

Blocking validation errors include:

- minimum player count greater than maximum player count
- negative playtime values
- minimum playtime greater than maximum playtime
- negative minimum age
- rating values outside the range `0` to `10`
- complexity values outside the range `0` to `5`
- negative user rating counts

Incomplete but still usable data is treated as a warning rather than a blocking error:

- missing description
- missing rating data

Invalid records are skipped and recorded in `import_errors`.

## Synchronization Logic

The synchronization service supports both a local development workflow and live API integration.

### Local Fixture Sync

For development without external API access:

```bash
python -m scripts.sync_sample_game
```

The local fixture is parsed, validated and synchronized into PostgreSQL.

### Duplicate Handling

The external `bgg_id` is unique in the database.

```text
First synchronization of a BGG ID  → new game is created
Later synchronization of same ID   → existing game is updated
```

This prevents duplicate records during repeated imports.

### Live BGG Integration

The live client is implemented in:

```text
app/services/bgg_client.py
```

It supports:

- BoardGameGeek `thing` requests with statistics
- BoardGameGeek `search` requests for future expansion
- Bearer token authorization
- configurable timeout
- configurable delay between requests
- controlled handling of temporary service errors

A registered and authorized BoardGameGeek API token is required to perform real live imports.

## Analytical Reports

### Family-Friendly Score

The family-friendly report calculates a `family_score` between `0` and `100`.

The score considers:

- average rating
- average complexity
- minimum recommended age
- playing time
- supported player range

Games receive higher scores when they are well rated, comparatively easy to learn, suitable for younger players, playable within a reasonable duration and usable with family-sized groups.

Very high complexity and very long playtime reduce the score.

### Derived Labels

The report service also derives readable labels from numeric data.

#### Complexity

```text
0.0 - 1.5  → Very Light
1.6 - 2.5  → Light / Medium
2.6 - 3.5  → Medium / Heavy
3.6 - 5.0  → Heavy
```

#### Playtime

```text
0 - 30 minutes    → Quick
31 - 60 minutes   → Standard
61 - 120 minutes  → Long
More than 120     → Very Long
```

#### Age Group

```text
Up to 7 years     → Kids
8 - 12 years      → Family
13 - 15 years     → Teen
16+ years         → Adult
```

## Run Locally

### Requirements

Install these tools before starting:

- Python 3.12 or compatible Python 3 version
- Docker with Docker Compose
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/STU6266/board-game-intelligence-api.git
cd board-game-intelligence-api
```

Replace `<repository-url>` with the public GitHub repository URL.

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Local Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

The local `.env` file contains database and optional BoardGameGeek API configuration.

Example:

```env
APP_NAME=Board Game Intelligence API
APP_ENV=development

POSTGRES_DB=board_games
POSTGRES_USER=boardgame_user
POSTGRES_PASSWORD=boardgame_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

DATABASE_URL=postgresql+psycopg://boardgame_user:boardgame_password@localhost:5432/board_games

BGG_BASE_URL=https://boardgamegeek.com/xmlapi2
BGG_API_TOKEN=
BGG_REQUEST_DELAY_SECONDS=5
BGG_REQUEST_TIMEOUT_SECONDS=15
```

Never commit a real API token or local `.env` file to GitHub.

### 5. Start PostgreSQL

```bash
docker compose up -d
```

Check that the container is running:

```bash
docker compose ps
```

### 6. Apply Database Migrations

```bash
alembic upgrade head
```

### 7. Add Development Seed Data

```bash
python -m scripts.seed_games
```

The seed script creates clearly identified development-only records. Their negative `bgg_id` values separate them from later imported BoardGameGeek records.

### 8. Synchronize the Local XML Fixture

```bash
python -m scripts.sync_sample_game
```

This tests the parser, validation and synchronization workflow without requiring live API access.

### 9. Start the API

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Testing

Run the full automated test suite:

```bash
pytest -v
```

Current result:

```text
36 passed
```

The test suite covers:

- XML parser field extraction
- handling of missing parser data
- data quality validation rules
- local synchronization creation and update behavior
- synchronization error logging
- derived labels and family score calculation
- analytical report filtering and sorting
- BoardGameGeek client authorization and HTTP error handling
- live-sync service behavior using mocked client responses

Tests do not require real BoardGameGeek network access or a real API token.

## API Source and Usage Note

Board game data accessed through the live synchronization feature is provided by BoardGameGeek through its XML API2.

The live integration is implemented, but real execution requires an authorized BoardGameGeek application token configured locally. Any public-facing deployment displaying BoardGameGeek data should follow the applicable BoardGameGeek XML API terms and attribution requirements.

## Project Scope

This version is a portfolio-ready MVP.

Included in the MVP:

- structured external XML data processing
- controlled database synchronization
- data validation and error recording
- documented REST endpoints
- analytical reports
- automated tests

Possible future extensions:

- persist designers and publishers in dedicated relational tables
- expose a public game-search synchronization workflow
- add pagination and advanced filters to game endpoints
- deploy the API publicly with securely configured BGG authorization
- add CI test execution through GitHub Actions

## What I Learned

This project strengthened my understanding of:

- separating API, service, repository and database responsibilities
- building repeatable database migrations
- translating external XML data into relational application data
- validating external input before database storage
- preventing duplicate records during repeated synchronization
- designing useful API reports from stored data
- testing external integrations without relying on live network requests
- handling configuration and secrets safely through environment variables