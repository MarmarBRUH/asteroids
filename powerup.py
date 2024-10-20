import pygame
import random
from constants import *
from circleshape import CircleShape

# global variables
power_up_start_time = None

class PowerUp(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.type = random.choice(['shot_speed', 'shot_cd', 'move_speed', 'shield', 'shot_radius'])
        self.notification_start_time = None
        self.notification_message = None
    def draw(self, screen):
        pygame.draw.circle(screen, "red", self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def draw_notification(self, screen, font):
        if self.notification_start_time is not None:
            elapsed = pygame.time.get_ticks() - self.notification_start_time
            if elapsed < PWR_DISPLAY_TIME:
                text_surface = font.render(self.notification_message, True, "white")
                screen.blit(text_surface, (self.position.x - 50, self.position.y + 50))
            else:
                self.notification_start_time = None
                self.notification_message = None

    def apply(self, player, screen, font):
        if self.type == 'shot_speed':
            player.shoot_speed += 10
            player.powerup_count += 1
            self.notification_message = "Projectile speed +10"
        elif self.type == 'shot_cd':
            if player.shoot_cd > 0.1:
                player.shoot_cd -= 0.01
                player.powerup_count += 1
                self.notification_message = "Projectile shooting cooldown -0.01"
            else:
                print("Powerup not applied! Value too low!")
                self.type = random.choice(['shot_speed', 'move_speed', 'shield', 'shot_radius'])
                self.apply(player, screen, font)
        elif self.type == 'move_speed':
            player.move_speed += 10
            player.powerup_count += 1
            self.notification_message = "Move speed +10"
        elif self.type == 'shield':
            if player.shield < 3:
                player.shield += 1
                player.powerup_count += 1
                self.notification_message = "Shield +1"
            else:
                print("Powerup not applied! Value too high!")
                self.type = random.choice(['shot_speed', 'move_speed', 'shot_cd', 'shot_radius'])
                self.apply(player, screen, font)
        elif self.type == 'shot_radius':
            if player.shot_radius < 10:
                player.shot_radius += 1
                player.powerup_count += 1
                self.notification_message = "Projectile radius +1"
            else:
                print("Powerup not applied! Value too high!")
                self.type = random.choice(['shot_speed', 'move_speed', 'shield', 'shot_cd'])
                self.apply(player, screen, font)
        print("Powerup applied!")
        print(f"Powerup type: {self.type}")
        print(f"Powerup count: {player.powerup_count}")

        self.notification_start_time = pygame.time.get_ticks()
        self.draw_notification(screen, font)
