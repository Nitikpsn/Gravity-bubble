# Gravity Bubble

A small web game made with Python, PyScript and Pygame. The Python game code is in `game.py`.

Bubbles fall from the sky in many colors. Click a bubble to burst it. 1 burst = 1 point.

## Play in the browser

The game loads its Python modules through PyScript, so it must be served over HTTP
(opening `index.html` directly from disk will not work).

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/> in your browser.

The first load downloads Python and Pygame-CE (a few MB), so it can take a while
before the bubbles show up. After that the browser caches everything and it
loads fast.

Files:

- `index.html` – page and `<script type="py-game">` entry point
- `game.py` – game loop, input and score
- `bubble.py` – bubble object (movement, drawing, hit testing)
- `physics.py` – gravity, wall bounce and bubble collisions
- `settings.py` – tunable constants
- `pyscript.json` – tells PyScript to copy the Python modules into its virtual filesystem

## Play on the desktop

If you have `pygame` installed, you can also run the game locally:

```bash
python3 game.py
```
