import math

from settings import WIDTH, GRAVITY, WALL_BOUNCE, COLLISION_BOUNCE


def update_bubbles(bubbles, dt=1.0):
    for b in bubbles:
        b.vy += GRAVITY * dt
        b.x += b.vx * dt
        b.y += b.vy * dt

        if b.x - b.radius < 0:
            b.x = b.radius
            b.vx = abs(b.vx) * WALL_BOUNCE
        elif b.x + b.radius > WIDTH:
            b.x = WIDTH - b.radius
            b.vx = -abs(b.vx) * WALL_BOUNCE

    for i in range(len(bubbles)):
        for j in range(i + 1, len(bubbles)):
            collide(bubbles[i], bubbles[j])


def collide(a, b):
    dx = b.x - a.x
    dy = b.y - a.y
    reach = a.radius + b.radius

    if abs(dx) > reach or abs(dy) > reach:
        return

    dist = math.sqrt(dx * dx + dy * dy)
    if dist == 0 or dist >= reach:
        return

    nx = dx / dist
    ny = dy / dist
    push = (reach - dist) / 2

    a.x -= nx * push
    a.y -= ny * push
    b.x += nx * push
    b.y += ny * push

    av = a.vx * nx + a.vy * ny
    bv = b.vx * nx + b.vy * ny
    if bv - av >= 0:
        return

    kick = (bv - av) * COLLISION_BOUNCE
    a.vx += kick * nx
    a.vy += kick * ny
    b.vx -= kick * nx
    b.vy -= kick * ny
