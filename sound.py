"""Procedurally generated sound effects (no audio files required)."""

import array
import math
import random
import sys

import pygame

from settings import POP_DURATION, POP_SAMPLE_RATE, POP_VOLUME

_pops = []
_ready = False


def _build_pop(base_frequency):
    count = int(POP_SAMPLE_RATE * POP_DURATION)
    phase = 0.0
    samples = array.array("h")

    for i in range(count):
        t = i / POP_SAMPLE_RATE
        envelope = math.exp(-t * 42)
        frequency = 140 + base_frequency * math.exp(-t * 22)
        phase += 2 * math.pi * frequency / POP_SAMPLE_RATE

        value = math.sin(phase) * envelope * 0.8
        if t < 0.006:  # a tiny "click" right at the start
            value += random.uniform(-1, 1) * (1 - t / 0.006) * 0.35
        value = max(-1.0, min(1.0, value))
        samples.append(int(value * 32767))

    if sys.byteorder == "big":
        samples.byteswap()
    return samples.tobytes()


def init():
    """Set up the mixer and pop samples. Safe to call more than once."""
    global _ready
    if _ready:
        return
    _ready = True

    try:
        if not pygame.mixer.get_init():
            pygame.mixer.init(
                frequency=POP_SAMPLE_RATE, size=-16, channels=1, buffer=512
            )
        for frequency in (760, 880, 1000):
            pop = pygame.mixer.Sound(buffer=_build_pop(frequency))
            pop.set_volume(POP_VOLUME)
            _pops.append(pop)
    except Exception:
        # No audio device (or audio unavailable in this browser session):
        # the game stays fully playable without sound.
        _pops.clear()


def play_pop():
    """Play a bubble-pop sound. Called from a click, i.e. a user gesture."""
    init()
    if _pops:
        try:
            random.choice(_pops).play()
        except Exception:
            pass
