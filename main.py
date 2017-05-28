import pygame
import sys

pygame.init()
font = pygame.font.SysFont("monospace", 15)

screen_rect = pygame.Rect(0, 0, 640, 480)
screen = pygame.display.set_mode(screen_rect.size)

target = pygame.image.load("data/bullseye.png")
rect = target.get_rect()
rect.x = (screen_rect.width - rect.width) / 2
rect.y = (screen_rect.height - rect.height) / 2

bwidth = bheight = 15
bullseye = pygame.Rect((screen_rect.width - bwidth) / 2,
                       (screen_rect.height - bheight) / 2,
                       bwidth,
                       bheight)

gwidth = gheight = 50
green = pygame.Rect((screen_rect.width - gwidth) / 2,
                    (screen_rect.height - gheight) /2,
                    gwidth,
                    gheight)

ywidth = yheight = 100
yellow = pygame.Rect((screen_rect.width - ywidth) / 2,
                     (screen_rect.height - yheight) /2,
                     ywidth,
                     yheight)

text = font.render("Click on the target!", True, (0, 0, 255))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bullseye.collidepoint(event.pos):
                text = font.render("Bull's Eye!", True, (255, 255, 255))
            elif green.collidepoint(event.pos):
                text = font.render("Green!", True, (0, 255, 0))
            elif yellow.collidepoint(event.pos):
                text = font.render("Yellow!", True, (255, 255, 0))
            else:
                text = font.render("Missed!", True, (255, 0, 0))

    screen.fill((0, 0, 0))
    screen.blit(target, rect)
    screen.blit(text, (0, 0))
    #pygame.draw.rect(screen, (255, 255, 255), bullseye)
    #pygame.draw.rect(screen, (255, 0, 0), green)
    #pygame.draw.rect(screen, (0, 0, 255), yellow)
    pygame.display.flip()
