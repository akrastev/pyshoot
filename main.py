import logging
import pygame
import random
import sys

logging.basicConfig(format="%(asctime)s %(levelname)s    %(message)s",
                    level=logging.INFO)
logging.info("Hello, pyshoot.")

random.seed()
pygame.init()
pygame.mixer.init()

font = pygame.font.SysFont("monospace", 20)
boom = pygame.mixer.Sound("data/paa.ogg")

screen_rect = pygame.Rect(0, 0, 640, 480)
screen = pygame.display.set_mode(screen_rect.size)

def create_centered_square(enclosing_rect, side):
    return pygame.Rect((enclosing_rect.width - side) / 2,
                       (enclosing_rect.height - side) / 2,
                       side,
                       side)

class Target(object):
    def __init__(self):
        self.bullseye = create_centered_square(screen_rect, 15)
        self.green = create_centered_square(screen_rect, 50)
        self.yellow = create_centered_square(screen_rect, 100)
        self.target = pygame.image.load("data/bullseye.png")
        self.rect = self.target.get_rect()
        self.rect.x = (screen_rect.width - self.rect.width) / 2
        self.rect.y = (screen_rect.height - self.rect.height) / 2

    def in_bullseye(self, pos):
        return self.bullseye.collidepoint(pos)

    def in_green(self, pos):
        return self.green.collidepoint(pos)

    def in_yellow(self, pos):
        return self.yellow.collidepoint(pos)

    def render(self, screen):
        screen.blit(self.target, self.rect)
    
    def move(self, dw, dh):
        self.rect.x += dw
        self.rect.y += dh
        self.bullseye.x += dw
        self.bullseye.y += dh
        self.green.x += dw
        self.green.y += dh
        self.yellow.x += dw
        self.yellow.y += dh

    def get_rect(self):
        return self.rect

def random_move(enclosing_rect, rect):
    assert enclosing_rect.width >= rect.width
    assert enclosing_rect.height >= rect.height
    dw = random.randint(-rect.x, enclosing_rect.width - rect.width - rect.x)
    dh = random.randint(-rect.y, enclosing_rect.height - rect.height - rect.y)
    return dw, dh
        
target = Target()

text = font.render("Click on the target!", True, (0, 0, 255))

score = 0
score_text = font.render("Score: {0}".format(score), True, (255, 255, 255))

move_ms = pygame.time.get_ticks()
game_ms = pygame.time.get_ticks()

click = 0
bullseye = 0
green = 0
yellow = 0
miss = 0

playing = True

def print_stats(screen):
    click_text = font.render("Click: {0}".format(click), True, (255, 255, 255))
    bullseye_text = font.render("Bull's Eye: {0}".format(bullseye), True, (255, 255, 255))
    green_text = font.render("Green: {0}".format(green), True, (255, 255, 255))
    yellow_text = font.render("Yellow: {0}".format(yellow), True, (255, 255, 255))
    miss_text = font.render("Miss: {0}".format(miss), True, (255, 255, 255))

    screen.blit(click_text, (screen_rect.width / 2 - click_text.get_rect().width,
                             screen_rect.height / 2 - click_text.get_rect().height))

    screen.blit(bullseye_text, (screen_rect.width / 2 - bullseye_text.get_rect().width,
                                screen_rect.height / 2))

    screen.blit(green_text, (screen_rect.width / 2 - green_text.get_rect().width,
                             screen_rect.height / 2 + green_text.get_rect().height))

    screen.blit(yellow_text, (screen_rect.width / 2 - yellow_text.get_rect().width,
                              screen_rect.height / 2 + \
                              green_text.get_rect().height + \
                              yellow_text.get_rect().height))
    
    screen.blit(miss_text, (screen_rect.width / 2 - miss_text.get_rect().width,
                            screen_rect.height / 2 + \
                            green_text.get_rect().height + \
                            yellow_text.get_rect().height + \
                            miss_text.get_rect().height))

while True:
    if playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logging.info("Time to go now")
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                boom.play()
                click = click + 1
                if target.in_bullseye(event.pos):
                    text = font.render("Bull's Eye!", True, (255, 255, 255))
                    score += 50
                    logging.info("{0}: +50".format(event.pos))
                    bullseye = bullseye + 1
                elif target.in_green(event.pos):
                    text = font.render("Green!", True, (0, 255, 0))
                    score += 30
                    logging.info("{0}: +30".format(event.pos))
                    green = green + 1
                elif target.in_yellow(event.pos):
                    text = font.render("Yellow!", True, (255, 255, 0))
                    score += 10
                    logging.info("{0}: +10".format(event.pos))
                    yellow = yellow + 1
                else:
                    text = font.render("Missed!", True, (255, 0, 0))
                    logging.info("{0}: +0".format(event.pos))
                    miss = miss + 1
                    
                score_text = font.render("Score: {0}".format(score),
                                         True, (255, 255, 255))

    screen.fill((0, 0, 0))
    if playing:
        target.render(screen)
    else:
        print_stats(screen)
        
    screen.blit(text, (0, 0))
    screen.blit(score_text, (screen_rect.width - score_text.get_rect().width, 0))
    pygame.display.flip()

    ms = pygame.time.get_ticks()
    if playing and ms - move_ms > 1000:
        dw, dh = random_move(screen_rect, target.get_rect())
        logging.info("Moving {0}, {1}".format(dw, dh))
        target.move(dw, dh)
        move_ms = ms

    if ms - game_ms > 1500 * 60:
        playing = False
