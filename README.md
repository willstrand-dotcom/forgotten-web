# Sketch 006 — Poolsuite OS Homepage

## Design stance

A retro web desktop / fake operating system for The Forgotten Web, inspired by Poolsuite’s interface confidence but translated into a haunted human-web archive.

## Key choices

- Layout: desktop launcher icons and one default main window, with mobile collapsing into stacked cards/windows.
- Typography: system UI for chrome, Georgia for human/editorial text, Monaco-style monospace for metadata/status.
- Color: hot-pink/magenta background with 90s pastel blocks: banana menu bar, lavender buttons, aqua/mint/lavender year tags, blush archive badges, mint online badges, apricot notes/status bars.
- Interaction: first-visit boot sequence, icon launcher, random relic loading state, window content switching, browser-history support, and auto-scroll back to the active window on mobile.

## Included content

- Web Architecture: Tim Berners-Lee — Cool URIs don’t change; John Allsopp — A Dao of Web Design
- Pre-Platform Culture: Rebecca Blood — Weblogs: A History and Perspective; Clay Shirky — A Group Is Its Own Worst Enemy
- Old Programming Blogs: Joel Spolsky — The Law of Leaky Abstractions; Richard P. Gabriel — The Rise of Worse is Better
- Markets That Aged Well: Calculated Risk — Housing: Speculation is the Key; Warren Buffett — Mr. Buffett on the Stock Market
- Weird Useful Corners: Jo Freeman — The Tyranny of Structurelessness; Bertrand Russell — In Praise of Idleness

## Button behavior

- **Start Here**: Opens the default intro window. Explains the product plainly, shows the launch finds, and gives quick actions into Latest Finds, Random Relic, Submit, and Source Notes.
- **Latest Finds**: Opens a list of the current ten world-class finds, two per archive category. Each row shows sequence number, title, why it matters, and source status.
- **Archive**: Opens five clickable collection folders: Web Architecture, Pre-Platform Culture, Old Programming Blogs, Markets That Aged Well, and Weird Useful Corners. Each folder opens a filtered collection view with exactly two top-tier finds.
- **Random Relic**: Shows a short “loading random find…” state, then picks one of the ten real finds at random and opens it as a file in the main window. Keep this lightweight until the archive has 50+ relics.
- **Source Notes**: Opens rights/ethics policy plus “About the machine.” Core rule: link and contextualize, do not republish wholesale.
- **RSS + Submit**: Opens a real submit flow first: `Email Winston` uses a prefilled `mailto:` for URL/archive link, why it matters now, and original author if known. The panel also includes a real local `feed.xml` link that opens separately.
- **Menu bar**: File, Finds, Collections, and Utilities are real controls mapped to Start, Latest Finds, Archive, and RSS + Submit. The RSS label opens `feed.xml` separately.

## Content/view improvements

- Start Here now states the product promise in one sentence: old web artifacts, human-selected, summarized fast, linked to original/archive.
- The intro promise card has extra top/bottom/internal spacing so it does not feel wedged into the window on mobile, and the old Recovery Brief side card has been removed.
- Quick-action buttons use plain labels and stronger clickable 90s colors: aqua, banana, mint, coral, lime, hot pink, and candy cyan, with thick borders and chunky shadows.
- The top menu and launcher icons now show an active state, so the current section is visible instead of implied.
- The weird-useful folder now explicitly frames pre-web essays as “older than the web — but too sharp to leave outside the machine.”
- Prototype leftovers from the earlier player/note/preview/drawer layout were removed from CSS and JS.
- Launcher/content buttons scroll the active window into view after switching, so Latest Finds does not update invisibly below the current mobile scroll position.
- Internal navigation now writes browser history/hash state, so Back returns to the previous section instead of replaying Start Here. The boot screen is skipped after the first visit in the same browser session.
- External original/archive links are marked to open in a new tab/window with `target="_blank"` and `rel="noopener noreferrer"`, so opening an original URL should not destroy the current in-page archive state. The `feed.xml` button now points to a real local feed file instead of `#`, so it no longer jumps back to Start Here.
- The old technical `/system/start-here...` line has been replaced with plainer product copy.
- Archive folders are now real buttons, not dead decorative cards.
- Archive has been reduced from six folders to five by removing Lost Personal Sites as a separate category.
- Each relic view now includes metadata cells: what it is, why now, status, and collection.
- Relic pages include a short “Why it still matters” note, a best-opened-as quote, and original/archive buttons.
- Launcher icons are intentionally distinct: monitor, document stack, archive folder, random device, clipboard, and RSS signal.

## Visual fix

The first version used a radio-style icon for Random Relic with two circular knobs. That read as two stray circles in front of the label, so the icon was changed to a simple mystery-device tile with a `?` mark.

## Trade-offs

- Strong at: making the homepage feel like a place/machine rather than a publication.
- Weak at: desktop metaphor will need careful mobile and accessibility handling in production.

## Best next iteration

Make the OS stronger with richer pixel icons, a more distinctive wallpaper, and a more tactile open-file article view — without hiding primary navigation.
