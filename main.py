import pygame
from constants import *

def main():
    pygame.init()
    print("Starting asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    running = True  # Main loop flag
    while running:
        for event in pygame.event.get():  # Event loop to handle window events
            if event.type == pygame.QUIT:  # If the user clicks the close button
                running = False  # Exit the loop to close the window

        screen.fill("black")  # Fill the screen with black
        pygame.display.flip()  # Update the screen display
    
    pygame.quit()

if __name__ == "__main__":
    main()