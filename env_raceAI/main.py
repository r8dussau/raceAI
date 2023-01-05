#-----------------------------------------------------------------------------
#import area

import pygame
import time
import math
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from utils import scale_image, car_rotate_center, text_center, distance, movePoint, rotation
from neurol_function import fitness

pygame.font.init()

#-----------------------------------------------------------------------------
#image loading

TRACK = scale_image(pygame.image.load("env_raceAI/imgs/track_1.png"),1.7)#1.7
GRASS = scale_image(pygame.image.load("env_raceAI/imgs/grass.jpg"),500*1.7/311)
FINISH = scale_image(pygame.image.load("env_raceAI/imgs/finish.png"),0.475)


BORDER = scale_image(pygame.image.load("env_raceAI/imgs/border_1.png"),1.7)
BORDER_MASK = pygame.mask.from_surface(BORDER)  #create a mask of the border track for the collision 

CAR_GREEN = scale_image(pygame.image.load("env_raceAI/imgs/car_green.png"),0.04)#0.04
CAR_PURPLE = scale_image(pygame.image.load("env_raceAI/imgs/car_purple.png"),0.04)

#-----------------------------------------------------------------------------
#display on the screen area

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, 780)) #HEIGHT
pygame.display.set_caption("Racing Game with Genetic Algorithm!")

MAIN_FONT = pygame.font.SysFont("comicsans", 30)
INFO_FONT = pygame.font.SysFont("comicsans", 15)

WHITE = (255,255,255)
GREEN = (0, 255, 0) 
BLUE = (0, 0, 128)  
BLACK = (1,1,1,255)

GREY_TRACK = (110,111,114,255)
GREY_TRACK2= (93,92,94,255)

COLOR_LINE = (255, 0, 0)

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

        self.mask = pygame.mask.from_surface(self.img)
        self.rect = (0, 0)

        self.width = 320
        self.height = 651
        self.center = (0, 0)

        self.distFromGoal = 0
        self.numbFromTurn = 0

        #Show lines of the car if it's True
        self.showlines = False

        #Coordinates of the contact point between the line and the wall
        self.left = (0, 0)
        self.right = (0, 0)
        self.ahead = (0, 0)

        #distance between the center of the car and the coordinates of the top
        self.distLeft = 0
        self.distRight = 0
        self.distAhead = 0

        #Coordinates of the 
        self.topLeft = (0, 0)
        self.topRight = (0, 0)
        self.bottomLeft = (0, 0)
        self.bottomRight = (0, 0)

        self.input = np.array([[self.distLeft], [self.distRight], [self.distAhead]])
        self.output = np.array([[0], [0]])
        

    #function to rotate the car 
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

        self.numbFromTurn += 1

    #function to call the car_rotate_center function with the arguments of the car class + refresh self.rect and self.mask (for the collision)
    def draw(self, win):
        self.rect, self.mask = car_rotate_center(win, self.img, (self.x, self.y), self.angle)   

        if self.showlines:
            pygame.draw.line(win,COLOR_LINE,self.center,self.right,2)
            pygame.draw.line(win,COLOR_LINE,self.center,self.left,2) 
            pygame.draw.line(win,COLOR_LINE,self.center,self.ahead,2)

    def showLines(self):
        self.showlines = not self.showlines

    #function to modify the velocity of the car to go forward
    def move_forward(self):
        self.vel = min(self.vel + self.acc, self.max_vel)
        self.move()
        
        self.distFromGoal += 1

    def update(self):
        self.center = (self.x + 0.5*round(self.width*0.04), self.y + 0.5*round(self.height*0.04)) #modified the center of the car when rotation

        self.topLeft = (self.center[0] - 0.04*self.width/2, self.center[1] + 0.04*self.height/2)
        self.topRight = (self.center[0] + 0.04*self.width/2, self.center[1] + 0.04*self.height/2)
        self.bottomLeft = (self.center[0] - 0.04*self.width/2, self.center[1] - 0.04*self.height/2)
        self.bottomRight = (self.center[0] + 0.04*self.width/2, self.center[1] - 0.04*self.height/2)

        self.topLeft = rotation(self.center, self.topLeft, math.radians(self.angle))
        self.topRight = rotation(self.center, self.topRight, math.radians(self.angle))
        self.bottomLeft = rotation(self.center, self.bottomLeft, math.radians(self.angle))
        self.bottomRight = rotation(self.center, self.bottomRight, math.radians(self.angle))

        self.left = movePoint((self.x, self.y),self.angle+30,1.5) #1
        while TRACK.get_at((int(self.left[0]),int(self.left[1]))) == GREY_TRACK:
            self.left = movePoint((self.left[0],self.left[1]),self.angle+30,1.5) #0.5
        while TRACK.get_at((int(self.left[0]),int(self.left[1]))) == GREY_TRACK2 or TRACK.get_at((int(self.left[0]),int(self.left[1]))) ==  BLACK:
        #while TRACK.get_at((int(self.left[0]),int(self.left[1]))) != GREY_TRACK:
            self.left = movePoint((self.left[0],self.left[1]),self.angle+30,-0.5) 

        self.right = movePoint((self.x, self.y),self.angle-30,1.5) #1
        while TRACK.get_at((int(self.right[0]),int(self.right[1]))) == GREY_TRACK:
            self.right = movePoint((self.right[0],self.right[1]),self.angle-30,1.5)#0.5
        while TRACK.get_at((int(self.right[0]),int(self.right[1]))) == GREY_TRACK2 or TRACK.get_at((int(self.right[0]),int(self.right[1]))) ==  BLACK:
        #while TRACK.get_at((int(self.right[0]),int(self.right[1]))) != GREY_TRACK:
            self.right = movePoint((self.right[0],self.right[1]),self.angle-30,-0.5)

        self.ahead = movePoint((self.x, self.y),self.angle,1.5) #1
        while TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) == GREY_TRACK:
            self.ahead = movePoint((self.ahead[0],self.ahead[1]),self.angle,1.5)#0.5
        while TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) == GREY_TRACK2 or TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) ==  BLACK:
        #while TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) != GREY_TRACK:
            self.ahead = movePoint((self.ahead[0],self.ahead[1]),self.angle,-0.5)

        self.distAhead = int(distance(self.center, self.ahead)) 
        self.distLeft = int(distance(self.center, self.left))
        self.distRight = int(distance(self.center, self.right)) 

    #function to modify the velocity of the car to go backward
    """ def move_backward(self):
        self.vel = -0.35
        self.move() """

    #function to move the car according to the angle 
    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel 

        self.x -= horizontal
        self.y -= vertical 
    
    #function to return a no none result if a car collide with the border track
    def collision(self, mask, x=0, y=0):
        offset = (int(self.rect.x - x), int(self.rect.y - y)) 
        #offset = (int(self.rect[0] - x), int(self.rect[1] - y)) 
        col = mask.overlap(self.mask, offset) 
        return col

    #
    def calcul(self):
        return self.distFromGoal-self.numbFromTurn
    #

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0
        self.numbFromTurn = 0
        self.distFromGoal = 0


#class of the player's car
class PlayerCar(Car):
    IMG = CAR_GREEN
    START_POS = (300, 660)


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

    info_text1 = INFO_FONT.render("RIGHT to turn right, LEFT to turn left", 1, (255, 255, 255))   #Press the key: UP to go forward, DOWN to go back, RIGHT to go right, LEFT to go left
    win.blit(info_text1, (10, 780 - info_text1.get_height()-30)) #HEIGHT

    info_text2 = INFO_FONT.render("When all the car are crashed press ENTER", 1, (255, 255, 255)) #Select the parents of the next generation by clicking on them and then press ENTER
    win.blit(info_text2, (10, 780 - info_text2.get_height()-10)) #HEIGHT

    

    player_car.draw(win)
    pygame.display.update()

#function to move the car's image
def move_player(plr_car,keys,collision=False):

    #action in function of wich key was pressed
    if not collision:
        if keys[pygame.K_LEFT]:
            player_car.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            player_car.rotate(right=True)
        #if keys[pygame.K_UP]:
            #player_car.move_forward()
        player_car.move_forward()
        player_car.update()
        """ if keys[pygame.K_DOWN]:
            player_car.move_backward() """

    if collision:    
        if keys[pygame.K_RETURN]:
            player_car.reset()
            game_info.next_stage()
        

                


#-----------------------------------------------------------------------------
#initialization area

#test = BORDER_MASK.to_surface()
run = True
clock = pygame.time.Clock()
imgs = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (283, 649))]
player_car = PlayerCar(1.5, 4) #1.5
game_info = GameInfo()


selected = 0
selectedCar = []

""" aiCars = []
numbOfCar = 1 
aliveCar = numbOfCar
collidedCar = []

for i in range(numbOfCar):
    aiCars.append(PlayerCar(1.5,4)) """

#-----------------------------------------------------------------------------
#while run area

while run:
    clock.tick(60)  #FPS

    #display the screen with the images and the informations
    draw(WIN,imgs, player_car, game_info) 

    #Display text before the begining of each generation 
    while not game_info.started:
        text_center(WIN, MAIN_FONT, f"Press any key to start the generation {game_info.stage}!")
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

    """ for aicar in aiCars:
        
        if aicar.collision(BORDER_MASK) == None:
            colli = False
            move_player(aicar,keys,colli)
        else:
            colli = True
            move_player(aicar,keys,colli)
        
        if keys[pygame.K_a]:
            aicar.showLines() """
    
    #stop the car if there is a collision between the track border and the car
    
    keys = pygame.key.get_pressed() #get the key of the keyboard pressed
    if player_car.collision(BORDER_MASK) == None:
        colli = False
        move_player(player_car,keys,colli)
    else:
        colli = True
        move_player(player_car,keys,colli)
    
    if keys[pygame.K_a]:
        player_car.showLines()
        
    mouses = pygame.mouse.get_pressed()
    if mouses[0]:   
            pos = pygame.mouse.get_pos()
            point = Point(pos[0], pos[1])            

            """ for aicar in aiCars:

                polygon = Polygon([aicar.bottomLeft, aicar.topLeft, aicar.topRight, aicar.bottomRight, aicar.bottomLeft])

                if (polygon.contains(point)):
                    if aicar.img == CAR_GREEN:
                        aicar.img = CAR_PURPLE
                    elif aicar.img == CAR_PURPLE:
                        aicar.img = CAR_GREEN
                    aicar.update() """


            polygon = Polygon([player_car.bottomLeft, player_car.topLeft, player_car.topRight, player_car.bottomRight, player_car.bottomLeft])

            if (polygon.contains(point)):
                if player_car.img == CAR_GREEN:
                    player_car.img = CAR_PURPLE
                elif player_car.img == CAR_PURPLE:
                    player_car.img = CAR_GREEN
                player_car.update()

pygame.quit() 
