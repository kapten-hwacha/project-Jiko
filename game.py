import pygame

pygame.init()

SW=747
SH=656

screen= pygame.display.set_mode((SW, SH))
pygame.display.set_caption('Greetings fella')

image = pygame.image.load(r'whiteman.jpg')


run=True
while run:
    screen.fill((255, 255, 255))
    screen.blit(image, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False
        if event.type == pygame.KEYDOWN:
            print("key has been pressed")
    pygame.display.update()        
            
    
pygame.quit()
            