This project implements a Django-based website to manage resources for the EcoFlux lab.

## Carbonique Hub integration

The unified Carbonique application is in **[carbonique-hub/](carbonique-hub/README.md)**. It combines field planning and visits, EcoFlux-compatible inventory, instrument deployments, scientific data caveats, dated configurations, team access and offline field recording.

The existing EcoFlux application runs from the repository root. To test the new unified application, change into `carbonique-hub` and follow its README. The two entry points are alternative runtimes: start each from its own directory and use a separate database/media configuration when comparing them.

The public Field Notes report is included at `carbonique-hub/public/fieldnotes/index.html`. The Hub serves it at `/fieldnotes/` without login. Replacing that HTML on the running Hub server updates the next public page load without a restart. GitHub changes must also be pulled/deployed to the server.

For moving existing operational data, see **[carbonique-hub/docs/IMPORTS.md](carbonique-hub/docs/IMPORTS.md)**. Upgrade a staging copy of the database and media first; coordinate the final switch with the server administrator. The repository reference is included, but live EcoFlux/Firebase records and credentials are not bundled.

### Quick start for the unified application (Windows)

Requires Python 3.12 or newer; this build was tested with Python 3.12. Run commands one at a time. If `py -3.12` reports no runtime, install Python 3.12 before continuing.

```powershell
cd carbonique-hub
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py setup_hub --with-reference
```

Create a login and complete its interactive prompts:

```powershell
.\.venv\Scripts\python.exe manage.py createsuperuser
```

Then run:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ for the team app and http://127.0.0.1:8000/fieldnotes/ for the public report. Linux/macOS and production instructions are in the application README and deployment documentation.

### Checks

From `carbonique-hub/`, with its dependencies installed:

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py collectstatic --noinput
python manage.py test hub
```

The root legacy application has separate regression tests for preserving records/files during a site edit and resolving navigation fallbacks. These use isolated in-memory SQLite settings, independently of the deployment `.env`:

```bash
python -m pip install -r requirements-legacy-tests.txt
python manage.py test inventory --settings=EcoFlux.test_settings
```

Run that second pair from the **repository root**, using an appropriate Python environment. The root GitHub Actions workflow `.github/workflows/carbonique-hub.yml` runs both suites in separate jobs.

See **[carbonique-hub/docs/INTEGRATION_REVIEW.md](carbonique-hub/docs/INTEGRATION_REVIEW.md)** for layout, compatibility and review notes.
