import pygame
import time
import math

GRASS = pygame.image.load("env_raceAI/imgs/grass.jpg")
BORDER = pygame.image.load("env_raceAI/imgs/border_1.png")
TRACK = pygame.image.load("env_raceAI/imgs/track_1.png")
FINISH = pygame.image.load("env_raceAI/imgs/finish.png")
CAR_GREEN = pygame.image.load("env_raceAI/imgs/car_green.png")
CAR_PURPLE = pygame.image.load("env_raceAI/imgs/car_purple.png")

WIDTH, HEIGHT = GRASS.get_width()*1.5, GRASS.get_height()*1.5
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")


run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60) #FPS

    WIN.blit(GRASS, (0, 0)) 
    WIN.blit(TRACK, (0, 0))
    WIN.blit(CAR_PURPLE, (0, 0))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
pygame.quit()