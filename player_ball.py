import pygame, math
from baseball import BaseBall

pygame.init()
sound_hit = 'collision_sound.wav'
pygame.mixer.music.load(sound_hit)
pygame.mixer.music.set_volume(0.7)


class PlayerBall(BaseBall):

    def handle_collision_2d(self, other, mouse_speed_x, mouse_speed_y):
        distance, angle = self.distance(other)
        if self.check_collison_2d(other):
            m1, m2 = self.mass, other.mass
            v1x, v1y = mouse_speed_x, mouse_speed_y
            v2x, v2y = other.ball_speed_x, other.ball_speed_y
            if mouse_speed_x == 0:
                u2x = v2x * (-1)
            else:
                u2x = ((m2 - m1) * v2x + 2 * m1 * v1x) / (m1 + m2)
            if mouse_speed_y == 0:
                u2y = v2y * (-1)
            else:
                u2y = ((m2 - m1) * v2y + 2 * m1 * v1y) / (m1 + m2)

            other.ball_speed_x = u2x
            other.ball_speed_y = u2y

            overlap = (self.radius + other.radius) - distance
            other.x += overlap * math.cos(angle)
            other.y += overlap * math.sin(angle)

            pygame.mixer.music.play()
