import asyncio

import pygame

from bubble import Bubble
from physics import update_bubbles
from settings import (
    WIDTH,
    HEIGHT,
    FPS,
    SPAWN_FRAMES,
    BACKGROUND,
    TEXT_COLOR,
    SCORE_POS,
)

pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Bubble")
font = pygame.font.Font(None, 40)

bubbles = []
score = 0
timer = 0


async def main():
    global score, timer
    running = True

    while running:
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

        timer += 1
        if timer >= SPAWN_FRAMES:
            bubbles.append(Bubble())
            timer = 0

        update_bubbles(bubbles)
        bubbles[:] = [b for b in bubbles if not b.offscreen()]

        screen.fill(BACKGROUND)
        for b in bubbles:
            b.draw(screen)

        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        screen.blit(score_text, SCORE_POS)
        pygame.display.flip()

        await asyncio.sleep(1 / FPS)


asyncio.create_task(main())
