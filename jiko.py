import numpy
import pygame

"""
TODO juurde
- level design
- scaling

TODO parandada
- collison window'i äärtega

"""

ruudud = 40  # kui mitmeks ruuduks jagame
ruudu_suurus = 30 # küljepikkus pikslites
pikkus = ruudud * ruudu_suurus
laius = pikkus
lahutusvõime = (pikkus, laius)
lahutusvõime2 = (laius-ruudu_suurus*30, pikkus-ruudu_suurus*30)
#lahutusvõime2=(laius, pikkus)
mängija_teleport_sihtkoht=((ruudu_suurus*20, lahutusvõime[0] - (ruudu_suurus*6)))#player = Player((ruudu_suurus*20, lahutusvõime[0] - (ruudu_suurus*6)))

#liigutab kaamerat vastaval player'i liikumisele
blitx=0-ruudu_suurus*15
blity=0-ruudu_suurus*29

sammud_loendur = 0
on_maas = False
vaja_uuendada = False
mängija_X = 0
mängija_Y = 0
blokk_up_timer = False
blokk_up_timer_loendur = 0
temp_blokk_sisu = None 

class World():
    # ruutude piltide ja väärtuste jaoks dictionary
    # vb peaks lahenduse üle vaatama, aga prg töötab
    pildid = {
        1: "",
        2: "",
        3: ""
    }

    def lisa_pilt(tüüp, rea_lugeja, veeru_lugeja):
        global ruudu_suurus
        img = World.pildid[tüüp]
        img = img[0]
        img = pygame.transform.scale(img, (ruudu_suurus, ruudu_suurus))
        # loob recti (default asukoht on (0,0))
        img_rect = img.get_rect()
        # rect on pygame'i objekt (risttahukas), mis sisaldab koordinaate
        img_rect.x = veeru_lugeja * ruudu_suurus
        img_rect.y = rea_lugeja * ruudu_suurus
        return (img, img_rect)

    def __init__(self, maatriks):
        self.maatriks=maatriks
        self.ruudud_list = []
        self.responsive_blocks = {}
        self.responsive_blocks_temp = {}
        self.responsive_blocks_taimers = {}
        self.responsive_blocks_activation_zones_Y= {}
        self.responsive_blocks_activation_zones_X= {}
        tekstuur1 = pygame.image.load("tekstuur.jpg") #TELLISKIVID
        tekstuur2 = pygame.image.load("tekstuur1.jpg") #LEHED
        tekstuur5 = pygame.image.load("tekstuur1.jpg") #MITTE MUUTUVAD LEHED
        npc0_ülemine = pygame.transform.flip(pygame.image.load("player_6lemine.png"), True, False) #VANAMEES ÜLAKEHA
        npc0_alumine = pygame.transform.flip(pygame.image.load("player_alumine.png"), True, False) #VANAMEES ALAKEHA
        
        #World.pildid[] = [tekstuur, <kas ta on taimeriga kadumine(True or False)> ]
        
        World.pildid[1] = [tekstuur1, False ] 
        World.pildid[2] = [tekstuur2, True ]
        World.pildid[3] = [npc0_ülemine, False ]
        World.pildid[4] = [npc0_alumine, False ]
        World.pildid[5] = [tekstuur5, False ]

        """
        tekstuur2 = pygame.image.load()
        ...
        """
        # võtab maatriksist väärtuse andmed ja muudab selle
        # koordinaatidega seotud objektideks
        rea_lugeja = 0
        for rida in maatriks:
            veeru_lugeja = 0
            for ruut in rida:
                if ruut != 0:
                    #kontrollib kas permanent ruut või 'interactable' ruut
                    
                    if ruut == 2:
                        ruut = World.lisa_pilt(ruut, rea_lugeja, veeru_lugeja)
                        responsive_blocks_dict_nimi= str(rea_lugeja)+ "//"+ str(veeru_lugeja)
                        activation_zone_y = (rea_lugeja+1)*30 - (3*30)
                        activation_zone_x_min = ((veeru_lugeja + 1) * 30) - 30 - 30
                        activation_zone_x_max = ((veeru_lugeja + 1) * 30) + 30 - 30
                        activation_zone_x = (activation_zone_x_min, activation_zone_x_max)
                        self.responsive_blocks_activation_zones_Y[responsive_blocks_dict_nimi] = activation_zone_y
                        self.responsive_blocks_activation_zones_X[responsive_blocks_dict_nimi] = activation_zone_x
                        self.responsive_blocks_temp[responsive_blocks_dict_nimi] = "place holder"
                        self.responsive_blocks[responsive_blocks_dict_nimi]= ruut
                        self.responsive_blocks_taimers[responsive_blocks_dict_nimi] = "place holder"
                        
                    else:
                        ruut = World.lisa_pilt(ruut, rea_lugeja, veeru_lugeja)
                        self.ruudud_list.append(ruut)
                        
                veeru_lugeja += 1
            rea_lugeja += 1
            
        pass
    
    #maailma uuendaja
    def uuenda(self):
        global vaja_uuendada, blokk_up_timer
        
        for midagi in self.responsive_blocks_taimers.keys():
                if self.responsive_blocks_taimers[midagi] != "place holder":
                    vaja_uuendada = True
                    blokk_up_timer = True 
        
        if vaja_uuendada:
            for ruut in self.responsive_blocks.values():
                if ruut == "TEMP GONE":
                    pass
                else:
                    window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity)) #window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity))
        
        """
        activation_zone_y = (rea_lugeja+1)*30 - (2*30)
        activation_zone_x_min = ((veeru_lugeja + 1) * 30) - 30
        activation_zone_x_max = ((veeru_lugeja + 1) * 30) + 30
        activation_zone_x = (activation_zone_x_min, activation_zone_x_max)
        activation_zone = (activation_zone_y, activation_zone_x)
        self.responsive_blocks_activation_zones[responsive_blocks_dict_nimi] = activation_zone
        """
        
        
        # kui mängija on aktiveerimis tsoonis, siis:
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
                        #muuda alumine augu muru blokk õhuks ajutiselt
                        try:
                            if self.responsive_blocks[player_asukoht] != "TEMP GONE":
                                self.responsive_blocks_temp[player_asukoht] = self.responsive_blocks[player_asukoht]
                                self.responsive_blocks[player_asukoht] = "TEMP GONE"
                                self.responsive_blocks_taimers[player_asukoht] = 0
                                blokk_up_timer = True
                                print(player_asukoht)
                                #print("vaja_uuendada = True")
                        except:
                            pass
                        
        
            
        if blokk_up_timer:
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
                        
                            
            
            
        
    def joonista(self):
        for ruut in self.ruudud_list:
            window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity)) #window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity))
        for ruut in self.responsive_blocks.values():
                if ruut == "TEMP GONE":
                    pass
                else:
                    window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity)) #window.blit(ruut[0], (ruut[1][0]+blitx, ruut[1][1]+blity))
        pass
        


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
        self.rect = self.img_parem.get_rect()
        self.rect.x = asukoht[0]
        self.rect.y = asukoht[1]
        laius = self.img_parem.get_width()
        pikkus = self.img_vasak.get_height()
        self.suurus = (laius, pikkus)
        self.kiirus_y = 0
        self.suund = 0
        
     

    def uuenda(self):
        global sammud_loendur, on_maas, blitx, blity, mängija_X, mängija_Y
        
        #player character sammude animation frames
        sammud_frames_parem=[self.img_samm_parem, self.img_samm_parem, self.img_samm_parem,self.img_samm_parem, self.img_samm_parem, self.img_samm_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_samm_parem2, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem, self.img_parem]
        sammud_frames_vasak=[self.img_samm_vasak, self.img_samm_vasak, self.img_samm_vasak,self.img_samm_vasak, self.img_samm_vasak, self.img_samm_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_samm_vasak2, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak, self.img_vasak]
        dx = 0
        dy = 0
        liikumine=False
        

        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_SPACE]) and self.hüpe is False and on_maas is True:
            self.kiirus_y = -20
            self.hüpe = True
            on_maas=False
        if key[pygame.K_w] is False and key[pygame.K_SPACE] is False:
            self.hüpe = False
        if key[pygame.K_a]:
            dx -= 10
            self.suund = -1
            liikumine=True 
        if key[pygame.K_d]:
            dx += 10
            self.suund = 1
            liikumine=True

        self.kiirus_y += 1
        if self.kiirus_y > 10:
            self.vel_y = 10
        dy += self.kiirus_y

        # collision detect for perma bloks
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
                    on_maas=True
                    
        # collision detect for interactable bloks
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
                        on_maas=True
                    

        # uuendab mängija koordinaate ja kaamera (tegelt maailma) asukohta
        self.rect.x += dx
        self.rect.y += dy
        mängija_X = self.rect.x
        mängija_Y = self.rect.y
        #print(f"X={self.rect.x} Y={self.rect.y}")

        blitx = blitx -dx  
        blity = blity -dy

        # joonistab mängija ekraanile
        if self.suund == 1:
            img = self.img_parem
            if liikumine==True :
                if sammud_loendur==23:
                    sammud_loendur=0
                img = sammud_frames_parem[sammud_loendur]
                sammud_loendur+=1
        else:
            img = self.img_vasak
            if liikumine==True :
                if sammud_loendur==23:
                    sammud_loendur=0
                img = sammud_frames_vasak[sammud_loendur]
                sammud_loendur+=1
                
        window.blit(img, (self.rect[0]+blitx, self.rect[1]+blity))
        #pygame.draw.rect(window, (0, 255, 0 ), self.rect, 2)
        
# joonistab ruudustiku välja
def ruudustik():
    global window, ruudu_suurus, ruudud, lahutusvõime
    for i in range(ruudud):
        pygame.draw.line(window, (255, 255, 255), (i * ruudu_suurus, 0),
                         (i * ruudu_suurus, lahutusvõime[1]))
        pygame.draw.line(window, (255, 255, 255), (0, i * ruudu_suurus),
                         (lahutusvõime[0], i * ruudu_suurus))
        
# uuendaja kõigile
def Uuenda_kõik(mängija, maailm):
    Player.uuenda(mängija)
    World.uuenda(maailm)
    


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
    world_maatriks[0:3] = 5  
    world_maatriks[1:39, 0:3] = 5
    world_maatriks[1:39, 36:40] = 1
    world_maatriks[36:40] = 1
    world_maatriks[32, 3:28] = 2
    world_maatriks[28, 6:36] = 2
    world_maatriks[35, 30:36] = 1
    world_maatriks[33, 33] = 3
    world_maatriks[34, 33] = 4
    world = World(world_maatriks)
    
    
    player = Player((ruudu_suurus*20, lahutusvõime[0] - (ruudu_suurus*6)))

    fpsKell = pygame.time.Clock()  # loob objekti aja jälgimiseks
    run = True
    while run:

        # lisab pildi aknas kuvatavale frame'ile
        # järjekord oluline !
        window.blit(taust, (0+blitx, 0+blity))
        # window.blit(man, (0, 600))

        #ruudustik()  # loob ruudusitku

        World.joonista(world)  # joonistab tekstuuriga ruudud ekraanile
        
        Uuenda_kõik(player, world) # uuendab kõiki asju

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    run = False
                elif event.key == pygame.K_e:
                    print("vajutati e")
                

        pygame.display.update()  # värksendab aknas kuvatavat frame'i

        # pärast määrata muutuja väärtuseks, et liikumine toimuks ühtselt?
        fpsKell.tick(FPS)  # uuendab 'kella' väärtust

    
    pygame.quit()


if __name__ == "__main__":
    main()

