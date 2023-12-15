import matplotlib.pyplot as plt
import math 
from utils import * 
import random
from Chromosome import * 
from operator import attrgetter
from Poplute import * 
from GeneticProgram import * 
import os

function_set = { 2: [add , sub , div , mul , math.pow] ,1:[math.sin , math.cos , math.sqrt ]} #math.sin , math.cos ,, math.log   ,, math.exp
# if the input is only one dim

terminals = []
for i in range(40) : 
    chance = random.random() 
    if (chance > 0.5) : 
        terminals.append(random.randint(1,20) ) 
    elif ( chance <= 0.2 ) : 
        terminals.append( math.pi )
    else : 
        terminals.append('x') 

def f(x):
    return x**2 + 2*x


def f2(x):
    return math.sin(x)

input = [x for x in np.arange(-1 , 1 , 0.001)] #function inputs
output = [f2(x) for x in input]

stat = -1

while(stat == -1 ) :
    try : 
        algorith_runner = GeneticAlgorithmRunner( function_set=function_set , terminals=terminals , input=input , output=output,iter=100)
        stat = algorith_runner.run_genetic_algorithm()
        if ( stat.fitness <= 0.0001 ) :
            break 
        if( stat == -1 or stat.fitness > 0.001 ):
            os.system('cls' if os.name == 'nt' else 'clear')
            stat = -1
    except :
        os.system('cls' if os.name == 'nt' else 'clear')
        print("ERROR HAS BEEN OCCURED ...")
        print("STARTING OVER :)")
        stat = -1 
        continue

best = stat[0]
list_loss_gen = stat[1]
print(list_loss_gen)
print("best function :" ,best.gen) #print best function
print("best fitness :" ,  best.fitness)

y_pred = [[best.Calcule_Function(x , best.root)] for x in input] #predictions of our best calculated function
 
plt.plot(input, output, color='r', dashes=[6, 2], label='Expected')  #plot original function 
plt.plot(input, y_pred, color='g', dashes=[6, 3], label='Predicted') #plot calculated function
plt.legend()
plt.savefig('output_plot.png')
plt.show() 