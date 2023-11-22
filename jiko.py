import numpy
import pygame
from random import randint as rng

"""
TODO juurde
- level design
- scaling

TODO parandada
- collison window'i äärtega

"""

ruudud = 40  # kui mitmeks ruuduks jagame
ruudu_suurus = 30  # küljepikkus pikslites
pikkus = ruudud * ruudu_suurus
laius = pikkus
lahutusvõime = (pikkus, laius)
lahutusvõime2 = (laius - ruudu_suurus * 30, pikkus - ruudu_suurus * 30)
# lahutusvõime2=(laius, pikkus)
blitx = 0 - ruudu_suurus * 16
blity = 0 - ruudu_suurus * 26

sammud_loendur = 0
on_maas = False


class World():
    # ruutude piltide ja väärtuste jaoks dictionary
    # vb peaks lahenduse üle vaatama, aga prg töötab
    # peaks vast võtmeteks natuke iseloomulikumad asjad
    # nvm läheb keeruliseks
    pildid = {
        1: "",
        2: "",
        3: ""
    }

    def lisa_pilt(tüüp, rea_lugeja, veeru_lugeja):
        global ruudu_suurus
        img = World.pildid[tüüp]
        img = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        # loob recti (default asukoht on (0,0))
        img_rect = img.get_rect()
        # rect on pygame'i objekt (risttahukas), mis sisaldab koordinaate
        img_rect.x = veeru_lugeja * ruudu_suurus
        img_rect.y = rea_lugeja * ruudu_suurus
        return (img, img_rect)

    def __init__(self, maatriks):
        self.ruudud_list = []
        # ei tekita collisionit
        self.objektid_list = []
        World.pildid[1] = pygame.image.load("tekstuur.jpg")
        # kivi = 1
        World.pildid[2] = pygame.image.load("tekstuur1.jpg")
        # muru = 2
        World.pildid[3] = pygame.image.load("mexico.png")
        """
        tekstuur2 = pygame.image.load()
        ...
        """
        # võtab maatriksist väärtuse andmed ja muudab selle
        # koordinaatidega seotud objektideks
        rea_lugeja = 0
        print(maatriks)
        for rida in maatriks:
            veeru_lugeja = 0
            for ruut in rida:
                if ruut == 3:
                    if int(maatriks[rea_lugeja + 1][veeru_lugeja]) == 2:
                        ruut = World.lisa_pilt(ruut, rea_lugeja, veeru_lugeja)
                        self.objektid_list.append(ruut)
                elif ruut > 0:
                    ruut = World.lisa_pilt(ruut, rea_lugeja, veeru_lugeja)
                    self.ruudud_list.append(ruut)
                veeru_lugeja += 1
            rea_lugeja += 1

    def joonista(self):
        for ruut in self.ruudud_list:
            window.blit(ruut[0], (ruut[1][0] + blitx, ruut[1][1] + blity))
        for objekt in self.objektid_list:
            window.blit(objekt[0], (objekt[1][0] + blitx, objekt[1][1] + blity))

class Player():
    global window, lahutusvõime, world

    def __init__(self, asukoht):
        img = pygame.image.load("seisab.png")
        img1 = pygame.image.load("samm1.png")
        img2 = pygame.image.load("samm2.png")
        self.img_parem = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus * 2))
        self.img_vasak = pygame.transform.flip(self.img_parem, True, False)  # flipib pildi ümber y-telje
        self.img_samm_parem = pygame.transform.scale(img1, (ruudu_suurus, ruudu_suurus * 2))
        self.img_samm_vasak = pygame.transform.flip(self.img_samm_parem, True, False)
        self.img_samm_parem2 = pygame.transform.scale(img2, (ruudu_suurus, ruudu_suurus * 2))
        self.img_samm_vasak2 = pygame.transform.flip(self.img_samm_parem2, True, False)
        self.sammud_frames_parem = [self.img_samm_parem, self.img_samm_parem, self.img_samm_parem, self.img_samm_parem, self.img_samm_parem, self.img_samm_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem]
        self.sammud_frames_vasak = [self.img_samm_vasak, self.img_samm_vasak, self.img_samm_vasak, self.img_samm_vasak, self.img_samm_vasak, self.img_samm_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak]

        self.rect = self.img_parem.get_rect()
        self.rect.x = asukoht[0]
        self.rect.y = asukoht[1]
        laius = self.img_parem.get_width()
        pikkus = self.img_vasak.get_height()
        self.suurus = (laius, pikkus)

        self.kiirus_y = 0
        self.suund = 0
        self.maas = True

    def uuenda(self):
        global sammud_loendur, blitx, blity

        dx = 0
        dy = 0
        liikumine = False

        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.hüpe is False:
            self.kiirus_y = -20
            self.hüpe = True
            self.maas = False
        # lisasin self.hüpe muutmise collision detecti alla,
        # nüüd ei saa hüppamist spammida
        if key[pygame.K_w] is False and key[pygame.K_SPACE] is False and self.maas is True:
            self.hüpe = False
        if key[pygame.K_a]:
            dx -= 10
            self.suund = -1
            liikumine = True
        if key[pygame.K_d]:
            dx += 10
            self.suund = 1
            liikumine = True

        self.kiirus_y += 1
        # kukkumisel on max kiirus
        if self.kiirus_y > 30:
            self.kiirus_y = 30
        dy += self.kiirus_y

        # collision detect
        for ruut in world.ruudud_list:
            if ruut[1].colliderect(self.rect.x + dx, self.rect.y, self.suurus[0], self.suurus[1]):
                dx = 0
            if ruut[1].colliderect(self.rect.x, self.rect.y + dy, self.suurus[0], self.suurus[1]):
                # kui collision tekib hüppamisel
                if self.kiirus_y < 0:
                    dy = ruut[1].bottom - self.rect.top
                    self.kiirus_y = 0
                # kui collision tekib kukkumisel
                else:
                    dy = ruut[1].top - self.rect.bottom
                    self.kiirus_y = 0
                    self.maas = True

        # ei kuku frame'ist välja
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > lahutusvõime[0] - ruudu_suurus:
            self.rect.x = lahutusvõime[0] - ruudu_suurus
        if self.rect.y < 0:
            self.rect.y = 0

        # uuendab mängija koordinaate
        self.rect.x += dx
        self.rect.y += dy
        blitx -= dx
        blity -= dy

        # joonistab mängija ekraanile
        if self.suund == 1:
            img = self.img_parem
            if liikumine is True:
                if sammud_loendur == 23:
                    sammud_loendur = 0
                img = self.sammud_frames_parem[sammud_loendur]
                sammud_loendur += 1
        else:
            img = self.img_vasak
            if liikumine is True:
                if sammud_loendur == 23:
                    sammud_loendur = 0
                img = self.sammud_frames_vasak[sammud_loendur]
                sammud_loendur += 1

        window.blit(img, (self.rect[0] + blitx, self.rect[1] + blity))
        # pygame.draw.rect(window, (0, 255, 0 ), self.rect, 2)


# joonistab ruudustiku välja
def ruudustik():
    global window, ruudu_suurus, ruudud, lahutusvõime
    for i in range(ruudud):
        pygame.draw.line(window, (255, 255, 255), (i * ruudu_suurus, 0),
                         (i * ruudu_suurus, lahutusvõime[1]))
        pygame.draw.line(window, (255, 255, 255), (0, i * ruudu_suurus),
                         (lahutusvõime[0], i * ruudu_suurus))


def main():
    global window, lahutusvõime, world
    pygame.init()

    FPS = 60  # et programm töötaks olenemata riistvarast samasuguselt
    nimi = "Jiko"

    window = pygame.display.set_mode(lahutusvõime2)
    pygame.display.set_caption(nimi)

    # laeb tausta
    taust = pygame.image.load("background.png")
    taust = pygame.transform.scale(taust, lahutusvõime)

    # loob maatirksi, kus iga element vastab mingile ruudustiku väärtusele
    # ja elemendi väärtus määrab ruudu tüübi (pildi)
    world_maatriks = numpy.zeros((ruudud, ruudud))
    world_maatriks[0:3] = 1  # testimiseks
    world_maatriks[1:39, 0:3] = 1
    world_maatriks[1:39, 36:40] = 1
    world_maatriks[36:40] = 2
    world_maatriks[32, 3:33] = 2
    world_maatriks[28, 6:36] = 2
    for i in range(7):
        blunt = rng(5, 35)
        world_maatriks[27, blunt] = 3

    world = World(world_maatriks)

    player = Player((ruudu_suurus*20, lahutusvõime[0] - (ruudu_suurus*10)))

    fpsKell = pygame.time.Clock()  # loob objekti aja jälgimiseks
    run = True
    while run:

        # lisab pildi aknas kuvatavale frame'ile
        # järjekord oluline !
        window.blit(taust, (0+blitx, 0+blity))
        # window.blit(man, (0, 600))

        # ruudustik()  # loob ruudusitku

        World.joonista(world)  # joonistab tekstuuriga ruudud ekraanile
        Player.uuenda(player)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_q:
                    run = False

        pygame.display.update()  # värksendab aknas kuvatavat frame'i

        # pärast määrata muutuja väärtuseks, et liikumine toimuks ühtselt?
        fpsKell.tick(FPS)  # uuendab 'kella' väärtust

    mapfail = open("map.txt", "w")
    mapfail.write(str(world_maatriks))
    mapfail.close()
    pygame.quit()


if __name__ == "__main__":
    main()
