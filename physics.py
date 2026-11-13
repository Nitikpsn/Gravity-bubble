import math

from settings import WIDTH, GRAVITY, WALL_BOUNCE, COLLISION_BOUNCE


def update_bubbles(bubbles):
    for b in bubbles:
        b.vy += GRAVITY
        b.x += b.vx
        b.y += b.vy
        bounce_walls(b)

    for i in range(len(bubbles)):
        for j in range(i + 1, len(bubbles)):
            collide(bubbles[i], bubbles[j])


def bounce_walls(b):
    if b.x - b.radius < 0:
        b.x = b.radius
        b.vx = abs(b.vx) * WALL_BOUNCE
    elif b.x + b.radius > WIDTH:
        b.x = WIDTH - b.radius
        b.vx = -abs(b.vx) * WALL_BOUNCE


def collide(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    dist = math.hypot(dx, dy)
    min_dist = a.radius + b.radius

    if dist == 0 or dist >= min_dist:
        return

    nx = dx / dist
    ny = dy / dist
    overlap = (min_dist - dist) / 2

    a.x -= nx * overlap
    a.y -= ny * overlap
    b.x += nx * overlap
    b.y += ny * overlap

    avn = a.vx * nx + a.vy * ny
    bvn = b.vx * nx + b.vy * ny

    if bvn - avn >= 0:
        return

    impulse = (bvn - avn) * COLLISION_BOUNCE
    a.vx += impulse * nx
    a.vy += impulse * ny
    b.vx -= impulse * nx
    b.vy -= impulse * ny
