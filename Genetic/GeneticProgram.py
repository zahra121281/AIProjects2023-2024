import math
from typing import Any 
from utils import * 
import random
from Chromosome import * 
from Poplute import * 
import sys

class GeneticAlgorithmRunner : 
    def __init__(self, function_set , terminals, input , output ,iter=30):
        self.functions = function_set
        self.terminals = terminals 
        self.poplutor = Population(function_set , terminals ,scale=MEDIUM)
        self.period = 10000
        self.input = input 
        self.output = output
        self.iteration = iter 
    def run_genetic_algorithm(self) : 
        """
            1- create generation\n
            2- select parents\n 
            3- create children\n
            4- generation meet conditions ? stop : jump to 1
        """
        last_fitnest = sys.maxsize
        best_gen = None
        count = 1 
        loss_in_generation = []
        generation = self.poplutor.make_generation()
        _, generation = self.poplutor.set_fitness( generation=generation , input=self.input , output=self.output) 
        # self.poplutor.set_fitness( generation=generation , input=self.input , output=self.output)
        while( count < self.iteration  ) : 
            stat = self.poplutor.print_info_generation(generation=generation , i=count)
            # best_gen = min( generation , key=attrgetter("fitness")).gen
            if( stat == -1 ) :
                return -1
            best_in_generation = min( generation , key=attrgetter("fitness")).fitness
            loss_in_generation.append((count , best_in_generation ) )
            if (best_in_generation == 0 and count >= 6 ) :
                break
            count +=1    
            new_ones = self.poplutor.Selection( input=self.input , output=self.output,generation=generation,prob=(count/self.iteration))
            # choosen_parents = self.poplutor.TournamentSelection( input=self.input , output=self.output,generation=generation)
            # new_ones = self.poplutor.next_generation( choosen_parents )
            generation = new_ones
            _, generation = self.poplutor.set_fitness( generation=generation , input=self.input , output=self.output) 

        # print best gen 
        best_gen = min( generation , key=attrgetter("fitness")) 
        return best_gen,loss_in_generation
        