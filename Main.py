import random
import pygame, sys

from ball_obj import Ball


def update_text(ball):
    return font.render('Ball 1 speed x=' + str(ball.ball_speed_x), True, 'white', bg_color), font.render(
        'Ball 1 speed y=' + str(ball.ball_speed_y), True, 'white', bg_color)


def moving_ball(ball_obj, ball2_obj):
    ball_speed_x, ball_speed_y = ball_obj.ball_animation(ball2_obj)
    return ball_speed_x, ball_speed_y


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

#Setup sound for hit


screen_width = 1280
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
framer = 60
pygame.display.set_caption("tomySim")

# Ball rectangle
# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Pyshics
ball_speed_x = 0
ball_speed_y = 0
accelaration_y = 9.8
opponent_speed = 7
radius = 30

ball_object = Ball(ball_speed_x=ball_speed_x, ball_speed_y=ball_speed_y, acceleration_y=accelaration_y, radius=radius,
                   screen_height=screen_height, screen_width=screen_width, mass=1, mode=1)
ball = ball_object.ball
ball_object2 = Ball(ball_speed_x=ball_speed_x, ball_speed_y=ball_speed_y, acceleration_y=accelaration_y, radius=radius,
                    screen_height=screen_height, screen_width=screen_width, mass=1, mode=12)
ball2 = ball_object2.ball

# text:
font = pygame.font.Font('freesansbold.ttf', 32)
text_speed = font.render('', True, 'white', bg_color)
textRect_x = text_speed.get_rect()
textRect_y = text_speed.get_rect()
textRect_x.center = (200, 100)
textRect_y.center = (screen_height - 500, 100)

textRect_x2 = text_speed.get_rect()
textRect_y2 = text_speed.get_rect()
textRect_x2.center = (200, 200)
textRect_y2.center = (screen_height - 400, 200)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                while ball_speed_x < 0:
                    ball_speed_x += 1
                ball_speed_x += 5
            if event.key == pygame.K_LEFT:
                while ball_speed_x > 0:
                    ball_speed_x -= 1
                ball_speed_x -= 5
            if event.key == pygame.K_0:
                ball_object.ball_restart()
                ball_object.update(ball_speed_x, ball_speed_y, ball)
                print("0")
            if event.key == pygame.K_9:
                ball_object.acceleration_y *= -1
                ball_object.update(ball_speed_x, ball_speed_y, ball)
                print("Gravity changed")
            if event.key == pygame.K_p:
                ball_object.acceleration_y +=1
                ball_object.update(ball_speed_x, ball_speed_y, ball)
                print("Gravity +1")
            if event.key == pygame.K_m:
                ball_object.acceleration_y -= 1
                ball_object.update(ball_speed_x, ball_speed_y, ball)
                print("Gravity -1")
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                ball_speed_x -= 5
            if event.key == pygame.K_LEFT:
                ball_speed_x += 5
    ball_object.update(ball_speed_x, ball_speed_y, ball)
    #ball_speed_x, ball_speed_y = ball_object.ball_animation(ball_object2)
    ball_speed_x, ball_speed_y=moving_ball(ball_object, ball_object2)
    ball_speed_x2, ball_speed_y2=moving_ball(ball_object2, ball_object)
    ball_object2.update(ball_speed_x2,ball_speed_y2, ball_object2.ball)
    ball_object.update(ball_speed_x, ball_speed_y, ball)
    # Visuals
    screen.fill(bg_color)
    pygame.draw.ellipse(screen, light_grey, ball)
    pygame.draw.ellipse(screen, "red", ball2)
    pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0), (screen_width / 2, screen_height))

    # Text
    text_speed_x,text_speed_y=update_text(ball_object)
    text_speed_x2,text_speed_y2=update_text(ball_object2)
    screen.blit(text_speed_x, textRect_x)
    screen.blit(text_speed_y, textRect_y)
    screen.blit(text_speed_x2, textRect_x2)
    screen.blit(text_speed_y2, textRect_y2)

    # Update Screen
    pygame.display.flip()
    clock.tick(60)
