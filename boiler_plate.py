import pygame

pygame.init()

WIDTH, HEIGHT = 1600, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gaming")

FPS = 60


def main():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT -> red x pygame window
                run = False
                break

        # place rest of game code to run each tick in loop

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
