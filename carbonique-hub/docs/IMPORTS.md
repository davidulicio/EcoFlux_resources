# Importing existing Carbonique records

Run imports against a **staging copy** first. The project does not contain the live EcoFlux database, Firebase credentials, or its private operational records.

## Existing EcoFlux database: preserve original IDs

The `inventory` app retains upstream migrations `0001`–`0012` and the table/model names `Site`, `Equipment`, `FieldNote`, `Photo`, `Document`, `History`, and `DOI`. New migrations add archive/reference/version fields and protect sites referenced by field notes. New workflow tables live in the separate `hub` app.

1. Back up the original database and media directory using the existing server's normal database tooling.
2. Restore the database into an isolated staging database and copy the media directory to a staging media location.
3. Configure `DATABASE_URL` or the original `DB_ENGINE`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` in this project's `.env`. Set `MEDIA_ROOT` to the copied media directory. Existing filename paths remain valid.
4. For MySQL/MariaDB, install its driver separately: `python -m pip install mysqlclient`. The bundled Linux Docker image is configured for PostgreSQL; a MySQL image also needs the system libraries required by mysqlclient.
5. Run:

```bash
python manage.py showmigrations inventory
python manage.py migrate
python manage.py setup_hub --grant-existing-users viewer
python manage.py import_fieldnotes --match-legacy-ids
```

`backfill_visits`, called by setup, creates exactly one visit linked to each original `FieldNote`. Original notes, IDs, text, photos, documents and equipment history remain intact. Date-only records use noon fixed EST as a storage placeholder, with that precision limitation retained in import provenance. It is not a measured arrival/departure time.

Existing superusers remain administrators. Other existing users get viewer access only if you pass `--grant-existing-users viewer`; otherwise assign roles individually in Django administration. Prefer deliberate role assignment rather than promoting all legacy accounts.

When original EcoFlux notes exist, the reference importer skips the copied Field Notes summaries by default. `--match-legacy-ids` adds classifications only when the original ID, site and visit date all agree. Unmatched notes are not guessed from date alone. Review counts and discrepancies before importing additional summaries with `--notes`.

The checked-in upstream source may differ from your deployed database. This upgrade was checked against the repository migrations, not your unseen production schema. If `showmigrations` differs, reconcile those migrations in staging first.

## Firebase / Field Log

The supplied Field Log stores tasks, visits and comments in nested Firestore collections. The read-only export script creates normalized JSON:

```bash
python -m pip install firebase-admin
python scripts/export_firestore.py --credential /secure/path/service-account.json --output /private/path/field-log.json
```

The credential file must belong to your Firebase project and stay outside the repository. The script reads collections; it does not alter Firestore or migrate passwords. The output contains team emails and operational records and should stay private.

Create an explicit site mapping file:

Save JSON inputs as UTF-8 (an optional UTF-8 BOM is accepted). Imports use an explicit encoding so accented names and scientific symbols are retained on Windows as well as Linux.

```json
{
  "actual-Firebase-site-document-ID": "UQAM_3",
  "another-Firebase-site-document-ID": "MCGILL_1"
}
```

Then import:

```bash
python manage.py import_field_log --file /private/path/field-log.json --site-map /private/path/site-map.json
```

No name-based fuzzy matching is performed. Stable UUIDs and import mappings make repeat imports idempotent without overwriting later edits. The importer preserves original JSON in `ImportRecord`, retains comments and system notes, and associates authors with existing Django accounts by email when available. Unmatched authors remain as recorded author names. Create Django team accounts separately; Firebase passwords are not copied.

The old Field Log overwrote task completion state when a task was reopened. Its export may therefore lack the full earlier sequence. Imported historical reports are labeled as reconstructed and preserve the available original records; missing events are not invented.

## Replacement Field Notes HTML

For public display, simply replace `public/fieldnotes/index.html`. No import is needed.

To also extract its embedded reference into structured JSON:

```bash
python scripts/extract_fieldnotes.py public/fieldnotes/index.html --output /private/path/reference-extract
python manage.py import_fieldnotes --file /private/path/reference-extract/fieldnotes.json
```

The extractor reads JSON constants and decodes embedded JPEG/PNG images. It never executes the source JavaScript.

The importer creates new source records, adds missing site reference metadata, and preserves existing edited records on subsequent runs. Updating the public HTML does not silently overwrite a researcher's reviewed caveat or configuration. To reconcile changed records, compare the new extract with import provenance and edit/review those changes through the application.

The bundled reference includes site setup information but does not establish purchase dates and identities for every individual instrument. It therefore does not invent inventory items. Configuration imports are document snapshots dated 2026-09-29, with historical effective periods explicitly unestablished. Uncertain caveat boundaries remain as prose until reviewed.

For UQAM_5, the source activation description is an installation range rather than a single date. The imported required date uses its earliest documented visit as a placeholder and records this basis in site metadata; verify it before using the date as station commissioning metadata.

## Reconciliation checks

- Site codes are mapped to a single canonical record; existing case variants such as `McGill_1` are matched case-insensitively.
- Compare source/export and destination record counts.
- Check original attachments, serial numbers and instrument histories.
- Confirm crews and authors; dates alone are not unique visit identifiers.
- Keep provenance records and the source exports until the migration is accepted.
- Test creating, editing and closing visits on the staging copy before switching the team.
