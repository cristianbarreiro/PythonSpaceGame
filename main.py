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
meteor_width = 85  # Tamaño de la imagen
meteor_height = 85  # Tamaño de la imagen
meteor_collision_width = 60  # Tamaño del área de colisión
meteor_collision_height = 60  # Tamaño del área de colisión
meteors = []

# Balas
bullets = []
bullet_width = 5
bullet_height = 15
bullet_speed = 7

# Nivel y puntuación
level = 1
score = 0
lives = 3
game_over = False
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 74)

def reset_player():
    return pygame.Rect(WIDTH // 2 - player_width // 2,
                      HEIGHT - player_height - 10, player_width, player_height)

player = reset_player()

def create_meteor():
    # Velocidad base según el nivel
    if level == 1:
        base_speed = 3
    elif level == 2:
        base_speed = 5
    else:  # nivel 3
        base_speed = 7
    
    # Velocidad aleatoria adicional
    random_speed = random.randint(1, 3)
    speed = base_speed + random_speed
    
    # Tamaño según el nivel
    if level == 1:
        collision_width = meteor_collision_width
        collision_height = meteor_collision_height
    elif level == 2:
        collision_width = int(meteor_collision_width * 1.2)
        collision_height = int(meteor_collision_height * 1.2)
    else:  # nivel 3
        collision_width = int(meteor_collision_width * 1.4)
        collision_height = int(meteor_collision_height * 1.4)
    
    meteor = {
        'rect': pygame.Rect(
            random.randint(0, WIDTH - meteor_width),
            0,
            collision_width,
            collision_height
        ),
        'speed': speed
    }
    return meteor

def get_points():
    # Puntos base según el nivel
    if level == 1:
        return 5  # 5 puntos por meteorito que pasa
    elif level == 2:
        return 10  # 10 puntos por meteorito que pasa
    else:  # nivel 3
        return 15  # 15 puntos por meteorito que pasa

def get_destroy_points():
    # Puntos por destruir meteorito según el nivel
    if level == 1:
        return 15  # 15 puntos por destruir
    elif level == 2:
        return 25  # 25 puntos por destruir
    else:  # nivel 3
        return 40  # 40 puntos por destruir

#Reloj para control de FPS
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if not game_over:
                    bullet = pygame.Rect(player.centerx - bullet_width//2,
                                       player.top,
                                       bullet_width,
                                       bullet_height)
                    bullets.append(bullet)
            if event.key == pygame.K_r and game_over:
                # Reiniciar juego
                level = 1
                score = 0
                lives = 3
                game_over = False
                meteors.clear()
                bullets.clear()
                player = reset_player()

    if not game_over:
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
            meteors.append(create_meteor())

        # Mover meteoritos
        for meteor in meteors[:]:
            meteor['rect'].y += meteor['speed']
            if meteor['rect'].top > HEIGHT:
                meteors.remove(meteor)
                score += get_points()

        # Mover balas
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Detectar colisiones balas-meteoritos
        for bullet in bullets[:]:
            for meteor in meteors[:]:
                if bullet.colliderect(meteor['rect']):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if meteor in meteors:
                        meteors.remove(meteor)
                    score += get_destroy_points()
                    break

        # Detectar colisiones jugador-meteoritos
        for meteor in meteors[:]:
            if player.colliderect(meteor['rect']):
                lives -= 1
                meteors.remove(meteor)
                if lives <= 0:
                    game_over = True
                else:
                    # Reiniciar posición del jugador
                    player = reset_player()
                    # Limpiar meteoritos y balas
                    meteors.clear()
                    bullets.clear()
                break

        # Cambiar de nivel
        if score >= 150 and level == 1:
            level = 2
            # Limpiar meteoritos actuales
            meteors.clear()
            # Limpiar balas
            bullets.clear()
        elif score >= 500 and level == 2:
            level = 3
            # Limpiar meteoritos actuales
            meteors.clear()
            # Limpiar balas
            bullets.clear()

    # Dibujar
    screen.fill(BLACK)
    screen.blit(bg_img, (0, 0))

    if not game_over:
        # Dibujar balas
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        screen.blit(player_img, player)
        for meteor in meteors:
            # Dibujamos la imagen del meteorito centrada en el rectángulo de colisión
            screen.blit(meteor_img, (meteor['rect'].x - (meteor_width - meteor['rect'].width)//2,
                                   meteor['rect'].y - (meteor_height - meteor['rect'].height)//2))

        # Mostrar puntuación, nivel y vidas
        score_text = font.render(f"Puntuación: {score}", True, WHITE)
        level_text = font.render(f"Nivel: {level}", True, WHITE)
        lives_text = font.render(f"Vidas: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 50))
        screen.blit(lives_text, (10, 90))
    else:
        # Pantalla de Game Over
        game_over_text = big_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Puntuación final: {score}", True, WHITE)
        restart_text = font.render("Presiona R para reiniciar", True, WHITE)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 50))

    pygame.display.flip()
    clock.tick(60)
pygame.quit()