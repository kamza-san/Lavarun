import pygame
import sys
from offline.button import Button
from image import button,title_photo,quit_button1,button2,quit_button2
from offline.textbox import Textbox
import json


def record(clock,screen,FPS,MYFONT):
    MYFONT1 = MYFONT
    hard = Button(200,420,200,80,button,"hard:0",MYFONT1,0,0,0,screen)
    normal = Button(200,540,200,80,button,"normal:0",MYFONT1,0,0,0,screen)
    easy = Button(200,660,200,80,button,"easy:0",MYFONT1,0,0,0,screen)
    quit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    user_name = "player"
    def drawing():
        hard.draw()
        normal.draw()
        easy.draw()
        quit.draw()
        pygame.display.update()

    with open("./data.json","r",encoding="utf-8")as f:
        dict = json.load(f)
    hard.text = "hard:"+str(dict["player"]["hard"])
    normal.text = "normal:"+str(dict["player"]["normal"])
    easy.text = "easy:"+str(dict["player"]["easy"])
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
        quit.image = quit_button1
        if quit.click(pygame.mouse.get_pos()):
            quit.image = quit_button2
        drawing()