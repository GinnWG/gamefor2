import os.path

import pygame
import sys
from pygame.locals import *

WIDTH, HEIGHT = 500, 900
WIN = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Game For 2_GG")

WHITE = (255, 255, 255)
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

FPS = 60

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png'))  # "assets/spaceship_yellow.png"
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_red.png")
RED_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)


def draw_window():
    WIN.fill(WHITE)
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (300, 100))
    WIN.blit(RED_SPACESHIP_IMAGE, (700, 100))
    pygame.display.update()
    pass


def main():
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw_window()

    pygame.quit()


if __name__ == "__main__":
    main()
