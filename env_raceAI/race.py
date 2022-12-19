#-----------------------------------------------------------------------------
#import area

import pygame
import time
import math
from utils import scale_image, car_rotate_center

#-----------------------------------------------------------------------------
#image loading

TRACK = scale_image(pygame.image.load("env_raceAI/imgs/track_1.png"),1.7)
GRASS = scale_image(pygame.image.load("env_raceAI/imgs/grass.jpg"),500*1.7/311)
FINISH = scale_image(pygame.image.load("env_raceAI/imgs/finish.png"),0.475)

BORDER = scale_image(pygame.image.load("env_raceAI/imgs/border_1.png"),1.7)
BORDER_MASK = pygame.mask.from_surface(BORDER)  #create a mask for the collision 

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
        self.angle = 90
        self.x, self.y = self.START_POS
        self.acc = 0.05

    #function to rotate the car 
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

    #function to call the car_rotate_center function with the arguments of the car class
    def draw(self, win):
        car_rotate_center(win, self.img, (self.x, self.y), self.angle)

    #function to modify the velocity of the car to go forward
    def move_forward(self):
        if self.vel < 0:
            self.vel = 0
        self.vel = min(self.vel + self.acc, self.max_vel)
        self.move()

    #function to modify the velocity of the car to go backward
    def move_backward(self):
        self.vel = -0.35
        self.move()

    #function to move the car according to the angle 
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel 

        self.x -= horizontal
        self.y -= vertical

    def collision(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        col = mask.overlap(car_mask, offset)
        return col

#class of the player's car
class PlayerCar(Car):
    IMG = CAR_GREEN
    START_POS = (300, 660) #300, 585

#function to display a large number of images
def draw(win, imgs, plr_car):
    for img, pos in imgs:
        win.blit(img, pos)

    player_car.draw(win)    #draw the player's car after rotating
    pygame.display.update()

#function to move the car's image
def move_player(plr_car,collision=False):
    keys = pygame.key.get_pressed() #get the key of the keyboard pressed

    #action in function of wich key was pressed
    if not collision:
        if keys[pygame.K_q] or keys[pygame.K_LEFT]:
            player_car.rotate(left=True)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player_car.rotate(right=True)
        if keys[pygame.K_z] or keys[pygame.K_UP]:
            player_car.move_forward()
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player_car.move_backward()

run = True
clock = pygame.time.Clock()
imgs = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (283, 649))]
player_car = PlayerCar(1.5, 4)

while run:
    clock.tick(60)  #FPS

    draw(WIN,imgs, player_car)   

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
    #move_player(player_car,colli)
    
    if player_car.collision(BORDER_MASK) == None:
        colli = False
        move_player(player_car,colli)
    else:
        colli = True
        move_player(player_car,colli)

pygame.quit() 