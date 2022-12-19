#-----------------------------------------------------------------------------
#import area

import pygame
import time
import math
from utils import scale_image, car_rotate_center

#-----------------------------------------------------------------------------
#image loading

TRACK = scale_image(pygame.image.load("env_raceAI/imgs/track_1.png"),1.5)
BORDER = scale_image(pygame.image.load("env_raceAI/imgs/border_1.png"),1.5)
GRASS = scale_image(pygame.image.load("env_raceAI/imgs/grass.jpg"),500*1.5/311)
FINISH = pygame.image.load("env_raceAI/imgs/finish.png")
CAR_GREEN = scale_image(pygame.image.load("env_raceAI/imgs/car_green.png"),0.04)
CAR_PURPLE = pygame.image.load("env_raceAI/imgs/car_purple.png") 

#-----------------------------------------------------------------------------

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")

#class of the car
class Car:
    #function ton initialize all parameters
    def __init__(self, max_vel, rot_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rot_vel = rot_vel
        self.angle = 0
        self.x, self.y = self.START_POS

    #function to rotate the car 
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

    #function to call the car_rotate_center function with the arguments of the car class
    def draw(self, win):
        car_rotate_center(win, self.img, (self.x, self.y), self.angle)

#class of the player's car
class PlayerCar(Car):
    IMG = CAR_GREEN
    START_POS = (300, 585)


def draw(win, imgs, plr_car):
    for img, pos in imgs:
        win.blit(img, pos)

    player_car.draw(win)    #draw the player's car after rotating
    pygame.display.update()


run = True
clock = pygame.time.Clock()
imgs = [(GRASS, (0, 0)), (TRACK, (0, 0))]
player_car = PlayerCar(4, 4)

while run:
    clock.tick(60)  #FPS

    draw(WIN,imgs, player_car)  #function to display a large number of images 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    
    keys = pygame.key.get_pressed() #get the key of the keyboard pressed

    #action in function of wich key was pressed
    if keys[pygame.K_q] or keys[pygame.K_LEFT]:
        player_car.rotate(left=True)
    elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        player_car.rotate(right=True)

pygame.quit()