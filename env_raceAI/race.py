#-----------------------------------------------------------------------------
#import area

import pygame
import time
import math
from utils import scale_image, car_rotate_center, text_center

pygame.font.init()

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

MAIN_FONT = pygame.font.SysFont("comicsans", 30)
INFO_FONT = pygame.font.SysFont("comicsans", 15)

#-----------------------------------------------------------------------------
#class area

#class of the game info
class GameInfo:
    #function to initialize all parameters of the game info class 
    def __init__(self, stage=1):
        self.stage = stage
        self.started = False
        self.stage_start_time = 0

    #function to increment the generation
    def next_stage(self):
        self.stage += 1
        self.started = False

    #function to reset 
    def reset(self):
        self.stage = 1
        self.started = False
        self.stage_start_time = 0

    #function to start the time
    def start_stage(self):
        self.started = True
        self.stage_start_time = time.time()

    #function to get the time 
    def get_stage_time(self):
        if not self.started:
            return 0
        return int(time.time() - self.stage_start_time)

#class of the car
class Car:
    #function to initialize all parameters of the car class 
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

    #function to return a no none result if a car collide with the border track
    def collision(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        col = mask.overlap(car_mask, offset)
        return col

#class of the player's car
class PlayerCar(Car):
    IMG = CAR_GREEN
    START_POS = (300, 660) #300, 585

#-----------------------------------------------------------------------------
#display and move function

#function to display images and texts
def draw(win, imgs, plr_car,gm_inf):
    for img, pos in imgs:
        win.blit(img, pos)

    stage_text = MAIN_FONT.render(f"Generation: {game_info.stage}", 1, (255, 255, 255))
    win.blit(stage_text, (10, 0))

    time_text = MAIN_FONT.render(f"Time: {game_info.get_stage_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, 30))

    info_text1 = INFO_FONT.render("Press the key: UP to go forward, DOWN to go back, RIGHT to go right, LEFT to go left", 1, (255, 255, 255))
    win.blit(info_text1, (10, HEIGHT - info_text1.get_height()-30))

    info_text2 = INFO_FONT.render("Select the parents of the next generation by clicking on them and then press ENTER", 1, (255, 255, 255))
    win.blit(info_text2, (10, HEIGHT - info_text2.get_height()-10))

    player_car.draw(win)
    pygame.display.update()

#function to move the car's image
def move_player(plr_car,collision=False):
    keys = pygame.key.get_pressed() #get the key of the keyboard pressed

    #action in function of wich key was pressed
    if not collision:
        if keys[pygame.K_LEFT]:
            player_car.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            player_car.rotate(right=True)
        if keys[pygame.K_UP]:
            player_car.move_forward()
        if keys[pygame.K_DOWN]:
            player_car.move_backward()

#-----------------------------------------------------------------------------

run = True
clock = pygame.time.Clock()
imgs = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (283, 649))]
player_car = PlayerCar(1.5, 4)
game_info = GameInfo()

while run:
    clock.tick(60)  #FPS

    draw(WIN,imgs, player_car, game_info) 

    while not game_info.started:
        text_center(WIN, MAIN_FONT, f"Press any key to start the stage {game_info.stage}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break

            if event.type == pygame.KEYDOWN:
                game_info.start_stage()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    #stop the car if there is a collision between the track border and the car
    if player_car.collision(BORDER_MASK) == None:
        colli = False
        move_player(player_car,colli)
    else:
        colli = True
        move_player(player_car,colli)

pygame.quit() 