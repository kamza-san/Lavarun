import pygame
import sys
import threading
from offline.button import Button
from offline.textbox import Textbox
from image import button,title_photo,button2
import socket
from pygame.locals import *

def receive_messages(sock):
    global my_port
    while True:
        try:
            msg = sock.recv(1024).decode()
            data = msg.split("]")[-1].strip()
            data = list(data.split(','))
            print("[DATA]", data)
            if data[0] == "port":
                my_port = data[1]
        except:
            pass

def matching(clock,screen,FPS,MYFONT,host):
    port = 20000
    
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.daemon = True
    receive_thread.start()
    
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

    text = Textbox(200,300,200,80,button,"matching...",MYFONT,0,0,0,screen)
    quit = Textbox(200,420,200,80,button,"quit",MYFONT,0,0,0,screen)
    global my_port
    my_port = None
    while True:    
        clock.tick(FPS)
        screen.blit(title_photo,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if quit.click(pygame.mouse.get_pos()):
                    client.close()
                    return "online"
        if my_port != None:
            text.text = "succeed!"
            text.draw()
            quit.draw()
            pygame.display.update()
            client.close()
            return my_port
        text.draw()
        quit.draw()
        pygame.display.update()