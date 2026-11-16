import math

from settings import WIDTH, GRAVITY, WALL_BOUNCE, COLLISION_BOUNCE


def update_bubbles(bubbles, dt=1.0):
    """Advance the simulation by dt frames (1.0 == one 60 FPS frame)."""
    steps = max(1, math.ceil(dt))
    step = dt / steps

    for _ in range(steps):
        for b in bubbles:
            b.vy += GRAVITY * step
            b.x += b.vx * step
            b.y += b.vy * step
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

    a_speed = a.vx * nx + a.vy * ny
    b_speed = b.vx * nx + b.vy * ny
    if b_speed - a_speed >= 0:
        return

    kick = (b_speed - a_speed) * COLLISION_BOUNCE
    a.vx += kick * nx
    a.vy += kick * ny
    b.vx -= kick * nx
    b.vy -= kick * ny
