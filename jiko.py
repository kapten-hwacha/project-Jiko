import numpy
import pygame
# from random import randint as rng
import math
import pandas as pd

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

# igasugu erinevaid muutujaid
vaja_uuendada = False
mängija_X = 0
mängija_Y = 0
blokk_down_timer = False
blokk_up_timer = False
temp_blokk_sisu = None
vana_mees_joonistatud = 0
start_menu = True
lõpp_lõpp = False 


class World():
    def __init__(self, maatriks):
        self.ruudud_list = []
        
        # temp blokkide dictionary'd
        self.responsive_blocks = {}
        self.responsive_blocks_temp = {}
        self.responsive_blocks_taimers = {}
        self.responsive_blocks_up_taimers = {}
        self.responsive_blocks_activation_zones_Y= {}
        self.responsive_blocks_activation_zones_X= {}

        self.pildid = {}
        self.pildid[21] = pygame.image.load("player_6lemine.png")
        self.pildid[20] = pygame.image.load("player_alumine.png")
        self.pildid[1] = pygame.image.load("tekstuur.jpg")
        self.pildid[2] = pygame.image.load("tekstuur1.jpg")
        for pilt in self.pildid:
            self.pildid[pilt] = pygame.transform.scale(self.pildid[pilt], (RUUDU_SUURUS, RUUDU_SUURUS))

        self.maatriks = maatriks
        self.spawn(min=0, max=3, üleval=0)

    def spawn(self, min, max, üleval):
        global vana_mees_joonistatud
        # võtab maatriksist väärtuse andmed ja muudab selle
        # koordinaatidega seotud objektideks
        rea_lugeja = 0
        for rida in self.maatriks:
            veeru_lugeja = 0
            for ruut in rida:
                if vana_mees_joonistatud < 2:
                    if ruut == 20:
                        pilt = self.tagasta_pilt(ruut)
                        self.ruudud_list.append(self.loo_rect(pilt, rea_lugeja, veeru_lugeja, üleval))
                        vana_mees_joonistatud += 1
                    if ruut == 21:
                        pilt = self.tagasta_pilt(ruut)
                        self.ruudud_list.append(self.loo_rect(pilt, rea_lugeja, veeru_lugeja, üleval))
                        vana_mees_joonistatud += 1 
                if max > ruut > min:
                    # lisa_pilt tagastab ennikuna ruudule vastava pildi
                    # ja recti
                    
                    # kui ruut on temp blokk, siis ...
                    if ruut == 2:
                        pilt = self.tagasta_pilt(ruut)
                        responsive_blocks_dict_nimi= str(rea_lugeja)+ "//"+ str(veeru_lugeja)
                        activation_zone_y = (rea_lugeja+1)*RUUDU_SUURUS - (3*RUUDU_SUURUS)
                        activation_zone_x_min = ((veeru_lugeja + 1) * RUUDU_SUURUS) - RUUDU_SUURUS - RUUDU_SUURUS
                        activation_zone_x_max = ((veeru_lugeja + 1) * RUUDU_SUURUS) + RUUDU_SUURUS - RUUDU_SUURUS
                        activation_zone_x = (activation_zone_x_min, activation_zone_x_max)
                        self.responsive_blocks_activation_zones_Y[responsive_blocks_dict_nimi] = activation_zone_y
                        self.responsive_blocks_activation_zones_X[responsive_blocks_dict_nimi] = activation_zone_x
                        self.responsive_blocks_temp[responsive_blocks_dict_nimi] = "place holder"
                        self.responsive_blocks_taimers[responsive_blocks_dict_nimi] = "place holder"
                        self.responsive_blocks_up_taimers[responsive_blocks_dict_nimi] = "place holder"
                        self.responsive_blocks[responsive_blocks_dict_nimi]= self.loo_rect(pilt, rea_lugeja, veeru_lugeja, üleval)
                    else:
                        pilt = self.tagasta_pilt(ruut)
                        self.ruudud_list.append(self.loo_rect(pilt, rea_lugeja, veeru_lugeja, üleval))
                veeru_lugeja += 1
            rea_lugeja += 1

    def tagasta_pilt(self, ruut):
        return self.pildid[ruut]

    def loo_rect(self, pilt, rea_lugeja, veeru_lugeja, üleval):
        global RUUDU_SUURUS
        rect = pilt.get_rect()
        rect.x = veeru_lugeja * RUUDU_SUURUS
        rect.y = (rea_lugeja + üleval) * RUUDU_SUURUS
        return [pilt, rect]

    def joonista(self):
        for ruut in self.ruudud_list:
            window.blit(ruut[0], (ruut[1][0] + blitx, ruut[1][1] + blity))
            
        
        for ruut in self.responsive_blocks.values():
                if ruut == "TEMP GONE":
                    pass
                else:
                    window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity)) #window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity))

    def collision(self):
        global vaja_uuendada, blokk_down_timer, blokk_up_timer
        
        for midagi in self.responsive_blocks_taimers.keys():
                if self.responsive_blocks_taimers[midagi] != "place holder":
                    vaja_uuendada = True
                    blokk_down_timer = True
                    
        for midagi in self.responsive_blocks_up_taimers.keys():
                if self.responsive_blocks_taimers[midagi] != "place holder":
                    vaja_uuendada = True
                    blokk_up_timer = True
        
        if vaja_uuendada:
            for ruut in self.responsive_blocks.values():
                if ruut == "TEMP GONE":
                    pass
                else:
                    window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity)) #window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity))
                    
        if blokk_up_timer:
            for midagi in self.responsive_blocks_up_taimers.keys():
                if self.responsive_blocks_up_taimers[midagi] == "place holder":
                    pass
                else:
                    if self.responsive_blocks_up_taimers[midagi] == 10:
                        try:
                            if self.responsive_blocks[midagi] != "TEMP GONE":
                                self.responsive_blocks_temp[midagi] = self.responsive_blocks[midagi]
                                self.responsive_blocks[midagi] = "TEMP GONE"
                                self.responsive_blocks_up_taimers[midagi] = "place holder"
                                self.responsive_blocks_taimers[midagi] = 0
                                blokk_down_timer = True
                                #print(midagi)
                        except:
                            pass
                    else:
                        self.responsive_blocks_up_taimers[midagi] += 1
            
        if blokk_down_timer:
            for midagi in self.responsive_blocks_taimers.keys():
                if self.responsive_blocks_taimers[midagi] == "place holder":
                    pass
                else:
                    if self.responsive_blocks_taimers[midagi] == 100:
                        self.responsive_blocks[midagi] = self.responsive_blocks_temp[midagi]
                        self.responsive_blocks_temp[midagi] = "place holder"
                        self.responsive_blocks_taimers[midagi] = "place holder"
                        
                    else:
                        self.responsive_blocks_taimers[midagi] += 1
                        
        for midagi in self.responsive_blocks_activation_zones_Y.keys():
            if mängija_Y == self.responsive_blocks_activation_zones_Y[midagi]:
                rea_kordinaat = midagi.split("//")
                player_seisab_real = rea_kordinaat[0]
                #print(player_seisab_real, "rida")
                for midagi in self.responsive_blocks_activation_zones_X.keys():
                    if mängija_X>self.responsive_blocks_activation_zones_X[midagi][0] and mängija_X<self.responsive_blocks_activation_zones_X[midagi][1]:
                        veeru_kordinaat = midagi.split("//")
                        player_seisab_veerus=veeru_kordinaat[1]
                        #print(player_seisab_veerus, "veerg")
                        vaja_uuendada = True
                        player_asukoht = player_seisab_real + "//" + player_seisab_veerus
                        try:
                            if self.responsive_blocks_up_taimers[player_asukoht] == "place holder":
                                self.responsive_blocks_up_taimers[player_asukoht] = 0
                                blokk_up_timer = True
                        except:
                            pass

        
        for viiner in viinerid:
            for ruut in self.ruudud_list:
                if pygame.Rect.colliderect(viiner.rect, ruut[1]):
                    viinerid.pop(viinerid.index(viiner))
                    
        


class Taco(World):
    def __init__(self, maatriks, pilt):
        self.ruudud_list = []
        self.maatriks = maatriks
        self.pilt = pygame.transform.scale(pygame.image.load(pilt), (2 * RUUDU_SUURUS, 2 * RUUDU_SUURUS))
        self.pildid = [self.pilt, pygame.transform.flip(self.pilt, True, False)]
        self.asend = 0
        self.spawn(min=2, max=4, üleval=-1)
        for ruut in self.ruudud_list:
            # võib kolm korda viineriga pihta saada
            # cursed lahendus aga...
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
                    ruut[2] -= 1
                    # del viiner
                if ruut[2] == 0:
                    self.ruudud_list.pop(self.ruudud_list.index(ruut))

    def tagasta_pilt(self, ruut=None):
        return self.pilt

    def joonista(self, pilt):
        for ruut in self.ruudud_list:
            window.blit(pilt, (ruut[1].x + blitx, ruut[1].y + blity))


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
        # mingil põhjusel ei pööra pygame pilti ümber selle keskpunkti kui 45 kraadi
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
            window.blit(self.pilt, (self.rect.x + blitx, self.rect.y + blity))
            return 1

    def collision():
        taco.collision()
        world.collision()


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
        global blitx, blity, mängija_X, mängija_Y

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
        if self.kiirus_y > 25:
            self.kiirus_y = 25
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
                    
        for ruut in world.responsive_blocks.values():
            if ruut == "TEMP GONE":
                pass
            else:
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
        mängija_X = self.rect.x
        mängija_Y = self.rect.y
        
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
    global window, lahutusvõime, world, taco, viinerid, start_menu, lõpp_lõpp
    pygame.init()

    FPS = 60  # et programm töötaks olenemata riistvarast samasuguselt
    nimi = "Jiko"

    window = pygame.display.set_mode(lahutusvõime2)
    pygame.display.set_caption(nimi)

    # laeb tausta
    taust = pygame.image.load("background.png")
    taust = pygame.transform.scale(taust, lahutusvõime)
    
    # start menu pilt
    start_menu_pilt = pygame.image.load("start_menu_pilt.png")
    start_menu_pilt = pygame.transform.scale(start_menu_pilt, lahutusvõime2)
    
    # lõpu pilt
    lõpu_pilt = pygame.image.load("l6pu_pilt.png")
    lõpu_pilt = pygame.transform.scale(lõpu_pilt, lahutusvõime2)

    # loob maatirksi, kus iga element vastab mingile ruudustiku väärtusele
    # ja elemendi väärtus määrab ruudu tüübi (pildi)
    map_excel = pd.read_excel("jiko.xlsx", header=None)
    world_maatriks = map_excel.values

    world = World(world_maatriks)

    player = Player((RUUDU_SUURUS*20, lahutusvõime[0] - (RUUDU_SUURUS*10)))

    taco = Taco(maatriks=world_maatriks, pilt="mexico.png")

    viinerid = []

    fpsKell = pygame.time.Clock()  # loob objekti aja jälgimiseks
    run = True
    while run:
        
        if start_menu:
            window.blit(start_menu_pilt, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x or event.key == pygame.K_q:
                        run = False
                    if event.key == pygame.K_e:
                        start_menu = False
            pygame.display.update()
                        
        elif lõpp_lõpp:
            window.blit(lõpu_pilt, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x or event.key == pygame.K_q:
                        run = False
                    if event.key == pygame.K_e:
                        lõpp_lõpp = False
            pygame.display.update()
        
        else:

            # lisab pildi aknas kuvatavale frame'ile
            # järjekord oluline !
            window.blit(taust, (0 + blitx, 0 + blity))
            # ruudustik()  # loob ruudusitku

            world.joonista()
            taco.flip()
            for viiner in viinerid:
                if viiner.liikumine() == 0:
                    viinerid.pop(viinerid.index(viiner))
                    del viiner
            Viiner.collision()

            player.uuenda()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_x or event.key == pygame.K_q:
                        run = False
                    if event.key == pygame.K_c:
                        # prindib player'i koordinaadid ja maatriksi elemendi (rida, veerg)
                        #print(vaja_uuendada, blokk_down_timer, blokk_up_timer)
                        print(f"x: {player.rect.x}, y: {player.rect.y}, maatriks r:{int(player.rect.y / RUUDU_SUURUS)}, v:{int(player.rect.x / RUUDU_SUURUS)}")
                    if event.key == pygame.K_e:
                        if mängija_X == 120 and mängija_Y == 90:
                            lõpp_lõpp = True 
                    

            pygame.display.update()  # värksendab aknas kuvatavat frame'i

            # pärast määrata muutuja väärtuseks, et liikumine toimuks ühtselt?
            fpsKell.tick(FPS)  # uuendab 'kella' väärtust

    pygame.quit()


if __name__ == "__main__":
    main()
