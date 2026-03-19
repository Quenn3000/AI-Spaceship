import pygame
import pymunk as pmk
import random
import environment_generator as env
import DFF_DeepFeedForward as dff
import naturalSelection as nat_select

AI_TO_KEEP = 10



# AI generations
AIs = []
for i in range(int(input("Number of AI : "))):
    cellList = [9] # inputs : old position (size:2), new position (size:2), mass, flag1 position (size:2), flag2 position (size:2)
    for i in range(random.randint(6, 15)):
        cellList.append(random.randint(10, 20))
    cellList.append(2) # outputs : force on reactor left-right, force on reactor bottom
    AIs.append(dff.DFF_DeepFeedForward(cellList, "sigmoid", factor=80, gap=-0.5))

AI_group = nat_select.AI_Group(AIs, AI_TO_KEEP, [(0, 0), (0.5, 0.05), (1, 0.1), (2, 0.15)], 10, 7)



# display & environment initialisation
pygame.init()
FPS = 60
display_width = 600
display_height = 600

display = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
space = pmk.Space(threaded=True)

duration = 1
i=1
while True:
    print("round :", i, "ai number :", len(AI_group.ais))
    AI_group.train(env.environment_emulation, env.environment_emulation_display, display, space, clock, FPS, duration)
    i+=1

"""
while env.environment_emulation(display, space, clock, FPS, AIs[0]) != -1:
    pass
"""




pygame.quit()
