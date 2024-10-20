import pygame
from constants import *
from player import *
import subprocess
from time import sleep
from asteroid import *
from asteroidfield import *
from shot import*
from powerup import PowerUp
from paths import *
from stats import Statistics as S

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
    active_notifs = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable,drawable, shots)
    PowerUp.containers = (updatable, drawable, powerups)

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroidfield = AsteroidField()
    font = pygame.font.SysFont('Comic Sans MS', 30)
    path = paths()
    stats = S()

    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    dt = 0
    accumulated_dt = 0
    SHIELDS_USED = 0
    KILLS = 0
    TOTAL_SHOTS = 0
    TOTAL_POWERUPS = 0
    TIME_PLAYED = 0
    

    running = True
    pygame.event.pump()
    def draw_stats(screen, player):
        stats = [
            f"powerups: {player.powerup_count}",
            f"shield: {player.shield}",
            f"shoot speed: {player.shoot_speed}",
            f"move speed: {player.move_speed}",
            f"shoot cooldown: {round(player.shoot_cd, 2)}",
            f"shot radius: {player.shot_radius}",
            f"score: {round(player.score, 1)}",
            f"highscore: {round(highscore, 1)}"
        ]

        for i, stat in enumerate(stats):
            text_surface = font.render(stat, True, "white")
            screen.blit(text_surface, (10, 10 + 30 * i))
    def end_screen():
        active = True
        endstats = [
            f"total powerups: {TOTAL_POWERUPS}",
            f"shields used: {SHIELDS_USED}",
            f"kills: {KILLS} asteroids killed",
            f"total shots: {player.total_shots} projectiles shot",
            f"time played: {TIME_PLAYED} seconds",
            f"score: {round(player.score, 1)}",
            f"highscore: {round(highscore, 1)}"
        ]

        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            screen.fill("white")
            font = pygame.font.SysFont('Arial', 30)
            font2 = pygame.font.SysFont('Arial', 90)

            text_surface = font2.render("Game Over", True, "black")
            screen.blit(text_surface, (SCREEN_WIDTH / 2 - 120, SCREEN_HEIGHT / 2 - 300))
            for i, stat in enumerate(endstats):
                text_surface = font.render(stat, True, "black")
                screen.blit(text_surface, (SCREEN_WIDTH / 2 - 90, 350 + 30 * i))
            text_surface = font.render("Press SPACE to restart", True, "black")
            screen.blit(text_surface, (SCREEN_WIDTH / 6, 450))
            text_surface = font.render("Press Q to quit", True, "black")
            screen.blit(text_surface, (SCREEN_WIDTH / 6, 430))
            pygame.display.flip()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                active = False
                main()
            elif pygame.key.get_pressed()[pygame.K_q]:
                exit()
            sleep(0.01)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        for obj in updatable:
            obj.update(dt)
       ## stats.update(player.score, player.kills, player.powerups, player.shields_used, player.time_played, player.total_shots)
        for asteroid in asteroids:
            if asteroid.collides_with(player) and player.shield <= 0:
                print("Game over!")
                stats.update(time_played = accumulated_dt, kills = KILLS, shields_used = SHIELDS_USED, powerup_count = player.powerup_count, shots_fired = TOTAL_SHOTS)
                running = False
                end_screen()
            elif asteroid.collides_with(player) and player.shield > 0:
                player.shield -= 1
                player.powerup_count -= 1
                SHIELDS_USED += 1
                print("debug // used a shield")
                asteroid.split()

            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    KILLS += 1
                    asteroid.split()
                    player.score += 1
        for power_up in powerups:
            if power_up.collides_with(player):
                power_up.apply(player, screen, font)
                TOTAL_POWERUPS += 1
                active_notifs.add(power_up)
                powerups.remove(power_up)
                drawable.remove(power_up)
                player.score += 0.2

        screen.fill("black")

        for obj in drawable:
            obj.draw(screen)
        
        for notification in active_notifs:
            notification.draw_notification(screen, font)
            if notification.notification_start_time is None:
                active_notifs.remove(notification)
        if accumulated_dt >= 1:
            player.score += random.uniform(0.2, 1)
            TIME_PLAYED += 1
            accumulated_dt = 0
        try:
            with open(path.highscore, "r") as f:
                highscore = float(f.read())
                if player.score > highscore:
                    with open(path.highscore, "w") as f:
                        f.write(str(player.score))
                        f.close()
        except FileNotFoundError:
            print("File not found")
            f.close()       
        draw_stats(screen, player)
        stats.update(time_played = TIME_PLAYED, kills = KILLS, shields_used = SHIELDS_USED, powerup_count = TOTAL_POWERUPS, shots_fired = TOTAL_SHOTS)

        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000
        accumulated_dt += dt
if __name__ == "__main__":
    main()