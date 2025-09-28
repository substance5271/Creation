import pygame
import random
import math
import time

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Creation")

# Clock
clock = pygame.time.Clock()

# Color palette (cyclic rainbow effect)
def get_color(t):
    r = int(128 + 127 * math.sin(t))
    g = int(128 + 127 * math.sin(t + 2))
    b = int(128 + 127 * math.sin(t + 4))
    return (r, g, b)

# Particle class
class Particle:
    def __init__(self, x, y, color, lifespan):
        self.x = x
        self.y = y
        self.radius = 2
        self.original_color = color
        self.color = color
        self.lifespan = lifespan
        self.birth = time.time()
        self.vel = [random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)]

    def update(self):
        self.x += self.vel[0]
        self.y += self.vel[1]
        self.radius += 0.05
        age = time.time() - self.birth
        fade = max(0, (1 - age / self.lifespan)) ** 3  # Much slower fade
        self.color = tuple(int(c * fade) for c in self.original_color)
        return age < self.lifespan

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.radius))

# Variables
particles = []
t = 0
message_start_time = None
message_duration = 6  # seconds
show_message = False
last_message_time = 0
message_cooldown = 12  # seconds between messages

# Main loop
running = True
while running:
    clock.tick(60)
    t += 0.01

    # Very slow background fade (allows long-lasting trails)
    fade_surface = pygame.Surface((WIDTH, HEIGHT))
    fade_surface.set_alpha(2)  # Lower value = slower fade
    fade_surface.fill((0, 0, 0))
    screen.blit(fade_surface, (0, 0))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Handle mouse drawing
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # Left mouse button
        mx, my = pygame.mouse.get_pos()
        for _ in range(5):
            particles.append(Particle(mx, my, get_color(t), lifespan=20))  # Long lifespan

    # Update and draw particles
    particles = [p for p in particles if p.update()]
    for p in particles:
        p.draw(screen)

    # Show message occasionally
    current_time = time.time()
    if current_time - last_message_time > message_cooldown:
        show_message = True
        message_start_time = current_time
        last_message_time = current_time

    if show_message:
        elapsed = current_time - message_start_time
        if elapsed < message_duration:
            font = pygame.font.SysFont(None, 36)
            text = font.render("Create, even knowing it will fade", True, get_color(t))
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 30))
        else:
            show_message = False

    # Update display
    pygame.display.flip()

# Clean up
pygame.quit()

