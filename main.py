import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lluvia Espacial")

#Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Jugador
player_width = 50
player_height = 50

# Meteoritos
meteor_width = 30
meteor_height = 30
meteors = []

# Puntuación
score = 0
font = pygame.font.Font(None, 36)

player = pygame.Rect(WIDTH // 2 - player_width // 2,
                     HEIGHT - player_height - 10, player_width, player_height)
#Reloj para control de FPS
clock  = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right > 0:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom > 0:
        player.y += 5

    # Generar meteoritos
    if len(meteors) < 5:
        meteor = pygame.Rect(random.randint(0, WIDTH - meteor_width),
                             0, meteor_width, meteor_height)
        meteors.append(meteor)

    # Mover meteoritos
    for meteor in meteors:
        meteor.y += 5
        if meteor.top > HEIGHT:
            meteors.remove(meteor)

    # Detectar colisiones
    for meteor in meteors:
        if player.colliderect(meteor):
            running = False

    # Mostrar puntuación
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    for meteor in meteors:
        pygame.draw.rect(screen, RED, meteor)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()