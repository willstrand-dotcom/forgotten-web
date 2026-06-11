# Brief: 1990s 8-bit Nintendo-style synth for The Forgotten Web Games

Path: `/Users/niklas/Documents/Codex/forgotten-web-public`

## Goal
Add a playable 2-octave synth under the existing `Games` section on The Forgotten Web.

## Working title
`8-Bit Web Synth`

## Concept
A small browser synth that looks like a 1990s shareware / early web music toy. The user can press on-screen keys or use the computer keyboard to play short Nintendo 8-bit style tones.

It should feel like something found on an old Geocities page, but polished enough not to break the site.

## Placement
Add it under `Games` alongside Pong:

- Games section button: `Press to play 8-Bit Web Synth`
- Games list item: `8-Bit Web Synth`
- It should open inside the existing Forgotten Web OS window, not as a separate page.

## Visual style
1990s old-web / retro toy:

- hot-pink / cyan / yellow palette matching The Forgotten Web
- chunky pixel borders
- fake LCD display
- small blinking status text
- cheesy labels like `MIDI NOT FOUND`, `CARTRIDGE AUDIO`, `FWOS SOUND DRIVER`
- piano keys should look plastic, slightly toy-like, and clickable
- layout must work on desktop and mobile

## Sound style
Use Web Audio API only. No external audio files.

Nintendo 8-bit inspired, not copyrighted samples:

- square wave as default
- optional pulse / triangle / noise selector if simple
- short attack, clean decay
- mild vibrato optional
- no heavy effects
- should sound like NES-ish bleeps, not modern synth pads

## Musical range
2 octaves total.

Suggested range:

- C4 to B5, including sharps/flats
- 24 keys total
- white and black keys visually separated

## Controls
Desktop keyboard:

Lower octave:
- `A W S E D F T G Y H U J`

Upper octave:
- `K O L P ; ' ]` etc. if comfortable, or a clearer mapped row shown on screen.

Important: show the active keyboard mapping visibly inside the game.

Mouse/touch:
- clicking/tapping a key plays its note
- holding should sustain briefly if easy
- releasing stops the note

## Features for v1
Must have:

- 2-octave on-screen keyboard
- keyboard input support
- visible active key highlight
- volume control or mute button
- waveform selector: `Square`, `Triangle`, `Noise` if stable; otherwise just `Square`
- restart/reset not necessary, but a `Panic / Stop Sound` button is useful

Nice to have:

- tiny demo riff button
- fake cartridge display showing current note
- octave labels
- simple arpeggio mode if very stable

## Non-goals
Do not:

- use copyrighted Nintendo audio samples
- call it an official Nintendo/NES product
- add dependencies
- add a build step
- break Pong
- overbuild a DAW
- use autoplay audio before user interaction

## Technical requirements
- Single-file static implementation in `index.html` unless a tiny separate JS file is clearly cleaner.
- No npm.
- No external assets.
- Must respect browser audio restrictions: audio starts only after click/key interaction.
- Must avoid stuck notes. Add a `panic()` / stop-all function.
- Must clean up listeners when switching away from the game window, following the existing game-session pattern if present.

## Acceptance criteria
- Games shows Pong plus `8-Bit Web Synth`.
- Clicking `Press to play 8-Bit Web Synth` opens the synth.
- Pressing visible keys plays audio.
- Pressing mapped keyboard keys plays audio.
- Active keys visually highlight.
- `Panic / Stop Sound` silences everything.
- Pong still opens and plays.
- No console errors in Start, Games, Pong, or Synth.
- No layout overflow at 375px mobile width.
- Works without network after page load.

## Tone
This should be a toy, not a product.

The ideal feeling: someone finds a weird little 1990s web page, presses `A`, and the browser chirps like a lost cartridge waking up.