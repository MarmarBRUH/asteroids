import pygame
from circleshape import *
from constants import *

class Shot(CircleShape):
    def __init__(self, x, y, direction):
        super().__init__(x, y, SHOT_RADIUS)
        self.SHOT_RADIUS = 5
        self.velocity = pygame.Vector2(0, -1).rotate(direction) * PLAYER_SHOOT_SPEED
    
    def draw(self, screen):
        pygame.draw.circle(screen, "white", (self.position.x, self.position.y), self.radius, 2)
        
    def update(self, dt):
        self.position += self.velocity * dt
    
    def collision(self, other_obj):
        distance = pygame.math.Vector2.distance_to(self.position, other_obj.position)
        return distance <= self.radius + other_obj.radius