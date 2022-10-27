import pygame
import time
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Firetwerks")

FPS = 60
COLORS = [
    # rgb color values
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
]
GRAVITY = 0.01


class Projectile:
    WIDTH = 5
    HEIGHT = 10
    ALPHA_DECREMENT = 3  # alpha ranges from 0-255

    def __init__(self, x, y, x_vel, y_vel, color):
        self.x = x
        self.y = y
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.color = color
        self.alpha = 255

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel
        self.alpha = max(0, self.alpha - self.ALPHA_DECREMENT)

    def draw(self, win):
        self.draw_rect_alpha(
            win, self.color + (self.alpha,), (self.x, self.y, self.WIDTH, self.HEIGHT)
        )

    @staticmethod  # doesn't require access to any class properties
    def draw_rect_alpha(surface, color, rect):

        # in pygame everything you draw is a surface
        shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
        pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
        surface.blit(shape_surf, rect)  # blit places one surfaces onto another


class Firework:
    RADIUS = 10
    MAX_PROJECTILES = 50
    MIN_PROJECTILES = 25
    PROJECTILE_VEL = 4

    def __init__(self, x, y, y_vel, explode_height, color):
        self.x = x
        self.y = y
        self.y_vel = y_vel
        self.explode_height = explode_height
        self.color = color
        self.exploded = False
        self.projectiles = []

    def explode(self):
        self.exploded = True
        num_projectiles = random.randrange(self.MIN_PROJECTILES, self.MAX_PROJECTILES)

        if random.randint(0, 1) == 0:
            self.create_circular_projectiles(num_projectiles)
        else:
            self.create_star_projectiles()

    def create_circular_projectiles(self, n_proj):
        angle_dif = (2 * math.pi) / n_proj
        current_angle = 0
        vel = random.randrange(self.PROJECTILE_VEL - 1, self.PROJECTILE_VEL + 1)
        for _ in range(n_proj):
            x_vel = vel * math.cos(current_angle)
            y_vel = vel * math.sin(current_angle)
            color = random.choice(COLORS)
            projectile = Projectile(self.x, self.y, x_vel, y_vel, color)
            self.projectiles.append(projectile)
            current_angle += angle_dif

    def create_star_projectiles(self):
        angle_dif = math.pi / 4
        current_angle = 0
        n_proj = 32
        for i in range(1, n_proj + 1):
            vel = self.PROJECTILE_VEL + (i % (n_proj / 8))
            x_vel = math.cos(current_angle) * vel
            y_vel = math.sin(current_angle) * vel
            color = random.choice(COLORS)
            self.projectiles.append(Projectile(self.x, self.y, x_vel, y_vel, color))
            if i % (n_proj / 8) == 0:
                current_angle += angle_dif

    def move(self, max_width, max_height):
        if not self.exploded:
            self.y += self.y_vel
            if self.y <= self.explode_height:
                self.explode()
            self.y_vel += GRAVITY

        projectiles_to_remove = []
        for projectile in self.projectiles:
            projectile.move()

            if projectile.x >= max_width or projectile.x < 0:
                projectiles_to_remove.append(projectile)
            elif projectile.y >= max_height or projectile.y < 0:
                projectiles_to_remove.append(projectile)

        for projectile in projectiles_to_remove:
            self.projectiles.remove(projectile)

    def draw(self, win):
        if not self.exploded:
            pygame.draw.circle(win, self.color, (self.x, self.y), self.RADIUS)

        for projectile in self.projectiles:
            projectile.draw(win)


class Launcher:
    WIDTH = 20
    HEIGHT = 20
    COLOR = "white"

    def __init__(self, x, y, period):
        self.x = x
        self.y = y
        self.period = period  # ms
        self.start_time = time.time()
        self.fireworks = []

    def draw(self, win):  # win = surface we draw onto
        pygame.draw.rect(win, self.COLOR, (self.x, self.y, self.WIDTH, self.HEIGHT))

        for firework in self.fireworks:
            firework.draw(win)

    def launch(self):
        color = random.choice(COLORS)
        explode_height = random.randrange(50, 400)
        firework = Firework(self.x + self.WIDTH / 2, self.y, -5, explode_height, color)
        self.fireworks.append(firework)

    def loop(self, max_width, max_height):
        current_time = time.time()
        time_elapsed = current_time - self.start_time

        if time_elapsed * 1000 >= self.period:
            self.start_time = current_time
            self.launch()

        fireworks_to_remove = []
        for firework in self.fireworks:
            firework.move(max_width, max_height)
            if firework.exploded and len(firework.projectiles) == 0:
                fireworks_to_remove.append(firework)

        for firework in fireworks_to_remove:
            self.fireworks.remove(firework)


def draw(launchers):
    win.fill("black")
    for launcher in launchers:
        launcher.draw(win)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()  # game clock

    launchers = [
        Launcher(100, HEIGHT - Launcher.HEIGHT, 4000),
        Launcher(300, HEIGHT - Launcher.HEIGHT, 3000),
        Launcher(500, HEIGHT - Launcher.HEIGHT, 2000),
        Launcher(700, HEIGHT - Launcher.HEIGHT, 1000),
    ]

    while run:
        clock.tick(FPS)

        # loop through game events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pygame.QUIT -> red x pygame window
                run = False
                break

        for launcher in launchers:
            launcher.loop(WIDTH, HEIGHT)

        draw(launchers)

    # quit pygame and python
    pygame.quit()
    quit()


if __name__ == "__main__":
    main()
