from Chromosome import *
import random 
import numpy as np 
from operator import attrgetter
import numpy
import copy
import warnings
warnings.filterwarnings("error")

LARGE = 1000
MEDIUM = 500
SMALL = 100 
MAX_DEPTH = 8 

class Population() : 
    def __init__(self , functions , terminals ,scale=SMALL , depth=4):
        self.function_set = functions 
        self.terminals = terminals 
        self.scale = scale 
        self.Individuals = []
        self.depth = depth 
       

    def make_generation(self) : 
        individuals = []
        for i in range(self.scale):
            c = Chromosome(self.terminals, self.function_set, self.depth)
            c.depth = c.get_depth()
            individuals.append(c)
        return individuals

    def depth_limit( self , chromosome1 , cross_point1 , chromosome2 , cross_point2) : 
        g1 = chromosome1.gen[cross_point1]
        g2 = chromosome2.gen[cross_point2]
        if ( ((chromosome1.root.depth-g1.depth+g2.depth ) > MAX_DEPTH ) or ((chromosome2.root.depth-g2.depth+g1.depth ) > MAX_DEPTH )) :
            return False 
        return True  

    def can_swich( self , chromosome1 , cross_point1 , chromosome2 , cross_point2) : 
        b2 = self.same_condition( chromosome1 , cross_point1 , chromosome2 , cross_point2)
        if ( b2 == True) : 
            return self.depth_limit( chromosome1 , cross_point1 , chromosome2 , cross_point2)
        else  :
            return False 
            

    def crossOver(self , chromosome1 , chromosome2) : 
        hash_set = set()
        len1 = len(chromosome1.gen ) 
        len2 = len(chromosome2.gen )
        minL = min( len1 , len2 )
        while(True) : 
            cross_point1 = random.randint( 0 , minL-1 )
            cross_point2 = random.randint( 0 , minL-1 )
            hstr = str(cross_point1)+str(cross_point2)
            if( hstr not in hash_set ) :
                hash_set.add(hstr)
                if(  self.can_swich( chromosome1 , cross_point1 , chromosome2 , cross_point2)) : 
                    child1 = Chromosome(chromosome1.terminals , chromosome1.functions , chromosome1.depth,mode='None')
                    child1.gen = copy.deepcopy(chromosome1.gen )
                    child2 = Chromosome(chromosome2.terminals , chromosome2.functions , chromosome2.depth,mode='None')
                    child2.gen = copy.deepcopy(chromosome2.gen )
                    child1.root = child1.gen[0]
                    child2.root = child2.gen[0]
                    subtree1 = child1.extract_subtree(cross_point1)
                    subtree2 = child2.extract_subtree(cross_point2)
                    child1.replace_subtree(cross_point1 ,subtree2)
                    child2.replace_subtree(cross_point2,subtree1) 
                    return  child1,child2
            if ( len(hash_set )== minL**2 ) :
                return None , None 


    def same_condition(self , chromosome1 , cross_point1 , chromosome2 , cross_point2) : 
        if( chromosome1.gen[cross_point1].value in self.terminals and chromosome2.gen[cross_point2].value not in self.terminals) :
            return False 
        elif ( chromosome2.gen[cross_point2].value in self.terminals and chromosome1.gen[cross_point1].value not in self.terminals) :
            return False 
        else : 
            return True
        

    def mutation(self, individuals ,predefinedFuncs1,predefinedFuncs2) : 
        #self.individuals = sorted( self.individuals ,key=Chromosome.fitness,reversed=True)
        for item in individuals : 
            choosen_indx = random.randint(0,len(item.gen))
            item.Mutate(predefinedFuncs1,predefinedFuncs2,choosen_indx)
        return individuals 
    
#*********************************************************must change
    def Selection( self,input ,output,generation , prob ): 
        survived_parents = []
        i = 0 
        _,new_gen = self.set_fitness( generation=generation , input=input , output=output)
        inverse_mse_values = [1 / (ind.fitness+0.0000001) for ind in new_gen]
        while ( i < (len ( generation )//2) ): 
            i+=1
            parents = [self.roulette_wheel_selection(inverse_mse_values=inverse_mse_values) for _ in range(2)]
            p1 = generation[parents[0]]
            p2 = generation[parents[1]]
            ch1,ch2 = self.crossOver(chromosome1=p1,chromosome2=p2)
            if ( ch1 == None ) :
                # print("NONEEEEEEEEEEEEEEEEEEEEEEEEEEE1")
                ch1 = p1

            if ( ch2 == None ) :
                # print("NONEEEEEEEEEEEEEEEEEEEEEEEEEEE2")
                ch2 = p2
            rand = random.random()
            if( rand >= prob ) : 
                ch1.mutate( self.function_set[1] , self.function_set[2])
                ch2.mutate( self.function_set[1] , self.function_set[2])
            ch1.get_fitness( input , output )
            ch2.get_fitness(input , output )

            if ( ch1.fitness == None ) :
                # print("NONEEEEEEEEEEEEEEEEEEEEEEEEEEE1")
                ch1 = p1

            if ( ch2.fitness == None ) :
                # print("NONEEEEEEEEEEEEEEEEEEEEEEEEEEE2")
                ch2 = p2
            
            pops = [ch1 , ch2  , p1 , p2]
            
            sorted_pops = sorted(pops, key=lambda x: x.fitness)
            # sorted_children = sorted(children, key=lambda x: x.value)
            """
                pop the 2 best parts of each family :)
            """
            survived_parents.append(sorted_pops[0])
            survived_parents.append(sorted_pops[1])

        return survived_parents 
    

    def roulette_wheel_selection( self , inverse_mse_values ) : 
        total_fitness = sum(inverse_mse_values)
        selection_point = random.uniform(0, total_fitness)
        cumulative_fitness = 0
        for i, fitness in enumerate(inverse_mse_values):
            cumulative_fitness += fitness
            if cumulative_fitness >= selection_point:
                return i 

    def TournamentSelection( self , input , output , generation ) : 
        survived_parents = []
        _,new_gen = self.set_fitness( generation=generation , input=input , output=output)
        tournament_size = random.randint(6 , len(new_gen))
        for _ in range(tournament_size):
            # Randomly select individuals for the tournament
            tournament_individuals = random.sample(new_gen, tournament_size)
            # Calculate fitness for each individual in the tournament
            tournament_fitness = [ind.fitness for ind in tournament_individuals ]
            # Find the index of the individual with the minimum fitness (MSE in this case)
            winner_index = tournament_fitness.index(min(tournament_fitness))
            # Select the winning individual and add it to the list of selected parents
            survived_parents.append(tournament_individuals[winner_index])
        return survived_parents 


    def sigmoid(self, x):
        return 1 / (1 + numpy.exp(-x))

    def best_of_generation(self , generation ) : 
        try :
            return min( generation , key=attrgetter("fitness")).fitness
            
        except :
            print("Run has been failed")
            return -1
    
    def worst_of_generation( self , generation ) : 

        return max( generation , key=attrgetter("fitness")).fitness
    
    def get_average_fitness( self , generation ) : 
        return sum(chromosome.fitness for chromosome in generation)/len(generation)
    
    def print_best_function(self , generation ) : 
        best = min( generation , key=attrgetter("fitness")).gen
        b = [i.value for i in best]
        print(b)

    def set_fitness( self , generation ,input , output) : 
        sum = 0 
        new_gens = []
        d=0
        for item in generation : 
            if ( item != None ) : 
                d = item.get_fitness(input , output ) 
                if( d != None ):
                    sum += d 
                    new_gens.append( item)
        return sum,new_gens
            

    def print_info_generation( self , generation , i ) : 
        best_fitness = self.best_of_generation( generation=generation)
        if( best_fitness == -1 ) :
            return -1 
        loss = self.get_average_fitness( generation=generation)
        worst_fitness = self.worst_of_generation( generation=generation)
        population = len(generation)
        print( "*****************************************************************\n","generation number :" , i )
        print("best fitness: ", best_fitness , "\nworst fitness " , worst_fitness , "\naverage loss :" , loss , "\npopulation :" ,population,"\nbest funct :")
        self.print_best_function(generation=generation)

