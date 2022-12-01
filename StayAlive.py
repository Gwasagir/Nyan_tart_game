import pygame
from ominaisuudet import lataa_kuvat, satunnainen_koord, lataa_musat
from mallit import PeliObjekti, Kissa, Pokale
from pygame.math import Vector2
import math

class StayAlive:
    pokale_etaisyys = 250
    def __init__(self):
        self._init_pygame()
        self.naytto = pygame.display.set_mode((1280, 720))
        self.taustakuva = lataa_kuvat("taustakuva720p", False)

        self.aloitus = True
        self.odotusaika = 0

        self.kello = pygame.time.Clock()
        self.aika = 0
        self.supertimer = 0
        self.supertimernollaus = False
        self.superbreak = 0
        self.superbreaknollaus = False

        self.fontti = pygame.font.SysFont("Arial", 20)
        self.fontti2 = pygame.font.SysFont("Arial", 30)

        self.pisteet = 0
        self.pokaleet = []
        self.kissa = Kissa((640,360))
        for x in range(31):
            while True:
                sijainti = satunnainen_koord(self.taustakuva)
                if sijainti.distance_to(self.kissa.sijainti) > self.pokale_etaisyys: break
            self.pokaleet.append(Pokale(sijainti))

    def suorita(self):
        while True:
            self._tapahtumat()
            self._peli_logiikka()
            self._piirra()
            self._musiikki(False)

            if self.kissa:
                if self.kissa.supervoima:
                    if self.supertimernollaus == False:
                        supertimer = pygame.time.get_ticks()
                        self.supertimernollaus = True
                    seconds=(pygame.time.get_ticks()-supertimer)/1000 #calculate how many seconds
                    if seconds>10: # laskee 10sec ja de-aktivoi supervoiman
                        self.kissa.aktivoi_supervoima(False)
                        self.supertimernollaus = False

                if self.kissa.supervoima == False:
                    if self.superbreaknollaus == False:
                        superbreak = pygame.time.get_ticks()
                        self.superbreaknollaus = True
                    seconds=(pygame.time.get_ticks()-superbreak)/1000 #calculate how many seconds
                    if seconds>20: # laskee 10sec ja de-aktivoi supervoiman
                        self.kissa.supervoima_valmiina = True
                        self.superbreaknollaus = False

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Stay Alive, Stay Nyan")

    def _lisaa_pokaleita(self):
        vaikeus = [x for x in range(1,100)]
        pokaleita = 30 + vaikeus[int(self.aika/1)]
        if len(self.pokaleet) < pokaleita:
            while True:
                sijainti = satunnainen_koord(self.taustakuva)
                if sijainti.distance_to(self.kissa.sijainti) > self.pokale_etaisyys: break
            self.pokaleet.append(Pokale(sijainti))

    def _hae_peliobjektit(self):
        objektit = [*self.pokaleet]
        if self.kissa:
            objektit.append(self.kissa)
        return objektit

    def _tuhoa_pokale(self, index):
        return self.pokaleet.pop(index)

    def _peli_logiikka(self):
        if self.aloitus == False:
            self._lisaa_pokaleita()
            tormays = False
            for objekti in self._hae_peliobjektit():
                objekti.liiku(self.taustakuva)
            if self.kissa:
                for indx, pokale in enumerate(self.pokaleet):
                    if pokale.tormays(self.kissa):
                        if self.kissa.supervoima == True:
                            self._tuhoa_pokale(indx)
                            self.pisteet += 1
                            break
                        else: 
                            self.kissa = None
                            break

    def _uusi_peli(self):
        stay_alive = StayAlive()
        stay_alive.suorita()
        self.pokaleet = []
        self.pisteet = 0
        self.odotusaika += round(pygame.time.get_ticks()/1000,1)

    def _hae_suunta(self, hiiri):
        kissakoord = self.kissa.sijainti
        kissasuunta = self.kissa.suunta
        dx =  hiiri[0] - kissakoord[0]
        dy = hiiri[1] - kissakoord[1] 
        hiirenkulma = math.atan2(dy,dx)
        kissankulma = math.atan2(kissasuunta[1], kissasuunta[0])
        if kissankulma > 0:
            if hiirenkulma > 0:
                if hiirenkulma > kissankulma: return True
            else:
                if kissankulma > math.pi - math.fabs(hiirenkulma): return True
                else: return False
        else:
            if hiirenkulma < 0:
                if math.fabs(hiirenkulma) > math.fabs(kissankulma): return False
                else: return True
            else:
                if math.fabs(hiirenkulma) < math.pi - hiirenkulma: return True
                else: return False
                    
    def _tapahtumat(self):
        pygame.event.set_grab(True)
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_ESCAPE:
                    exit()
                if tapahtuma.key == pygame.K_SPACE and self.aloitus == True:
                    self.aloitus = False
                    self.odotusaika = round(pygame.time.get_ticks()/1000,1)
                if tapahtuma.key == pygame.K_F2 and self.aloitus == False:
                    self._uusi_peli()

                if self.kissa and self.aloitus == False:
                    if tapahtuma.key == pygame.K_SPACE:
                        self.kissa.suuntaa_kiihdyta()
                    if tapahtuma.key == pygame.K_LCTRL:
                        self.kissa.aktivoi_supervoima(True)

            if tapahtuma.type == pygame.QUIT:
                exit()
            #hiiri kääntää alusta
            if self.kissa and self.aloitus == False:
                if tapahtuma.type == pygame.MOUSEMOTION:
                    self.kissa.kaanna(clockwise=self._hae_suunta(tapahtuma.pos))
                if tapahtuma.type == pygame.MOUSEBUTTONDOWN:
                    if tapahtuma.button == 1:
                        self.kissa.suuntaa_kiihdyta()
                    if tapahtuma.button == 3:
                        self.kissa.aktivoi_supervoima(True)

    def _text_objects(self, text, font):
        textSurface = font.render(text, True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def _musiikki(self, bool):
        if self.kissa != None and bool == True:
            #pygame.mixer.init(44100, 16, 2, 20000)
            musa = self.kissa.taustamusa
            musa.set_volume(0.6)
            musa.play()

    def _piirra(self):
        self.naytto.blit(self.taustakuva, (0,0))

        if self.aloitus == False:
            for objekti in self._hae_peliobjektit():
                objekti.piirra(self.naytto)

            if self.kissa:
                self.aika = round(pygame.time.get_ticks()/1000,1) - self.odotusaika
                if self.kissa.supervoima_valmiina:
                    Text_pohja, Text_nelio = self._text_objects("SUPERVOIMA VALMIS, PAINA CTRL/MOUSE2", self.fontti)
                    Text_nelio.center = ((1280/2),(200))
                    self.naytto.blit(Text_pohja, Text_nelio)
            teksti = self.fontti.render("Vauhtia = Välilyönti & Mouse1 " +
            "Supervoima = CTRL & Mouse2" +
            "Lopeta = ESC" +
            f"        Olet ollut elossa {self.aika:.1f} sekuntia"+
            f"        Tuhottuja pökäleitä {self.pisteet}", True, (0,0,0))
            self.naytto.blit(teksti, (20, 695))
            if self.kissa == None:
                teksti1 = self.fontti2.render("Peli ohi. " + 
                f"Selvisit {self.aika:.1f} sekuntia ja sait {self.pisteet} pistettä." + 
                " Uusi peli = F2", True,(200,0,0))
                self.naytto.blit(teksti1, (250, 360))

        if self.aloitus == True:
            TextSurf, TextRect = self._text_objects("Kissa seuraa hiirtä. Välilyönti tai mouse1 antaa vauhtia. Lopettaaksesi, paina ESC", self.fontti)
            TextRect.center = ((1280/2),(660/2))
            self.naytto.blit(TextSurf, TextRect)
            TextSurf, TextRect = self._text_objects("Saat supervoiman 10 sekunin välein, paina CTRL tai Mouse2 aktivoidaksesi. Paina välilyöntiä aloittaaksesi", self.fontti)
            TextRect.center = ((1280/2),(720/2))
            self.naytto.blit(TextSurf, TextRect)
            TextSurf, TextRect = self._text_objects("Pokaleet lisääntyvät pelin edetessä 1 tart / sec", self.fontti)
            TextRect.center = ((1280/2),(780/2))
            self.naytto.blit(TextSurf, TextRect)

        pygame.display.flip()
        self.kello.tick(60)