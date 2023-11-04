import numpy
import pygame

ruudud = 50  # küljepikkus pikslites
ruudu_suurus = 32
pikkus = ruudud * ruudu_suurus
laius = pikkus
lahutusvõime = (pikkus, laius)


class World():

    # ruutude piltide ja väärtuste jaoks dictionary
    pildid = {
        1: pygame.image.load("tekstuur.jpg")
        # 2: ""
        # 3: ""
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
        # tekstuur1 = 
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
                if ruut == 0:
                    continue
                else:
                    ruut = World.lisa_pilt(ruut, rea_lugeja, veeru_lugeja)
                    self.ruudud_list.append(ruut)
                veeru_lugeja += 1
            rea_lugeja += 1
        pass

    def draw(self):
        for ruut in self.ruudud_list:
            window.blit(ruut[0], ruut[1])
        pass


class Player():
    pass


# joonistab ruudustiku välja
def ruudustik():
    global window, ruudu_suurus, ruudud, lahutusvõime
    for i in range(ruudud):
        pygame.draw.line(window, (255, 255, 255), (i * ruudu_suurus, 0),
                         (i * ruudu_suurus, lahutusvõime[1]))
        pygame.draw.line(window, (255, 255, 255), (0, i * ruudu_suurus),
                         (lahutusvõime[0], i * ruudu_suurus))


"""
TODO

- scaling


"""


def main():
    global window, lahutusvõime
    pygame.init()

    FPS = 60  # et programm töötaks olenemata riistvarast samasuguselt
    nimi = "Jiko"

    window = pygame.display.set_mode(lahutusvõime)
    pygame.display.set_caption(nimi)

    # loob maatirksi, kus iga element vastab mingile ruudustiku väärtusele
    # ja elemendi väärtus määrab ruudu tüübi (pildi)
    world_maatriks = numpy.zeros((ruudud, ruudud))
    world_maatriks[20] = 1  # testimiseks
    world = World(world_maatriks)
    print(world.ruudud_list)

    # laeb spritide pildid
    taust = pygame.image.load("background.png")
    taust = pygame.transform.scale(taust, lahutusvõime)
    # man = pygame.image.load("whiteman.jpg")

    fpsKell = pygame.time.Clock()  # loob objekti aja jälgimiseks
    run = True
    while run:

        # lisab pildi aknas kuvatavale frame'ile
        # järjekord oluline !
        window.blit(taust, (0, 0))
        # window.blit(man, (0, 600))

        ruudustik()  # loob ruudusitku

        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                run = False

        pygame.display.update()  # värksendab aknas kuvatavat frame'i

        # pärast määrata muutuja väärtuseks, et liikumine toimuks ühtselt?
        fpsKell.tick(FPS)  # uuendab 'kella' väärtust

    pygame.quit()


if __name__ == "__main__":
    main()
