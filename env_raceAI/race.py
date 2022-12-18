import pygame
import time
import math
from utils import scale_image

TRACK = scale_image(pygame.image.load("env_raceAI/imgs/track_1.png"),1.3)
BORDER = scale_image(pygame.image.load("env_raceAI/imgs/border_1.png"),1.3)
GRASS = scale_image(pygame.image.load("env_raceAI/imgs/grass.jpg"),500*1.3/311)
FINISH = pygame.image.load("env_raceAI/imgs/finish.png")
CAR_GREEN = scale_image(pygame.image.load("env_raceAI/imgs/car_green.png"),0.04)
CAR_PURPLE = pygame.image.load("env_raceAI/imgs/car_purple.png")

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")


run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60) #FPS

    WIN.blit(GRASS, (0, 0)) 
    WIN.blit(TRACK, (0, 0))
    WIN.blit(CAR_GREEN, (50, 150))

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
pygame.quit()