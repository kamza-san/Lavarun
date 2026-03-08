import random 
from offline.object import Object

objects = []
def generate_map(screen,now_y):
    x = random.randint(12,88)*5
    width = 100
    height = 40
    y = now_y
    objects.append(Object(x,y,width,height,255,255,0,screen))

def touch(player,obj):
    return player.get_rect().colliderect(obj.get_rect())

def touch_side(player,obj):
    p_rect = player.get_rect()
    o_rect = obj.get_rect()

    if not p_rect.colliderect(o_rect):
        return None

    delta_left = p_rect.right - o_rect.left
    delta_right = o_rect.right - p_rect.left
    delta_top = p_rect.bottom - o_rect.top
    delta_bottom = o_rect.bottom - p_rect.top

    min_delta = min(delta_left, delta_right, delta_top, delta_bottom)

    if min_delta == delta_top:
        return "top"    
    elif min_delta == delta_bottom:
        return "bottom" 
    elif min_delta == delta_left:
        return "left"   
    else:
        return "right"

def touch_near(player,obj):
    p_rect = player.get_rect()
    o_rect = obj.get_rect()

    delta_top = p_rect.bottom - o_rect.top
    delta_bottom = o_rect.bottom - p_rect.top
    delta_left = p_rect.right - o_rect.left
    delta_right = o_rect.right - p_rect.left
    
    if 0 == delta_top and 0 <= delta_right and 0 <= delta_left:
        return "top"    
    elif 0 == delta_bottom and 0 <= delta_right and 0 <= delta_left:
        return "bottom" 
    elif 0 == delta_left and 0 <= delta_top and 0 <= delta_bottom:
        return "left"   
    elif 0 == delta_right and 0 <= delta_top and 0 <= delta_bottom:
        return "right"