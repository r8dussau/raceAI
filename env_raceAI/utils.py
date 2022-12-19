import pygame 

#function to reajust the size of the images
def scale_image(img,factor):
    size = round(img.get_width()*factor), round(img.get_height()*factor)
    return pygame.transform.scale(img,size)

#function that rotates the image according to its center
def car_rotate_center(win, img, top_left, angle):
    rotated_img = pygame.transform.rotate(img, angle)                               #rotate around the top-left 
    new_rect = rotated_img.get_rect(center=img.get_rect(topleft=top_left).center)   #rotate around the center according to the rotation of the top-left
    win.blit(rotated_img, new_rect.topleft)                                         #display the car with the rotation

#function to print the text in the middle of the window
def text_center(win, font, text):
    render = font.render(text, 1, (200, 200, 200))
    win.blit(render, (win.get_width()/2 - render.get_width()/2, win.get_height()/2 - render.get_height()/2))