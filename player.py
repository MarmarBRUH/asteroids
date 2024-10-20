import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot
from powerup import PowerUp


class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.move_speed = PLAYER_SPEED
        self.shoot_speed = PLAYER_SHOOT_SPEED
        self.shoot_cd = PLAYER_SHOOT_COOLDOWN
        self.powerup_count = 0
        self.shield = PLAYER_SHIELD
        self.shot_radius = SHOT_RADIUS
        self.score = 0

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), 2)

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        if keys[pygame.K_p]:
         power_up = PowerUp(self.position.x, self.position.y, POWERUP_RADIUS)
    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = self.shoot_cd
        shot = Shot(self.position.x, self.position.y, self.shot_radius)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * self.shoot_speed

    def rotate(self, dt):
        self.rotation += (self.move_speed * 0.80) * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * self.move_speed * dt
