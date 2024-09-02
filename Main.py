import time

import pygame, sys, random
from BALLS import balls
from playerball import PlayerBall
from ball_obj import BallObj
import numpy as np
from grid import Grid


def generate_gradient_steps(start_color, end_color, steps):
    gradient_steps = []

    # Interpolate the colors
    for i in range(steps):
        r = np.interp(i, [0, steps - 1], [start_color[0], end_color[0]])
        g = np.interp(i, [0, steps - 1], [start_color[1], end_color[1]])
        b = np.interp(i, [0, steps - 1], [start_color[2], end_color[2]])
        gradient_steps.append((int(r), int(g), int(b)))

    return gradient_steps


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Setup sound for hit

screen_width = 1280
screen_height = 980
screen = pygame.display.set_mode((screen_width, screen_height))
fps = 60
pygame.display.set_caption("tomySim")

# Colors
bg_color = pygame.Color('grey12')
light_grey = (200, 200, 200)

# Pyshics
gravity = 9.8

# Ball Attribute
radius = 50
# create the grid
grid = Grid(screen, 15)
# create the main ball
grid.new_player_to_grid(gravity=0, radius=radius, color=light_grey)
main_ball_index = grid.check_grid(screen_width / 2, screen_height / 2)
main_ball=grid.grids[main_ball_index].balls[0]

# Other features:
fps_flag = True
dragging = False
touched_ball = False
spawn_flag = False

# Mouse speed configuration:
mouse_speed_x, mouse_speed_y, max_speed_x, max_speed_y = 0, 0, 0, 0

# Define the start and end colors in RGB
start_color = (255, 0, 0)  # Red
end_color = (0, 0, 255)  # Blue
# Define the number of steps of color change
steps = 100
# Generate the gradient steps and print the RGB values
gradient_steps = generate_gradient_steps(start_color, end_color, steps)
loop_count = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if max(main_ball.x, mouse_x) - min(main_ball.x, mouse_x) < radius and max(main_ball.y, mouse_y) - min(
                        main_ball.y, mouse_y) < radius:
                    touched_ball = True
                else:
                    touched_ball = False
        if event.type == pygame.MOUSEMOTION:
            if dragging and touched_ball:
                mouse_speed_x, mouse_speed_y = event.rel
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Will Not Go More Than Bounderies
                main_ball.x = max(main_ball.radius, min(mouse_x, screen_width - main_ball.radius))
                main_ball.y = max(main_ball.radius, min(mouse_y, screen_height - main_ball.radius))
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # If you press a button:
        if event.type == pygame.KEYDOWN:
            # Movement Keys:
            if event.key == pygame.K_a:
                spawn_flag = True
            if event.key == pygame.K_h:
                grid.new_to_grid(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                                 gravity=gravity, radius=10,
                                 color=(
                                     255, 255,
                                     255))
            if event.key == pygame.K_j:
                grid.new_to_grid(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                                 gravity=gravity, radius=10,
                                 color=(220, 95, 0))
            if event.key == pygame.K_g:
                grid.new_to_grid(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                                 gravity=gravity, radius=random.randint(10, 30),
                                 color=(
                                     random.randint(0, 255), random.randint(0, 255),
                                     random.randint(0, 255)))
                grid.new_to_grid(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                                 gravity=gravity, radius=random.randint(10, 100),
                                 color=(220, 95, 0))
            if event.key == pygame.K_DOWN:
                main_ball.ball_speed_y = 10
            if event.key == pygame.K_UP:
                main_ball.ball_speed_y = -10
            if event.key == pygame.K_RIGHT:
                main_ball.ball_speed_x = 10
            if event.key == pygame.K_LEFT:
                main_ball.ball_speed_x = -10
            # Fetures Like Gravity Change:
            if event.key == pygame.K_9:
                if grid.count > 1:
                    gravity *= -1
                    grid.change_gravity(gravity)
                    print("Gravity Reversed")
                else:
                    print("Cant Change gravity, Add more ball by pressing A")
            if event.key == pygame.K_z:
                if fps_flag:
                    fps = 10
                    fps_flag = False
                else:
                    fps = 60
                    fps_flag = True
            if event.key == pygame.K_r:
                grid.restart()

        # If you release a button:
        if event.type == pygame.KEYUP:
            #controll with mouse
            # if event.key == pygame.K_DOWN:
            #     main_ball.ball_speed_y -= 10
            #     main_ball.ball_speed_x = 0
            # if event.key == pygame.K_UP:
            #     main_ball.ball_speed_y += 10
            #     main_ball.ball_speed_x = 0
            # if event.key == pygame.K_RIGHT:
            #     main_ball.ball_speed_x -= 10
            #     main_ball.ball_speed_y = 0
            # if event.key == pygame.K_LEFT:
            #     main_ball.ball_speed_x += 10
            #     main_ball.ball_speed_y = 0
            if event.key == pygame.K_a:
                spawn_flag = False
                print(grid.count)

    # Visuals
    screen.fill(bg_color)
    if spawn_flag:
        color_now = gradient_steps[loop_count]
        grid.new_to_grid(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                         gravity=gravity, radius=random.randint(10, 30),
                         color=color_now)
        if loop_count != steps - 1:
            loop_count += 1
        else:
            gradient_steps.reverse()
            loop_count = 0
    grid.check_collisions_grid(mouse_speed_x, mouse_speed_y)
    # Draw to screen
    grid.draw_and_move_balls()
    # Update Screen
    print(int(clock.get_fps()))  # print current fps
    pygame.display.flip()
    clock.tick(fps)
