import pygame
from pygame import Vector2
from pygame.locals import *
import sys
import BGScrolling
import random

# AI
import cv2
import time
import HandTrackingModule as htm

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)


pTime = 0

detector = htm.handDetector(detectionCon=0.75)

tipIds = [8, 12, 16]

# pygame

pygame.init()

WIDTH, HEIGHT = 1200, 600
WIDTH_FLOOR, HEIGHT_FLOOR = 120, 40
PLAYER_SIZE = 40

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

PLAYER_COLOR = (125, 140, 200)
FLOOR_COLOR = (200, 240, 170)
BLACK = (0, 0, 0)
GRAVITY = 2
velocity = 6
speed_y = 0
speed_x = velocity
player = pygame.Rect(
    3 * WIDTH // 4 + PLAYER_SIZE, 3 * HEIGHT // 4, PLAYER_SIZE, PLAYER_SIZE
)
font = pygame.font.Font(None, 72)
game_over_text = font.render("GAME OVER", True, (20, 50, 80))
text_rect = game_over_text.get_rect()
score = 0
totalFingers = 0
border_thickness = 1
floor_boolean = [False, False]
floor = []
floor_border = []
for i in range(150):
    floor_border.append(
        pygame.Rect(
            (
                3 * WIDTH // 4 + i * WIDTH_FLOOR,
                3 * HEIGHT // 4 + PLAYER_SIZE,
                WIDTH_FLOOR,
                HEIGHT_FLOOR,
            )
        )
    )

    aux = floor_boolean[1]
    if not floor_boolean[0] and not floor_boolean[-1]:
        floor.append(
            pygame.Rect(
                (
                    3 * WIDTH // 4 + i * WIDTH_FLOOR,
                    3 * HEIGHT // 4 + PLAYER_SIZE,
                    WIDTH_FLOOR,
                    HEIGHT_FLOOR,
                )
            )
        )
        floor_boolean[1] = True
    else:
        if 1:  # random.choice([True, False]):
            floor.append(
                pygame.Rect(
                    (
                        3 * WIDTH // 4 + i * WIDTH_FLOOR,
                        3 * HEIGHT // 4 + PLAYER_SIZE,
                        WIDTH_FLOOR,
                        HEIGHT_FLOOR,
                    )
                )
            )
            floor_boolean[1] = True
        else:
            floor_boolean[1] = False
    floor_boolean[0] = aux


def render_score(score):
    # Convert score to string and format with leading zeros
    score_str = f"Score: {score:.1f}"  # 05d formats to 5 digits with leading zeros

    # Render the text with the font and chosen color (white here)
    text_surface = font.render(score_str, True, (255, 255, 255))
    return text_surface


"""
Create a BACKGROUND object with your display surface and image.
"""
bg = BGScrolling.BACKGROUND(screen, pygame.image.load("Gemini_Generated_Image (4).jpg"))


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
    # AI
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        fingers = []

        for id in tipIds:
            if lmList[id][2] < lmList[id - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        # print(fingers)
        totalFingers = fingers.count(1)

    img = cv2.resize(img, (200, 200))
    cv2.imshow("Image", img)
    cv2.waitKey(1)

    # pygame

    bg.update()  # This repositions the background

    screen.fill((0, 0, 0))

    bg.draw()  # Draws all the image

    pygame.draw.rect(screen, PLAYER_COLOR, player)

    for part in floor:
        pygame.draw.rect(screen, FLOOR_COLOR, part)

    for border in floor_border:
        pygame.draw.rect(screen, BLACK, border, border_thickness)

    if player.x < 0 or player.y > 3 * HEIGHT // 4 + 10:
        screen.blit(game_over_text, text_rect)
    else:
        score += 0.1
        bg.move_x(-velocity)
        player.x -= speed_x
        player.y += speed_y
        speed_y += GRAVITY

        for part in floor:
            part.x -= velocity
            if player.colliderect(part):
                speed_y = 0
                speed_x = velocity
                if totalFingers == 1:
                    player.x += 0
                    speed_y = -14
                    speed_x = -2
                if totalFingers == 2:
                    player.x += 8
                    speed_y = -28
                    speed_x = -2
                if totalFingers == 3:
                    player.x -= 0
                    speed_y = -44
                    speed_x = -2

        for border in floor_border:
            border.x -= velocity

    score_text = render_score(score)
    screen.blit(score_text, (2 * WIDTH // 3, 10))

    pygame.display.update()
    clock.tick(30)
