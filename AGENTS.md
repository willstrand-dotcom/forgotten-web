# Forgotten Web maintenance

Preserve the existing hot-pink retro OS, desktop icons, window navigation and games. The HTML catalog is an additional crawlable reading view, not a redesign.

## Discovery dates and ordering

- **Newest means most recently added to this site**, never the source’s original publication date.
- `finds.json` is the discovery-date ledger. Existing addition timestamps and `addedCommit` values were recovered from the first Git commit containing each relic.
- Keep the original publication date separate. Never overwrite an existing `addedAt` when updating a find.
- When adding a find, add one metadata record to `finds.json`, including key, title, current local ISO `addedAt` with timezone, matching `addedDate`, original publication metadata, source URL, category and description. The new record's `addedCommit` can be null until its first publication commit exists; do not invent a hash.
- Add the full relic object to the `relics` registry and add its `finds.json` record. The builder creates or updates Start, Latest, category membership, random keys and RSS automatically. Existing hand-written row descriptions are preserved; new rows use the supplied metadata description.

## Required build and checks

```sh
python3 scripts/build_catalog.py
python3 scripts/test_catalog.py
```

The builder sorts Start, Latest and every collection using `finds.json`; adds visible addition dates; gives RSS entries their discovery timestamps while preserving original publication details and existing GUIDs; and generates `catalog.html`, `finds/*.html`, `sitemap.xml`, and `robots.txt`.

Commit all changed generated files along with source metadata. Do not stage unrelated files from `scripts/` or runtime caches. Serve locally and test navigation, original/archive links, and layouts at narrow mobile, tablet and desktop widths. Existing source dates can be approximate: do not invent more precision than the original artifact supports.

After pushing, verify GitHub Pages is built, fetch the public homepage and feed, and verify the new catalog/find pages and sitemap are live. A push alone is not proof of deployment. Google/Bing choose when to crawl and index; never claim they indexed the site merely because a sitemap was published.

## Historical card

The homepage’s W3C milestone is labeled “From web history” and dated October 1, 1994. It is evergreen history, not a current-week promise. If restoring a weekly card, provide a genuinely current week-aligned event and verify its primary source.
