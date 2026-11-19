# Gravity Bubble

A small web game made with Python, PyScript and Pygame. The Python game code is in `game.py`.

Bubbles fall from the sky in many colors. Click a bubble to burst it into a shower of
shards with a pop sound. Each burst awards `POINTS_PER_CLICK` points (set in
`settings.py`, default 1). The pop sound is synthesised in code, so there are no audio
files to download.

## Play in the browser

The game loads its Python modules through PyScript, so it must be served over HTTP
(opening `index.html` directly from disk will not work).

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in your browser.

The first load downloads Python and Pygame-CE (a few MB), so it can take a while
before the bubbles show up. A simple loading spinner is shown while it starts,
and a service worker (`sw.js`) caches the PyScript/Pyodide files so later visits
start much faster. Service workers need `http://localhost` or HTTPS; on a plain
HTTP address the game still works, it just does not get the extra cache.

Files:

- `index.html` – page and `<script type="py-game">` entry point
- `game.py` – game loop, input and score
- `bubble.py` – bubble object (movement, drawing, hit testing)
- `physics.py` – gravity, wall bounce and bubble collisions
- `effects.py` – particle burst animation when a bubble pops
- `sound.py` – synthesised pop sound effect
- `settings.py` – tunable constants
- `pyscript.json` – tells PyScript to copy the Python modules into its virtual filesystem
- `sw.js` – service worker that caches the Python/Pygame runtime between visits

The UI and in-game score use the [Grape Squishy](https://www.dafont.com/grape-squishy.font)
font by Khurasan. It is loaded from CDNFonts and is free for personal use only.

## Play on the desktop

If you have `pygame` installed, you can also run the game locally:

```bash
python3 game.py
```
