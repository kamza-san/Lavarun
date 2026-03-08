import pygame
class Button:
    def __init__(self,x,y,si_x,si_y,image,text,font,red,green,blue,screen):
        self.x = x
        self.y = y
        self.si_x = si_x
        self.si_y = si_y
        self.screen = screen
        self.image = image
        self.text = text
        self.font = font
        self.red = red
        self.green = green
        self.blue = blue
    def draw(self):
        self.screen.blit(self.image,(self.x,self.y))
        text_surface = self.font.render(str(self.text), True, (self.red, self.green, self.blue))
        text_rect = text_surface.get_rect(center=(self.x + self.si_x // 2, self.y + self.si_y // 2))
        self.screen.blit(text_surface, text_rect)

    def click(self,mouse):
        if self.x <= mouse[0] and mouse[0] <= (self.x + self.si_x) :
            if self.y <= mouse[1] and mouse[1] <= (self.y + self.si_y) :
                return True
        return False