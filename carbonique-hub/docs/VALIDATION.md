# Build validation

Checked on 2026-10-06 with Python 3.12.14, Django 5.2.18, SQLite, Gunicorn 23.0.0 and Chromium 153. No live operational database or Firebase project was accessed.

## Automated checks

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test hub
python manage.py collectstatic --noinput
```

All **45 backend tests passed**. Django reported no model/settings issues and no missing migrations. The frontend JavaScript passed syntax checks.

## Latest upstream update checks

EcoFlux `main` at `295f850fdd7d999c3f415531da2e36be312510a6` was merged into David's published integration at `a7f5ff81f1247fbf2784caeda1031c0191cf6e6d`. All 11 upstream commits merge cleanly; upstream inventory models and migrations are unchanged. The original public report retains its original bytes.

All **45 Hub tests and five original EcoFlux regression tests pass** after this update. The three additional legacy tests render the updated site, equipment and fieldnote pages through `EcoFlux.urls` with isolated SQLite settings. The site-page test reproduced a missing `{% load static %}` error before the correction. The existing edit-preservation and navigation-fallback checks still pass.

The updated Hub passed system checks, migration consistency checks, collection of 166 static files, and JavaScript syntax checks. A fresh temporary database was migrated and initialized with the six-site reference; no deployment database was used.

Chromium browser checks for this update verified:

- Anonymous original-report rendering and a correctly sized public header logo.
- All five site tabs, keyboard activation/wrapping, selected-state attributes and visit-report navigation.
- Selected-site equipment and files, using new and legacy documents from two separate sites to detect cross-site display mistakes.
- Equipment-dialog tab changes retain a typed service observation and do not submit the form; saving while the Files tab is selected still persists the note.
- Upgrading an actual v2 service worker to v3 retains the prepared shell, caches new visual assets and removes the old cache. No API replies appear in the shell cache.
- After the upgrade, a mobile browser fully reloads offline, reopens site tabs, records a visit and observation, and closes the visit. All three pending operations survive another reload, synchronize on reconnection, and appear in the frozen visit report.
- Desktop, 390 px mobile and dark-mode rendering, with no horizontal page overflow or unhandled JavaScript errors.

A focused diagram check verifies that heights of 24, 22, 21.9 and 1.68 metres all remain visible and that closely spaced label positions do not overlap. The refreshed browser preview exercises that diagram in the actual site view.

The 56-file copy payload was applied to a fresh integration checkout after merging upstream, with Windows-style Git conversion (`core.autocrlf=true`). The complete Git index tree matches the prepared update, and the public report's SHA-256 remains `4c147b6d76c2a54b9c480095772fc37e458aeab4164832955af65fb73f07ca8d`.

Earlier broader workflow/backup checks are recorded below. They are not claims that a live production upgrade was performed. This update's original-runtime checks exercise Django rendering and file preservation; its browser checks exercise the Hub.

The tests cover related-record preservation during site edits; protected site deletion; optimistic edit conflicts; role/site restrictions; retry-safe operations and uploads; frozen visit reports and revisions; dependency ordering; closed-visit restrictions; deployment overlap, removal and equipment identity; configuration immutability; date validation; attachment scope and file validation; spreadsheet-safe exports; legacy backfill; repeat reference/Firestore imports; CSRF enforcement; and anonymous live HTML replacement.

The public replacement test writes Version A and then Version B to the same configured HTML path and verifies that the next response serves Version B, with caching disabled and a response-level sandbox.

## Browser checks

The actual Django application was exercised in headless Chromium, using desktop and 390 px mobile viewports:

- Original public HTML renders without signing in; its iframe scripts render the site reference.
- Team login, navigation and site selection work.
- Preparing a site saves the application shell and selected snapshots.
- With the browser offline, a visit, observation and visit closure are retained across a full page reload.
- Reconnection uploads the ordered queue and the resulting frozen report contains the observation.
- A database with no sites supports creating its first site and immediately opening its workspace.
- Task planning, equipment creation, deployment height, configuration creation, caveat review and evidence upload work through the forms.
- An administrator can create a viewer account; that account can inspect task activity without field-write controls.
- Sign-out clears the device copies and returns to login. Navigation remains scrollable on shorter displays.
- No unhandled JavaScript errors were observed. The mobile history view had no horizontal page overflow.

## Startup, production server and backup checks

A fresh SQLite database was migrated and initialized from the bundled reference. It contained **6 sites, 127 visits, 19 caveats and 30 attachment records/files**. Repeat imports retained the same records and later edits.

A portable backup was restored into a separate migrated, empty database and media directory. The site/visit/caveat counts, a temporary account's password hash and every attachment path were verified; all **30 media files had identical SHA-256 hashes** before and after restore. Temporary test accounts and databases are excluded from the source package.

Gunicorn was started with production settings, a temporary random secret and local HTTP for the smoke check. Health, public HTML, login and collected static-asset routes returned successful responses. Production HTTPS redirection and proxy settings still need to match the actual host.

`check --deploy` completed with one deliberate warning, `security.W021`: HSTS preload is disabled. Submitting an actual hostname to a browser preload list is a separate administrator decision; normal HTTPS and HSTS settings are enabled in production defaults.

## Scope and remaining deployment checks

These checks validate this build, not an unseen production installation. Docker Compose, PostgreSQL/MariaDB, real SMTP, live Firestore credentials, production TLS and an actual EcoFlux database upgrade were not exercised here. Windows startup instructions are provided, but the build environment was Linux.

Validate an upgrade against a staging copy of the live database/media before switching the team. Confirm counts, original attachments, crews and instrument identities. The bundled import intentionally leaves uncertain scientific periods for researcher review. No flux computation or automatic reconciliation of replacement HTML with edited database records occurs.

See [IMPORTS.md](IMPORTS.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for those steps.
