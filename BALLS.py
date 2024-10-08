from ball_obj import BallObj
from playerball import PlayerBall
import random


class balls:

    def __init__(self):
        self.balls_list = []

    def new_player(self, gravity, radius, color, screen):
        ball = PlayerBall(screen.get_width() / 2, screen.get_height() / 2, gravity, radius, radius / 10, color,
                          id, screen)  # x,y,gravity,radius,mass,color,id
        self.balls_list.append(ball)

    def new_ball(self, gravity, radius, color, screen, x, y, id):
        if x and y:
            ball = BallObj(x, y, gravity, radius, radius / 10, color,
                           id, screen)  # x,y,gravity,radius,mass,color,id
        else:
            ball = BallObj(screen.get_width() / 2, screen.get_height() / 2, gravity, radius, radius / 10, color,
                           id, screen)  # x,y,gravity,radius,mass,color,id
        self.balls_list.append(ball)

    def add_ball(self, ball):
        self.balls_list.append(ball)

    def combine_balls_list(self, other_balls):
        new_list = self.balls_list
        for ball in other_balls.balls_list:
            self.add_ball(ball)
        return new_list

    def check_walls(self):
        for ball in self.balls_list:
            ball.check_wall_collision()

    def handle_collisions(self):
        for ball in self.balls_list:
            for other_ball in self.balls_list:
                if ball.id != other_ball.id:
                    ball.handle_collision_2d(other_ball)

    def handle_collisions_mouse(self,ball_list, mouse_speed_x, mouse_speed_y):
        for ball in ball_list:
            for other_ball in ball_list:
                if ball.id != other_ball.id:
                    if type(ball) is BallObj and type(other_ball) is BallObj:
                        ball.handle_collision_2d(other_ball)
                    elif type(ball) is PlayerBall:
                        ball.handle_collision_2d(other_ball, mouse_speed_x, mouse_speed_y)
                    else:
                        other_ball.handle_collision_2d(ball, mouse_speed_x, mouse_speed_y)

    def handle_collisions_other_grid(self, other_grid, mouse_speed_x, mouse_speed_y):
        temp_list = self.balls_list + other_grid.balls_list
        self.handle_collisions_mouse(temp_list, mouse_speed_x, mouse_speed_y)

    def restart(self):
        self.balls_list = [self.balls_list[0]]

    def change_gravity(self, gravity):
        id = self.balls_list[0].id
        for ball in self.balls_list:
            if ball.id != id:
                ball.gravity = gravity

    def how_much_balls(self):
        return len(self.balls_list)

    def draw_balls(self, screen):
        for ball in self.balls_list:
            ball.draw(screen)

    def draw_and_move_balls(self, screen):
        for ball in self.balls_list:
            ball.draw(screen)
            if type(ball) is BallObj:
                ball.move(screen)

    def is_exist(self, ball):
        place = 0
        for inside_ball in self.balls_list:
            place += 1
            if ball.id == inside_ball.id:
                return True, place
        return False

    def is_empty(self):
        if self.balls_list:
            return True
        return False

    def remove_ball(self, ball):
        self.balls_list.remove(ball)

    def get_ball_by_id(self, id):
        for ball in self.balls_list:
            if ball.id == id:
                return ball

    def __str__(self):
        return f"Balls : ({self.balls_list.__str__()})"
