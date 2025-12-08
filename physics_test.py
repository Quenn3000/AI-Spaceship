import pygame
import pymunk as pmk

FPS = 60

pygame.init()

display_width = 600
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
space = pmk.Space()
space.gravity = 0, -1000

def convert_coordinates(point): # between pygame and pymunk systems
    global display_height
    return point[0], display_height-point[1]


body = pmk.Body()
body.position = display_width/6, display_height
shape = pmk.Circle(body, 10)
shape.density = 1
shape.elasticity = 0.7
space.add(body, shape)

segment_body = pmk.Body(body_type=pmk.Body.STATIC)
segment_shape = pmk.Segment(segment_body, (0, 100), (display_width, 2), 4)
segment_shape.elasticity = 1
space.add(segment_body, segment_shape)

continuer = True
while continuer:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            continuer = False

    x, y = convert_coordinates(body.position)

    display.fill((160, 240, 250))
    pygame.draw.circle(display, (255, 0, 0), (int(x), int(y)), 10)
    pygame.draw.line(display, (0, 0, 0), (0, display_height-94), (display_width, display_height-6), 4)

    pygame.display.update()
    clock.tick(FPS)

    space.step(1/FPS)

pygame.quit()
