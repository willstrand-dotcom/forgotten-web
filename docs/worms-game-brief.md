# Brief: Worms-style artillery game for The Forgotten Web

Path: `/Users/niklas/Documents/Codex/forgotten-web-public`

## Goal
Replace the failed Flappy experiment with a small, stable Worms-inspired artillery game inside the existing Forgotten Web Games section.

## Working title
`Worms: Link Rot Artillery`

## Fit
The game should feel like a corrupted old web-desktop toy:
- tiny pixel worms crawling on a broken website landscape
- weapons named after old-web decay: `404 Mortar`, `Banner Bomb`, `Popup Mine`, `Broken Link Bazooka`
- terrain made of browser windows, folders, underlined blue links, banner ads, and archive fragments
- hot-pink retro OS tone, matching the existing site

## Scope
Implement a simple local browser game in `index.html`:
- 2 teams, 2 worms each
- turn-based aiming and shooting
- destructible or pseudo-destructible terrain
- wind indicator
- health bars
- one projectile type is enough for v1
- playable with keyboard and touch/click controls
- restart button
- no external assets
- no build step

## Controls
Desktop:
- Left/right: move current worm a little
- Up/down: aim
- Hold space: charge power
- Release space: fire

Mobile:
- visible buttons for move, aim, power/fire
- no layout overflow at 375px width

## Non-goals
- Do not clone Worms wholesale.
- Do not use copyrighted art, names, sounds, or exact weapon set.
- Do not add dependencies.
- Do not break Pong.
- Do not change the Forgotten Web visual metaphor.

## Acceptance criteria
- Games section shows Pong plus Worms.
- `Press to play Worms: Link Rot Artillery` opens the game.
- Pong still opens and plays.
- No console errors when opening Games, Pong, or Worms.
- Works at desktop and 375px mobile width.
- If destructible terrain becomes fragile, fake it visually rather than shipping a freezing canvas.

## Implementation note
Keep the game loop conservative. Stability beats clever physics. Flappy died because the toy got twitchy; Worms should be slow, turn-based, and boringly reliable — artillery, not caffeine.
