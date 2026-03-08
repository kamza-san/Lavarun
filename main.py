import pygame
import sys
import os
sys.path.append(os.path.dirname(__file__))
from pygame.locals import *
from offline.game import game
from offline.title import title
from online.online import online
from offline.level_setting import level_set
from online.enter import enter
from offline.record import record
from offline.set import setting
from online.matching import matching

pygame.init()
pygame.mixer.init()
#Object 만들때 무조건 가로와 가로위치를 5의 배수로 만들어야함ㅇㅇ
bgm = pygame.mixer.Sound("./eximage/bgm2.mp3")    
bgm.set_volume(0.5)
bgm.play(-1)
FPS = 60
MAX_WIDTH = 600
MAX_HEIGHT = 800
MYFONT = pygame.font.SysFont('malgungothic', 25)

clock = pygame.time.Clock()
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))
using_host = "0.0.0.0"
using_port = 0
answer = "title"
if __name__ == "__main__":
    level = "normal"
    while True:
        if answer == "title":
            answer = title(clock,screen,FPS,MYFONT,level)
        elif answer == "game":
            answer = game(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,level)
        elif answer == "online":
            n = online(clock,screen,FPS,MYFONT)
            if n == "title":
                answer = "title"
            else:
                using_host = n
                answer = "matching"
        elif answer == "level_setting":
            level = level_set(clock,screen,FPS,MYFONT,level)
            answer = "title"
        elif answer == "enter":
            answer = enter(clock,screen,FPS,MAX_WIDTH,MAX_HEIGHT,MYFONT,using_host,using_port)
        elif answer == "record":
            answer = record(clock,screen,FPS,MYFONT)
        elif answer == "setting":
            answer = setting(clock,screen,FPS,MYFONT)
        elif answer == "matching":
            n = matching(clock,screen,FPS,MYFONT,using_host)
            if n == "online":
                answer = "online"
            else:
                using_port = int(n)
                answer = "enter"