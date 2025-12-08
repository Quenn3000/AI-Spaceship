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
    def __init__(self, ais, keeping_number, mutations, generatingFromKeeping_number):
        self.ais = ais  #list of AI
        self.keeping_number = keeping_number #number of best AI to keep
        self.generatingFromKeeping_number = generatingFromKeeping_number #how much AI have to be generated from each keept AI
        self.mutations = mutations #list of tuple (degree of mutation in pound interval [-x, x], average of chance to add a neuron)

    def sort(self): # problem : all AIs are the same at the end
        bests = []
        best_index = [0, 0]
        lowest_index = 0
        for i in range(len(self.ais)):
            if len(bests) < self.keeping_number:
                try:
                    best_index[len(bests)] = i
                    bests.append(deepcopy(self.ais[i]))
                    continue
                except IndexError:
                    continue

            for j in range(len(bests)):
                if self.ais[i].score > bests[j].score:
                    bests[lowest_index] = deepcopy(self.ais[i])
                    best_index[lowest_index] = i

                    for k in range(len(bests)): # keep true the lowest index
                        if bests[lowest_index].score > bests[k].score:
                            lowest_index = k

                    break

        self.ais = []
        for i in range(len(bests)):
            for j in range(len(self.mutations)):
                for k in range(self.generatingFromKeeping_number):
                    self.ais.append(deepcopy(bests[i]))
                    ai = self.ais[-1]
                    for w_line in range(len(ai.W)):
                        for w_column in range(len(ai.W[w_line])):
                            ai.W[w_line][w_column] += rd.random()*self.mutations[j][0]

                    if rd.randint(1, 100) <= self.mutations[j][1]:
                        for l in range(1, len(ai.cellList)-1):
                            if rd.randint(1, ai.cellList.size()-2) == 1: #then add a neuron
                                ai.cellList[l] += 1
                                ai.hiddenSize
                                ai.W[l].append(np.random.randn(ai.cellSize[l+1]))





    def train(self, scoring, display, space, clock, FPS, duration):
        scores = []
        i=0
        for ai in self.ais:
            ai.score = scoring(display, space, clock, FPS, duration, ai, is_best=i<=AI_TO_KEEP)
            i+=1

        self.sort()
