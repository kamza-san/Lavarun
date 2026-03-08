import pygame
import sys
import time
import random
from pygame.locals import *
from offline.player import Player
from offline.object import Object
from offline.button import Button
from offline.textbox import Textbox
from . import map
import json
from offline.map import objects
from image import button,wait_ground,scoreimage,background,player_right,player_left,button2
from pathlib import Path


def player_gravity(a):
    for obj in objects:
        obj.up(a)
    lava.up(a)
    global high
    global m
    global score
    high += a
    m += a
    score += a

def game(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,level):
    with open("set.json","r") as f:
        data = f.read()
        data = data.replace("{","").replace("}","").replace('"',"").split(",")
        right_num = int(data[0].split(":")[1])
        left_num = int(data[1].split(":")[1])
        jump_num = int(data[2].split(":")[1])
        down_num = int(data[3].split(":")[1])
    if level == "easy":
        speed = -1
    elif level == "normal":
        speed = -2
    else:
        speed = -4
    out = False
    jump_sound = pygame.mixer.Sound("./eximage/jump.mp3")
    while True:
        screen.blit(wait_ground,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                out = True
        if out:
            break
        pygame.display.update()
        clock.tick(FPS)
    global player
    global lava
    global score
    global high
    global m
    score = -10
    player = Player(MAX_WIDTH//2-30,MAX_HEIGHT-250,1,player_right,player_left,right_num,left_num,screen)
    objects.append(Object(0, 600, 600, 300, 255,255,0,screen))
    lava = Object(0,800,600,800,255,127,0,screen)
    scoreboard = Button(20,20,200,80,scoreimage,score,MYFONT,153,217,234,screen)
    if_jump = False
    second_jump = False
    high = -800
    m = 600
    jump_speed = 5
    while True:
        right = True
        left = True
        high = high % 1600 
        screen.blit(background,(0,high+1600))
        screen.blit(background,(0,high))
        screen.blit(background,(0,high-1600))
        if jump_speed >= -20:
            jump_speed -= 1
        for obj in objects: 
            if map.touch_side(player,obj) == "top" or map.touch_near(player,obj) == "top" or (map.touch_side(player,obj) == "left" and jump_speed < 0) or (map.touch_side(player,obj) == "right" and jump_speed < 0):
                jump_speed = 0
                if_jump = True
                second_jump = False
                a = player.y - obj.y + 60
                for obj in objects:
                    obj.up(a)
                lava.up(a)
                high += a
                m += a
                score += a
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == jump_num:
                    if if_jump:
                        jump_speed = 25
                        if_jump = False
                        second_jump = True
                        jump_sound.play()
                    elif second_jump:
                        jump_speed = 20
                        second_jump = False
                        jump_sound.play()
                if event.key == down_num:
                    jump_speed = -20
        pressed_keys = pygame.key.get_pressed()
        player_gravity(jump_speed)
        for obj in objects:
            if map.touch_near(player,obj) == "right":
                left = False
            elif map.touch_near(player,obj) == "left":
                right = False
            elif map.touch(player,obj) and jump_speed > 0:
                jump_speed = 0
                a = player.y - obj.y - obj.si_y
                for obj in objects:
                    obj.up(a)
                lava.up(a)
                high += a
                m += a
                score += a     
                break
        player.move(pressed_keys,right,left)
        if lava.y >= 750:
            lava.up(speed-6)
        else:
            lava.up(speed)
        if player.get_rect().colliderect(lava.get_rect()):
            with open("./data.json","r",encoding="utf-8") as f:
                dict = json.load(f)
            if score > dict["player"][level]:
                dict["player"][level] = score
                with open("./data.json","w",encoding="utf-8")as f:
                    json.dump(dict, f, ensure_ascii=False,indent=4)
            restart = Button(200,300,200,80,button,"재시작(R)",MYFONT,0,0,0,screen)
            menu = Button(200,420,200,80,button,"타이틀로",MYFONT,0,0,0,screen)
            while True:
                screen.blit(background,(0,high+1600))
                screen.blit(background,(0,high))
                screen.blit(background,(0,high-1600))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart.click(pygame.mouse.get_pos()):
                            objects.clear()
                            return "game"
                        elif menu.click(pygame.mouse.get_pos()):
                            objects.clear()
                            return "title"
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            objects.clear()
                            return "game"
                restart.image = button
                menu.image = button
                if restart.click(pygame.mouse.get_pos()):
                    restart.image = button2
                elif menu.click(pygame.mouse.get_pos()):
                    menu.image = button2
                for obj in objects:
                    obj.draw()
                player.draw()
                lava.draw()
                scoreboard.draw()
                restart.draw()
                menu.draw()
                pygame.display.update()        
        if lava.y <= objects[0].y:
            del objects[0]
        if m >= 0:
            m -= random.randint(120,180)
            map.generate_map(screen, m)
        scoreboard.text = score
        for obj in objects:
            obj.draw()
        player.draw()
        lava.draw()
        scoreboard.draw()
        pygame.display.update()
        clock.tick(FPS)