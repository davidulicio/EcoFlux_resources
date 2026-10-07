# Source provenance

This application was built for the Carbonique site network from the workflows and source supplied by the user:

| Repository | Inspected commit | Reused content |
|---|---|---|
| https://github.com/hknox/EcoFlux_resources | `295f850fdd7d999c3f415531da2e36be312510a6` | Inventory models, original migrations 0001–0012, upload-path helpers; latest navigation, related-record layout, header photograph and icons; retained author comments |
| https://github.com/davidulicio/carbonique-field-log | `d08166970f69b09480796ba2277f7b56d49522eb` | Field workflow design and Carbonique SVG branding |
| https://github.com/davidulicio/carbonique_fieldnotes | `c75bdcff90d1f993f53f79c3137176b231ba90d7` | Original public HTML; extracted classified notes, caveats, site reference, photographs and plots |

The field frontend, Django APIs, new workflow models, synchronization, import/backup commands and deployment package were implemented for this unified application. Original source/data attribution remains with its authors. This package does not assign a new license to upstream material.

The original Field Notes HTML is intentionally preserved rather than rewritten. It is available as a replaceable public snapshot independently of the editable database reference.

The initial integration used EcoFlux commit `664dc23ffcaef148b1a66e03d1cc627a7ca810a8`. The 2026-10-06 update merges the 11 subsequent upstream commits through `295f850` into the original runtime and adapts their related-record navigation and visual assets for the Hub. No upstream inventory model or migration changes occurred in that interval. See [docs/UPSTREAM_UPDATE.md](docs/UPSTREAM_UPDATE.md) for the update and validation details.
