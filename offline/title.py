import pygame
import sys
import random
from offline.button import Button
from offline.textbox import Textbox
from offline.image import button,title_photo,button2,setting_button1,setting_button2,quit_button1,quit_button2,small_button,small_button2
import threading

def title(clock,screen,FPS,MYFONT,level):
    gamestart = Button(200,300,200,80,button,"게임시작",MYFONT,0,0,0,screen)
    gameonline = Button(200,540,200,80,button,"온라인",MYFONT,0,0,0,screen)
    setting = Button(20,700,80,80,setting_button1,"",MYFONT,0,0,0,screen)
    gamequit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    level_setting = Button(200,420,200,80,button,"난이도:"+level,MYFONT,0,0,0,screen)
    rank = Button(200,660,200,80,button,"최고기록",MYFONT,0,0,0,screen)
    tutorial = Button(20,650,100,40,small_button,"튜토리얼",MYFONT,0,0,0,screen)
    def drawing():
        gamestart.draw()
        gameonline.draw()
        setting.draw()
        gamequit.draw()
        level_setting.draw()
        rank.draw()
        tutorial.draw()
        pygame.display.update()
    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if gamestart.click(pygame.mouse.get_pos()):
                    return "game"
                elif gameonline.click(pygame.mouse.get_pos()):
                    return "online"
                elif setting.click(pygame.mouse.get_pos()):
                    return "setting"
                elif gamequit.click(pygame.mouse.get_pos()):
                    pygame.quit()
                    sys.exit()
                elif level_setting.click(pygame.mouse.get_pos()):
                    return "level_setting"
                elif rank.click(pygame.mouse.get_pos()):
                    return "record"
                elif tutorial.click(pygame.mouse.get_pos()):
                    return "tutorial"
        gamestart.image = button
        gameonline.image = button
        setting.image = setting_button1
        gamequit.image = quit_button1
        level_setting.image = button
        rank.image = button
        tutorial.image = small_button
        if gamestart.click(pygame.mouse.get_pos()):
            gamestart.image = button2
        elif gameonline.click(pygame.mouse.get_pos()):
            gameonline.image = button2
        elif setting.click(pygame.mouse.get_pos()):
            setting.image = setting_button2
        elif gamequit.click(pygame.mouse.get_pos()):
            gamequit.image = quit_button2
        elif level_setting.click(pygame.mouse.get_pos()):
            level_setting.image = button2
        elif rank.click(pygame.mouse.get_pos()):
            rank.image = button2
        elif tutorial.click(pygame.mouse.get_pos()):
            tutorial.image = small_button2
        drawing()