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
from image import scoreimage,background,player_right,player_left,button,title_photo,button2

def receive_messages(sock):
    global game_overing
    global map_data
    while True:
        try:
            msg = sock.recv(1024).decode()
            data = msg.split("]")[-1].strip()
            data = list(data.split(','))
            if data[0] == "move":
                global score
                enemy.x = int(data[1])
                enemy.y = 550 + score - int(data[2])
            elif data[0] == "start":
                global out
                out = False
            elif data[0] == "win":
                game_overing = "lose"
            elif data[0] == "obj":
                map_data = data
        except:
            pass

def enter(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,host,port):
    
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((host, port))
    except TimeoutError:
        print("서버에 연결할 수 없습니다. (TimeoutError 발생)")
        pygame.quit()
        sys.exit()
    except Exception as e:
        print(f"서버 연결 중 오류가 발생했습니다: {e}")
        pygame.quit()
        sys.exit()

    print("서버에 연결되었습니다.(Ctrl+C로 종료)")

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()
    
    global out
    out = True
    level = "normal"
    start = Button(200,300,200,80,button,"start",MYFONT,0,0,0,screen)
    quit = Button(200,420,200,80,button,"quit",MYFONT,0,0,0,screen)
    while out:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start.click(pygame.mouse.get_pos()):
                    if start.text == "start":
                        try:
                            client.send("play".encode())
                        except KeyboardInterrupt:
                            print("\n[!] 클라이언트를 종료합니다.")
                            client.close()
                            pygame.quit()
                            sys.exit()
                        start.text = "cancel"
                    elif start.text == "cancel":
                        try:
                            print("cancel game")
                            client.send("cancel".encode())
                            print("cancel game")
                        except KeyboardInterrupt:
                            print("\n[!] 클라이언트를 종료합니다.")
                            print("client QUIT!")
                            client.close()
                            pygame.quit()
                            sys.exit()
                        start.text = "start"
                elif quit.click(pygame.mouse.get_pos()):
                    client.close()
                    return "online"
        start.image = button
        quit.image = button
        if start.click(pygame.mouse.get_pos()):
            start.image = button2
        elif quit.click(pygame.mouse.get_pos()):
            quit.image = button2
        start.draw()
        quit.draw()
        pygame.display.update()
    game(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,level)
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
        msg = "move"+","+str(player.x)+","+str(score)
        try:
            client.send(msg.encode())
        except KeyboardInterrupt:
            print("\n[!] 클라이언트를 종료합니다.")
            client.close()
            pygame.quit()
            sys.exit()
            
def map_gen(objs,screen):
    for i in range(100):
        objects.append(Object(int(objs[1+i*2]), int(objs[2+i*2]), 100, 40, 255,255,0,screen))
            
def game_over(fight,MYFONT,screen):
    if fight == "":
        return ""
    win_lose = Button(200,300,200,80,button,"",MYFONT,0,0,0,screen)
    ok = Button(200,420,200,80,button,"ok",MYFONT,0,0,0,screen)
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
                    return "online"
        for obj in objects:
            obj.draw()
        enemy.draw()
        player.draw()
        scoreboard.draw()
        win_lose.draw()
        ok.draw()
        pygame.display.update()
                            

def game(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,level):
    global objects
    objects = []
    map_gen(map_data,screen)
    with open("set.json","r") as f:
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
    game_overing = ""
    srv_timer = 0
    enemy = Player(MAX_WIDTH//2-30,MAX_HEIGHT-250,1,player_right,player_left,right_num,left_num,screen)
    if level == "easy":
        speed = -1
    elif level == "normal":
        speed = -2
    else:
        speed = -4
    score = -10
    player = Player(MAX_WIDTH//2-30,MAX_HEIGHT-250,1,player_right,player_left,right_num,left_num,screen)
    objects.append(Object(0, 600, 600, 300, 255,255,0,screen))
    scoreboard = Button(40,40,200,80,scoreimage,str(score)+"m",MYFONT,153,217,234,screen)
    if_jump = False
    second_jump = False
    high = -800
    jump_speed = 5
    while True:
        srv_timer += 1
        if srv_timer >= 3:
            say("move")
            srv_timer = 0
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
                    elif second_jump:
                        jump_speed = 20
                        second_jump = False
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
            client.send("win".encode())
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