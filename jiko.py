import numpy
import pygame
# from random import randint as rng
import math

"""
TODO juurde
- level design
- scaling

TODO parandada
- collison window'i äärtega

"""

RUUDUD = 40  # kui mitmeks ruuduks jagame
RUUDU_SUURUS = 30  # küljepikkus pikslites
PIKKUS = RUUDUD * RUUDU_SUURUS
LAIUS = PIKKUS
lahutusvõime = (PIKKUS, LAIUS)
lahutusvõime2 = (LAIUS - RUUDU_SUURUS * 30, PIKKUS - RUUDU_SUURUS * 30)

# miks 16 ja 26 ???
blitx = 0 - RUUDU_SUURUS * 16
blity = 0 - RUUDU_SUURUS * 26


class World():
    global RUUDU_SUURUS

    def __init__(self, maatriks):
        self.ruudud_list = []

        self.pildid = {}
        self.pildid[1] = pygame.image.load("tekstuur.jpg")
        self.pildid[2] = pygame.image.load("tekstuur1.jpg")
        for pilt in self.pildid:
            self.pildid[pilt] = pygame.transform.scale(self.pildid[pilt], (RUUDU_SUURUS, RUUDU_SUURUS))

        self.maatriks = maatriks
        self.spawn()

    def spawn(self):
        # võtab maatriksist väärtuse andmed ja muudab selle
        # koordinaatidega seotud objektideks
        rea_lugeja = 0
        for rida in self.maatriks:
            veeru_lugeja = 0
            for ruut in rida:
                if ruut > 0:
                    # lisa_pilt tagastab ennikuna ruudule vastava pildi
                    # ja recti
                    pilt = self.tagasta_pilt(ruut)
                    self.ruudud_list.append(self.loo_rect(pilt, rea_lugeja, veeru_lugeja))
                    veeru_lugeja += 1
            rea_lugeja += 1

    def tagasta_pilt(self, ruut):
        return self.pildid[ruut]

    def loo_rect(self, pilt, rea_lugeja, veeru_lugeja):
        global RUUDU_SUURUS
        rect = pilt.get_rect()
        rect.x = veeru_lugeja * RUUDU_SUURUS
        rect.y = rea_lugeja * RUUDU_SUURUS
        return [pilt, rect]

    def joonista(self):
        for ruut in self.ruudud_list:
            window.blit(ruut[0], (ruut[1][0] + blitx, ruut[1][1] + blity))


class Taco(World):
    def __init__(self, maatriks, pilt):
        self.ruudud_list = []
        self.maatriks = maatriks
        self.pilt = pygame.transform.scale(pygame.image.load(pilt), (2 * RUUDU_SUURUS, 2 * RUUDU_SUURUS))
        self.pildid = [self.pilt, pygame.transform.flip(self.pilt, True, False)]
        self.asend = 0
        self.spawn()
        for ruut in self.ruudud_list:
            # võib kolm korda viineriga pihta saada
            ruut.append(2)
        self.lugeja = 0

    def flip(self):
        self.joonista(self.pildid[self.asend])
        if self.lugeja == 30:
            if self.asend == len(self.pildid) - 1:
                self.asend = 0
            else:
                self.asend += 1
            self.lugeja = 0
        self.lugeja += 1

    def collision(self):
        for viiner in viinerid:
            for ruut in self.ruudud_list:
                if pygame.Rect.colliderect(viiner.rect, ruut[1]):
                    viinerid.pop(viinerid.index(viiner))
                    del viiner
                    ruut[2] -= 1
                if ruut[2] == 0:
                    self.ruudud_list.pop(self.ruudud_list.index(ruut))

    def tagasta_pilt(self, ruut=None):
        return self.pilt

    def joonista(self, pilt):
        for ruut in self.ruudud_list:
            window.blit(pilt, (ruut[1][0] + blitx, ruut[1][1] + blity))


class Viiner():
    global blitx, blity

    def __init__(self, x, y, suund):
        self.pilt = pygame.transform.scale(pygame.image.load("viiner.png"), (RUUDU_SUURUS / 2, RUUDU_SUURUS / 2))
        self.rect = self.pilt.get_rect()
        self.rect.x = x
        self.rect.y = y + RUUDU_SUURUS / 2
        self.suund = suund
        self.lugeja = 0

    def liikumine(self):
        # mingil põhjusel ei pööra pygame pilti ümber selle keskpunkti
        if self.lugeja == 6:
            self.pilt = pygame.transform.rotate(self.pilt, 90)
            self.lugeja = 0
        self.lugeja += 1
        if self.suund < 0:
            self.rect.x -= 5
        else:
            self.rect.x += 5
        if self.rect.x > (LAIUS - RUUDU_SUURUS) or self.rect.x < RUUDU_SUURUS or self.rect.y > (PIKKUS - RUUDU_SUURUS):
            return 0
        else:
            window.blit(self.pilt, (self.rect[0] + blitx, self.rect[1] + blity))
            return 1


class Player():
    global window, lahutusvõime, world, taco, viinerid

    def __init__(self, asukoht):
        img = pygame.image.load("seisab.png")
        img1 = pygame.image.load("samm1.png")
        img2 = pygame.image.load("samm2.png")
        self.img_parem = pygame.transform.scale(img, (RUUDU_SUURUS, RUUDU_SUURUS * 2))
        self.img_vasak = pygame.transform.flip(self.img_parem, True, False)  # flipib pildi ümber y-telje
        img_samm_parem = pygame.transform.scale(img1, (RUUDU_SUURUS, RUUDU_SUURUS * 2))
        img_samm_vasak = pygame.transform.flip(img_samm_parem, True, False)
        img_samm_parem2 = pygame.transform.scale(img2, (RUUDU_SUURUS, RUUDU_SUURUS * 2))
        img_samm_vasak2 = pygame.transform.flip(img_samm_parem2, True, False)
        self.sammud_frames_parem = [img_samm_parem, self.img_parem,
                                    img_samm_parem2, self.img_parem]
        self.sammud_frames_vasak = [img_samm_vasak, self.img_vasak,
                                    img_samm_vasak2, self.img_vasak]

        self.rect = self.img_parem.get_rect()
        self.rect.x = asukoht[0]
        self.rect.y = asukoht[1]
        laius = self.img_parem.get_width()
        pikkus = self.img_vasak.get_height()
        self.suurus = (laius, pikkus)

        self.kiirus_y = 0
        self.suund = 0
        self.maas = True
        self.sammud_loendur = 0
        self.lugeja = 0

    def uuenda(self):
        # global sammud_loendur
        global blitx, blity

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
        if key[pygame.K_f] and self.laseb_viinerit is False:
            viinerid.append(Viiner(x=self.rect.x, y=self.rect.y, suund=self.suund))
            self.laseb_viinerit = True
        elif key[pygame.K_f] is False:
            self.laseb_viinerit = False

        self.kiirus_y += 1
        # kukkumisel on max kiirus
        if self.kiirus_y > 30:
            self.kiirus_y = 30
        dy += self.kiirus_y

        objektid = world.ruudud_list + taco.ruudud_list
        # collision detect
        for ruut in objektid:
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
        elif self.rect.x > lahutusvõime[0] - RUUDU_SUURUS:
            self.rect.x = lahutusvõime[0] - RUUDU_SUURUS
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
            list_sammud = self.sammud_frames_parem
        else:
            img = self.img_vasak
            list_sammud = self.sammud_frames_vasak

        sammud_tsükkel_pikkus = 24
        if liikumine is False:
            self.sammud_loendur = 0
        pilt_index = math.floor(self.sammud_loendur / (sammud_tsükkel_pikkus / len(list_sammud)))
        img = list_sammud[pilt_index]
        if self.sammud_loendur == sammud_tsükkel_pikkus - 1:
            self.sammud_loendur = 0
        else:
            self.sammud_loendur += 1

        window.blit(img, (self.rect[0] + blitx, self.rect[1] + blity))
        # pygame.draw.rect(window, (0, 255, 0 ), self.rect, 2)


# joonistab ruudustiku välja
def ruudustik():
    global window, RUUDU_SUURUS, RUUDUD, lahutusvõime
    for i in range(RUUDUD):
        pygame.draw.line(window, (255, 255, 255), (i * RUUDU_SUURUS, 0),
                         (i * RUUDU_SUURUS, lahutusvõime[1]))
        pygame.draw.line(window, (255, 255, 255), (0, i * RUUDU_SUURUS),
                         (lahutusvõime[0], i * RUUDU_SUURUS))


def main():
    global window, lahutusvõime, world, taco, viinerid
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
    world_maatriks = numpy.zeros((RUUDUD, RUUDUD))
    world_maatriks[0:3] = 1  # testimiseks
    world_maatriks[1:39, 0:3] = 1
    world_maatriks[1:39, 36:40] = 1
    world_maatriks[36:40] = 2
    world_maatriks[32, 3:33] = 2
    world_maatriks[28, 6:36] = 2

    world = World(world_maatriks)

    player = Player((RUUDU_SUURUS*20, lahutusvõime[0] - (RUUDU_SUURUS*10)))

    taco_maatriks = numpy.zeros((RUUDUD, RUUDUD))
    taco_maatriks[30, 20:28] = 1
    taco = Taco(maatriks=taco_maatriks, pilt="mexico.png")

    viinerid = []

    fpsKell = pygame.time.Clock()  # loob objekti aja jälgimiseks
    run = True
    while run:

        # lisab pildi aknas kuvatavale frame'ile
        # järjekord oluline !
        window.blit(taust, (0 + blitx, 0 + blity))
        # ruudustik()  # loob ruudusitku

        world.joonista()
        taco.flip()
        # taco.flip()
        for viiner in viinerid:
            if viiner.liikumine() == 0:
                viinerid.pop(viinerid.index(viiner))
                del viiner
        taco.collision()

        player.uuenda()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x or event.key == pygame.K_q:
                    run = False
                if event.key == pygame.K_c:
                    # prindib player'i koordinaadid ja maatriksi elemendi (rida, veerg)
                    print(f"x: {player.rect.x}, y: {player.rect.y}, maatriks r:{int(player.rect.y / RUUDU_SUURUS)}, v:{int(player.rect.x / RUUDU_SUURUS)}")

        pygame.display.update()  # värksendab aknas kuvatavat frame'i

        # pärast määrata muutuja väärtuseks, et liikumine toimuks ühtselt?
        fpsKell.tick(FPS)  # uuendab 'kella' väärtust

    mapfail = open("map.txt", "w")
    mapfail.write(str(world_maatriks))
    mapfail.close()
    pygame.quit()


if __name__ == "__main__":
    main()
