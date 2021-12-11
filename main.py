import pygame
import sys
import random

pygame.init()
clock = pygame.time.Clock()
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# load images and fonts
backgroundImg1 = pygame.image.load("images/background1.png")
backgroundImg2 = pygame.image.load("images/background2.png")
backgroundImg3 = pygame.image.load("images/background3.png")
font = pygame.font.Font("fonts/menu.TTF", 32)
largeFont = pygame.font.Font("fonts/menu.TTF", 64)


# variables
UP_FORCE = 8.5
GRAVITY = 0.9
PIPE_SPEED = 8.0
PIPE_INTERVAL = 1500
FONT_COLOR = (255, 255, 255)

score = 0
highestScore = 0


class Player:
    def __init__(self):
        self.gravity = GRAVITY
        self.movement = 0
        self.y = SCREEN_HEIGHT / 2
        self.img = pygame.image.load("images/player.png").convert_alpha()
        self.rect = self.img.get_rect(center=(300, self.y))

    def render(self):
        self.movement += self.gravity
        self.y += self.movement
        self.rect.centery = self.y
        screen.blit(self.img, self.rect)


class Pipes:
    def __init__(self):
        self.pipes = []
        self.bottomImg = pygame.image.load("images/pipe.png")
        self.topImg = pygame.transform.flip(self.bottomImg, False, True)

    def create(self):
        global score
        gap = random.randint(120, 250)
        top = random.randint(0, 300)
        bottom = top + gap
        topRect = self.topImg.get_rect(midbottom=(SCREEN_WIDTH + 100, top))
        bottomRect = self.bottomImg.get_rect(midtop=(SCREEN_WIDTH + 100, bottom))
        self.pipes.append((bottomRect, 0))
        self.pipes.append((topRect, 1))
        score += 1

    def render(self):
        for pipe in self.pipes:
            pipe[0].centerx -= PIPE_SPEED
            if pipe[1] == 0:
                screen.blit(self.bottomImg, pipe[0])
            else:
                screen.blit(self.topImg, pipe[0])


class Background:
    def __init__(self):
        self.movement = 0
        self.backgroundImg = backgroundImg1

    def render(self):
        self.movement -= 2
        if self.movement <= -1164:
            self.movement = 0
        screen.blit(self.backgroundImg, (self.movement, 0))
        screen.blit(self.backgroundImg, (self.movement + 1164, 0))


def check_collision(avatar, objects):
    if avatar.y <= -40 or avatar.y >= SCREEN_HEIGHT + 40:
        return True
    for obj in objects.pipes:
        if avatar.rect.colliderect(obj[0]):
            return True
    return False


def get_score():
    return max(0, score - 2)


def render_menu():
    title = largeFont.render("FLAPPY ASTRONAUT", True, FONT_COLOR)
    titleRect = title.get_rect(center=(500, 175))
    screen.blit(title, titleRect)
    startText = font.render("START (PRESS S)", True, FONT_COLOR)
    startTextRect = startText.get_rect(center=(500, 275))
    quitText = font.render("QUIT (PRESS Q)", True, FONT_COLOR)
    quitTextRect = quitText.get_rect(center=(500, 325))
    screen.blit(startText, startTextRect)
    screen.blit(quitText, quitTextRect)


def render_header():
    startText = font.render("SCORE: " + str(get_score()), True, FONT_COLOR)
    startTextRect = startText.get_rect(topleft=(15, 10))
    screen.blit(startText, startTextRect)


def render_endpage():
    global highestScore
    highestScore = max(highestScore, get_score())
    scoreText = largeFont.render("YOUR SCORE: " + str(get_score()), True, FONT_COLOR)
    scoreTextRect = scoreText.get_rect(center=(500, 150))
    screen.blit(scoreText, scoreTextRect)
    highestScoreText = font.render("HIGHEST SCORE: " + str(highestScore), True, FONT_COLOR)
    highestScoreTextRect = highestScoreText.get_rect(center=(500, 250))
    screen.blit(highestScoreText, highestScoreTextRect)
    startText = font.render("RESTART (PRESS S)", True, FONT_COLOR)
    startTextRect = startText.get_rect(center=(500, 300))
    screen.blit(startText, startTextRect)
    quitText = font.render("QUIT (PRESS Q)", True, FONT_COLOR)
    quitTextRect = quitText.get_rect(center=(500, 350))
    screen.blit(quitText, quitTextRect)


gameStart = False
gameOver = False
background = Background()
player = Player()
pipes = Pipes()
TIMER = pygame.USEREVENT
pygame.time.set_timer(TIMER, PIPE_INTERVAL)

while True:
    if not gameStart:
        background.render()
        render_menu()
    elif not gameOver:
        background.render()
        player.render()
        pipes.render()
        render_header()
    else:
        background.render()
        render_endpage()
        player = Player()
        pipes = Pipes()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if not gameStart:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    gameStart = True
            elif not gameOver:
                if event.key == pygame.K_SPACE:
                    player.movement = 0
                    player.movement -= UP_FORCE
            else:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_s:
                    gameOver = False
                    score = 0
        elif event.type == TIMER and gameStart and not gameOver:
            pipes.create()

    if check_collision(player, pipes):
        gameOver = True

    pygame.display.update()
    clock.tick(120)
