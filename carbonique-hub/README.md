# Carbonique Hub

A unified Django application for Carbonique eddy covariance site operations, instrument records and scientific context. It brings together the workflows of **carbonique-field-log**, **EcoFlux_resources** and **carbonique_fieldnotes**.

Updated against Hank's EcoFlux `main` at **`295f850`** on 2026-10-06. This update adds related-record tabs and the latest EcoFlux visual assets, with no new database migration. See [docs/UPSTREAM_UPDATE.md](docs/UPSTREAM_UPDATE.md) for changes and upgrade steps.

## Start locally

Requires **Python 3.12 or newer** (tested with Python 3.12), a modern browser, and no Node build step. SQLite is included with Python. Windows runs the Django development server; Gunicorn is for Linux production servers.

### Windows PowerShell

From the EcoFlux_resources checkout, open its `carbonique-hub` subdirectory in PowerShell. Run commands one at a time, stopping if any command fails. If Python 3.12 is missing, install it before creating the environment. Then run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py setup_hub --with-reference
.\.venv\Scripts\python.exe manage.py createsuperuser
.\.venv\Scripts\python.exe manage.py runserver
```

If your installed Python is newer, use `py -m venv .venv` instead of `py -3.12`.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py setup_hub --with-reference
python manage.py createsuperuser
python manage.py runserver
```

Open **http://127.0.0.1:8000/** for the team workspace and **http://127.0.0.1:8000/fieldnotes/** for the public Field Notes. No passwords or default login accounts are included.

`setup_hub --with-reference` imports the supplied repository snapshot: **6 sites, 127 classified visit summaries, 19 data caveats, photographs, diagnostic plots and instrument reference information**. The caveats enter the editable database as drafts; a researcher reviews them. Equipment inventory from the live EcoFlux database and tasks from Firebase are not in the public repositories and must be imported separately.

To start without the bundled records, use `python manage.py setup_hub` without `--with-reference` and create sites under Administration.

## Public Field Notes: drop in a replacement HTML

The original `carbonique_fieldnotes` report is included unchanged at:

```text
public/fieldnotes/index.html
```

Replace this file with your updated self-contained HTML, keeping the filename. **/fieldnotes/** immediately reads the current file on the running server, without a login, database import or restart. The maintenance timeline, caveats, plots, site cards and mast diagrams remain those of the supplied report.

- If you replace the file on the server, the next page load uses the new version.
- If you upload it to GitHub, pull/deploy that commit to the server.
- The supplied Docker Compose setup mounts this folder, so host-file replacements appear immediately.
- It runs in a sandbox that allows its own scripts but isolates it from private workspace cookies and APIs.
- The public HTML is a snapshot; replacing it does not overwrite database records.

An optional database-driven public view at **/reference/** publishes only selected sites and reviewed caveats. Enable `PUBLIC_REFERENCE_ENABLED=True`, then explicitly mark sites and caveats for publication. The richer original HTML remains available at `/fieldnotes/`.

## What the team workspace includes

| Section | Features |
|---|---|
| Overview | Site network, pending tasks, visits and unresolved caveats |
| Field work | Off-site planning; on-site visits; task completion; unplanned work; observations; checklists |
| History | Searchable visits and all task activity, classifications, frozen report revisions, CSV exports and attachments |
| Sites & instruments | Tabs for reference metadata, sensor-height/deployment history, site equipment, visits, photos/documents and DOI records |
| Data & processing | Draft/reviewed/resolved caveats, affected periods, evidence and immutable configuration versions |
| Inventory | Serial numbers, models, current locations, service-history/files tabs and archived equipment |
| Administration | Sites, accounts, roles, site access and maintenance checklists |

The selected site is shared by all sections. The browser polls changes every 15 seconds while online, and uploads queued operations when connectivity returns.

## Roles

| Role | Read records | Field work / attachments | Scientific records / inventory | Team and sites |
|---|---|---|---|---|
| Viewer | Yes | No | No | No |
| Member | Yes | Yes; may propose draft caveats | Service observations only | No |
| Researcher | Yes | Yes | Yes; may review caveats and create configurations | No |
| Admin | Yes | Yes | Yes | Yes |

A superuser is an administrator. Other accounts need a `TeamMember` role. An empty allowed-sites list means all sites; selecting sites restricts access to those sites. The public HTML is intentionally visible to everyone independently of private team restrictions. Create accounts in Administration; passwords are hashed by Django. No automatic invitation email is sent.

## Offline fieldwork

1. Sign in while connected, on a trusted device.
2. Use **Prepare for fieldwork** and select the sites and attachments to download.
3. Open the prepared site. Visits, tasks, observations, draft issues and files are stored in IndexedDB before upload.
4. The app can be reopened offline after its shell and site data have been prepared. This needs **HTTPS**, or `localhost` / `127.0.0.1` during development.
5. Reconnect and open the app. Check that the sync queue is empty before clearing the device.

The interface distinguishes local pending records from synchronized data. Retried operations and uploads use stable identifiers, avoiding duplicate records. Conflicting edits pause the queue and require review rather than silently overwriting another user's work. Use **Sync queue** to review, retry or export a blocked record.

The app must be open to upload; it does not promise synchronization while a phone/browser is closed. New-device login requires a connection. Server sessions can expire while offline: sign in again with the original account to upload its queued work. Browser storage can be cleared by the operating system; keep pending records synchronized when possible. Sign out and clear the device only after resolving pending work.

## Scientific record conventions

- Logger/measurement times use **fixed EST, UTC−05:00**, without daylight saving time. The configuration and caveat editors explicitly convert those timestamps to UTC for storage.
- Visit and installation timestamps use actual instants; the UI displays local browser time.
- Unknown historical boundaries remain unspecified, with an explanatory period label. The import does not infer questionable timestamps from caveat prose.
- Instrument deployment periods cannot overlap for the same individual instrument.
- Configuration records are immutable; a correction creates a new version linked to its predecessor.
- Closing a visit freezes a report. Reopening a task does not change an earlier report. Reopening and reclosing a visit creates another report revision.
- Sites, tasks and equipment are archived, not deleted through the working app.

## Import existing operational data

See **[docs/IMPORTS.md](docs/IMPORTS.md)** for:

- Upgrading a copy of the EcoFlux database without changing its original table identities.
- Importing Firestore tasks, visits and comments with an explicit site-ID mapping.
- Extracting a replacement Field Notes HTML into structured reference data.

## Deployment

See **[docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)** for a Linux/Gunicorn installation and Docker Compose with PostgreSQL. GitHub stores the source; **GitHub Pages cannot run this Django backend**. Serve the application at the root of its own hostname; subpath hosting such as `/ecoflux/` is not configured in this build.

Before production, set a strong random `SECRET_KEY`, `DEBUG=False`, your hostname in `ALLOWED_HOSTS`, HTTPS/CSRF origin settings, a persistent database/media location, and SMTP if password resets are needed. The application refuses an insecure development secret with `DEBUG=False`.

## Checks and backups

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test hub
python manage.py collectstatic --noinput
python manage.py backup_hub --output backups/carbonique.zip
```

`backup_hub` includes fixture data and uploaded files. Pause writers before portable backups for a consistent snapshot. Use native database backups plus media backups for production. Keep backups private: they contain research records and account password hashes. Restore into a migrated, empty database using:

```bash
python manage.py restore_hub --file /path/to/carbonique.zip
```

Public `public/fieldnotes/index.html` is managed by the repository and should be backed up through Git as well.

## Repository upload

This application is included as the `carbonique-hub/` subdirectory of EcoFlux_resources. Commit that directory together with the root integration documentation, legacy fixes/tests and `.github/workflows/carbonique-hub.yml`. Keep the directory structure and include `seed/media/`, which contains the supplied reference photographs and plots. `.gitignore` excludes local databases, passwords, uploads and exports. The downloadable source archive excludes the test database and test accounts.

## Upstream and implementation notes

See **[UPSTREAM.md](UPSTREAM.md)** for source provenance and **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for data relationships, API and synchronization behavior. **[docs/VALIDATION.md](docs/VALIDATION.md)** records the checks performed for this build.
