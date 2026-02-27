import pygame, sys, time, random
from pathlib import Path

# to make sure the files are read from the script directory
script_dir = Path(__file__).resolve().parent

#variables
width = 1000
height = 600
border = 20
fgColour = (255,255,255)
bgColour = (0,0,0)
radius = 20
thickness = 20

#classes
class Ball(object):
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    
    def update(self):
        pygame.draw.circle(screen, bgColour, (self.x, self.y), radius)
        self.x += self.vx
        self.y += self.vy
        pygame.draw.circle(screen, fgColour, (self.x, self.y), radius)

class Paddle(object):
    def __init__(self, vy, thickness, paddle_height):
        self.vy = vy
        self.th = thickness
        self.h = paddle_height
        self.y = .5 * (height - self.h)
        self.move_up = False
        self.move_down = False

    def update(self):
        pygame.draw.rect(screen, fgColour, pygame.Rect(width - self.th, self.y, self.th, self.h))
        if self.move_down:
            pygame.draw.rect(screen, bgColour, pygame.Rect(width - self.th, self.y, self.th, self.h))
            self.y += self.vy
            pygame.draw.rect(screen, fgColour, pygame.Rect(width - self.th, self.y, self.th, self.h))
        if self.move_up:
            pygame.draw.rect(screen, bgColour, pygame.Rect(width - self.th, self.y, self.th, self.h))
            self.y -= self.vy
            pygame.draw.rect(screen, fgColour, pygame.Rect(width - self.th, self.y, self.th, self.h))

pygame.font.init()
font = pygame.font.SysFont(None, 38)

def show_scores():
    with open(script_dir/'highscore.txt') as file:
        highscore = int(file.read())

    current_score = font.render('Score: ' + str(score), False, (100, 100, 200), bgColour)
    high_score = font.render('Highscore: '+str(highscore), True, (100,150, 200), bgColour)

    screen.blit(current_score, (border, border))
    screen.blit(high_score, (width / 2, border))

#game functions
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')

pygame.draw.rect(screen, fgColour, pygame.Rect(0,0, width, border))
pygame.draw.rect(screen, fgColour, pygame.Rect(0,0, border, height))
pygame.draw.rect(screen, fgColour, pygame.Rect(0,height - border, width, border))

x = -random.choice([2, 3])
y = -random.choice([2, 3])
print(x, y)
ball = Ball(width - radius -thickness, height/2, x, y)
paddle = Paddle(4,thickness, 100)
score = 0
while True:
    #print(clock.get_fps())
    pygame.draw.rect(screen, (255,0,0), pygame.Rect(
        width - thickness, border, .1, height - 2 * border
        ))
    ball.update()
    if ball.y <= border + radius or ball.y >= (height - border - radius):
        ball.vy *= -1
    if ball.x <= border + radius:
        ball.vx *= -1
    if (ball.x + radius == width - paddle.th and (
        ball.y >= paddle.y and ball.y <= paddle.y + paddle.h
        )):
        ball.vx *= -1
        score += 1
    paddle.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or ball.x >= width:
            print('Your score: '+str(score))
            with open(script_dir/'highscore.txt') as file:
                highscore = int(file.read())
                print('highscore: '+str(highscore))
                if score > highscore:
                    with open(script_dir/'highscore.txt','w') as file:
                        file.write(str(score))
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle.move_up = True
            elif event.key == pygame.K_DOWN:
                paddle.move_down = True
            elif event.key == pygame.K_LALT and pygame.K_F4:
                sys.exit()
    
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                paddle.move_up = False
            if event.key == pygame.K_DOWN:
                paddle.move_down = False
    
    if paddle.y <= border:
        paddle.move_up = False
    elif paddle.y + paddle.h >= height - border:
        paddle.move_down = False
    clock.tick(144)
    show_scores()
    pygame.display.flip()
