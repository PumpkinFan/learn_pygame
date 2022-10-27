import pygame
import numpy as np

pygame.init()

WIDTH, HEIGHT = 1600, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("gaming")

FPS = 60

COLORS = [
    # rgb color values
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

GRAVITY = 0.5


class Ball:
    RADIUS = 50

    def __init__(self, x, y, color, x_vel=0, y_vel=0):
        self.x = x
        self.y = y
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel

    def move(self):
        if (self.y + self.RADIUS) >= HEIGHT:
            self.y_vel = -self.y_vel
        self.x += self.x_vel
        self.y += self.y_vel
        self.y_vel += GRAVITY

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)


def draw(items):
    # WIN.fill("white")
    for item in items:
        item.draw(WIN)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 32)

    items = [Ball(WIDTH / 2, HEIGHT / 2, "darkblue")]
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT -> red x pygame window
                run = False
                break

        # place rest of game code to run each tick in loop
        ball = items[0]
        kinetic_energy = 0.5 * ball.y_vel**2
        potential_energy = GRAVITY * (HEIGHT - ball.y)
        vel_text = font.render(
            f"total energy = {kinetic_energy + potential_energy:.2f}",
            True,
            "black",
            "white",
        )
        text_rect = vel_text.get_rect()
        text_rect.center = (400, 300)

        WIN.fill("white")
        WIN.blit(vel_text, text_rect)

        draw(items)
        for item in items:
            item.move()

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
