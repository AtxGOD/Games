import pygame

FPS = 60
W = 700
H = 400

pygame.init()
sc = pygame.display.set_mode((W, H))
pygame.display.set_caption("Ping Pong")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

f = pygame.font.SysFont("HeadLineA", 80)

wall = pygame.Surface((W, 10))
wall.fill(WHITE)
wall_rect_up = wall.get_rect()
wall_rect_down = wall.get_rect(center=(W//2, H-wall.get_height()//2))

gate = pygame.Surface((20, H))
gate_rect_left = gate.get_rect()
gate_rect_right = gate.get_rect(center=(W - gate.get_width()//2, H//2))

user = pygame.Surface((10, 50))
user.fill(WHITE)
user_rect = user.get_rect(center=(W-50, H//2))

opponent = pygame.Surface((10, 50))
opponent.fill(WHITE)
opponent_rect = opponent.get_rect(center=(50, H//2))

ball = pygame.Surface((8, 8))
ball.fill(WHITE)
ball_rect = ball.get_rect(center=(W//2, H//2))

sc.blit(ball, ball_rect)
sc.blit(user, user_rect)
sc.blit(opponent, opponent_rect)
pygame.display.update()

speed = 3
speed_ball = 3
ball_move_y = 0
user_point = 0
opponent_point = 0


def draw_text():
    global sc_text
    sc_text_left = f.render(str(opponent_point), True, WHITE)
    sc_text_right = f.render(str(user_point), True, WHITE)
    pos_text_left = sc_text_left.get_rect(center=(W//2 - 50, 50))
    pos_text_right = sc_text_right.get_rect(center=(W // 2 + 50, 50))
    sc.blit(sc_text_left, pos_text_left)
    sc.blit(sc_text_right, pos_text_right)


def collide_ball():
    global ball_move_y, speed_ball, user_point, opponent_point

    def change_angel(where_collide):
        global ball_move_y, speed_ball
        ball_move_y = where_collide // 6 * -1
        speed_ball *= -1

    if user_rect.colliderect(ball_rect):
        where_collide = user_rect.center[1] - ball_rect.center[1]
        change_angel(where_collide)
    elif opponent_rect.colliderect(ball_rect):
        where_collide = opponent_rect.center[1] - ball_rect.center[1]
        change_angel(where_collide)

    if wall_rect_up.colliderect(ball_rect) or wall_rect_down.colliderect(ball_rect):
        ball_move_y *= -1

    if gate_rect_left.colliderect(ball_rect):
        user_point += 1
        ball_rect.x = W//2
        ball_rect.y = H//2
        ball_move_y = 0
    elif gate_rect_right.colliderect(ball_rect):
        opponent_point += 1
        ball_rect.x = W // 2
        ball_rect.y = H // 2
        ball_move_y = 0


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        user_rect.y -= speed
        if user_rect.y < 0:
            user_rect.y = 0

    elif keys[pygame.K_DOWN]:
        user_rect.y += speed
        if user_rect.y > H - user_rect.height:
            user_rect.y = H - user_rect.height

    if keys[pygame.K_w]:
        opponent_rect.y -= speed
        if opponent_rect.y < 0:
            opponent_rect.y = 0

    elif keys[pygame.K_s]:
        opponent_rect.y += speed
        if opponent_rect.y > H - opponent_rect.height:
            opponent_rect.y = H - opponent_rect.height

    ball_rect.x += speed_ball
    ball_rect.y += ball_move_y

    collide_ball()

    sc.fill((0, 0, 0))
    sc.blit(wall, (0, 0))
    sc.blit(wall, (0, H-wall.get_height()))
    sc.blit(ball, ball_rect)
    sc.blit(user, user_rect)
    sc.blit(opponent, opponent_rect)
    draw_text()
    pygame.display.update()

    clock.tick(FPS)
