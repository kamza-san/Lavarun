import pygame
import sys
from offline.button import Button
from image import button,title_photo,quit_button1,quit_button2,button2

def level_set(clock,screen,FPS,MYFONT,level):
    hard = Button(200,300,200,80,button,"hard",MYFONT,0,0,0,screen)
    normal = Button(200,420,200,80,button,"normal",MYFONT,0,0,0,screen)
    easy = Button(200,540,200,80,button,"easy",MYFONT,0,0,0,screen)
    quit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hard.click(pygame.mouse.get_pos()):
                    return "hard"
                elif normal.click(pygame.mouse.get_pos()):
                    return "normal"
                elif easy.click(pygame.mouse.get_pos()):
                    return "easy"
                elif quit.click(pygame.mouse.get_pos()):
                    return level
        hard.image = button
        normal.image = button
        easy.image = button
        quit.image = quit_button1
        if hard.click(pygame.mouse.get_pos()):
            hard.image = button2
        elif normal.click(pygame.mouse.get_pos()):
            normal.image = button2
        elif easy.click(pygame.mouse.get_pos()):
            easy.image = button2
        elif quit.click(pygame.mouse.get_pos()):
            quit.image = quit_button2
        hard.draw()
        normal.draw()
        easy.draw()
        quit.draw()
        pygame.display.update()