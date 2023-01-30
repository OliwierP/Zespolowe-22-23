import pygame,random
class Karta() :
    def __init__(self,value,color):
        self.value = value
        self.color = color
        self.obraz = pygame.image.load(f"O/{self.value}{self.color}.png")
        self.obraz_wymiar = self.obraz.get_rect()
class Talia() :
    def __init__(self):
        self.talia = []
        color = ["trefl","kier","karo","pik"]
        value = [2,3,4,5,6,7,8,9,10,"j","d","k","a"]
        for colors in color :
            for values in value :
                self.talia.append(Karta(values,colors))

    def rozdawanie(self):
        """rozdawanie kart"""
        karta = random.choice(self.talia)
        self.talia.remove(karta)
        return karta
    """def show_deck(self):
        for karts in self.talia :
            print(f"Karta koloru:{karts.color} o wartości {karts.value}")
        print(len(self.talia))"""
class Zeton() :
    def __init__(self,value):
        self.value = int(value)
        self.image = pygame.image.load(f"O/{value}.png")
        self.img_rect = self.image.get_rect()
    def nacisniecie(self,mysz):
        x , y = mysz
        if x >= self.img_rect.x and x <= self.img_rect.x + self.img_rect.width and y >= self.img_rect.y and y <= self.img_rect.y + self.img_rect.height :
            return True
    def wyswietl_zeton(self,okno):
        okno.blit(self.image,self.img_rect)
class Gracz() :
    def __init__(self):
        self.karty = []
        self.money = 1000

    def ile_pkt(self):
        pkt = 0
        for karta in self.karty :
            if karta.value in [2,3,4,5,6,7,8,9,10] :
                pkt += int(karta.value)
            elif karta.value == "a" :
                pkt += 11
            else :
                pkt += 10
        return pkt

    def dobierz_karte(self,talia):
        self.karty.append(talia.rozdawanie())