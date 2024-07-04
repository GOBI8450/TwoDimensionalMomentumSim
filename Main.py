import pygame, sys, random
from BALLS import balls

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

balls_list = balls()
balls_list.new_ball_exact_mass(gravity=0, radius=radius, mass=1, color=light_grey, screen=screen)
main_ball = balls_list.balls[0]

# Other features:
fps_flag = True
dragging = False
touched_ball = False
spawn_flag = False

# Mouse speed configuration:
max_speed_x = 0
max_speed_y = 0
mouse_speed_x, mouse_speed_y, max_speed_x, max_speed_y = 0, 0, 0, 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                dragging = True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                print(mouse_x + main_ball.radius)
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
                balls_list.new_ball_exact_pos(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                                              gravity=gravity, radius=random.randint(10, 100),
                                              color=(
                                                  random.randint(0, 255), random.randint(0, 255),
                                                  random.randint(0, 255)),
                                              screen=screen)
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
                if len(balls_list.balls) > 1:
                    balls_list.change_gravity(balls_list.balls[1].gravity * -1)
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
                balls_list.restart()

        # If you release a button:
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                balls_list.balls[0].ball_speed_y -= 10
                balls_list.balls[0].ball_speed_x = 0
            if event.key == pygame.K_UP:
                balls_list.balls[0].ball_speed_y += 10
                balls_list.balls[0].ball_speed_x = 0
            if event.key == pygame.K_RIGHT:
                balls_list.balls[0].ball_speed_x -= 10
                balls_list.balls[0].ball_speed_y = 0
            if event.key == pygame.K_LEFT:
                balls_list.balls[0].ball_speed_x += 10
                balls_list.balls[0].ball_speed_y = 0
            if event.key == pygame.K_a:
                spawn_flag = False

    # Visuals
    screen.fill(bg_color)
    if spawn_flag:
        balls_list.new_ball_exact_pos(x=random.randint(0, screen_width), y=random.randint(0, screen_height),
                                      gravity=gravity, radius=random.randint(10, 30),
                                      color=(
                                          random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                      screen=screen)
    balls_list.handle_collisions(mouse_speed_x, mouse_speed_y)
    main_ball.draw(screen)
    for ball in balls_list.balls[1:]:
        ball.draw(screen)
        ball.move(screen)

    # Update Screen
    pygame.display.flip()
    clock.tick(fps)
