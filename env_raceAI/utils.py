import pygame 
import math
import numpy as np

#function to reajust the size of the images
def scale_image(img,factor):
    size = round(img.get_width()*factor), round(img.get_height()*factor)
    return pygame.transform.scale(img,size)

#function that rotates the image according to its center
def car_rotate_center(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)                               #rotate around the top-left 
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_left).center)   #center new rotated image on the center of original image
    win.blit(rotated_img, new_rect.topleft)                                          #display the car with the rotation

    """ pygame.draw.rect(win, (255, 0, 0), new_rect, 2)   #draw rectangle of the image
    car_mask = pygame.mask.from_surface(img).to_surface()
    pygame.draw.rect(win, (0, 255, 0), car_mask.get_rect(center=img.get_rect(topleft=top_left).center), 2)  #draw the rectangle if mask isn't rotated when checking collision """                      
    return new_rect, pygame.mask.from_surface(rotated_img)

#function to print the text in the middle of the window
def text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))

def movePoint(point,angle,velo):
        x = point[0]
        y = point[1]

        radians = math.radians(angle%360)
        vertical = math.cos(radians) * velo
        horizontal = math.sin(radians) * velo

        x -= horizontal
        y -= vertical

        return x, y

def distance(center, end):
        return math.sqrt((end[0]-center[0])**2 + (end[1]-center[1])**2)

def rotation(origin, point, angle): #Used to rotate points #rotate(origin, point, math.radians(10))
    ox, oy = origin
    px, py = point
    angle = -angle

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
   
    return qx, qy 