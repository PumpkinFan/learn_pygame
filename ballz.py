import pygame
import numpy as np
import random

pygame.init()


WIDTH, HEIGHT = 1600, 900

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ballz")

FPS = 60
DT = 0.5

# TODO: Linear interpolation of collisions
# TODO: Use RK4 for time stepping

COLORS = [
    # rgb color values
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]

GRAVITY = 0.5


class Ball:
    RADIUS = 25

    def __init__(self, x, y, color="red", x_vel=0, y_vel=0, mass=1):
        self.x = x
        self.y = y
        self.color = color
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.mass = mass
        # self.next_x = self.x + self.x_vel * DT
        # self.next_y = self.y + self.y_vel * DT

    def check_wall_collisions(self):
        if self.y - self.RADIUS <= 0:
            self.y = self.RADIUS
            self.y_vel = -self.y_vel
        if self.y + self.RADIUS >= HEIGHT:
            self.y = HEIGHT - self.RADIUS
            self.y_vel = -self.y_vel
        if self.x - self.RADIUS <= 0:
            self.x = self.RADIUS
            self.x_vel = -self.x_vel
        if self.x + self.RADIUS >= WIDTH:
            self.x = WIDTH - self.RADIUS
            self.x_vel = -self.x_vel

    def move(self, air_resistance=False):
        self.check_wall_collisions()

        self.x += self.x_vel * DT
        self.y += self.y_vel * DT
        self.y_vel += GRAVITY * DT

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
    unit_tang = np.array([-unit_norm[1], unit_norm[0]])

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
    # iterate over all combinations of balls
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


def make_lots_of_balls(sqrt_n_balls):
    sqrt_n_balls
    x_grid = np.linspace(
        WIDTH / sqrt_n_balls, WIDTH - WIDTH / sqrt_n_balls, sqrt_n_balls
    )
    y_grid = np.linspace(
        HEIGHT / sqrt_n_balls, HEIGHT - HEIGHT / sqrt_n_balls, sqrt_n_balls
    )
    x_mgrid, y_mgrid = np.meshgrid(x_grid, y_grid)
    balls = [
        Ball(
            x,
            y,
            random.choice(COLORS),
            x_vel=np.random.randint(-5, 5),
            y_vel=np.random.randint(-5, 5),
            mass=np.random.randint(1, 3),
        )
        for x, y in zip(x_mgrid.ravel(), y_mgrid.ravel())
    ]
    return balls


def main():
    run = True
    clock = pygame.time.Clock()
    font = pygame.font.Font("freesansbold.ttf", 32)

    # balls = [
    #     Ball(WIDTH / 4, HEIGHT / 2, x_vel=50),
    #     Ball(3 * WIDTH / 4, HEIGHT / 2, x_vel=-50),
    # ]
    balls = make_lots_of_balls(9)

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
        ball_masses = np.array([ball.mass for ball in balls])
        kinetic_energy = np.sum(0.5 * ball_masses * ball_vels**2)
        ball_heights = np.array([(HEIGHT - ball.y) for ball in balls])
        potential_energy = np.sum(ball_masses * GRAVITY * ball_heights)
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
