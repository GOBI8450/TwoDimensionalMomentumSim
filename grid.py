import math
from BALLS import balls
from baseball import BaseBall
from playerball import PlayerBall
from ball_obj import BallObj


class Grid:

    def __init__(self, screen, grid_count):
        self.count = 0
        self.screen = screen
        self.grid_count = grid_count
        # Initialize screen_container with empty lists
        self.grids = [balls() for _ in range(
            grid_count * grid_count)]  # Create an empty balls list, every object of the list is balls type.
        # Calculate grid cell dimensions
        self.grid_height = screen.get_height() / grid_count
        self.grid_width = screen.get_width() / grid_count

    def check_grid(self, x, y):
        # Calculate which grid cell the point (x, y) falls into
        grid_x = min(math.floor(x / self.grid_width), self.grid_count - 1)
        grid_y = min(math.floor(y / self.grid_height), self.grid_count - 1)
        index_grid = grid_y * self.grid_count + grid_x
        return index_grid

    def add_to_grid(self, ball):
        index_grid = self.check_grid(ball.x, ball.y)
        self.grids[index_grid].balls.append(ball)

    def add_player_to_grid(self, ball):
        index_grid = self.check_grid(ball.x, ball.y)
        self.grids[index_grid].balls.insert(0, ball)

    def new_to_grid(self, x, y, gravity, radius, color):
        self.count += 1
        index_grid = self.check_grid(x, y)
        self.grids[index_grid].new_ball(gravity, radius, color, self.screen, x, y, self.count)

    def new_player_to_grid(self, gravity, radius, color):
        self.count += 1
        index_grid = self.check_grid(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.grids[index_grid].new_player(gravity, radius, color, self.screen)

    def remove_ball_from_grid_by_id(self, grid_index, ball_id):
        ball = self.grids[grid_index].get_ball_by_id(ball_id)
        self.grids[grid_index].remove_ball(ball)

    # def rearrange_grids(self):
    #     for grid in self.grids:
    #         for ball in grid.balls:
    #             grid_index = self.check_grid(ball.x, ball.y)
    #             self.grids[grid_index].balls.append(ball)

    def rearrange_grids(self):
        new_grids = [balls() for _ in range(self.grid_count * self.grid_count)]  # Create a balls object for every grid
        for grid in self.grids:
            for ball in grid.balls:
                index_grid = self.check_grid(ball.x, ball.y)
                new_grids[index_grid].balls.append(ball)
        self.grids = new_grids

    def check_collisions_grid(self, mouse_speed_x, mouse_speed_y):
        self.rearrange_grids()
        row = 0
        column = 0
        for grid in self.grids:
            row += 1
            grid_x = min(math.floor(row / self.grid_width), self.grid_count - 1)
            grid_y = min(math.floor(column / self.grid_height), self.grid_count - 1)
            if grid.balls:
                balls.handle_collisions_mouse(self.get_near_grids(grid_x, grid_y), mouse_speed_x, mouse_speed_y) #####################mouse?
            if row == self.grid_count:
                row = 0
                column += 1

    def change_gravity(self, gravity):
        for grid in self.grids:
            grid.change_gravity(gravity)

    def restart(self):
        for grid in self.grids:
            if grid.balls:
                if type(grid.balls[0]) is PlayerBall:
                    grid.restart()
                else:
                    grid.balls = []

    def draw_and_move_balls(self):
        for grid in self.grids:
            for ball in grid.balls:
                if type(ball) is BallObj:
                    grid.draw_and_move_balls(self.screen)
                else:
                    grid.draw_balls(self.screen)

    def get_near_grids(self, grid_x, grid_y):
        near_grids = balls()

        # Check grid above
        if grid_y > 0:
            near_grids.combine_balls_list(self.grids[(grid_y - 1) * self.grid_count + grid_x])

        # Check grid below
        if grid_y < self.grid_count - 1:
            near_grids.combine_balls_list(self.grids[(grid_y + 1) * self.grid_count + grid_x])

        # Check grid to the left
        if grid_x > 0:
            near_grids.combine_balls_list(self.grids[grid_y * self.grid_count + (grid_x - 1)])

        # Check grid to the right
        if grid_x < self.grid_count - 1:
            near_grids.combine_balls_list(self.grids[grid_y * self.grid_count + (grid_x + 1)])

        # Check grid diagonally: top-left
        if grid_y > 0 and grid_x > 0:
            near_grids.combine_balls_list(self.grids[(grid_y - 1) * self.grid_count + (grid_x - 1)])

        # Check grid diagonally: top-right
        if grid_y > 0 and grid_x < self.grid_count - 1:
            near_grids.combine_balls_list(self.grids[(grid_y - 1) * self.grid_count + (grid_x + 1)])

        # Check grid diagonally: bottom-left
        if grid_y < self.grid_count - 1 and grid_x > 0:
            near_grids.combine_balls_list(self.grids[(grid_y + 1) * self.grid_count + (grid_x - 1)])

        # Check grid diagonally: bottom-right
        if grid_y < self.grid_count - 1 and grid_x < self.grid_count - 1:
            near_grids.combine_balls_list(self.grids[(grid_y + 1) * self.grid_count + (grid_x + 1)])

        return near_grids
