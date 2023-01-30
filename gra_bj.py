import sys
from talia import Gracz,Talia, Zeton
import pygame
import time

class Stol() :
    def __init__(self):
        pygame.init()
        self.okno = pygame.display.set_mode((600,480))
        pygame.display.set_caption("BJ-Oczko-21")
        self.tlo = pygame.image.load("O/BJSTART.jpg")
        self.tlo_wymiar = self.tlo.get_rect()
        self.tlo1 = pygame.image.load("O/BJPLAY.png")
        self.tlo1_wymiar = self.tlo1.get_rect()
        self.loading = True
        self.czcionka = pygame.font.SysFont(None,36)
        self.gracz = Gracz()
        self.krupier = Gracz()
        self.talia = Talia()
        self.rozdanie = False
        self.first = True
        self.dobierz = False
        self.czekaj = False
        self.end = False
        self.obstaw = False
        self.stawka = 0
        self.zetony = []
        nominaly_zeton = [1,5,10,20,25,50,100,500,1000,2000]
        for i in nominaly_zeton :
            self.zetony.append(Zeton(i))
    def wiadomosc(self, tekst, x, y, width, height, rozmiar,okno,kolor = (255,255,255)):
        """Funkcja do budowania tekstu"""
        czcionka = pygame.font.SysFont(None,int(rozmiar))
        wiadomosci = czcionka.render(tekst,True,kolor)
        wiadomosci_okno = wiadomosci.get_rect()
        wiadomosci_okno.x = x
        wiadomosci_okno.y = y
        wiadomosci_okno.width = width
        wiadomosci_okno.height = height
        okno.blit(wiadomosci,wiadomosci_okno)
    def play(self):
        while True :
            for event in pygame.event.get() :
                if event.type == pygame.QUIT :
                    sys.exit()
                if event.type == pygame.KEYDOWN :
                    if event.key == pygame.K_s :
                        self.loading = False
                    if event.key == pygame.K_q :
                        self.loading = True
                    #if event.key == pygame.K_l and self.first == True :
                        #self.rozdanie = True
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        x, y = pygame.mouse.get_pos()
                        for i in range(10) :
                            if self.zetony[i].nacisniecie(pygame.mouse.get_pos()) :
                                if self.stawka + self.zetony[i].value <= self.gracz.money and self.obstaw == True :
                                    self.stawka += self.zetony[i].value
                        if x >= 500 and x <= 600 and y >= 240 and y <= 290 and self.obstaw == True :
                            self.gracz.money =  self.gracz.money - self.stawka
                            self.obstaw = False
                            self.rozdanie = True
                        if x >= 500 and x <= 560 and y >=350 and y <= 385 :
                            self.dobierz = True
                        elif x >= 500 and x<=560 and y >=390 and y <= 425 :
                            self.czekaj = True
            if self.rozdanie :
                for i in range(2) :
                    self.gracz.dobierz_karte(self.talia)
                    self.krupier.dobierz_karte(self.talia)
                    self.dobierz = False
                    self.rozdanie = False
                    self.czekaj = False
                    self.first = False
                    self.end = False
            if self.loading == True :
                self.okno.blit(self.tlo,self.tlo_wymiar)
                napis = self.czcionka.render("LOADING",True,(255,255,255))
                napis_miejsce = napis.get_rect()
                napis_miejsce.x = 240
                napis_miejsce.y = 380
                self.okno.blit(napis,napis_miejsce)
                self.obstaw = True
            elif self.loading == False and self.obstaw == True :
                self.okno.blit(self.tlo1, self.tlo1_wymiar)
                self.wiadomosc("Obstaw", 500, 240, 100, 50, 36, self.okno)
                self.wiadomosc(f"Obstawiasz {self.stawka}",280,180,100,40,36,self.okno)
                for i in range(10) :
                    self.zetony[i].img_rect.x = 50 * i
                    self.zetony[i].img_rect.y = 240
                    self.zetony[i].wyswietl_zeton(self.okno)
                #self.obstaw = False
            else :
                self.okno.blit(self.tlo1,self.tlo1_wymiar)
                self.wiadomosc("Dobierz",500,350,60,35,32,self.okno)
                self.wiadomosc("Czekaj",500,390,60,35,32,self.okno)
                print(self.gracz.ile_pkt())
                for i in range(len(self.gracz.karty)) :
                    x = 240 + 60*i
                    y = 380
                    self.gracz.karty[i].obraz_wymiar.x = x
                    self.gracz.karty[i].obraz_wymiar.y = y
                    self.okno.blit(self.gracz.karty[i].obraz,self.gracz.karty[i].obraz_wymiar)
                    if len(self.krupier.karty) > 0 :
                        self.krupier.karty[0].obraz_wymiar.x = 240
                        self.krupier.karty[0].obraz_wymiar.y = 160
                        self.okno.blit(self.krupier.karty[0].obraz,self.krupier.karty[0].obraz_wymiar)
                if self.gracz.ile_pkt() < 21 and self.dobierz == True and self.first == False and self.czekaj == False :
                    self.gracz.dobierz_karte(self.talia)
                    self.dobierz =False
                if self.gracz.ile_pkt() > 21 :
                    self.wiadomosc("Przegrales !!!!",250,260,100,80,48,self.okno)
                    self.gracz.karty[-1].obraz_wymiar.x = self.gracz.karty[-2].obraz_wymiar.x + 60
                    self.gracz.karty[-1].obraz_wymiar.y = 380
                    self.okno.blit(self.gracz.karty[-1].obraz, self.gracz.karty[-1].obraz_wymiar)
                    self.gracz.karty = []
                    self.krupier.karty = []
                    self.end = True
                    self.first = True
                if self.gracz.ile_pkt() == 21 :
                    self.wiadomosc("Wygrales !!!!", 250, 260, 100, 80, 48, self.okno)
                    self.gracz.karty[-1].obraz_wymiar.x = self.gracz.karty[-2].obraz_wymiar.x + 60
                    self.gracz.karty[-1].obraz_wymiar.y = 380
                    self.okno.blit(self.gracz.karty[-1].obraz,self.gracz.karty[-1].obraz_wymiar)
                    self.gracz.money = self.gracz.money + 2 * self.stawka
                    self.gracz.karty = []
                    self.krupier.karty = []
                    self.end = True
                    self.first = True
                if self.czekaj == True :
                    for i in range(len(self.krupier.karty)) :
                        x = 240 + 60 * i
                        y = 160
                        self.krupier.karty[i].obraz_wymiar.x = x
                        self.krupier.karty[i].obraz_wymiar.y = y
                        self.okno.blit(self.krupier.karty[i].obraz, self.krupier.karty[i].obraz_wymiar)
                    if self.krupier.ile_pkt() > self.gracz.ile_pkt() and self.krupier.ile_pkt() <= 21:
                        self.wiadomosc("Przegrales !!!!", 250, 260, 100, 80, 48, self.okno)
                        self.gracz.karty = []
                        self.krupier.karty = []
                        self.first = True
                        self.czekaj = False
                        self.end = True

                    elif self.krupier.ile_pkt() <= self.gracz.ile_pkt() :
                        self.krupier.dobierz_karte(self.talia)
                    elif self.krupier.ile_pkt() > 21 :
                        self.wiadomosc("Wygrales !!!!", 250, 260, 100, 80, 48, self.okno)
                        self.gracz.money = self.gracz.money + 2 * self.stawka
                        self.gracz.karty = []
                        self.krupier.karty = []
                        self.first = True
                        self.czekaj = False
                        self.end = True
            if len(self.krupier.karty) > 0 and len(self.gracz.karty) >0 :
                print(f"Krupier:{self.krupier.karty[0].value}, gracz:{self.gracz.karty[0].value}")
            if not self.rozdanie and not self.loading :
                self.wiadomosc(f"Monety: {self.gracz.money}",450,0,100,40,24,self.okno,(0,0,0))
            pygame.display.flip()
            if self.end :
                self.stawka = 0
                self.obstaw = True
                if self.gracz.money == 0:
                    self.gracz.money = 1000
                    self.wiadomosc("Bankrut !", 150, 100, 300, 300, 72, self.okno)
                pygame.display.flip()
                time.sleep(2)
                self.end = False
                self.talia = Talia()

if __name__ == "__main__" :
    bj = Stol()
    bj.play()