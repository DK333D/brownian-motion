# Symulacja ruchu Browna

import pygame
import random
import math

# Kolory
WHITE = (255, 255, 255)
RED = "#bc4749" # Male czastki
DARK_GREEN = "#386641" # Duza czastka
GREEN = "#a7c957" # Linia trajektorii

# Ustawienia okna
WIDTH, HEIGHT = 800, 600

# Parametry cząsteczek
PARTICLE_RADIUS = 5
BIG_PARTICLE_RADIUS = 20
NUM_PARTICLES = 250
SPEED = 2
BIG_PARTICLE_SPEED = 1 # Prędkość większej cząsteczki

# Inicjalizacja Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Symulacja ruchu Browna')
clock = pygame.time.Clock()


# Klasa cząsteczki
class Particle:
    def __init__(self, x, y, radius, color, speed):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = speed

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)

        # Odbicie od ścian
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.angle = math.pi - self.angle
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.angle = -self.angle

        # Oddalenie od ścianki w osi OX
        if self.x - self.radius < 0:
            self.x = self.radius
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius

        # Oddalenie od ścianki w osi OY
        if self.y - self.radius < 0:
            self.y = self.radius
        elif self.y + self.radius > HEIGHT:
            self.y = HEIGHT - self.radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def check_collision(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        distance = math.hypot(dx, dy)
        if distance <= self.radius + other.radius:
            # Proste odbicie
            angle = math.atan2(dy, dx)

            # Uproszczenie wzoru na prędkość po odbiciu v' = 2 * (n * v) * n - v
            self.angle = 2 * angle - self.angle
            other.angle = 2 * angle - other.angle


# Funkcja tworząca cząsteczki
def create_particles():
    particles = []
    for _ in range(NUM_PARTICLES):
        x = random.randint(PARTICLE_RADIUS, WIDTH - PARTICLE_RADIUS)
        y = random.randint(PARTICLE_RADIUS, HEIGHT - PARTICLE_RADIUS)
        particle = Particle(x, y, PARTICLE_RADIUS, RED, SPEED)
        particles.append(particle)

    # Dodanie większej cząsteczki z prędkością
    big_particle = Particle(WIDTH // 2, HEIGHT // 2, BIG_PARTICLE_RADIUS, DARK_GREEN, BIG_PARTICLE_SPEED)
    particles.append(big_particle)

    return particles


def main():
    particles = create_particles()

    # Lista do przechowywania punktów trajektorii dużej cząsteczki
    trajectory = []

    running = True
    while running:
        screen.fill(WHITE)

        # Obsługa zdarzenia wyjścia
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rysowanie i poruszanie cząsteczek
        for i, particle in enumerate(particles):
            particle.move()
            particle.draw(screen)

            # Sprawdz, czy wystapila kolizja
            for other_particle in particles[i + 1:]:
                particle.check_collision(other_particle)

        # Aktualizacja trajektorii dużej cząsteczki
        big_particle = particles[-1]  # Zakładamy, że ostatnia cząsteczka jest dużą cząsteczką
        trajectory.append((big_particle.x, big_particle.y))

        # Rysowanie trajektorii
        if len(trajectory) > 1:
            pygame.draw.aalines(screen, GREEN, False, trajectory, 1)

        # Rysowanie dużej cząsteczki
        big_particle.draw(screen)

        # Odśwież ekran
        pygame.display.flip()
        clock.tick(60)  # FPS

    # Zakończ symulację
    pygame.quit()


if __name__ == "__main__":
    main()
