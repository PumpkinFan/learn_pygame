from re import I
import pygame
import numpy as np

pygame.init()

# TODO: implement proper 2D collision (https://www.vobarian.com/collisions/2dcollisions2.pdf)

WIDTH, HEIGHT = 1600, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ballz")

FPS = 60
DT = 1  # in 1/FPS of a seconcd

COLORS = [
    # rgb color values
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

GRAVITY = 0.1


class Ball:
    RADIUS = 50

    def __init__(self, x, y, color, x_vel=0, y_vel=0, mass=1):
        self.x = x
        self.y = y
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass

    def check_wall_collisions(self):
        current_x = self.x
        current_y = self.y
        next_x = self.x + self.x_vel * DT
        next_y = self.y + self.y_vel * DT
        if self.y - self.RADIUS + self.y_vel <= 0:
            self.y = self.RADIUS
            self.y_vel = -self.y_vel
        if self.y + self.RADIUS + self.y_vel >= HEIGHT:
            self.y = HEIGHT - self.RADIUS
            self.y_vel = -self.y_vel
        if self.x - self.RADIUS + self.x_vel <= 0:
            self.x = self.RADIUS
            self.x_vel = -self.x_vel
        if self.x + self.RADIUS + self.x_vel >= WIDTH:
            self.x = WIDTH - self.RADIUS
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


def collide_balls(ball1: Ball, ball2: Ball):
    """based on: https://www.vobarian.com/collisions/2dcollisions2.pdf"""
    vel1 = np.array([ball1.x_vel, ball1.y_vel])
    vel2 = np.array([ball2.x_vel, ball2.y_vel])
    norm_vector = np.array([ball2.x - ball1.x, ball2.y - ball1.y])
    # linalg.norm = magnitude of vector
    unit_norm = norm_vector / np.linalg.norm(norm_vector)
    unit_tang = np.array([-unit_norm[1], unit_norm[0]])  # ut = <-un_y, un_x>

    # project initial vectors onto normal and tangent lines
    norm_scalar1 = np.dot(vel1, unit_norm)
    tang_scalar1 = np.dot(vel1, unit_tang)
    norm_scalar2 = np.dot(vel2, unit_norm)
    tang_scalar2 = np.dot(vel2, unit_tang)

    # perform 1D elastic collision on normal components
    new_norm_scalar1 = (
        norm_scalar1 * (ball1.mass - ball2.mass) + 2 * ball2.mass * norm_scalar2
    ) / (ball1.mass + ball2.mass)
    new_norm_scalar2 = (
        norm_scalar2 * (ball2.mass - ball1.mass) + 2 * ball1.mass * norm_scalar1
    ) / (ball1.mass + ball2.mass)

    new_vel1 = new_norm_scalar1 * unit_norm + tang_scalar1 * unit_tang
    new_vel2 = new_norm_scalar2 * unit_norm + tang_scalar2 * unit_tang

    ball1.x_vel, ball1.y_vel = new_vel1
    ball2.x_vel, ball2.y_vel = new_vel2


def check_ball_collisions(balls: list[Ball]):
    for ball1 in balls:
        for ball2 in balls:
            if ball1 == ball2:
                break
            dist = np.sqrt((ball1.x - ball2.x) ** 2 + (ball1.y - ball2.y) ** 2)
            if dist < ball1.RADIUS + ball2.RADIUS:
                collide_balls(ball1, ball2)


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
        Ball(WIDTH / 4, 100, "green", x_vel=10, y_vel=2),
        Ball(WIDTH * 3 / 4, 100, "green", x_vel=-10, y_vel=-2),
        Ball(WIDTH / 4, 500, "blue", x_vel=10),
        Ball(WIDTH * 3 / 4, 500, "blue", x_vel=-10),
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
