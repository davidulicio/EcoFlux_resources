# Integration review notes

## Proposed behavior

This contribution adds a runnable unified Carbonique Hub under `carbonique-hub/`, with one Django backend and one team interface for field operations, inventory and scientific reference records. Its public Field Notes section embeds the original supplied report, served from a replaceable HTML file without login. The integration now includes Hank's latest EcoFlux changes through `295f850` and their corresponding Hub adaptations.

The root EcoFlux runtime remains available during evaluation. Adoption of the Hub is an explicit server deployment and data-migration step, rather than an automatic switch caused by merging the source.

## Repository layout

| Path | Purpose |
|---|---|
| Root `manage.py`, `EcoFlux/`, `inventory/` | Existing EcoFlux runtime; legacy site-edit/navigation fixes and their tests |
| `carbonique-hub/manage.py` | Unified application entry point |
| `carbonique-hub/inventory/` | Compatible inventory model names and migrations 0001–0012; additional Hub migrations |
| `carbonique-hub/hub/` | New roles, field operations, reports, deployments, configurations, caveats, attachments and imports |
| `carbonique-hub/public/fieldnotes/index.html` | Original public report; replace on the server to update the public section |
| `carbonique-hub/seed/` | Repository reference data and intentionally tracked photographs/plots |
| `.github/workflows/carbonique-hub.yml` | Separate CI jobs for Hub and legacy regression tests |

The two runtime directories contain independent implementations of the Django app label `inventory`. Launch the selected runtime from its own directory; do not combine both implementations in one Python process. During evaluation use separate database/media locations. Production adoption should stop old writers and switch to the validated Hub runtime after migrating a staging copy.

Inventory models are duplicated intentionally for this opt-in review layout. This makes the complete new app independently testable without changing the original runtime's schema/settings. Consolidating to a single default runtime can follow an accepted deployment/migration decision. Until then, changes to shared schema assumptions should be reviewed against both copies.

## Existing application fixes

1. `SiteUpdateView.form_valid` previously deleted site documents, field notes, their photos and documents before saving an ordinary site edit. Those deletion loops have been removed. The regression test checks both database relationships and actual attachment bytes.
2. `get_return_url` previously attempted to reverse a fallback that might already be a resolved/lazy URL. With empty navigation history, this could raise `NoReverseMatch`. It now uses `resolve_url`, with regression cases for a route name, URL and lazy URL.

The legacy fixes require no database migration. They can be reviewed independently from the added Hub.

## Compatibility and provenance

- The Hub retains upstream inventory table identities and migration history. Its new fields and workflow tables require its additional migrations when upgrading a copied database.
- Backfill creates visits linked to original field notes; original IDs and files are retained. Imported summaries are not automatically guessed/duplicated when legacy notes exist.
- Firestore imports require an explicit site mapping and an authorized export. Passwords are not copied from Firebase.
- The bundled reference contains 6 sites, 127 visit summaries, 19 draft caveats and 30 attachment records/files. Uncertain historical periods remain for researcher review.
- Replacing public HTML does not overwrite edited database reference records. The public report is a separately maintained snapshot.
- Runtime uploads, databases, local environments and credentials are excluded by Git rules. `seed/media` is deliberately tracked.
- JSON imports explicitly read UTF-8 and accept its optional BOM, retaining accented names/scientific symbols independently of the Windows system encoding. The public report is stored as binary in Git to preserve its exact bytes across line-ending settings.
- Source commits and attribution are listed in [../UPSTREAM.md](../UPSTREAM.md). No new license is imposed on upstream material.

## Validation

The updated integrated layout was checked with Python 3.12 and Django 5.2.18. The **45 Hub tests and 5 legacy regression tests pass**. Django system checks, missing-migration checks, fresh initialization and static collection pass. The legacy preservation test was observed failing against the destructive update view before the fix. The new site-page rendering test also reproduced the upstream missing-static-import error before its fix.

The Hub's earlier browser checks verified anonymous report rendering, field workflows, offline reload/reconnection, forms, account roles and mobile layout. Its earlier portable backup/restore check verified matching attachment bytes. Those checks concern this implementation, not an unseen live deployment.

The original contribution was prepared against upstream `664dc23ffcaef148b1a66e03d1cc627a7ca810a8`. This update merges upstream `295f850fdd7d999c3f415531da2e36be312510a6` into the published integration at `a7f5ff81f1247fbf2784caeda1031c0191cf6e6d`. All 11 upstream commits merge without conflicts, and there are no upstream schema changes. Source assets include all 15 seed photographs/plots; the public report remains byte-for-byte unchanged. The existing CI jobs cover both runtimes and will run after this update is pushed. See [UPSTREAM_UPDATE.md](UPSTREAM_UPDATE.md) for the adaptation and upgrade instructions.

Docker, Windows execution, a real production database upgrade, SMTP and live Firebase were not exercised in this environment. Follow [IMPORTS.md](IMPORTS.md) and [DEPLOYMENT.md](DEPLOYMENT.md) for staged adoption.
