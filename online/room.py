import pygame
import sys
from offline.button import Button
from image import button,title_photo

def room(clock,screen,FPS,MYFONT):
    start = Button(200,300,200,80,button,"start",MYFONT,0,0,0,screen)
    quit = Button(200,420,200,80,button,"quit",MYFONT,0,0,0,screen)
    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.click(pygame.mouse.get_pos()):
                    return "start"
                elif quit.click(pygame.mouse.get_pos()):
                    return "quit"
        start.draw()
        quit.draw()
        pygame.display.update()