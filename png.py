import pygame, sys, random

pygame.init()
WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

PLAYER_SPEED = 7
CPU_SPEED = 3.5       
CPU_ERROR = 70        
BALL_SPEED = 5


player = pygame.Rect(20, HEIGHT // 2 - 50, 12, 100)
cpu = pygame.Rect(WIDTH - 32, HEIGHT // 2 - 50, 12, 100)
ball = pygame.Rect(WIDTH // 2 - 8, HEIGHT // 2 - 8, 16, 16)

ball_vx = BALL_SPEED * random.choice([-1, 1])
ball_vy = BALL_SPEED * random.choice([-1, 1])
score = [0, 0]  

cpu_y = float(cpu.y)  
cpu_offset = 0         
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and player.top > 0:
        player.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN] and player.bottom < HEIGHT:
        player.y += PLAYER_SPEED

    ball.x += ball_vx
    ball.y += ball_vy

  
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vy *= -1


    if ball.colliderect(player) and ball_vx < 0:
        ball_vx *= -1
        cpu_offset = random.randint(-CPU_ERROR, CPU_ERROR) 
    if ball.colliderect(cpu) and ball_vx > 0:
        ball_vx *= -1


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

    screen.fill((20, 20, 30))
    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", cpu)
    pygame.draw.ellipse(screen, "white", ball)
    pygame.draw.aaline(screen, "gray", (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    screen.blit(font.render(str(score[0]), True, "white"), (WIDTH // 4, 20))
    screen.blit(font.render(str(score[1]), True, "white"), (3 * WIDTH // 4, 20))

    pygame.display.flip()
    clock.tick(60)