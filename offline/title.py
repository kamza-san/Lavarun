import pygame
import sys
import random
from offline.button import Button
from offline.textbox import Textbox
from eximage.image import button,title_photo,button2,setting_button1,setting_button2,quit_button1,quit_button2,tip
import threading

def title(clock,screen,FPS,MYFONT,level):
    gamestart = Button(200,300,200,80,button,"게임시작",MYFONT,0,0,0,screen)
    gameonline = Button(200,540,200,80,button,"온라인",MYFONT,0,0,0,screen)
    setting = Button(20,700,80,80,setting_button1,"",MYFONT,0,0,0,screen)
    gamequit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    level_setting = Button(200,420,200,80,button,level,MYFONT,0,0,0,screen)
    rank = Button(200,660,200,80,button,"최고기록",MYFONT,0,0,0,screen)
    challenge = Button(380,120,200,80,button,"도전과제",MYFONT,0,0,0,screen)
    hangul = Button(185,210,240,80,tip,"튜토리얼: 설정에서 조작법확인과 조작법변경을 할수있습니다",MYFONT,0,0,0,screen)
    def drawing():
        gamestart.draw()
        gameonline.draw()
        setting.draw()
        gamequit.draw()
        level_setting.draw()
        rank.draw()
        challenge.draw()
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
        gamestart.image = button
        gameonline.image = button
        setting.image = setting_button1
        gamequit.image = quit_button1
        level_setting.image = button
        rank.image = button
        challenge.image = button
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
        elif challenge.click(pygame.mouse.get_pos()):
            challenge.image = button2
        hangul.draw()
        drawing()