import pygame
import numpy as np

pygame.init()

# TODO: implement proper 2D collision (https://www.vobarian.com/collisions/2dcollisions2.pdf)

WIDTH, HEIGHT = 1600, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ballz")

FPS = 60
DT = 1 / 5

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

    def check_wall_collisions(self):
        current_x = self.x
        current_y = self.y
        next_x = self.x + self.x_vel * DT
        next_y = self.y + self.y_vel * DT
        if self.y + self.RADIUS + self.y_vel >= HEIGHT:
            self.y = HEIGHT - self.RADIUS
            self.y_vel = -self.y_vel
        if self.x + self.RADIUS + self.x_vel >= WIDTH:
            self.x = WIDTH - self.RADIUS
            self.x_vel = -self.x_vel
        if self.x - self.RADIUS + self.x_vel <= 0:
            self.x = self.RADIUS
            self.x_vel = -self.x_vel

    def move(self, air_resistance=False):
        self.check_wall_collisions()

        self.x += self.x_vel * DT
        self.y += self.y_vel * DT
        self.y_vel += GRAVITY

        if air_resistance:
            self.x_vel = 0.999 * self.x_vel
            self.y_vel = 0.999 * self.y_vel

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)


def check_ball_collisions(balls: list[Ball]):
    for ball1 in balls:
        for ball2 in balls:
            if ball1 == ball2:
                pass
            dist = np.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
            if dist < ball1.RADIUS + ball2.RADIUS:
                ball1.x_vel, ball2.x_vel = ball2.x_vel, ball1.x_vel
                ball1.y_vel, ball2.y_vel = ball2.y_vel, ball1.y_vel
                break


def draw(items):
    # WIN.fill("white")
    for item in items:
        item.draw(WIN)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 32)

    balls = [
        Ball(WIDTH / 4, HEIGHT / 4, "darkblue", x_vel=100),
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

        draw(balls)
        for ball in balls:
            ball.move()

        check_ball_collisions(balls)

    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
