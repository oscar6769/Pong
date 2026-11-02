import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

# --- settings (tweak these to change difficulty) ---
PLAYER_SPEED = 7
CPU_SPEED = 3.5        # lower = easier
CPU_ERROR = 70         # max aiming error in px (bigger = more misses)
BALL_SPEED = 5

# --- game objects ---
player = pygame.Rect(20, HEIGHT // 2 - 50, 12, 100)
cpu = pygame.Rect(WIDTH - 32, HEIGHT // 2 - 50, 12, 100)
ball = pygame.Rect(WIDTH // 2 - 8, HEIGHT // 2 - 8, 16, 16)

ball_vx = BALL_SPEED * random.choice([-1, 1])
ball_vy = BALL_SPEED * random.choice([-1, 1])
score = [0, 0]  # [player, cpu]

cpu_y = float(cpu.y)   # float position so fractional speeds work
cpu_offset = 0         # how far off the CPU aims

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # --- player input ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PLAYER_SPEED

    # --- ball movement ---
    ball.x += ball_vx
    ball.y += ball_vy

    # bounce off top/bottom
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vy *= -1

    # bounce off paddles
    if ball.colliderect(player) and ball_vx < 0:
        ball_vx *= -1
        cpu_offset = random.randint(-CPU_ERROR, CPU_ERROR)  # new aiming error
    if ball.colliderect(cpu) and ball_vx > 0:
        ball_vx *= -1

    # --- CPU movement (only chases when the ball is coming at it) ---
    if ball_vx > 0:
        target = ball.centery + cpu_offset
        if cpu.centery < target - 10:
            cpu_y += CPU_SPEED
        elif cpu.centery > target + 10:
            cpu_y -= CPU_SPEED

    cpu_y = max(0, min(HEIGHT - cpu.height, cpu_y))
    cpu.y = round(cpu_y)

    # --- scoring ---
    if ball.left <= 0 or ball.right >= WIDTH:
        if ball.left <= 0:
            score[1] += 1
        else:
            score[0] += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_vx = BALL_SPEED * random.choice([-1, 1])
        ball_vy = BALL_SPEED * random.choice([-1, 1])

    # --- draw ---
    screen.fill((20, 20, 30))
    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", cpu)
    pygame.draw.ellipse(screen, "white", ball)
    pygame.draw.aaline(screen, "gray", (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    screen.blit(font.render(str(score[0]), True, "white"), (WIDTH // 4, 20))
    screen.blit(font.render(str(score[1]), True, "white"), (3 * WIDTH // 4, 20))

    pygame.display.flip()
    clock.tick(60)