import asyncio
import time

import pygame

from bubble import Bubble
from physics import update_bubbles
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    SPAWN_FRAMES,
    MAX_FRAME_STEP,
    BACKGROUND,
    TEXT_COLOR,
    SCORE_POS,
    FONT_PATH,
    FONT_SIZE,
)

# Only initialise what this game uses. Full pygame.init() also starts the
# mixer, which adds startup time in the browser and is not needed here.
pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Bubble")

try:
    font = pygame.font.Font(FONT_PATH, FONT_SIZE)
except (OSError, pygame.error):
    # Desktop runs may not have the webfont; the game still works without it.
    font = pygame.font.Font(None, FONT_SIZE)

bubbles = []
score = 0
timer = 0


def hide_loading_message():
    """Remove the HTML loading overlay once the first frame is drawn."""
    try:
        from pyscript import document
    except ImportError:
        return
    loading = document.getElementById("loading")
    if loading is not None:
        loading.remove()


async def main():
    global score, timer
    running = True
    first_frame = True
    last_time = time.perf_counter()

    while running:
        frame_start = time.perf_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for b in bubbles[:]:
                    if b.clicked(mx, my):
                        bubbles.remove(b)
                        score += 1
                        break

        now = time.perf_counter()
        dt = min(max((now - last_time) * FPS, 0.0), MAX_FRAME_STEP)
        last_time = now

        timer += dt
        if timer >= SPAWN_FRAMES:
            bubbles.append(Bubble())
            timer = 0

        update_bubbles(bubbles, dt)
        bubbles[:] = [b for b in bubbles if not b.offscreen()]

        screen.fill(BACKGROUND)
        for b in bubbles:
            b.draw(screen)

        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, SCORE_POS)
        pygame.display.flip()

        if first_frame:
            hide_loading_message()
            first_frame = False

     
        elapsed = time.perf_counter() - frame_start
        await asyncio.sleep(max(0.0, 1 / FPS - elapsed))


try:
   
    asyncio.get_running_loop()
    asyncio.create_task(main())
except RuntimeError:

    asyncio.run(main())
