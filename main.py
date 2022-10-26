import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Firetwerks")

FPS = 600
colors = [
    # rgb color values
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]


class Projectile:
    pass


class Firework:
    pass


class Launcher:
    WIDTH = 20
    HEIGHT = 20
    COLOR = "blue"

    def __init__(self, x, y, frequency):
        self.x = x
        self.y = y
        self.frequency = frequency


def draw():
    win.fill("black")
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()  # game clock

    while run:
        clock.tick(FPS)

        # loop through game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT -> red x pygame window
                run = False
                break

        draw()

    # quit pygame and python
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
