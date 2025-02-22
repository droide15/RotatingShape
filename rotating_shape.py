import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rotating Image with Sliders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
RED = (255, 0, 0)

# Load the image (replace 'image.png' with your file name)
try:
    original_image = pygame.image.load('image.png').convert_alpha()
    # Scale the image to a reasonable size (e.g., 200x200 pixels)
    original_image = pygame.transform.scale(original_image, (200, 200))
except pygame.error:
    print("Error: Could not load 'image.png'. Make sure the file exists in the same folder.")
    pygame.quit()
    exit()

# Center the image
image_rect = original_image.get_rect(center=(WIDTH // 4, HEIGHT // 2))

# Rotation variables
angle = 0
rotation_speed = 5.0  # Initial speed (degrees per frame)
max_rotation_speed = 50.0  # Max speed increased to 50 from 40

# FPS variables
target_fps = 60  # Initial FPS
max_fps = 134  # Max FPS set to 120 (down from 240)

# Slider setup
SLIDER_WIDTH, SLIDER_HEIGHT = 200, 20
SLIDER_Y_SPEED = HEIGHT - 100
SLIDER_Y_FPS = HEIGHT - 50
slider_x = WIDTH - 250  # Right side of screen

speed_slider = pygame.Rect(slider_x, SLIDER_Y_SPEED, SLIDER_WIDTH, SLIDER_HEIGHT)
fps_slider = pygame.Rect(slider_x, SLIDER_Y_FPS, SLIDER_WIDTH, SLIDER_HEIGHT)

speed_knob = pygame.Rect(slider_x + (rotation_speed / max_rotation_speed) * SLIDER_WIDTH - 10, SLIDER_Y_SPEED - 5, 20, 30)
fps_knob = pygame.Rect(slider_x + (target_fps / max_fps) * SLIDER_WIDTH - 10, SLIDER_Y_FPS - 5, 20, 30)

dragging_speed = False
dragging_fps = False

# Font for labels
font = pygame.font.Font(None, 36)

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if speed_knob.collidepoint(event.pos):
                dragging_speed = True
            elif fps_knob.collidepoint(event.pos):
                dragging_fps = True
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging_speed = False
            dragging_fps = False
        elif event.type == pygame.MOUSEMOTION and dragging_speed:
            speed_knob.x = max(slider_x, min(slider_x + SLIDER_WIDTH - speed_knob.width, event.pos[0]))
            rotation_speed = (speed_knob.x - slider_x) / SLIDER_WIDTH * max_rotation_speed
        elif event.type == pygame.MOUSEMOTION and dragging_fps:
            fps_knob.x = max(slider_x, min(slider_x + SLIDER_WIDTH - fps_knob.width, event.pos[0]))
            target_fps = (fps_knob.x - slider_x) / SLIDER_WIDTH * max_fps
            if target_fps < 1:  # Prevent FPS from going too low
                target_fps = 1

    # Clear the screen
    screen.fill(BLACK)

    # Rotate the image
    rotated_image = pygame.transform.rotate(original_image, angle)
    rotated_rect = rotated_image.get_rect(center=image_rect.center)

    # Draw the rotated image
    screen.blit(rotated_image, rotated_rect.topleft)

    # Update angle
    angle += rotation_speed
    if angle >= 360:
        angle -= 360

    # Draw sliders
    pygame.draw.rect(screen, GRAY, speed_slider)  # Speed slider background
    pygame.draw.rect(screen, GRAY, fps_slider)    # FPS slider background
    pygame.draw.rect(screen, RED, speed_knob)     # Speed knob
    pygame.draw.rect(screen, RED, fps_knob)       # FPS knob

    # Draw labels
    speed_label = font.render(f"Speed: {rotation_speed:.1f}", True, WHITE)
    fps_label = font.render(f"FPS: {int(target_fps)}", True, WHITE)
    screen.blit(speed_label, (slider_x, SLIDER_Y_SPEED - 40))
    screen.blit(fps_label, (slider_x, SLIDER_Y_FPS - 40))

    # Update the display
    pygame.display.flip()
    clock.tick(target_fps)  # Use the adjustable FPS

pygame.quit()