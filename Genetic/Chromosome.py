import random
import math
from utils import *
import numpy as np
from node import *


class Chromosome:
    def __init__(self, terminals, funcs, depth,mode='grow'):
        self.depth = depth
        self.gen = []
        self.terminals = terminals
        self.functions = funcs
        self.fitness = None
        self.root = None
        if(mode=='grow') : 
            self.grow()

    def __eq__(self, other):
        if isinstance(other, Chromosome):
            return id(self) == id(other)
        return False

    def grow(self, level = 0 , parent = None ):
        leave = Node(False,None , None,None,None)
        if level == self.depth:
            value = random.choice(self.terminals)
            leave = Node( True , value= value , left=None , right=None, parent=parent ,depth=self.depth-level)
            self.gen.append(leave)
            return leave 
        else:
            if (random.random() > 0.4 or level==0 ):
                val = random.choice(self.functions[1] + self.functions[2])
                if val in self.functions[2]:
                    leave = Node( False , value= val , left=None , right=None ,parent=parent,depth=self.depth-level)
                    self.gen.append(leave)
                    leave.left =  self.grow(level + 1 ,parent=leave)
                    leave.right = self.grow(level + 1,parent=leave)
                else:
                    leave = Node( False , value= val , left=None , right=None ,parent=parent,depth=self.depth-level)
                    self.gen.append(leave)
                    leave.left = self.grow(level + 1 , parent=leave)
            else:
                val = random.choice(self.terminals)
                leave = Node( True , value= val , left=None , right=None, parent=parent ,depth=self.depth-level)
                self.gen.append(leave)
                return leave
        
            if (level ==  0) : 
                self.root = self.gen[0]
        return leave


    def calculate2oper(self, operand1 , operand2 , op ) : 
        match op.__name__ : 
            case add.__name__: 
                try : 
                    return round (add(operand1 , operand2) ,4)
                except : 
                    return None
            case sub.__name__ : 
                try : 
                    return round(sub(operand1 , operand2),4) 
                except : 
                    return None
            case div.__name__ : 
                try :  
                    return round(div( operand1 , operand2),4)
                except : 
                    return None
            case mul.__name__ : 
                try : 
                    return round(mul( operand1 , operand2 ),4) 
                except : 
                    None
            case math.pow.__name__ : 
                try :
                    return round(math.pow( operand1 , operand2 ),4)
                except : 
                    return None
            case _ : 
                try : 
                    return round(op(operand1 , operand2 ),4) 
                except : 
                    return None


    def calculate1oper(self , opernad , op ) : 
         match op.__name__ : 
            case math.sqrt.__name__: 
                if ( opernad < 0 ) : 
                    return None 
                return round(math.sqrt( opernad ),4)
            case math.cos.__name__  : 
                try:
                    v = round(math.cos(opernad),4)
                    # print("cosssssssssssssssssssssssssssssssss" , v)
                    return v
                except : 
                    return None
            case math.sin.__name__ : 
                try:
                    v = round(math.sin(opernad),4)
                    # print("sinnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn" , v)
                    return v
                except : 
                    return None
            case math.exp.__name__ : 
                try : 
                    return round(math.exp(opernad),4)
                except : 
                    return None
            case _:
                try : 
                    round(op(opernad ) ,4)
                except : 
                    return None


    def Calcule_Function(self, input , Node):
        item = Node
        # print( Node.value)
        if (item.isTerminal == True) :
            try :
                parsed_value = int(item.value)   
                return item.value 
            except : 
                if (item.value.find('x') != -1 ) :
                    n =  input
                    return n 
        else : 
            if ( item.value in self.functions[2]) : 
                left = self.Calcule_Function(input , item.left )
                right = self.Calcule_Function(input ,item.right )
                if ( left == None or right == None ) : 
                    return None 
                # print("value*************" , item.value) 
                return self.calculate2oper( left , right,item.value )
            else : 
                operand = self.Calcule_Function( input , item.left)
                if ( operand == None ):
                    return None 
                return self.calculate1oper( operand , item.value )
            
    

    def get_fitness(self, inputs, outputs):
        diff = 0.0000
        for i in range(len(inputs)):
            try:
                d = self.Calcule_Function(inputs[i] , self.root ) 
                if ( d == None ) : 
                    return None
                v = round((d - outputs[i])**2 , 4)
                # print(v)
                diff += (v) 
                diff = round( diff , 4 )
            except (RuntimeError ,RuntimeWarning) :
                self.gen = []
                self.grow()
                self.get_fitness(inputs, outputs)

        if len(inputs) == 0:
            return 1e9
        fitness = round(diff/(len(inputs)),3) 
        self.fitness = fitness
        return self.fitness


    def extract_subtree(self , start) : 
        subtree = self.gen[start] 
        if (start == 0 ) : 
            return self.root
        return subtree
        

    def replace_subtree(self, start ,new_child) : 
        n = self.gen[start]
        new_parent = n.parent
        diff = new_child.depth - n.depth 
        if ( new_parent == None or start ==0  ) : 
            # new_child.parent = None   # root case 
            self.root = new_child 
        elif( new_parent.right == n ) : 
            new_parent.right = new_child
        else : 
            new_parent.left = new_child
       
        new_child.parent = new_parent
        self.gen = []
        self.update_depth(new_child , diff)
        self.tree_fixup( self.root )
    
    
    def tree_fixup(self, node ) :   
        self.gen.append( node ) 
        if node == None :
            print()
        if node.isTerminal  :
            return node
        elif node.value in self.functions[2]:
            self.tree_fixup(node.left)
            self.tree_fixup(node.right)
        else:
            self.tree_fixup(node.left )
            

    def mutate(self , prefunctions1 ,prefunctions2 ) :
        index = random.randint(0 , len(self.gen)-1) 
        gen = self.gen[index]
        if( gen.isTerminal ) : 
            rand = random.random()
            if ( rand > 0.3 ) : 
                self.gen[index].value = random.randint(1 , 20 )
            else :
                 self.gen[index].value = 'x'
        else : 
            if ( gen.value in self.functions[1] ) : 
                self.gen[index].value = random.choice( prefunctions1)
            else : 
                self.gen[index].value = random.choice( prefunctions2)
        # self.root = self.gen[0]


    def get_current_depth(self, parent):
        elem = parent
        if elem.value in self.terminals : 
            return 1
        elif elem.value in self.functions[2]:
            left = self.get_current_depth(elem.left)
            right = self.get_current_depth(elem.right)
            return 1 + max(left, right)
        else:
            left= self.get_current_depth(elem.left )
            return left + 1
        

    def get_depth(self):
        return self.get_current_depth(self.root)-1
        

    def update_depth( self , gen ,diff ) : 
        elem = gen.parent
        while ( elem != None) : 
            elem.depth += diff 
            elem = elem.parent 
    

   
