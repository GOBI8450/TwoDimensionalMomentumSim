import pygame, math
from baseball import BaseBall

pygame.init()
sound_hit = 'collision_sound.wav'
pygame.mixer.music.load(sound_hit)
pygame.mixer.music.set_volume(0.7)


class BallObj(BaseBall):

    def check_wall_collision(self, screen_height, screen_width):
        if self.y >= screen_height - self.radius:
            self.ball_speed_y *= -1
            self.y = screen_height - self.radius
        elif self.y <= self.radius:
            self.ball_speed_y *= -1
            self.y = self.radius
        if self.x >= screen_width - self.radius:
            self.ball_speed_x *= -1
            self.x = screen_width - self.radius
        elif self.x <= self.radius:
            self.ball_speed_x *= -1
            self.x = self.radius

    def move(self, screen):
        self.check_wall_collision(screen.get_height(), screen.get_width())
        self.ball_speed_y += self.gravity * self.time
        self.x += self.ball_speed_x
        self.y += self.ball_speed_y

    def handle_collision_2d(self, other):
        distance, angle = self.distance(other)
        if self.check_collison_2d(other):
            m1, m2 = self.mass, other.mass
            v1x, v1y = self.ball_speed_x, self.ball_speed_y
            v2x, v2y = other.ball_speed_x, other.ball_speed_y
            x1, y1 = self.x, self.y
            x2, y2 = other.x, other.y

            u1x = ((m1 - m2) * v1x + 2 * m2 * v2x) / (m1 + m2)
            u2x = ((m2 - m1) * v2x + 2 * m1 * v1x) / (m1 + m2)
            u1y = ((m1 - m2) * v1y + 2 * m2 * v2y) / (m1 + m2)
            u2y = ((m2 - m1) * v2y + 2 * m1 * v1y) / (m1 + m2)

            self.ball_speed_x = u1x
            self.ball_speed_y = u1y
            other.ball_speed_x = u2x
            other.ball_speed_y = u2y

            overlap = (self.radius + other.radius) - distance
            other.x += overlap * math.cos(angle)
            other.y += overlap * math.sin(angle)

            pygame.mixer.music.play()
