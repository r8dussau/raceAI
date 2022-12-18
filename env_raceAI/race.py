import pygame
import time
import math

PROFIL = pygame.image.load("env_raceAI/imgs/profil.jpg")

WIDTH, HEIGHT = PROFIL.get_width()/2, PROFIL.get_height()/4
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racing Game!")


run = True
clock = pygame.time.Clock()

while run:
    clock.tick(60) #FPS

    WIN.blit(PROFIL, (0, 0)) #show image 

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    
pygame.quit()