# Board Game Intelligence API — Portfolio Summary

## Short Description

Board Game Intelligence API is a backend and data integration project built with Python, FastAPI and PostgreSQL. It processes BoardGameGeek XML API2 data, validates and stores normalized game information, tracks synchronization results and exposes REST endpoints for game lookup and analytical recommendations.

## Technical Focus

- Python and FastAPI REST API design
- PostgreSQL relational data modeling
- SQLAlchemy ORM and Alembic migrations
- XML parsing and transformation
- external API client design with token configuration and throttling
- data quality validation
- duplicate-safe synchronization logic
- import history and error tracking
- analytical report generation
- automated testing with Pytest and mocked HTTP responses

## Main Features

- game listing and detail endpoints
- BoardGameGeek-style XML parsing
- controlled local and live synchronization workflows
- update-existing-record behavior based on unique external IDs
- import-run and error-history endpoints
- family-friendly recommendation scoring
- low-complexity/high-rating recommendation report
- Swagger/OpenAPI API documentation
- 36 passing automated tests

## Honest Project Status

The live BoardGameGeek integration is implemented and tested through mocked responses. Running a real external import requires an authorized BoardGameGeek API token configured locally.

## Portfolio Card Text

**Board Game Intelligence API**  
Backend and data integration API built with Python, FastAPI and PostgreSQL. Processes BoardGameGeek XML data, validates and synchronizes relational game records, tracks import errors and exposes analytical endpoints for family-friendly and accessible high-rated game recommendations.

## Skills Demonstrated

Python · FastAPI · PostgreSQL · SQLAlchemy · Alembic · REST APIs · XML Parsing · External API Integration · Data Validation · Docker Compose · Pytest