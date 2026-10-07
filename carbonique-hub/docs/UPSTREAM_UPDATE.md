# EcoFlux upstream update — 2026-10-06

Hank's `main` was compared at `295f850fdd7d999c3f415531da2e36be312510a6` with the original integration base `664dc23ffcaef148b1a66e03d1cc627a7ca810a8`. The published integration branch used for this update is David's `integrate-carbonique-hub` at `a7f5ff81f1247fbf2784caeda1031c0191cf6e6d`.

The 11 upstream commits merge cleanly into that branch. They improve navigation, template formatting, the related-record accordion/tab row, the header photograph and favicons. They do not change inventory models, migrations or deployment database settings.

## What was incorporated

| Area | Updated original EcoFlux runtime | Adaptation in Carbonique Hub |
|---|---|---|
| Navigation | Hank's reorganized responsive header and revised labels | Existing unified navigation retained; winter tower photograph added behind the site selector |
| Related records | Horizontal related-record layout for sites, equipment and fieldnotes | Site tabs for reference, assigned equipment, visits, files and data identifiers; equipment-dialog tabs for service history and files |
| Visual assets | All new upstream favicon sizes, SVG, manifest and header photograph | Same photograph, SVG favicon, PNG favicon, Apple touch icon and 192/512 px install icons; Carbonique sidebar branding retained |
| Template/form cleanup | Latest upstream templates and form-protection script | Explicit non-submit buttons for dialog/tab actions; switching equipment tabs preserves the typed service observation |
| Offline use | Original runtime has no Hub offline cache | New Hub assets cached under shell v3; an existing prepared shell is retained during cache upgrade |

The Hub tabs support Left/Right arrows, Home and End, selected-state announcements and associated panels. File and equipment lists are scoped to the selected site; the Inventory section continues to provide the network-wide equipment view.

## Bugs fixed and preservation checks

- The upstream site-detail template used `{% static %}` without loading the tag library. A rendering regression reproduced the error; the import is now present.
- Favicon HTML size attributes use the standard `x` separator. The site fieldnote label typo is corrected.
- Hub action buttons explicitly use `type="button"`, including those inside dialogs, so navigation and attachment actions do not submit the surrounding form.
- The public report's header logo fits within the header on desktop and mobile.
- Closely spaced sensor heights have separated diagram labels and connecting lines; the displayed heights and sensor positions still use the recorded values.
- The previous site-edit fix still preserves notes, photos, documents and their file bytes. The navigation fallback fix also remains present.

The original public Field Notes HTML is byte-for-byte unchanged. Anonymous access, replacing the HTML file while the server runs, site permissions, imports and existing offline records remain supported.

## Updating an existing local Hub

1. Stop the local server with Ctrl+C.
2. Apply the repository update files, replacing matching source files and adding the new assets. Keep your existing `.env`, `.venv`, database and uploaded media.
3. From `carbonique-hub`, run the existing environment's Python:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py runserver
```

There is no new migration in this update. Running `migrate` also checks whether the existing installation still needs an earlier migration. Do not rerun the seed import to apply an interface update.

Open http://127.0.0.1:8000/ while online. The service worker updates its assets automatically; a browser refresh loads the current interface. For a production deployment, run `collectstatic --noinput` and restart the app process as usual.

## Validation

Python 3.12.14 and Django 5.2.18 were used. All 45 Hub tests and five original-runtime regression tests pass. The three added rendering tests cover the updated site, equipment and fieldnote pages through the production URL configuration with isolated SQLite settings. Django checks, missing-migration checks, static collection and frontend JavaScript syntax checks pass.

The browser update checks use a temporary SQLite database and media directory, never a live installation. Detailed results are recorded in [VALIDATION.md](VALIDATION.md).

The GitHub Desktop copy payload was applied after an upstream merge in a fresh checkout with `core.autocrlf=true`. Its complete Git tree matches the prepared update and the public HTML bytes match the original report.

## Keeping up with future EcoFlux changes

Merge Hank's upstream branch into the integration branch before making the next adaptation. Check shared inventory model/migration changes against both runtimes, then adapt applicable frontend behavior in `carbonique-hub`. Record the inspected upstream commit here or in `UPSTREAM.md` and run both CI jobs. The Hub remains a separately launched evaluation app until the group agrees on deployment and consolidation.
