import pygame
import pymunk as pmk
from pymunk.vec2d import Vec2d
import random
import time

display_width = 600
display_height = 600
FLAG_DIFF = 100

def convert_coordinates(point): # between pygame and pymunk systems
    global display_height
    return point[0], display_height-point[1]


"""
Spaceship class :
    mass (float) : the mass of the spaceship
    display_width (float/int) : the width of the scene
    display_height (float/int) : the height of the scene
"""
class Spaceship:
    def __init__(self, mass, display_width, display_height):
        self.body = pmk.Body()
        self.body.position = display_width/2, display_height
        self.shape = pmk.Circle(self.body, 10)
        self.shape.density = 1
        self.shape.elasticity = random.uniform(0.1, 1) # set random


"""
Ground class :
    display_width (float/int) : the width of the scene
    display_height (float/int) : the height of the scene
    self.equation (func) : the affine function representing the line of the ground
"""
class Ground:
    def __init__(self, display_width, display_height):
        self.body = pmk.Body(body_type=pmk.Body.STATIC)

        self.equ_a = random.uniform(-0.5, 0.5)
        if self.equ_a <= 0:
            self.equ_b = -self.equ_a*display_width
        else:
            self.equ_b = 0
        self.equation = lambda x : self.equ_a*x + self.equ_b

        self.shape = pmk.Segment(self.body, (0, self.equation(0)), (display_width, self.equation(display_width)), 4)
        self.shape.elasticity = random.uniform(0.1, 0.5)

class Flag:
    def __init__(self, x, ground_equ):
        self.position = [0, 0]
        self.position[0] = x
        self.position[1] = ground_equ(self.position[0])+20



def environment_emulation(display, space, clock, FPS, duration, AI, is_best=False):
    score = 0
    font = pygame.font.Font("font/OpenSans.ttf", 32)
    best_text = font.render("One of the bests", True, (0, 255, 0))
    best_text_rect = best_text.get_rect()
    best_text_rect.move_ip(30, 30)

    for i in range(5):
        # object declaration
        space.gravity = 0, -4000 #random.uniform(-1000, -200)*4
        spaceship = Spaceship(1, 600, 600)
        space.add(spaceship.body, spaceship.shape)

        ground = Ground(600, 600)
        space.add(ground.body, ground.shape)

        flag1 = Flag(random.uniform(0, display_width-FLAG_DIFF), ground.equation) #idea : faire en sorte que les drapeaux ne puissent pas être en bordure (pour éviter de récompenser les comportements radicaux)
        flag2 = Flag(flag1.position[0]+FLAG_DIFF, ground.equation)
        flag_image = pygame.image.load("img/flag.png")
        flag_image = pygame.transform.scale(flag_image, (20, 20))


        time_start = time.time()
        continuer = True
        while continuer:
            spaceship.old_position = spaceship.body.position

            # event managment
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()

            x, y = convert_coordinates(spaceship.body.position)

            # drawing
            display.fill((160, 240, 250))
            pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), 10)
            pygame.draw.line(display, (0, 0, 0), convert_coordinates((0, ground.equation(0))), convert_coordinates((display_width, ground.equation(display_width))), 4)
            display.blit(flag_image, convert_coordinates((int(flag1.position[0]), int(flag1.position[1]))))
            display.blit(flag_image, convert_coordinates((int(flag2.position[0]), int(flag2.position[1]))))
            if is_best:
                display.blit(best_text, best_text_rect)

            # update
            pygame.display.update()
            clock.tick(FPS)
            space.step(1/FPS)

            # AI calculation
            AI_result = AI.forward([spaceship.old_position[0], spaceship.old_position[1], spaceship.body.position[0], spaceship.body.position[1], spaceship.body.mass, flag1.position[0], flag1.position[1], flag2.position[0], flag2.position[1]])
            spaceship.body.velocity = Vec2d(spaceship.body.velocity[0] + AI_result[0], spaceship.body.velocity[1] + AI_result[1])


            time_current = time.time() - time_start
            # exit condition : if on the ground (with an admitted error of 5 pixels) or if the time is elapsed
            if ground.equation(spaceship.body.position[0])+spaceship.shape.radius+5 >= spaceship.body.position[1] or time_current >= duration: # if the spaceship is on the ground
                continuer = False


        # set score for this AI
        score -= (ground.equation(spaceship.body.position[0])-spaceship.body.position[1])/3 # distance from the ground
        score -= abs(spaceship.old_position-spaceship.body.position) # landing speed

        if spaceship.body.position[0] > flag1.position[0] and spaceship.body.position[0] > flag2.position[0]:
            if flag1.position[0] >= flag2.position[0]:
                score -= abs(spaceship.body.position[0] - flag1.position[0])*10
            else:
                score -= abs(spaceship.body.position[0] - flag2.position[0])*10

        elif spaceship.body.position[0] < flag1.position[0] and spaceship.body.position[0] < flag2.position[0]:
            if flag1.position[0] <= flag2.position[0]:
                score -= abs(spaceship.body.position[0] - flag1.position[0])*10
            else:
                score -= abs(spaceship.body.position[0] - flag2.position[0])*10


        space.remove(spaceship.body, spaceship.shape)
        space.remove(ground.body, ground.shape)

    print("score :", score)
    return score
