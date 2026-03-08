import pygame
from pygame.locals import *

class Player:
    def __init__(self,x,y,head,image_right,image_left,right,left,screen):
        self.screen = screen
        self.x = x
        self.y = y
        self.head = head
        self.image_right = image_right
        self.image_left = image_left
        self.right = right
        self.left = left
    def draw(self):
            if self.head == 1:
                return self.screen.blit(self.image_right,(self.x,self.y))
            return self.screen.blit(self.image_left,(self.x,self.y))
    def move(self,pressed_keys,right,left):
        if pressed_keys[self.right] and self.x < 540:                
            if right:
                self.x += 5
                self.head = 1
        if pressed_keys[self.left] and self.x > 0:
            if left:    
                self.x -= 5
                self.head = 0
    def get_rect(self):
        return pygame.Rect(self.x, self.y, 60, 60)