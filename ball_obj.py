import pygame
import random
import math

#Create pygame music module and load hit sound
pygame.init()
sound_hit='collision_sound.wav'
pygame.mixer.music.load(sound_hit)
pygame.mixer.music.set_volume(0.7)


#create balls class


class Ball:
    time = 1 / 60
    ball_speed_x = 0
    ball_speed_y = 0
    count_balls = 0
    pos_x = ball_speed_x * time
    pos_y = ball_speed_y * time

    def __init__(self, ball_speed_x, ball_speed_y, acceleration_y, radius, screen_height, screen_width, mass, mode):
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.acceleration_y = acceleration_y
        self.radius = radius
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.mass = mass
        if mode == 1:
            self.ball = pygame.Rect(screen_width / 2 - radius / 2, screen_height / 2 - radius / 2, radius, radius)
        else:
            self.ball = pygame.Rect(random.randint(200, 1000), screen_height / 2 - radius / 2, radius, radius)
        Ball.count_balls += 1

    def ball_collision(self, ball2_obj):
        if self.ball.bottom >= self.screen_height or self.ball.top <= 0:
            self.ball_speed_y *= -1
        if self.ball.left <= 0 or self.ball.right >= self.screen_width:
            self.ball_speed_x *= -1
        self.ball_collision_2balls(ball2_obj)
        return self.ball_speed_x, self.ball_speed_y

    def ball_collision_2balls(self, ball2_obj):
        m1 = ball2_obj.mass
        m2 = self.mass
        v1 = self.ball_speed_x
        v2 = ball2_obj.ball_speed_x
        v1_y = self.ball_speed_y
        v2_y = ball2_obj.ball_speed_y
        distance = self.distance(ball2_obj)
        print("distance=", distance)
        if distance <= (self.radius / 2) + (ball2_obj.radius / 2):
            self.ball_speed_x = ((m1 - m2) * v1 + 2 * m2 * v2) / (m1 + m2)
            ball2_obj.ball_speed_x = ((m2 - m1) * v2 + 2 * m1 * v1) / (m1 + m2)
            self.ball_speed_y = ((m1 - m2) * v1_y + 2 * m2 * v2_y) / (m1 + m2)
            ball2_obj.ball_speed_y = ((m2 - m1) * v2_y + 2 * m1 * v1_y) / (m1 + m2)
            print("!!!!!!!!!!!!!!!!HIT!!!!!!!!!!!!!!!!HIT")
            pygame.mixer.music.play()

        return self.ball_speed_x, self.ball_speed_y

    def ball_animation(self, ball2_obj):
        # Pyhsics
        self.ball_speed_y += self.acceleration_y * self.time
        self.ball.x += self.ball_speed_x
        self.ball.y += self.ball_speed_y
        self.ball_collision(ball2_obj)
        return self.ball_speed_x, self.ball_speed_y

    def ball_restart(self):
        self.ball.center = (self.screen_width / 2, self.screen_height / 2)
        self.ball_speed_x = 3 * random.choice((1, -1))
        self.ball_speed_y = 7

    # update:
    def update(self, ball_speed_x, ball_speed_y, ball):
        self.ball_speed_x = ball_speed_x
        self.ball_speed_y = ball_speed_y
        self.ball = ball

    def set_speed_x(self, ball_speed_x):
        self.ball_speed_x = ball_speed_x

    def set_speed_y(self, ball_speed_y):
        self.ball_speed_y = ball_speed_y

    def x_pos(self):
        return self.ball.centerx

    def y_pos(self):
        return self.ball.centery

    def distance(self, ball2_obj):
        self_x = self.x_pos()
        self_y = self.y_pos()
        ball2_x = ball2_obj.x_pos()
        ball2_y = ball2_obj.y_pos()
        # print("x=", self_x)
        # print("y=", self_y)
        # print("x2=", ball2_x)
        # print("y2=", ball2_y)
        return math.sqrt((ball2_y - self_y) ** 2 + (ball2_x - self_x) ** 2)
