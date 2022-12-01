import random

from pygame.image import load
from pygame.math import Vector2
from pygame.mixer import Sound

def lataa_kuvat(nimi: str, with_alpha = True):
    path = f"kuvat/{nimi}.png"
    ladattu_kuva = load(path)
    if with_alpha:
        return ladattu_kuva.convert_alpha()
    else:
        return ladattu_kuva.convert()

def lataa_musat(nimi: str):
    path = f"musat/{nimi}.mp3"
    return Sound(path)

def rajaa_kartta(sijainti, tausta):
    x, y = sijainti
    w, h = tausta.get_size()
    return Vector2(x % w, y % h)

def satunnainen_koord(taustakuva):
    return Vector2(
        random.randrange(taustakuva.get_width()),
        random.randrange(taustakuva.get_height())
    )