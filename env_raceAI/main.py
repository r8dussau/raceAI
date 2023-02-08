#-----------------------------------------------------------------------------
#import area

import pygame
import time
import math
from random import randint
from utils import scale_image, car_rotate_center, text_center, distance, movePoint, rotation
from IAFunction import move_ai, draw_car, fitness, crossover, mutation

pygame.font.init()

#-----------------------------------------------------------------------------
#image loading

TRACK = scale_image(pygame.image.load("env_raceAI/imgs/track.png"),1.7)#1.7
GRASS = scale_image(pygame.image.load("env_raceAI/imgs/grass.jpg"),500*1.7/311)
FINISH = scale_image(pygame.image.load("env_raceAI/imgs/finish.png"),0.475)


BORDER = scale_image(pygame.image.load("env_raceAI/imgs/border.png"),1.7)
BORDER_MASK = pygame.mask.from_surface(BORDER)  #create a mask of the border track for the collision 

CAR_GREEN = scale_image(pygame.image.load("env_raceAI/imgs/car_green.png"),0.04)#0.04
CAR_PURPLE = scale_image(pygame.image.load("env_raceAI/imgs/car_purple.png"),0.04)

#-----------------------------------------------------------------------------
#display on the screen area

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, 780)) #HEIGHT
pygame.display.set_caption("Racing Game with Genetic Algorithm!")

#-----------------------------------------------------------------------------
#class area

#class of the game info
class GameInfo:
    #function to initialize all parameters of the game info class 
    def __init__(self, stage=1):
        self.stage = stage
        self.started = False
        self.stage_start_time = 0

        self.stopTimer = False
        self.finished = False
        self.stopTime = 0

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
        self.acc = 0.1

        self.mask = pygame.mask.from_surface(self.img)
        self.rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)

        self.collide = False
        self.alive = False

        self.width = 320
        self.height = 651
        self.center = (0, 0)

        #Show lines of the player_car if it's True
        self.showlines = False

        #Coordinates of the contact point between the line and the wall for the player_car
        self.left = (0, 0)
        self.right = (0, 0)
        self.ahead = (0, 0)

        #distance between the center of the car and the coordinates of the top for the player_car
        self.distLeft = 0
        self.distRight = 0
        self.distAhead = 0

        #Coordinates of the corner of the player_car
        self.topLeft = (0, 0)
        self.topRight = (0, 0)
        self.bottomLeft = (0, 0)
        self.bottomRight = (0, 0)

        #value to calculate the fitnessValue
        self.distTraveled = 0
        self.numbOfTurn = 0
        self.fitnessValue = 0

        #save the random decision into a list 
        self.decisionList = list()
        self.decisionListSave = list()
        self.parentOne = False
        self.parentTwo = False
        self.iteration = 0
     

    #function to rotate the car 
    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel

        self.numbOfTurn += 1

    #function to call the car_rotate_center function with the arguments of the car class + refresh self.rect and self.mask (for the collision) + display line of the player_car
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
        
        self.distTraveled += 1

    #for the player_car
    def update(self):
        self.center = (self.x + 0.5*round(self.width*0.04), self.y + 0.5*round(self.height*0.04)) 

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
            self.left = movePoint((self.left[0],self.left[1]),self.angle+30,1.5) #0.5s
        while TRACK.get_at((int(self.left[0]),int(self.left[1]))) == GREY_TRACK2 or TRACK.get_at((int(self.left[0]),int(self.left[1]))) ==  BLACK:
            self.left = movePoint((self.left[0],self.left[1]),self.angle+30,-0.5) 

        self.right = movePoint((self.x, self.y),self.angle-30,1.5) #1
        while TRACK.get_at((int(self.right[0]),int(self.right[1]))) == GREY_TRACK:
            self.right = movePoint((self.right[0],self.right[1]),self.angle-30,1.5)#0.5
        while TRACK.get_at((int(self.right[0]),int(self.right[1]))) == GREY_TRACK2 or TRACK.get_at((int(self.right[0]),int(self.right[1]))) ==  BLACK:
            self.right = movePoint((self.right[0],self.right[1]),self.angle-30,-0.5)

        self.ahead = movePoint((self.x, self.y),self.angle,1.5) #1
        while TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) == GREY_TRACK:
            self.ahead = movePoint((self.ahead[0],self.ahead[1]),self.angle,1.5)#0.5
        while TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) == GREY_TRACK2 or TRACK.get_at((int(self.ahead[0]),int(self.ahead[1]))) ==  BLACK:
            self.ahead = movePoint((self.ahead[0],self.ahead[1]),self.angle,-0.5)

        self.distAhead = int(distance(self.center, self.ahead)) 
        self.distLeft = int(distance(self.center, self.left))
        self.distRight = int(distance(self.center, self.right)) 

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
        col = mask.overlap(self.mask, offset) 
        return col

    #reset the value of the car
    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 90
        self.vel = 0
        self.numbOfTurn = 0
        self.distTraveled = 0
        self.alive = False
        self.fitnessValue = 0
        self.iteration = 0


#class of the car with the initial color and position
class PlayerCar(Car):
    IMG = CAR_GREEN
    START_POS = (300, 660)


#-----------------------------------------------------------------------------

#display the screen with the images and the informations
def draw_background(win,imgs, gm_inf):
    for img, pos in imgs:
        win.blit(img, pos)

    stage_text = MAIN_FONT.render(f"Generation: {gm_inf.stage}", 1, (255, 255, 255))
    win.blit(stage_text, (10, 0))

    alive_car = MAIN_FONT.render(f"Car still alive: {aliveCar} on {numbOfCar}", 1, (255, 255, 255))
    win.blit(alive_car, (10, 30))

    time_text = MAIN_FONT.render(f"Time: {gm_inf.get_stage_time()}s", 1, (255, 255, 255))
    win.blit(time_text, (10, 60))

    if aliveCar==0:
        text_center(WIN, MAIN_FONT, f"Press enter to pass to the generation {game_info.stage+1}!")

    info_text1 = INFO_FONT.render("If the player_car is activated, press RIGHT to turn right and press LEFT to turn left", 1, (255, 255, 255))   #Press the key: UP to go forward, DOWN to go back, RIGHT to go right, LEFT to go left
    win.blit(info_text1, (10, 780 - info_text1.get_height()-10)) #HEIGHT

#function to move the player_car's image
def move_player(plr_car,keys):

    #action in function of wich key was pressed
    if not plr_car.collide:
        if keys[pygame.K_LEFT]:
            plr_car.rotate(left=True)
        if keys[pygame.K_RIGHT]:
            plr_car.rotate(right=True)
        plr_car.move_forward()
        plr_car.update()

def draw_player(win, plr_car):
    plr_car.draw(win)

#-----------------------------------------------------------------------------
#initialization area

MAIN_FONT = pygame.font.SysFont("comicsans", 30)
INFO_FONT = pygame.font.SysFont("comicsans", 15)

WHITE = (255,255,255)
GREEN = (0, 255, 0) 
BLUE = (0, 0, 128)  
BLACK = (1,1,1,255)

GREY_TRACK = (110,111,114,255)
GREY_TRACK2= (93,92,94,255)

COLOR_LINE = (255, 0, 0)

run = True
clock = pygame.time.Clock()
imgs = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, (283, 649))]
player_car = PlayerCar(1.5, 4)
game_info = GameInfo()

aiCars = []
numbOfCar = 100
aliveCar = numbOfCar

for i in range(numbOfCar):
    aiCars.append(PlayerCar(1.5,4))


#-----------------------------------------------------------------------------
#while run area

while run:
    clock.tick(60)  #FPS

    draw_background(WIN,imgs,game_info)

    #get the key of the keyboard pressed
    keys = pygame.key.get_pressed() 

    #-------------------------------------------------------------------------
    #If you want to display and control a Car

    # #display the player_car
    # draw_player(WIN, player_car)

    # #control of the player's car
    # if player_car.collision(BORDER_MASK) == None:
    #     player_car.collide = False
    #     move_player(player_car,keys)
    # else:
    #     player_car.collide = True
    #     move_player(player_car,keys)
    #     aliveCar=0
    #     if keys[pygame.K_RETURN]:
    #         aliveCar=1
    #         player_car.reset()
    #         game_info.next_stage()
    
        
    # if keys[pygame.K_a]:
    #     player_car.showLines() 

    #-------------------------------------------------------------------------

    draw_car(WIN, aiCars)

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

    
    #stop the car if there is a collision between the track border and the car
    for aicar in aiCars:
        if aicar.collision(BORDER_MASK) == None:
            aicar.collide = False
            move_ai(aicar)
        else:
            aicar.collide = True
            if aicar.alive == False:
                aliveCar -=1
                aicar.alive = True

                fitness(aicar) 

    if aliveCar == 0:
        fitnessList=list() 
        for aicar in aiCars:
            fitnessList.append(aicar.fitnessValue)
        fitnessList.sort()
        for aicar in aiCars:
            #change the color of the car and turn on the bool of the parents
            if aicar.fitnessValue == fitnessList[0]:
                aicar.img = CAR_PURPLE
                aicar.parentOne = True
                aicar.parentTwo = False
            elif aicar.fitnessValue == fitnessList[1]:
                aicar.img = CAR_PURPLE
                aicar.parentOne = False
                aicar.parentTwo = True
            else:
                aicar.img = CAR_GREEN
                aicar.parentOne = False
                aicar.parentTwo = False

        #if keys[pygame.K_RETURN]:

        crossover(aiCars)  
        mutation(aiCars)

        for aicar in aiCars:
            aicar.reset()
        game_info.next_stage()
        aliveCar = numbOfCar
        game_info.start_stage()

    pygame.display.update()
pygame.quit() 
