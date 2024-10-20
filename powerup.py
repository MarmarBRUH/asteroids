import pygame
import random
from constants import *
from circleshape import CircleShape

class PowerUp(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.type = random.choice(['shot_speed', 'shot_cd', 'move_speed'])
    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def apply(self, player):
        if self.type == 'shot_speed':
            player.shoot_speed += 10
            player.powerup_count += 1
        elif self.type == 'shot_cd':
            if player.shoot_cd > 0.1:
                player.shoot_cd -= 0.01
                player.powerup_count += 1
            else:
                print("Powerup not applied! Value too low!")
                self.type = random.choice(['shot_speed', 'move_speed'])
                self.apply(player)
        elif self.type == 'move_speed':
            player.move_speed += 10
            player.powerup_count += 1
        print("Powerup applied!")
        print(f"Powerup type: {self.type}")
        print(f"Powerup count: {player.powerup_count}")