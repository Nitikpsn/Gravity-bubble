import math
import random

import pygame

from settings import (
    BURST_PARTICLES,
    BURST_SPEED_MIN,
    BURST_SPEED_MAX,
    BURST_LIFETIME,
    BURST_GRAVITY,
    BURST_DRAG,
    RING_LIFETIME,
    RING_GROWTH,
)


def _fade(color, amount):
    return tuple(int(channel * amount) for channel in color)


class Particle:
    def __init__(self, x, y, radius, color, angle, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(BURST_LIFETIME * 0.6, BURST_LIFETIME)
        self.max_life = self.life

    def update(self, dt):
        drag = BURST_DRAG ** dt
        self.vx *= drag
        self.vy = self.vy * drag + BURST_GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.life -= dt

    def draw(self, screen):
        if self.life <= 0:
            return
        amount = self.life / self.max_life
        radius = max(1, int(self.radius * amount))
        pygame.draw.circle(
            screen,
            _fade(self.color, amount),
            (int(self.x), int(self.y)),
            radius,
        )


class Burst:
    """A short shatter animation left behind by a popped bubble."""

    def __init__(self, bubble):
        self.x = bubble.x
        self.y = bubble.y
        self.color = bubble.color
        self.start_radius = bubble.radius
        self.ring_life = RING_LIFETIME
        self.particles = []

        for _ in range(BURST_PARTICLES):
            angle = random.uniform(0, 2 * math.pi)
            distance = bubble.radius * random.uniform(0.2, 0.9)
            self.particles.append(
                Particle(
                    self.x + math.cos(angle) * distance,
                    self.y + math.sin(angle) * distance,
                    random.randint(2, max(2, int(bubble.radius * 0.2))),
                    bubble.color,
                    angle,
                    random.uniform(BURST_SPEED_MIN, BURST_SPEED_MAX),
                )
            )

    def update(self, dt):
        self.ring_life -= dt
        for particle in self.particles:
            particle.update(dt)

    def draw(self, screen):
        if self.ring_life > 0:
            amount = self.ring_life / RING_LIFETIME
            radius = int(
                self.start_radius * (1 + (1 - amount) * (RING_GROWTH - 1))
            )
            pygame.draw.circle(
                screen,
                _fade(self.color, amount),
                (int(self.x), int(self.y)),
                max(1, radius),
                2,
            )

        for particle in self.particles:
            particle.draw(screen)

    def done(self):
        return self.ring_life <= 0 and all(p.life <= 0 for p in self.particles)


def update_bursts(bursts, dt):
    for burst in bursts:
        burst.update(dt)
    bursts[:] = [burst for burst in bursts if not burst.done()]


def draw_bursts(screen, bursts):
    for burst in bursts:
        burst.draw(screen)
