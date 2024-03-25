import pygame
from pygame import Vector2
from pygame.locals import *
import sys
import BGScrolling
import random


pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

PLAYER_COLOR = (25, 40, 70)
BLACK = (0, 0, 0)
ACELERATION = 0.001
velocity = 2
player = pygame.Rect(WIDTH // 2, HEIGHT // 2, 25, 25)
font = pygame.font.Font(None, 72)
game_over_text = font.render("GAME OVER", True, (20, 50, 80))
text_rect = game_over_text.get_rect()
score = 0
border_thickness = 2
floor_random = [True] + [random.choice([True, False]) for i in range(2)]
for i in range(10):
    if not floor_random[-2] and not floor_random[-1]:
        floor_random.append(True)
    else:
        floor_random.append(random.choice([True, False]))
print(floor_random)

floor = [
    pygame.Rect(
        (
            WIDTH // 2 - border_thickness,
            HEIGHT // 2 + 25 - border_thickness,
            50 + 2 * border_thickness,
            20 + 2 * border_thickness,
        )
    )
]


def render_score(score):
    # Convert score to string and format with leading zeros
    score_str = f"Score: {score:.1f}"  # 05d formats to 5 digits with leading zeros

    # Render the text with the font and chosen color (white here)
    text_surface = font.render(score_str, True, (255, 255, 255))
    return text_surface


"""
Create a BACKGROUND object with your display surface and image.
"""
bg = BGScrolling.BACKGROUND(screen, pygame.image.load("example-background-1.jpg"))


"""
There are three modes you can choose from.
    - Mode 1 will place buffers on the sides, 
    - Mode 2 will place buffers on the top and botton,
    - Mode 3 will place buffers on all 8 surrounding faces.

Set to Mode 1 by default, feel free to play around!
"""

bg.set_mode(1)


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            quit()
            sys.exit()

    """
    Move the background with the move() function
    The move funtion takes a Vector2 object as a parameter

    Alternativly, you can use the move_y() and move_x() functions as demonstrated below
    """
    """
    keys = pygame.key.get_pressed()
    if keys[K_a] or keys[K_LEFT]:
        bg.move_x(20)
    if keys[K_d] or keys[K_RIGHT]:
        bg.move_x(-20)
    """

    bg.move_x(-velocity)
    player.x -= velocity
    floor.x -= velocity

    bg.update()  # This repositions the background

    screen.fill((0, 0, 0))

    bg.draw()  # Draws all the images

    pygame.draw.rect(screen, PLAYER_COLOR, player)
    if player.x < 0:
        screen.blit(game_over_text, text_rect)
        velocity = 0
    else:
        score += 0.1
        velocity += ACELERATION

    score_text = render_score(score)
    screen.blit(score_text, (2 * WIDTH // 3, 10))

    pygame.draw.rect(screen, BLACK, floor, border_thickness)

    pygame.display.update()
    clock.tick(30)
