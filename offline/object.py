import pygame
class Object:
    def __init__(self,x,y,si_x,si_y,red,green,blue,screen):
        self.x = x
        self.y = y
        self.si_x = si_x
        self.si_y = si_y
        self.screen = screen
        self.red = red
        self.green = green
        self.blue = blue
    def draw(self):
        return pygame.draw.rect(self.screen, (self.red,self.green,self.blue), (self.x, self.y, self.si_x, self.si_y))
    def up(self,a):
         self.y += a
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.si_x, self.si_y)