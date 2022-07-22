import os.path

import pygame
import sys

pygame.font.init()  # init font
pygame.mixer.init()  # init sound

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game For 2_GG")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('assets', 'Gun+Silencer.mp3'))

# Text setting
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# creat new event
RED_HIT = pygame.USEREVENT + 1
YELLOW_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('assets', 'spaceship_yellow.png'))  # "assets/spaceship_yellow.png"
YELLOW_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load("assets/spaceship_red.png")
RED_SPACESHIP_IMAGE = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health), 1, WHITE
    )
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health), 1, WHITE
    )
    WIN.blit(red_health_text, (20, 20))
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 20, 20))
    WIN.blit(YELLOW_SPACESHIP_IMAGE, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP_IMAGE, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL > 0:
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL + red.width < BORDER.x:
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_LEFT] and BORDER.x + 10 < yellow.x - VEL:
        yellow.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and yellow.x + yellow.width < WIDTH:
        yellow.x += VEL
    if keys_pressed[pygame.K_UP] and yellow.y - VEL > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_DOWN] and yellow.y + VEL + yellow.height < HEIGHT - 15:
        yellow.y += VEL


def handle_bullet(red_bullets, yellow_bullets, red, yellow):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in yellow_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x < 0:
            yellow_bullets.remove(bullet)


def draw_winner(text):
    winner_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(winner_text, (WIDTH / 2 - winner_text.get_width() / 2, HEIGHT / 2 - winner_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    red = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_health = 3
    yellow_health = 3

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(red_bullets) < MAX_BULLETS:  # maximum 3 bullets on the screen
                    bullets = pygame.Rect(red.x + red.width, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullets)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullets = pygame.Rect(yellow.x, yellow.y + yellow.height // 2, 10, 5)
                    yellow_bullets.append(bullets)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health < 1:
            winner_text = "YELLOW WINS!"
        if yellow_health < 1:
            winner_text = "RED WINS!"
        if winner_text != "":
            draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        yellow_handle_movement(keys_pressed, yellow)

        handle_bullet(red_bullets, yellow_bullets, red, yellow)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # pygame.quit()
    main()  # restart game


if __name__ == "__main__":
    main()
