import pygame
from constants import *
from player import *
import subprocess
from time import sleep
from asteroid import *
from asteroidfield import *
from shot import*
from powerup import PowerUp

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
    shots = pygame.sprite.Group()
    powerups = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable,drawable, shots)
    PowerUp.containers = (updatable, drawable, powerups)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    font = pygame.font.SysFont('Comic Sans MS', 30)

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0

    running = True
    pygame.event.pump()
    def draw_stats(screen, player):
        stats = [
            f"powerups: {player.powerup_count}",
            f"shield: {player.shield}",
            f"shoot speed: {player.shoot_speed}",
            f"move speed: {player.move_speed}",
            f"shoot cooldown: {player.shoot_cd}",
        ]

        for i, stat in enumerate(stats):
            text_surface = font.render(stat, True, "white")
            screen.blit(text_surface, (10, 10 + 30 * i))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player) and player.shield <= 0:
                print("Game over!")
                running = False
            elif asteroid.collides_with(player) and player.shield > 0:
                player.shield -= 1
                player.powerup_count -= 1
                print("Used a shield!")
                asteroid.split()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()
        for power_up in powerups:
            if power_up.collides_with(player):
                power_up.apply(player)
                power_up.kill()

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        draw_stats(screen, player)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

    pygame.quit()

if __name__ == "__main__":
    main()