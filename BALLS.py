import pygame
import math
from ball_obj import Ball
from player_ball import PLAYER_BALL


class balls:

    def __init__(self):
        self.balls = []

    def new_ball(self, gravity, radius, color, screen):
        ball = PLAYER_BALL(screen.get_width() / 2, screen.get_height() / 2, gravity, radius, radius/10, color,
                    len(self.balls) + 1, screen)  # x,y,gravity,radius,mass,color,id
        self.balls.append(ball)

    def new_ball_exact_mass(self, gravity, radius, color,mass, screen):
        ball = PLAYER_BALL(screen.get_width() / 2, screen.get_height() / 2, gravity, radius, mass, color,
                    len(self.balls) + 1, screen)  # x,y,gravity,radius,mass,color,id
        self.balls.append(ball)

    def new_ball_exact_pos(self, x, y, gravity, radius, color, screen):
        ball = Ball(x, y, gravity, radius, radius/10, color, len(self.balls) + 1, screen)  # x,y,gravity,radius,mass,color,id
        self.balls.append(ball)

    def check_walls(self):
        for ball in self.balls:
            ball.check_wall_collision()

    def handle_collisions(self,mouse_speed_x,mouse_speed_y):
        for ball in self.balls:
            for other_ball in self.balls:
                if ball.id != other_ball.id:
                    if type(ball) is Ball and type(other_ball) is Ball:
                        ball.handle_collision_2d(other_ball)
                    elif type(ball) is PLAYER_BALL:
                        ball.handle_collision_2d(other_ball,mouse_speed_x,mouse_speed_y)
                    else:
                        other_ball.handle_collision_2d(ball,mouse_speed_x,mouse_speed_y)

    def restart(self):
        self.balls = [self.balls[0]]

    def change_gravity(self, gravity):
        id = self.balls[0].id
        for ball in self.balls:
            if ball.id != id:
                ball.gravity = gravity
