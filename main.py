import pygame, sys, random, math

pygame.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption("Dodge the circles")
clock = pygame.time.Clock()
font = pygame.font.SysFont("timesnewroman", 48, False, True)
small_font = pygame.font.SysFont("timesnewroman", 28, True, True)
restart_button = pygame.Rect(320, 430, 20, 10)

class Player:
    def __init__(self):
        self.rect = pygame.Rect(280, 520, 80, 80)
        self.speed = 2.5

    def move(self, keys, mouse_pos):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        elif keys[pygame.K_UP]:
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        if pygame.mouse.get_pressed()[0]:
            self.rect.center = mouse_pos

        self.rect.clamp_ip(screen.get_rect())
        self.speed += 0.005

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 120, 254), self.rect)

class Obstacle:
    def __init__(self, color, x, y, radius, speed):
        self.color = color
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x -= self.speed
        self.y -= self.speed / 2

        if self.x < -self.radius:
            self.x += self.speed + 640
        if self.y < -self.radius:
            self.y += 640 + self.speed

        self.speed += 0.005
        if self.speed > 6:
            self.speed = 6

    def collides_with_player(self, player):
        closest_x = max(player.rect.left, min(self.x, player.rect.right))
        closest_y = max(player.rect.top, min(self.y, player.rect.bottom))
        dx = self.x - closest_x
        dy = self.y - closest_y
        return dx * dx + dy * dy < self.radius * self.radius

def generate_coordinates():
    x = random.randint(50, 500)
    y = random.randint(40, 600)
    radius = random.randint(10, 30)
    speed = random.randint(1, 2)
    return Obstacle((200, 200, 200), x, y, radius, speed)

def reset_game():
    obstacle1 = generate_coordinates()
    obstacle2 = generate_coordinates()
    obstacle3 = generate_coordinates()
    player = Player()
    return player, obstacle1, obstacle2, obstacle3, 0

def draw_game_over(score):
    screen.fill((30, 0, 0))
    title = font.render("GAME OVER", True, (255, 80, 80))
    score_text = small_font.render(f"Score: {math.ceil(score)}", True, (255, 255, 255))
    info_text = small_font.render("Press ESC to exit", True, (220, 220, 220))
    restart_text = small_font.render("Restart", True, (250, 250, 250))
    
    pygame.draw.rect(screen, (20, 68, 39), restart_button, border_radius=8)
    screen.blit(title, title.get_rect(center=(320, 250)))
    screen.blit(score_text, score_text.get_rect(center=(320, 330)))
    screen.blit(info_text, info_text.get_rect(center=(320, 390)))
    screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
    pygame.display.update()

player, obstacle1, obstacle2, obstacle3, score = reset_game()
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                player, obstacle1, obstacle2, obstacle3, score = reset_game()
                game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button.collidepoint(event.pos):
                    player, obstacle1, obstacle2, obstacle3, score = reset_game()
                    game_over = False

    if not game_over:
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        player.move(keys, mouse_pos)

        obstacle1.move()
        obstacle2.move()
        obstacle3.move()

        if obstacle1.collides_with_player(player) or obstacle2.collides_with_player(player) or obstacle3.collides_with_player(player):
            game_over = True

        score += 0.01

        screen.fill((25, 25, 25))
        player.draw(screen)
        obstacle1.draw()
        obstacle2.draw()
        obstacle3.draw()

        score_surface = small_font.render(f"Score: {math.ceil(score)}", True, (255, 255, 255))
        screen.blit(score_surface, (20, 30))
        pygame.display.update()
    else:
        draw_game_over(score)

    clock.tick(60)

pygame.quit()
sys.exit()
