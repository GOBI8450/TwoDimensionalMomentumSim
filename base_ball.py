import pygame, random, math

pygame.init()
sound_hit = 'collision_sound.wav'
pygame.mixer.music.load(sound_hit)
pygame.mixer.music.set_volume(0.7)


class BASE_BALL:
    time = 1 / 60

    def __init__(self, x, y, gravity, radius, mass, color, id, screen):
        self.x = x
        self.y = y
        self.gravity = gravity
        self.radius = radius
        self.mass = mass
        self.color = color
        self.ball_speed_x = 0
        self.ball_speed_y = 0
        self.hit_flag = False
        self.id = id
        self.ball = pygame.Rect(screen.get_width() / 2 - radius / 2, screen.get_height() / 2 - radius / 2, radius,
                                radius)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def distance(self, other):
        x1, y1 = self.x, self.y
        x2, y2 = other.x, other.y
        return math.sqrt((other.y - self.y) ** 2 + (other.x - self.x) ** 2), math.atan2(other.y - self.y,
                                                                                        other.x - self.x)

    def check_collison_2d(self, other):
        distance, angle = self.distance(other)
        if distance <= other.radius + self.radius:
            print("HIT")
            return True
        return False
