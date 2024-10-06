import pygame
from constants import *
from player import *
import subprocess
from time import sleep
from asteroid import *
from asteroidfield import *

def start_xming():
    xming_command = r'powershell.exe Start-Process "Q:\Apps\Xming\Xming.exe" -ArgumentList "-ac"'
    subprocess.Popen(xming_command.split(), shell=False)
def main():
    start_xming()
    sleep(1.5)
    pygame.init()
    clock = pygame.time.Clock()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill("black")
        dt = clock.tick(60) / 1000
        for group in updatable:
            group.update(dt)
        for asteroid in asteroids:
            if player.collision(asteroid):
                print(" =============== Game over ===============")
                running = False
        for group in drawable:
            group.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()