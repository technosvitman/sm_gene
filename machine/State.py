
'''
    @brief this class describe what is a state and what it can do
'''
class State():

    '''
        @brief build state with selected name
        @param name the state's name
        @param comment some information on state
        @param enterBrief if not empty the state has action on enter
        @param exitBrief if not empty the state has action on exit
    '''
    def __init__(self, name, comment="", enterBrief="", exitBrief=""):
        self.__name = name
        self.__comment = comment
        self.__enter = enterBrief
        self.__exit = exitBrief
        self.__actions = []
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__actions)
        
    '''
        @brief check too much proximity between conditions of 2 actions
        @return tupple list with each 2 conditions in case of error, empty list otherwise
    '''
    def check(self) :
        output = []
        for i in range(0, len(self.__actions)) :
            for j in range(i+1, len(self.__actions)):
                o = self.__actions[i].check( self.__actions[j] )
                if o != [] :
                    output.append( (\
                        self.__actions[i].getState(),\
                        self.__actions[j].getState(),\
                        o ) )
        return output

    '''
        @brief get state name
        @return name
    '''            
    def getName(self) :
        return self.__name
        
    '''
        @brief get state comment
        @return comment
    '''            
    def getComment(self) :
        return self.__comment
        
    '''
        @brief set state name
        @param name the name
    '''            
    def setName(self, name) :
        self.__name = name
        
    '''
        @brief get state comment
        @brief comment the comment
    '''            
    def setComment(self, comment) :
        self.__comment = comment
        
    '''
        @brief get state actions
        @return action list
    '''            
    def getActions(self) :
        return self.__actions
        
    '''
        @brief remove state action
        @param index action index
    '''            
    def removeAction(self, index) :
        del self.__actions[index]
        
    '''
        @brief get if has enter callback
        @return true if has callback
    '''
    def hasEnter(self) :
        return self.__enter!=""
        
    '''
        @brief get if has exit callback
        @return true if has callbac
    '''            
    def hasExit(self) :
        return self.__exit!=""
        
    '''
        @brief get enter action brief
        @return enter brief
    '''
    def getEnter(self) :
        return self.__enter
        
    '''
        @brief get exit action brief
        @return exit brief
    '''            
    def getExit(self) :
        return self.__exit
        
    '''
        @brief set enter action brief
        @brief onenter enter brief
    '''
    def setEnter(self, onenter) :
        self.__enter = onenter
        
    '''
        @brief set exit action brief
        @param onexit exit brief
    '''            
    def setExit(self, onexit) :
        self.__exit = onexit
        
    '''
        @brief append action
        @param action the action object
    '''            
    def appendAction(self, action):
        self.__actions.append( action )

    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = "State( " + self.__name +" ): Actions( "
        
        for action in self.__actions :
            output += "\n"+str(action)
            
        return output + "\n)"
        

