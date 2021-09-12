
from .StateMachine import StateMachine

import graphviz

'''
    @brief this class describe what is a state machine
'''
class MachineGraph():

    MAIN_ENTRY="MAIN_ENTRY"
    
    '''
        @brief build state machine graph from state machine
        @param machine the state machine
    '''
    def __init__(self, machine):
        self.__machine=machine
        
    '''
        @brief add entry in state machine
        @param[in] name the entry name
    '''
    def __addEntry(self, name):
        self.__dot.node(name, label="", style="filled", shape="circle",fillcolor='black', width="0.15")

    
    '''
        @brief add state in state machine
        @param[in] name the state name
    '''
    def __buildLine(self, line, attr=""):
        return "<TR><TD %s>%s</TD></TR>"%(attr,line)
    
    '''
        @brief add state in state machine
        @param[in] name the state name
    '''
    def __addState(self, state):
        name = state.getName()
        content = "other<br/>stuff"
        content = "<<TABLE BORDER=\"0\">"
        content += self.__buildLine("<b>"+name+"</b>")
        content += self.__buildLine("<i ALIGN=\"left\">"+state.getComment()+"</i>", "ALIGN=\"left\"")
        content += self.__buildLine("")
        if state.hasEnter():
            content += self.__buildLine("<b>Entry :</b> / "+state.getEnter()+"", "ALIGN=\"left\"")
        if state.hasExit():
            content += self.__buildLine("<b>Exit :</b> / "+state.getExit()+"", "ALIGN=\"left\"")
        
        
        for action in state:
            if action.getState() == "" and action.getJob()!="":
                content += self.__buildLine("<b>On</b> : / do %s"%(action.getJob()), "ALIGN=\"left\"") 
            
            
        content += "</TABLE>>"
        
        self.__dot.node(name, label=content, style="filled, rounded", \
                        shape="record", fillcolor='#FFFFCC', color="#AA0000")
        
    '''
        @brief add state in state machine
        @param[in] name the state name
    '''
    def __addAction(self, fromState, action):   
        tt = ""
        first = True
        for cond in action:
            if not first :
                tt += " || "   
            first = False
            tt += "%s"%cond.getEvent()
            if cond.getCond() != "":
                tt += "[ %s ]"%cond.getCond()
        self.__dot.edge(fromState, action.getState(), label=tt)
        
    '''
        @brief compute machine graph
    '''
    def compute(self):
        self.__dot = graphviz.Digraph(format='png', comment=self.__machine.getName())
        
        self.__addEntry(MachineGraph.MAIN_ENTRY)
        
        for state in self.__machine.getStates():
            self.__addState(state)  
            for action in state:
                if action.getState() != "":
                    self.__addAction(state.getName(),action)              
            
        self.__dot.edge(MachineGraph.MAIN_ENTRY, self.__machine.getEntry(), label="")
        
        print(self.__dot.source)
        
        self.__dot.render('round-table.png', view=True)  

    
