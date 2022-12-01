from pygame.math import Vector2
from ominaisuudet import lataa_kuvat, rajaa_kartta, lataa_musat
from pygame.transform import rotozoom
import random
import pygame.mixer

OIKEA = Vector2(1, 0)
class PeliObjekti:
    def __init__(self, sijainti, kuva, nopeus):
        self.sijainti = Vector2(sijainti)
        self.kuva = kuva
        self.sade = kuva.get_width() / 2
        self.nopeus = Vector2(nopeus)
    
    def piirra(self, tausta):
        blit_sijainti = self.sijainti - Vector2(self.sade)
        tausta.blit(self.kuva, blit_sijainti)
    
    def liiku(self, taustakuva):
        self.sijainti = rajaa_kartta(self.sijainti + self.nopeus, taustakuva)

    def tormays(self, obj2):
        etaisyys = self.sijainti.distance_to(obj2.sijainti)
        return etaisyys < self.sade + obj2.sade

class Kissa(PeliObjekti):
    liikkuvuus = 1
    kiihtyvyys = 1
    def __init__(self, sijainti):
        self.suunta = Vector2(OIKEA)
        super().__init__(sijainti, lataa_kuvat("nyan20px", True), Vector2(0))
        self.kuva2 = lataa_kuvat("nyan_rainbow18px", True)
        self.supervoima = False
        self.supervoima_valmiina = True
        self.taustamusa = lataa_musat("let-the-games-begin-21858")

    def aktivoi_supervoima(self, bool):
        if self.supervoima_valmiina:
            self.supervoima = bool
            self.supervoima_valmiina = False
        if bool == False:
            self.supervoima = False

    def kaanna(self, clockwise=True):
        negpos = 1 if clockwise else -1
        kulma = self.liikkuvuus * negpos
        self.suunta.rotate_ip(kulma)

    def suuntaa_kiihdyta(self):
        self.nopeus += self.suunta * self.kiihtyvyys

    def piirra(self, tausta):
        kulma = self.suunta.angle_to(OIKEA)
        if self.supervoima:
            kaannetty_tausta = rotozoom(self.kuva2, kulma, 1.0)
        else:
            kaannetty_tausta = rotozoom(self.kuva, kulma, 1.0)
        kaannetty_tausta_koko = Vector2(kaannetty_tausta.get_size())
        blit_sijainti = self.sijainti - kaannetty_tausta_koko * 0.5
        tausta.blit(kaannetty_tausta, blit_sijainti)

class Pokale(PeliObjekti):
    def __init__(self, sijainti):
        super().__init__(sijainti, lataa_kuvat("poop30px", True),(0,0))
        self.nopeus = Vector2(1)
        self.suunta = Vector2((random.choice(range(-10,11))/10),(random.choice(range(-10,11))/10))

    def liiku(self, taustakuva):
        self.sijainti = rajaa_kartta(self.sijainti + self.nopeus, taustakuva)
        self.suunta.rotate_ip(2)

    def piirra(self, tausta):
        kulma = self.suunta.angle_to(OIKEA)
        kaannetty_tausta = rotozoom(self.kuva, kulma, 1.0)
        kaannetty_tausta_koko = Vector2(kaannetty_tausta.get_size())
        blit_sijainti = self.sijainti - kaannetty_tausta_koko * 0.5
        tausta.blit(kaannetty_tausta, blit_sijainti)

#taustakuva
#Image by <a href="https://pixabay.com/users/ractapopulous-24766/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2734972">JL G</a> from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=2734972">Pixabay</a>
#nyan rainbow kissakuva
#<a href=https://www.pngall.com/nyan-cat-png/download/8770 target="_blank">Nyan Cat PNG</a>
#nyan kuva
#<a href=https://www.pngall.com/nyan-cat-png/download/8781 target="_blank">Nyan Cat Transparent</a>
#Music by <a href="https://pixabay.com/users/psychronic-13092015/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=21858">Psychronic</a> 
# from <a href="https://pixabay.com//?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=music&amp;utm_content=21858">Pixabay</a>
