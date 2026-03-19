import random as rd
from inspect import isfunction
from copy import *
import pygame

AI_TO_KEEP = 10

class AI_elem:
    def __init__(self, neural_network, score):
        self.neural_network = neural_network
        self.score = score

class AI_Group:
    def __init__(self, ais, keeping_number, mutations, nb_mut_per_bestAI, nb_iter_per_AI_training):
        self.ais = ais  #list of AI
        self.keeping_number = keeping_number #number of best AI to keep
        self.nb_mut_per_bestAI = nb_mut_per_bestAI #how much AI have to be generated from each keept AI
        self.mutations = mutations #list of tuple (degree of mutation in pound interval [-x, x], average of chance to add a neuron)
        self.nb_iter_per_AI_training = nb_iter_per_AI_training #number iteration of the random simulation per AI

    def sort_and_mut(self): # problem : all AIs are the same at the end
        bests = []
        for i in range(len(self.ais)):
            #add the ai by default if there is no enougth AI in the bests list
            if len(bests) < self.keeping_number:
                bests.append(deepcopy(self.ais[i]))
                continue


            #if I already have a correct number of best AI

            for j in range(len(bests)):
                if self.ais[i].score > bests[j].score:
                    bests[j] = deepcopy(self.ais[i])
        
        print(bests)

        self.ais = []

        for i in range(len(bests)):
            for j in range(len(self.mutations)):
                for k in range(self.nb_mut_per_bestAI):

                    self.ais.append(deepcopy(bests[i]))

                    muted_ai = self.ais[-1]
                    for w_line in range(len(muted_ai.W)):
                        for w_column in range(len(muted_ai.W[w_line])):
                            muted_ai.W[w_line][w_column] += rd.random()*self.mutations[j][0]

                    if rd.randint(1, 100) <= self.mutations[j][1]:
                        for l in range(1, len(muted_ai.cellList)-1):
                            if rd.randint(1, muted_ai.cellList.size()-2) == 1: #then add a neuron
                                muted_ai.cellList[l] += 1
                                muted_ai.hiddenSize
                                muted_ai.W[l].append(np.random.randn(muted_ai.cellSize[l+1]))
                    
                    self.ais.append(deepcopy(muted_ai))





    def train(self, scoring, show, display, space, clock, FPS, duration):
        scores = []
        i=0
        for ai in self.ais:
            ai.score = scoring(space, FPS, duration, ai, self.nb_iter_per_AI_training)
            i+=1

        self.sort_and_mut()

        show(display, space, clock, FPS, duration, self.ais[0], self.nb_iter_per_AI_training, is_best=True)
