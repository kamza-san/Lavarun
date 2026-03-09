import pygame
import sys
from offline.button import Button
from offline.textbox import Textbox
from eximage.image import tutorial,quit_button1,quit_button2

def tutorial_screen(clock,screen,FPS,MYFONT):
    quit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    while True:    
        clock.tick(FPS)
        screen.blit(tutorial,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit.click(pygame.mouse.get_pos()):
                    return "title"
        quit.image = quit_button1
        if quit.click(pygame.mouse.get_pos()):
            quit.image = quit_button2        
        quit.draw()
        pygame.display.update()