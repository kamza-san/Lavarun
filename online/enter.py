import pygame
import socket
import threading
import sys
import time
import random
import socket
from pygame.locals import *
from offline.player import Player
from offline.object import Object
from offline.button import Button
from offline.map import generate_map,touch,touch_side,touch_near
import json
from offline.image import scoreimage,background,player_right,player_left,button,title_photo,button2

def receive_messages(sock):
    global game_overing
    global map_data
    global score

    buffer = ""

    while True:
        try:
            data = sock.recv(1024).decode()
            if not data:
                break

            buffer += data

            while "\n" in buffer:
                msg, buffer = buffer.split("\n", 1)

                data = msg.split(",")

                if data[0] == "move":
                    enemy.x = int(data[1])
                    enemy.y = 550 + score - int(data[2])

                elif data[0] == "win":
                    game_overing = "lose"

                elif data[0] == "lose":
                    game_overing = "win"

                elif data[0] == "obj":
                    map_data = data

        except:
            pass

def wait(clock,screen,FPS,MYFONT):
    
    text = Button(200,300,200,80,button,"3",MYFONT,0,0,0,screen)
    timing = 0

    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                client.close()
                pygame.quit()
                sys.exit()
        if timing >= 50:
            if text.text == "3":
                text.text = "2"
            elif text.text == "2":
                text.text = "1"
            else:
                return
            timing = 0
        timing += 1
        text.draw()
        pygame.display.update()

def enter(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,host,port):
    
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, int(port)))
    except Exception as e:
        pygame.quit()
        sys.exit()

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()

    global map_data
    map_data = None
    global game_overing
    game_overing = ""

    wait(clock,screen,FPS,MYFONT)

    while map_data is None:
        time.sleep(0.01)

    game(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT)

    client.close()
    return "online"

def player_gravity(a):
    for obj in objects:
        obj.up(a)
    global high
    global score
    high += a
    score += a

def say(type_):
    if type_ == "move":
        global player
        global score
        msg = "move,"+str(player.x)+","+str(score)+"\n"
        try:
            client.send(msg.encode())
        except KeyboardInterrupt:
            client.close()
            pygame.quit()
            sys.exit()
            
def map_gen(objs,screen):
    for i in range(100):
        objects.append(Object(int(objs[1+i*2]), int(objs[2+i*2]), 100, 40, 180,180,40,screen))
            
def game_over(fight,MYFONT,screen):
    if fight == "":
        return ""
    win_lose = Button(200,300,200,80,button,"",MYFONT,0,0,0,screen)
    ok = Button(200,420,200,80,button,"타이틀로",MYFONT,0,0,0,screen)
    if fight == "win":
        win_lose.text = "win"
    else:
        win_lose.text = "lose"
    while True:
        screen.blit(background,(0,high+1600))
        screen.blit(background,(0,high))
        screen.blit(background,(0,high-1600))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ok.click(pygame.mouse.get_pos()):
                    return "title"
        for obj in objects:
            obj.draw()
        enemy.draw()
        player.draw()
        scoreboard.draw()
        win_lose.draw()
        ok.draw()
        pygame.display.update()
                            

def game(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT):
    global objects
    objects = []
    map_gen(map_data,screen)
    with open("file/set.json","r") as f:
        data = f.read()
        data = data.replace("{","").replace("}","").replace('"',"").split(",")
        right_num = int(data[0].split(":")[1])
        left_num = int(data[1].split(":")[1])
        jump_num = int(data[2].split(":")[1])
        down_num = int(data[3].split(":")[1])  
    global player
    global score
    global high
    global enemy
    global game_overing
    global scoreboard
    jump_sound = pygame.mixer.Sound("eximage/jump.mp3")
    enemy = Player(MAX_WIDTH//2-30,MAX_HEIGHT-250,1,player_right,player_left,right_num,left_num,screen)
    score = -10
    player = Player(MAX_WIDTH//2-30,MAX_HEIGHT-250,1,player_right,player_left,right_num,left_num,screen)
    objects.append(Object(0, 600, 600, 300, 180,180,0,screen))
    scoreboard = Button(40,40,200,80,scoreimage,str(score)+"m",MYFONT,153,217,234,screen)
    if_jump = False
    second_jump = False
    high = -800
    jump_speed = 5
    while True:
        say("move")
        right = True
        left = True
        high = high % 1600 
        screen.blit(background,(0,high+1600))
        screen.blit(background,(0,high))
        screen.blit(background,(0,high-1600))
        clock.tick(FPS)
        if jump_speed >= -20:
            jump_speed -= 1
        for obj in objects: 
            if touch_side(player,obj) == "top" or touch_near(player,obj) == "top" or (touch_side(player,obj) == "left" and jump_speed < 0) or (touch_side(player,obj) == "right" and jump_speed < 0):
                jump_speed = 0
                if_jump = True
                second_jump = False
                a = player.y - obj.y + 60
                for obj in objects:
                    obj.up(a)
                high += a
                score += a
                break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
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
            if touch_near(player,obj) == "right":
                left = False
            elif touch_near(player,obj) == "left":
                right = False
            elif touch(player,obj) and jump_speed > 0:
                jump_speed = 0
                a = player.y - obj.y - obj.si_y
                for obj in objects:
                    obj.up(a)
                high += a
                score += a     
                break
        player.move(pressed_keys,right,left)
        if score >= 10000:
            client.send("win\n".encode())
            game_overing = "win"
        result = game_over(game_overing,MYFONT,screen)
        if result == "":
            pass
        else:
            return
        scoreboard.text = str(score)+"m"
        for obj in objects:
            obj.draw()
        enemy.draw()
        player.draw()
        scoreboard.draw()
        pygame.display.update()