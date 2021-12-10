import pygame

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Flappy Bird")

menuImg = pygame.image.load("images/menu.png")
backgroundImg = pygame.image.load("images/background.png")

font = pygame.font.Font("freesansbold.ttf", 32)


def render_background():
    screen.blit(backgroundImg, (0, 0))


def render_menu():
    screen.blit(menuImg, (0, 0))
    startTxt = font.render("Start (Press S)", True, (0, 0, 100))
    screen.blit(startTxt, (400, 200))


def main():
    running = True
    gameStarted = False
    gameOver = False
    while running:
        if not gameStarted:
            render_menu()
        else:
            render_background()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s and not gameStarted:
                    gameStarted = True
        pygame.display.update()


if __name__ == "__main__":
    main()
