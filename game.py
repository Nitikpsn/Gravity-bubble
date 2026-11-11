import asyncio
import random
import pygame

pygame.init()

WIDTH = 600
HEIGHT = 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Bubble")
font = pygame.font.Font(None, 40)

COLORS = [
    (255, 99, 132),
    (255, 205, 86),
    (75, 192, 192),
    (54, 162, 235),
    (153, 102, 255),
    (255, 159, 64),
    (0, 255, 128),
    (255, 0, 200)
]

bubbles = []
score = 0
timer = 0

def add_bubble():
    radius = random.randint(20, 45)
    bubble = {
        "x": random.randint(radius, WIDTH - radius),
        "y": -radius,
        "radius": radius,
        "speed": random.randint(2, 5),
        "color": random.choice(COLORS)
    }
    bubbles.append(bubble)

async def main():
    global score, timer
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for bubble in bubbles[:]:
                    dx = bubble["x"] - mouse_x
                    dy = bubble["y"] - mouse_y
                    if dx * dx + dy * dy <= bubble["radius"] ** 2:
                        bubbles.remove(bubble)
                        score += 1
                        break

        timer += 1
        if timer >= 30:
            add_bubble()
            timer = 0

        screen.fill((26, 32, 64))

        for bubble in bubbles[:]:
            bubble["y"] += bubble["speed"]
            x = int(bubble["x"])
            y = int(bubble["y"])
            pygame.draw.circle(screen, bubble["color"], (x, y), bubble["radius"])
            pygame.draw.circle(screen, (255, 255, 255), (x, y), bubble["radius"], 2)
            if bubble["y"] - bubble["radius"] > HEIGHT:
                bubbles.remove(bubble)

        score_text = font.render("Score: " + str(score), True, (255, 255, 255))
        screen.blit(score_text, (20, 20))
        pygame.display.flip()
        await asyncio.sleep(1 / 60)

asyncio.create_task(main())
