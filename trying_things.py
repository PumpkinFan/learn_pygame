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

    def move(self, air_resistance=False):
        # check collisons with walls/floor
        # should put into own method
        if self.y + self.RADIUS + self.y_vel >= HEIGHT:
            self.y = HEIGHT - self.RADIUS
            self.y_vel = -self.y_vel
        if self.x + self.RADIUS + self.x_vel >= WIDTH:
            self.x = WIDTH - self.RADIUS
            self.x_vel = -self.x_vel
        if self.x - self.RADIUS + self.x_vel <= 0:
            self.x = self.RADIUS
            self.x_vel = -self.x_vel

        self.x += self.x_vel
        self.y += self.y_vel
        self.y_vel += GRAVITY

        if air_resistance:
            self.x_vel = 0.999 * self.x_vel
            self.y_vel = 0.999 * self.y_vel

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

    items = [
        Ball(WIDTH / 4, HEIGHT / 4, "darkblue", x_vel=10),
        Ball(WIDTH / 2, HEIGHT / 2, "red", x_vel=-10, y_vel=15),
        Ball(WIDTH * 3 / 4, HEIGHT * 3 / 4, "darkgreen"),
    ]
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT -> red x pygame window
                run = False
                break

        # place rest of game code to run each tick in loop
        balls = [item for item in items if isinstance(item, Ball)]
        ball_vels = np.array(
            [np.sqrt(ball.x_vel**2 + ball.y_vel**2) for ball in balls]
        )
        kinetic_energy = np.sum(0.5 * ball_vels**2)
        ball_heights = np.array([(HEIGHT - ball.y) for ball in balls])
        potential_energy = np.sum(GRAVITY * ball_heights)
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
