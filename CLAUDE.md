# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Flask-based web application for conducting colour naming experiments. The application presents colour stimuli to participants and collects their naming responses. It supports multiple languages and includes a colour naming system that uses perceptual distance calculations to find nearest colour terms.

## Development Setup

The project uses uv for Python dependency management and npm for JavaScript dependencies.

### Installing Dependencies

```bash
# Install Python dependencies
uv sync --locked --extra dev

# Install JavaScript dependencies
npm install
```

### Database Setup

The application requires PostgreSQL. For local development with Docker:

```bash
# Start containers
docker compose up -d postgres

# Initialize database
docker compose run --rm web initdb

# Import centroids (example for English)
docker compose run --rm web import-centroids /path/to/dataset_en.csv English en

# Import colour targets
docker compose run --rm web import-col-targets /path/to/targets.csv

# Start web server
docker compose up web
```

Alternatively, use the `colnam.sh` helper script:
- `colnam.sh -u` - start the test instance
- `colnam.sh -r` - reinitialize the test database
- `colnam.sh -d` - tear down the test instance

### Running the Application

```bash
# With Docker (recommended for development)
docker compose up web

# Without Docker (requires PostgreSQL running and COLOURNAMING_CFG environment variable set)
uv run flask run
```

The application requires a configuration file pointed to by the `COLOURNAMING_CFG` environment variable. See `docker.cfg` or `github.cfg` for examples.

## Building Assets

Frontend assets are built using esbuild:

```bash
# Build CSS
make css

# Build JavaScript
make js

# Build audio files (converts .wav to .mp3)
make audio

# Build everything
make all
```

## Testing

```bash
# Run tests via Flask CLI
uv run flask test

# Run tests directly with pytest
uv run pytest

# Run tests in CI environment
uv run flask test
```

The tests in `tests/integration/` drive each experiment from start to finish in a browser with Playwright and check what is stored in the database. They need Chromium, which is installed with:

```bash
uv run playwright install chromium
```

Tests require a PostgreSQL database. In CI, the database configuration is set via the `COLOURNAMING_CFG` environment variable pointing to `github.cfg`.

## Code Quality

```bash
# Lint with ruff
uv run ruff check colournaming

# Format with black
uv run black colournaming

# Type check with pyright
uv run pyright
```

Black is configured with `line-length = 100` and excludes `targets.py`.

## Architecture

### Application Structure

The application follows a Flask blueprint architecture with the following main modules:

- **home**: Landing page and general information
- **namer**: Colour naming system that finds nearest colour terms using perceptual distance
- **experimentcol**: Main colour naming experiment (foreground colours)
- **experimentcolbg**: Colour naming experiment with background colours
- **mturk**: Mechanical Turk integration for participant management
- **mturkage**: Mechanical Turk age-specific experiments

Each module follows a consistent structure:
- `model.py`: SQLAlchemy database models
- `controller.py`: Business logic and data manipulation
- `views.py`: Flask blueprint with routes
- `forms.py`: WTForms form definitions

### Application Factory

The app is created using the factory pattern in `colournaming/__init__.py`:

```python
app = create_app()
```

The factory:
1. Loads configuration from the `COLOURNAMING_CFG` environment variable
2. Initializes database (SQLAlchemy) and mail extensions
3. Sets up Babel for i18n with locale selection based on session or Accept-Language header
4. Registers blueprints for each module
5. Instantiates colour namers from database centroids

### Colour Naming System

The `ColourNamer` class in `colournaming/namer/controller.py` uses colour centroids stored in the database to find perceptual neighbours:

- Centroids are stored as means (μ) and covariance matrices (Σ) in LAB colour space
- The namer calculates Mahalanobis distance to find the nearest colour term
- Multiple language datasets can be loaded, each with their own centroids
- Namers are instantiated at app startup and stored in `app.namers`

### Database Models

The application uses Flask-SQLAlchemy with PostgreSQL. Key models:

- `Language`: Available languages with codes and names
- `ColourCentroid`: Colour term centroids with LAB colour space parameters
- `ColourTarget`: Stimuli presented in experiments
- `Participant`: Experiment participants with demographic data
- `ColourResponse`: Participant responses to colour stimuli

The database schema is created with `flask initdb` and dropped with `flask dropdb`.

### Frontend Build Pipeline

Assets are processed through esbuild:
- Source files: `assets/js/` and `assets/css/`
- Output: `colournaming/static/js/` and `colournaming/static/css/`
- Audio: `.wav` files in `assets/audio/{lang}/` are converted to `.mp3` using lame encoder

### Internationalization

The application uses Flask-Babel for i18n:
- Translation files: `colournaming/translations/{lang}/LC_MESSAGES/`
- Extract strings: `pybabel extract -F babel.cfg -k lazy_gettext -o messages.pot .`
- Update translations: `pybabel update -i messages.pot -d colournaming/translations`
- Compile translations: `pybabel compile -d colournaming/translations`
- Initialize new language: `pybabel init -i messages.pot -d colournaming/translations -l [language code]`

Locale selection is based on the `interface_language` session variable or the `Accept-Language` header.

### Flask CLI Commands

Custom commands available via `flask` CLI:

- `flask initdb` - Create database tables
- `flask dropdb` - Drop database tables
- `flask test` - Run test suite
- `flask import-centroids <file> <language_name> <language_code>` - Import colour centroids
- `flask import-col-targets <file>` - Import colour targets for foreground experiment
- `flask import-colbg-targets <file> [--delete-existing]` - Import targets for background experiment
- `flask import-colbg-backgrounds <file> [--delete-existing]` - Import background colours
- `flask mturk-tasks` - List completed MTurk tasks
- `flask mturk-age-tasks` - List completed MTurk age tasks

## Configuration

Configuration is loaded from a Python file via `COLOURNAMING_CFG` environment variable. Required settings:

- `SQLALCHEMY_DATABASE_URI`: PostgreSQL connection string
- `SECRET_KEY`: Flask secret key
- `LANGUAGES`: List of supported interface languages with codes and names
- `ADMIN_PASSWORD`: Password for admin functions
- `MTURK_RESPONSE_COUNT`: Number of responses required for MTurk completion

## Adding Language Datasets

To add a new language to the colour namer:

1. Create a CSV file with centroids (see `docs/` for format examples)
2. Create `.wav` audio files for each colour term
3. Place audio files in `assets/audio/{language_code}/`
4. Add a make rule to the Makefile following existing patterns
5. Run `make` to convert audio to mp3
6. Import centroids: `flask import-centroids /path/to/dataset.csv "Language Name" lang_code`
