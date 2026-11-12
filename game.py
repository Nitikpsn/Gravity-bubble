import asyncio
import random
import pygame

pygame.init()

W = 600
H = 500
screen = pygame.display.set_mode((W, H))
pygame.display.set_caption("Gravity Bubble")
font = pygame.font.Font(None, 40)

bubbles = []   # all the bubbles that are alive rn
score = 0      # self explanatory lol
timer = 0      # counts frames until the next bubble spawns


def new_bubble():
    # random size and random spot at the top of the screen
    r = random.randint(20, 45)
    bubbles.append({
        "x": random.randint(r, W - r),
        "y": -r,
        "r": r,
        "speed": random.randint(2, 5),
        # start rgb at 60 so colors never get too dark to see
        "color": (random.randint(60, 255), random.randint(60, 255), random.randint(60, 255)),
    })


async def main():
    global score, timer
    running = True

    while running:
        # check what the player is doing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                for b in bubbles[:]:
                    dx = b["x"] - mx
                    dy = b["y"] - my
                    # circle hit test, no square roots needed
                    if dx * dx + dy * dy <= b["r"] ** 2:
                        bubbles.remove(b)
                        score += 1
                        break

        # spawn a bubble every 30 frames (twice a second at 60fps)
        timer += 1
        if timer >= 30:
            new_bubble()
            timer = 0

        screen.fill((26, 32, 64))  # night sky vibes

        # move and draw every bubble
        for b in bubbles[:]:
            b["y"] += b["speed"]
            x, y = int(b["x"]), int(b["y"])
            pygame.draw.circle(screen, b["color"], (x, y), b["r"])
            pygame.draw.circle(screen, (255, 255, 255), (x, y), b["r"], 2)  # white outline

            # if it fell off the bottom just delete it
            if b["y"] - b["r"] > H:
                bubbles.remove(b)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        pygame.display.flip()

        await asyncio.sleep(1 / 60)  # roughly 60 fps


asyncio.create_task(main())

