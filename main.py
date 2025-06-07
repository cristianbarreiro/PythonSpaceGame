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
YELLOW = (255, 255, 0)

# Jugador
player_width = 35
player_height = 80

# Cargar imágenes
player_img = pygame.image.load("spaceship.png").convert_alpha()
meteor_img = pygame.image.load("meteor.png").convert_alpha()
bg_img = pygame.image.load("bg-purple.png")

#Define las nuevas dimensiones
player_size = (80, 80) # Nuevo tamaño para la imagen del jugador
meteor_size = (85, 85) # Nuevo tamaño para la imagen del meteorito
bg_size = (800, 600)

player_img = pygame.transform.scale(player_img, player_size)
meteor_img = pygame.transform.scale(meteor_img, meteor_size)
bg_img = pygame.transform.scale(bg_img, bg_size)

# Meteoritos
meteor_width = 30
meteor_height = 30
meteors = []

# Balas
bullets = []
bullet_width = 5
bullet_height = 15
bullet_speed = 7

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
        # Disparar con la barra espaciadora
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = pygame.Rect(player.centerx - bullet_width//2,
                                   player.top,
                                   bullet_width,
                                   bullet_height)
                bullets.append(bullet)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.left > 0:
        player.x -= 5
    if keys[pygame.K_RIGHT] and player.right < WIDTH:
        player.x += 5
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= 5
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += 5

    # Generar meteoritos
    if len(meteors) < 5:
        meteor = pygame.Rect(random.randint(0, WIDTH - meteor_width),
                             0, meteor_width, meteor_height)
        meteors.append(meteor)

    # Mover meteoritos
    for meteor in meteors[:]:
        meteor.y += 5
        if meteor.top > HEIGHT:
            meteors.remove(meteor)
            score += 1

    # Mover balas
    for bullet in bullets[:]:
        bullet.y -= bullet_speed
        if bullet.bottom < 0:
            bullets.remove(bullet)

    # Detectar colisiones balas-meteoritos
    for bullet in bullets[:]:
        for meteor in meteors[:]:
            if bullet.colliderect(meteor):
                if bullet in bullets:
                    bullets.remove(bullet)
                if meteor in meteors:
                    meteors.remove(meteor)
                score += 2
                break

    # Detectar colisiones jugador-meteoritos
    for meteor in meteors:
        if player.colliderect(meteor):
            running = False

    screen.fill(BLACK)
    screen.blit(bg_img, (0, 0))

    # Dibujar balas
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)

    screen.blit(player_img, player)
    for meteor in meteors:
        screen.blit(meteor_img, meteor)

    # Mostrar puntuación
    score_text = font.render(f"Puntuación: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()