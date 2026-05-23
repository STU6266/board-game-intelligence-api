# Board Game Intelligence API

Board Game Intelligence API is a backend and data integration project built with Python, FastAPI and PostgreSQL.

The project will import board game data from the BoardGameGeek XML API, transform XML responses into structured relational data, and expose REST endpoints for search, filtering and analytical reports.

## Project Goal

This project is built as a professional portfolio project focused on:

- API integration
- XML data processing
- ETL-style import logic
- PostgreSQL relational modeling
- data quality checks
- REST API design
- automated testing
- OpenAPI documentation

## Current Status

Completed foundation and first API read flow:

- FastAPI application with versioned API routes
- PostgreSQL development database running through Docker Compose
- SQLAlchemy database connection and dependency setup
- Alembic migrations for the initial relational data model
- Core tables for games, ratings, categories and mechanics
- Import tracking tables for future external data synchronization
- Health and database health endpoints
- Read endpoints for listing games and retrieving game details
- Local demo seed script for API development and testing
- Local XML fixture representing a BoardGameGeek-style game response
- XML parser service with automated unit tests for game, rating and linked metadata extraction
- Data quality validation service with automated tests for invalid and incomplete imported game data
- Analytical report logic with family score, complexity, playtime and age-group labels
- Report endpoints for family-friendly and low-complexity/high-rating game recommendations

Current demo records are development-only seed data. Importing real board game data from the BoardGameGeek XML API is planned for a later phase.

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- Docker Compose
- Pytest
- SQLAlchemy
- Alembic

## Run Locally

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

## Health Check

```text
GET /api/v1/health
GET /api/v1/health/db
```

Expected response for the application health endpoint:

```json
{
  "status": "ok",
  "service": "board-game-intelligence-api"
}
```

Expected response for the database health endpoint:

```json
{
  "status": "ok",
  "database": "connected"
}
```

## Available Endpoints

### Health

```text
GET /api/v1/health
GET /api/v1/health/db
```

### Games

```text
GET /api/v1/games
GET /api/v1/games/{id}
```

`GET /api/v1/games` returns a list of stored board games with basic metadata and rating information.

`GET /api/v1/games/{id}` returns a detailed game record including rating data, categories and mechanics.

## Development Seed Data

For development testing, the project includes a small seed script with clearly marked demo board games. The records use negative `bgg_id` values so they do not conflict with future imported BoardGameGeek records.

Run the seed script:

```bash
python -m scripts.seed_games
```

The script can safely be run more than once. Existing demo games are skipped instead of being inserted again.

## XML Parser Development

The project includes a local XML fixture that represents the structure of a BoardGameGeek-style game detail response:

```text
sample_data/bgg_thing_sample.xml
```

The parser service converts XML data into validated Python objects before future database synchronization:

```text
app/services/bgg_parser.py
```

Currently extracted data includes:

- game ID and primary name
- publication year, player count, playtime and minimum age
- rating and complexity information
- overall rank
- categories and mechanics
- designers and publishers

The local XML fixture is used during development so parser behavior can be tested without depending on live API calls or external rate limits.

## Testing

Run the automated tests:

```bash
pytest -v
```

Current data quality tests verify:

- valid parsed data passes validation
- invalid player ranges are rejected
- invalid playtime and rating values are rejected
- missing optional data creates warnings without blocking import

## Data Quality Validation

Before parsed external data is written to the database, the project validates important business and consistency rules.

Current validation errors include:

- minimum player count greater than maximum player count
- negative playtime values
- minimum playtime greater than maximum playtime
- negative minimum age
- rating values outside the valid range of 0 to 10
- complexity values outside the valid range of 0 to 5
- negative user rating counts

Incomplete but still usable data is handled as a warning rather than a blocking error. Current warnings include:

- missing description
- missing rating data

This validation layer prepares the project for a controlled synchronization process in which invalid imported records can be rejected and logged instead of silently being stored in PostgreSQL.