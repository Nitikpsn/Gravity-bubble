import asyncio
import time

import pygame

from bubble import Bubble
from effects import Burst, draw_bursts, update_bursts
from physics import update_bubbles
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    SPAWN_FRAMES,
    POINTS_PER_CLICK,
    MAX_FRAME_STEP,
    BACKGROUND,
    TEXT_COLOR,
    SCORE_POS,
    FONT_PATH,
    FONT_SIZE,
)
from sound import play_pop

pygame.display.init()
pygame.font.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Bubble")

font = pygame.font.Font(FONT_PATH, FONT_SIZE)

bubbles = []
bursts = []
score = 0
timer = 0


def hide_loading():
    try:
        from pyscript import document
        loading = document.getElementById("loading")
        if loading:
            loading.remove()
    except Exception:
        pass


async def main():
    global score, timer
    running = True
    first = True
    last = time.perf_counter()

    while running:
        start = time.perf_counter()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for b in bubbles[:]:
                    if b.clicked(*event.pos):
                        bubbles.remove(b)
                        bursts.append(Burst(b))
                        play_pop()
                        score += POINTS_PER_CLICK
                        break

        now = time.perf_counter()
        dt = min(max((now - last) * FPS, 0), MAX_FRAME_STEP)
        last = now

        timer += dt
        if timer >= SPAWN_FRAMES:
            bubbles.append(Bubble())
            timer -= SPAWN_FRAMES

        update_bubbles(bubbles, dt)
        bubbles[:] = [b for b in bubbles if not b.offscreen()]
        update_bursts(bursts, dt)

        screen.fill(BACKGROUND)
        for b in bubbles:
            b.draw(screen)
        draw_bursts(screen, bursts)
        screen.blit(font.render(f"Score: {score}", True, TEXT_COLOR), SCORE_POS)
        pygame.display.flip()

        if first:
            hide_loading()
            first = False

        await asyncio.sleep(max(0, 1 / FPS - (time.perf_counter() - start)))


try:
    asyncio.get_running_loop()
    asyncio.create_task(main())
except RuntimeError:
    asyncio.run(main())
