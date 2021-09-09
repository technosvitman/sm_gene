
from .StateMachine import StateMachine

import graphviz

'''
    @brief this class describe what is a state machine
'''
class MachineGraph():
    '''
        @brief build state machine graph from state machine
        @param machine the state machine
    '''
    def __init__(self, machine):
        self.__machine=machine
        
    '''
        @brief compute machine graph
    '''
    def compute(self):
        dot = graphviz.Digraph(format='png', comment=self.__machine.getName())
        dot.render('round-table.png', view=True)  

    
