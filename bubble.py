import random

import pygame

from settings import (
    WIDTH,
    HEIGHT,
    MIN_RADIUS,
    MAX_RADIUS,
    MIN_SPEED,
    MAX_SPEED,
    MAX_DRIFT,
    MIN_COLOR,
    MAX_COLOR,
    OUTLINE_COLOR,
    OUTLINE_WIDTH,
)


class Bubble:
    def __init__(self):
        self.radius = random.randint(MIN_RADIUS, MAX_RADIUS)
        self.x = float(random.randint(self.radius, WIDTH - self.radius))
        self.y = float(-self.radius)
        self.vx = random.uniform(-MAX_DRIFT, MAX_DRIFT)
        self.vy = float(random.randint(MIN_SPEED, MAX_SPEED))
        self.color = (
            random.randint(MIN_COLOR, MAX_COLOR),
            random.randint(MIN_COLOR, MAX_COLOR),
            random.randint(MIN_COLOR, MAX_COLOR),
        )
                  
    def draw(self, screen):
        pos = (int(self.x), int(self.y))
        pygame.draw.circle(screen, self.color, pos, self.radius)
        pygame.draw.circle(screen, OUTLINE_COLOR, pos, self.radius, OUTLINE_WIDTH)

    def clicked(self, mx, my):
        dx = self.x - mx
        dy = self.y - my
        return dx * dx + dy * dy <= self.radius ** 2

    def offscreen(self):
        return self.y - self.radius > HEIGHT
