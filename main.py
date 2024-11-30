import pygame
import random
import math

pygame.init()

SCALE_FACTOR = 2
RES_WIDTH, RES_HEIGHT = 1280 * SCALE_FACTOR, 720 * SCALE_FACTOR
screen = pygame.display.set_mode((1280, 720))
render_surface = pygame.Surface((RES_WIDTH, RES_HEIGHT))

clock = pygame.time.Clock()
running = True
G = 6.67430 * 10 ** -11
MIN_DISTANCE = 40


class Body:
    def __init__(self, position, velocity, mass, color, radius=12):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.mass = mass
        self.color = color
        self.radius = radius
        self.previous_position = self.position.copy()

    def update_position(self, dt):
        self.previous_position = self.position.copy()
        self.position += self.velocity * dt

    def apply_force(self, force, dt):
        acceleration = force / self.mass
        self.velocity += acceleration * dt


def calculate_force(body1, body2):
    direction = body2.position - body1.position
    distance = direction.length()
    if distance > MIN_DISTANCE:
        direction = direction.normalize()
        force_magnitude = G * body1.mass * body2.mass / (distance ** 2)
        return direction * force_magnitude
    return pygame.Vector2(0, 0)


def initialize_random_bodies(num_bodies, screen_width, screen_height, mass_range, velocity_range):
    colors = ["red", "blue", "green", "yellow",
              "purple", "orange", "cyan", "pink"]
    bodies = []
    for i in range(num_bodies):
        position = (
            random.randint(100, screen_width - 100),
            random.randint(100, screen_height - 100)
        )
        velocity = (
            random.uniform(*velocity_range),
            random.uniform(*velocity_range)
        )
        mass = random.uniform(*mass_range)
        color = colors[i % len(colors)]
        bodies.append(
            Body(position=position, velocity=velocity, mass=mass, color=color))
    return bodies


def main():
    global running
    num_bodies = 3
    mass_range = (10**17.5, 10**17.5)
    velocity_range = (-0.05, 0.05)
    bodies = initialize_random_bodies(
        num_bodies, RES_WIDTH, RES_HEIGHT, mass_range, velocity_range)

    trail_surface = pygame.Surface((RES_WIDTH, RES_HEIGHT), pygame.SRCALPHA)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        render_surface.fill((0, 0, 0))

        forces = [pygame.Vector2(0, 0) for _ in bodies]

        for i, body1 in enumerate(bodies):
            for j, body2 in enumerate(bodies):
                if i != j:
                    forces[i] += calculate_force(body1, body2)

        dt = clock.tick(120) / 1000

        for body in bodies:
            body.apply_force(forces[bodies.index(body)], dt)
            body.update_position(dt)

            pygame.draw.line(
                trail_surface,
                body.color,
                (int(body.previous_position.x), int(body.previous_position.y)),
                (int(body.position.x), int(body.position.y)),
                3
            )

        render_surface.blit(trail_surface, (0, 0))

        for body in bodies:
            pygame.draw.circle(render_surface, body.color, (int(
                body.position.x), int(body.position.y)), body.radius * SCALE_FACTOR)

        scaled_surface = pygame.transform.smoothscale(
            render_surface, screen.get_size())
        screen.blit(scaled_surface, (0, 0))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
