import pygame
import sys
from offline.button import Button
from offline.textbox import Textbox
from image import button,title_photo,quit_button1,button2,quit_button2

def online(clock,screen,FPS,MYFONT):
    host = Textbox(200,300,200,80,button,"ip",MYFONT,0,0,0,screen)
    quit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    matching = Button(200,420,200,80,button,"매칭",MYFONT,0,0,0,screen)
    writing = Button(200,100,200,80,button,"입력중...",MYFONT,0,0,0,screen)
    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit.click(pygame.mouse.get_pos()):
                    return "title"
                elif host.click(pygame.mouse.get_pos()):
                    if host.text == "ip":
                        host.text = ""
                    while True:
                        writing.draw()
                        host.draw()
                        quit.draw()
                        pygame.display.update()
                        result = host.input()
                        if result == "end":
                            if host.text == "":
                                host.text = "ip"
                            break
                        if result == "del":
                            host.text = host.text[:-1]
                        else:
                            host.text += result
                elif matching.click(pygame.mouse.get_pos()):
                    return host.text
        host.image = button
        quit.image = quit_button1
        matching.image = button
        if host.click(pygame.mouse.get_pos()):
            host.image = button2
        elif quit.click(pygame.mouse.get_pos()):
            quit.image = quit_button2
        elif matching.click(pygame.mouse.get_pos()):
            matching.image = button2        
        host.draw()
        quit.draw()
        matching.draw()
        pygame.display.update()