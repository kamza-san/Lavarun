import pygame
import sys
from offline.button import Button
from offline.textbox import Textbox
from image import button,title_photo,button2,setting_button1,setting_button2,quit_button1,quit_button2

def setting(clock,screen,FPS,MYFONT):
    with open("set.json","r") as f:
        data = f.read()
        data = data.replace("{","").replace("}","").replace('"',"").split(",")
        right_num = int(data[0].split(":")[1])
        left_num = int(data[1].split(":")[1])
        jump_num = int(data[2].split(":")[1])
        down_num = int(data[3].split(":")[1])
    right = Button(200,300,200,80,button,"right : "+pygame.key.name(right_num),MYFONT,0,0,0,screen)
    left = Button(200,420,200,80,button,"left : "+pygame.key.name(left_num),MYFONT,0,0,0,screen)
    jump = Button(200,540,200,80,button,"jump : "+pygame.key.name(jump_num),MYFONT,0,0,0,screen)
    down = Button(200,660,200,80,button,"down : "+pygame.key.name(down_num),MYFONT,0,0,0,screen)
    gamequit = Button(500,20,80,80,quit_button1,"",MYFONT,0,0,0,screen)
    click = Button(200,100,200,80,button,"press the key",MYFONT,0,0,0,screen)
    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if right.click(pygame.mouse.get_pos()):
                    out = True
                    while out:
                        click.draw()
                        right.draw()
                        left.draw()
                        jump.draw()
                        down.draw()
                        gamequit.draw()
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                right.text = "right : "+event.unicode
                                right_num = event.key
                                out = False
                                break          
                elif left.click(pygame.mouse.get_pos()):
                    out = True
                    while out:
                        click.draw()
                        right.draw()
                        left.draw()
                        jump.draw()
                        down.draw()
                        gamequit.draw()
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                left.text = "left : "+event.unicode
                                left_num = event.key
                                out = False
                                break 
                elif jump.click(pygame.mouse.get_pos()):
                    out = True
                    while out:
                        click.draw()
                        right.draw()
                        left.draw()
                        jump.draw()
                        down.draw()
                        gamequit.draw()
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                jump.text = "jump : "+event.unicode
                                jump_num = event.key
                                out = False
                                break 
                elif down.click(pygame.mouse.get_pos()):
                    out = True
                    while out:
                        click.draw()
                        right.draw()
                        left.draw()
                        jump.draw()
                        down.draw()
                        gamequit.draw()
                        pygame.display.update()
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                down.text = "down : "+event.unicode
                                down_num = event.key
                                out = False
                                break 
                elif gamequit.click(pygame.mouse.get_pos()):
                    with open("set.json","w") as f:
                        f.write('{"right":'+str(right_num)+',"left":'+str(left_num)+',"jump":'+str(jump_num)+',"down":'+str(down_num)+'}')
                    return "title"
        right.image = button
        left.image = button
        jump.image = button
        down.image = button
        gamequit.image = quit_button1
        if right.click(pygame.mouse.get_pos()):
            right.image = button2
        elif left.click(pygame.mouse.get_pos()):
            left.image = button2
        elif jump.click(pygame.mouse.get_pos()):
            jump.image = button2
        elif down.click(pygame.mouse.get_pos()):
            down.image = button2
        elif gamequit.click(pygame.mouse.get_pos()):
            gamequit.image = quit_button2
        right.draw()
        left.draw()
        jump.draw()
        down.draw()
        gamequit.draw()
        pygame.display.update()