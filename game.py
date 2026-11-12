import asyncio
import random
import pygame

pygame.init()

W = 600
H = 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Gravity Bubble")
font = pygame.font.Font(None, 40)

bubbles = []
score = 0
timer = 0


def new_bubble():
    r = random.randint(20, 45)
    bubbles.append({
        "x": random.randint(r, W - r),
        "y": -r,
        "r": r,
        "speed": random.randint(2, 5),
        "color": (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255)),
    })


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
                    dx = b["x"] - mx
                    dy = b["y"] - my
                    if dx * dx + dy * dy <= b["r"] ** 2:
                        bubbles.remove(b)
                        score += 1
                        break

        timer += 1
        if timer >= 30:
            new_bubble()
            timer = 0

        screen.fill((26, 32, 64))

        for b in bubbles[:]:
            b["y"] += b["speed"]
            x, y = int(b["x"]), int(b["y"])
            pygame.draw.circle(screen, b["color"], (x, y), b["r"])
            pygame.draw.circle(screen, (255, 255, 255), (x, y), b["r"], 2)

            if b["y"] - b["r"] > H:
                bubbles.remove(b)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        pygame.display.flip()

        await asyncio.sleep(1 / 60)


asyncio.create_task(main())
