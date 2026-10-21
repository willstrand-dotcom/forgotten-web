# Site inventory and repair — 2026-10-21

## Inventory

- 22 unique finds; every find has a detail route, one collection membership and a Random Relic entry.
- Collections: Web Architecture 4; Pre-Platform Culture 11; Old Programming Blogs 3; Markets That Aged Well 2; Weird Useful Corners 2.
- All discovery timestamps were recovered from the first Git commit introducing the relic. The launch batch shares a timestamp; no finer arrival order is claimed for that batch.
- `finds.json` is the complete machine-readable inventory, with original publication metadata kept separate from archive-addition dates.

## Fixed

- Reconstructed newest-added order everywhere: Start’s newest five, Latest, each collection, random-key inventory and RSS. In particular, Vernacular Web, Barrett and the launch-batch items were not consistently ordered by actual addition date.
- Displayed explicit `Added YYYY-MM-DD` labels. Detail pages distinguish archive-addition date from historical publication date.
- RSS `pubDate` now represents publication to this curated feed. Historical source dates remain in the descriptions, and existing GUIDs remain unchanged to avoid duplicate subscriptions.
- **Anatomy of a Weblog:** the old CamWorld path omitted a slash (`99/0126.html`). Its supposed 1999 snapshot redirected into a 2024 capture and then an unrelated adult site. Recovered the correct original path (`99/01/26.html`) and a genuine 1999 capture using Wayback’s CDX index. Verified both normal replay and raw `id_` replay contain the actual essay. Corrected the detail page, archive-index link, feed and catalog.
- **Shirky and Rebecca Blood:** restored verified live original author pages as the primary buttons; retained archived alternatives. Their usable original pages are HTTP; the tested HTTPS variants had certificate/connectivity failures, so no broken forced-HTTPS upgrade was introduced.
- Corrected the submission email to Winston’s actual address, `winstonkilby@gmail.com`.
- Replaced the stale “This week” claim with an accurately dated evergreen “From web history” card.
- Removed an unsupported public-domain assertion about Russell’s essay.
- Fixed direct opening of `/#random`.

## Discoverability

- Added `catalog.html`, a full newest-added archive index, with real HTML links.
- Added one static, canonical HTML page per find under `finds/`. Context and source links can now be read without JavaScript; the existing retro OS remains the main interface.
- Added a 24-URL `sitemap.xml`, `robots.txt`, and structured data for the catalog and individual finds.
- Added a visible catalog link and a no-JavaScript fallback.
- Search engines decide when to crawl/index. These changes make the content crawlable; they are not evidence that Google/Bing has indexed it.

## Verification

- Automated checks passed for all 22 finds, 5 collections, 24 HTML pages, RSS order/dates/GUIDs, sitemap targets, internal links and all three JavaScript blocks.
- A temporary-only future-addition regression proves a new metadata/registry entry appears automatically in Start, Latest, its category, Random, RSS, catalog and sitemap. Rebuilding is byte-identical when content is unchanged.
- Browser navigation checked for every find; category picker, Random, Back, Oracle and Pong navigation also exercised.
- Tested 390, 768, 1024 and 1440 px browser viewports across Start, Latest, detail/collection pages, Games, Pong and Keyboard: no measured horizontal overflow or logo/window collision.
- Requested all 43 external source/archive buttons. Primary sources responded during the audit; Wayback subsequently refused some repeated requests. Those transient archive/network failures are not classified as permanently dead URLs. The CamWorld content mismatch was independently reproduced and repaired, not inferred from HTTP status alone.

## Maintenance

Run `python3 scripts/build_catalog.py` and `python3 scripts/test_catalog.py` for future changes. Repository `AGENTS.md` documents the discovery ledger and generated surfaces. Unrelated pre-existing scripts and runtime caches are not part of this repair.
