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

    def get_grid_index(self, x, y):
        # Calculate which grid cell the point (x, y) falls into
        grid_x, grid_y = self.get_grid_x_y(x, y)
        index_grid = grid_y * self.grid_count + grid_x
        return index_grid

    def get_grid_x_y(self, x, y):
        grid_x = min(math.floor(x / self.grid_width), self.grid_count - 1)
        grid_y = min(math.floor(y / self.grid_height), self.grid_count - 1)
        return grid_x, grid_y

    def add_to_grid(self, ball):
        index_grid = self.get_grid_index(ball.x, ball.y)
        self.grids[index_grid].balls_list.append(ball)

    def add_player_to_grid(self, ball):
        index_grid = self.get_grid_index(ball.x, ball.y)
        self.grids[index_grid].balls_list.insert(0, ball)

    def new_to_grid(self, x, y, gravity, radius, color):
        self.count += 1
        index_grid = self.get_grid_index(x, y)
        self.grids[index_grid].new_ball(gravity, radius, color, self.screen, x, y, self.count)

    def new_player_to_grid(self, gravity, radius, color):
        self.count += 1
        index_grid = self.get_grid_index(self.screen.get_width() / 2, self.screen.get_height() / 2)
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
            for ball in grid.balls_list:
                index_grid = self.get_grid_index(ball.x, ball.y)
                new_grids[index_grid].add_ball(ball)
        self.grids = new_grids

    def handle_grid(self, mouse_speed_x,
                    mouse_speed_y):  # The Most Important Function. checks collison with every ball
        index = 0
        for current_grid in self.grids:
            grid_x = index % self.grid_count  # Calculate grid_x from index
            grid_y = index // self.grid_count  # Calculate grid_y from index
            if current_grid.balls_list:
                current_grid.handle_collisions_other_grid(self.get_near_grids(grid_x, grid_y), mouse_speed_x,
                                                          mouse_speed_y)
            index += 1
        self.rearrange_grids()

    def change_gravity(self, gravity):
        for grid in self.grids:
            grid.change_gravity(gravity)

    def restart(self):
        for grid in self.grids:
            if grid.balls_list:
                if type(grid.balls_list[0]) is PlayerBall:
                    grid.restart()
                else:
                    grid.balls_list = []

    def draw_and_move_balls(self):
        for grid in self.grids:
            for ball in grid.balls_list:
                if type(ball) is BallObj:
                    grid.draw_and_move_balls(self.screen)
                else:
                    grid.draw_balls(self.screen)

    def get_near_grids(self, grid_x, grid_y):
        near_grids = balls()
        if not self.grids[grid_y * self.grid_count + grid_x].is_empty():
            return near_grids  # No balls?
        grid_count = self.grid_count

        # Above and below grids
        if grid_y > 0:  # Above
            near_grids.combine_balls_list(self.grids[(grid_y - 1) * grid_count + grid_x])
        if grid_y < grid_count - 1:  # Below
            near_grids.combine_balls_list(self.grids[(grid_y + 1) * grid_count + grid_x])

        # Left and right grids
        if grid_x > 0:  # Left
            near_grids.combine_balls_list(self.grids[grid_y * grid_count + (grid_x - 1)])
        if grid_x < grid_count - 1:  # Right
            near_grids.combine_balls_list(self.grids[grid_y * grid_count + (grid_x + 1)])

        # Diagonal grids
        if grid_y > 0 and grid_x > 0:  # Top-left
            near_grids.combine_balls_list(self.grids[(grid_y - 1) * grid_count + (grid_x - 1)])
        if grid_y > 0 and grid_x < grid_count - 1:  # Top-right
            near_grids.combine_balls_list(self.grids[(grid_y - 1) * grid_count + (grid_x + 1)])
        if grid_y < grid_count - 1 and grid_x > 0:  # Bottom-left
            near_grids.combine_balls_list(self.grids[(grid_y + 1) * grid_count + (grid_x - 1)])
        if grid_y < grid_count - 1 and grid_x < grid_count - 1:  # Bottom-right
            near_grids.combine_balls_list(self.grids[(grid_y + 1) * grid_count + (grid_x + 1)])

        return near_grids
