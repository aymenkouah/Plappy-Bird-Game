#Made by: Kouah Mohammed Aymen
#Computer science student at "National Computer science Engineering School, Algiers (ESI)"
#E-mail: jm_kouah@esi.dz
#Github: https://github.com/aymenkouah
#Requires the Pygame Package


# packages
import pygame
import random
import time

# classes

class bird():
    def __init__(self, width, height):
        self.x = 100
        self.y = height // 2
        self.radius = 20
        self.gravity = 2
        self.velocity = 0

    def draw(self, window, color):
        pygame.draw.circle(window, color, (self.x, self.y), self.radius)

    def update_pos(self, height):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y > height - self.radius:
            self.y = height - self.radius
        if self.y < self.radius:
            self.y = self.radius

    def up(self):
        self.velocity = -20

    def dead(self, pipes):
        for i in range(len(pipes)):
            if (self.y+self.radius > pipes[i].bottom or self.y-self.radius < pipes[i].top):
                if (pipes[i].x < self.x + self.radius < pipes[i].x + pipes[i].width + 2*self.radius):
                    return True
        return False


class pipe():
    def __init__(self, width, height, radius, velocity=2):
        self.width = 30
        self.gap = radius * 10
        self.top = random.randint(self.gap, height - self.gap)
        self.bottom = self.top + self.gap
        self.x = width
        self.velocity = velocity
        self.acceleration = 0.005

    def update(self, width, height):
        self.velocity += self.acceleration
        self.x -= self.velocity

    def draw(self, window, color, height, radius):
        pygame.draw.rect(window, color, (self.x, 0, self.width, self.top))

        pygame.draw.rect(
            window, color, (self.x, self.bottom, self.width, height - radius))


# variables

bird_color = (255, 255, 255)  # #FFFFFF
pipes_color = (255, 0, 0)  # #990000
background_color = (0, 0, 0)  # #000000
text_color = (153, 128, 0)  # #998000
width = 600
height = 800

game_running = True
fps = pygame.time.Clock()
pygame.init()
pygame.mixer.init()
window = pygame.display.set_mode((width, height))
pygame.mixer.music.load(
    "Nostalgia.mp3")
pygame.mixer.music.play(loops=-1)


flop = bird(width, height)
pipes = []
score = 0


# functions

def create_pipes(pipes):
    if len(pipes) > 0:
        pip = pipe(width, height, flop.radius, pipes[0].velocity)
    else:
        pip = pipe(width, height, flop.radius)

    pipes.append(pip)


def cancel_pipes(pipes, score):
    if len(pipes) > 0 and pipes[0].x < -pipes[0].width:
        pipes.pop(0)
        score += 1
        
    return score


def draw_pipes(pipes):
    for i in range(len(pipes)):
        pipes[i].update(width, height)
        pipes[i].draw(window, pipes_color, height, flop.radius)


def text_to_screen(window, score):
    window.fill(background_color)
    font = pygame.font.SysFont(None, 50)
    stext = "Your score is: " + str(score)
    score_text = font.render(stext, True, text_color)
    window.blit(score_text, [20, 100])


# main code

while game_running:
    game_running = not flop.dead(pipes)
    
    window.fill(background_color)
    
    if len(pipes) == 0 or pipes[-1].x < width // 2:
        create_pipes(pipes)

    score = cancel_pipes(pipes, score)
    draw_pipes(pipes)

    flop.update_pos(height)
    flop.draw(window, bird_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                flop.up()

    fps.tick(30)
    pygame.display.update()

pygame.mixer.quit()
text_to_screen(window, score)

pygame.display.update()
time.sleep(3)

pygame.quit()
