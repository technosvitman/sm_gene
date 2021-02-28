

class StateAction():
    '''
        @brief build state action
        @param event the event triggering the transition
        @param to the target state if any
        @param job the job to do if any
    '''
    def __init__(self, event=[], to=None, job=None):
        self.__to = to
        self.__job = job
        self.__events = event
        
    '''
        @brief get action state target
        @return state name
    '''            
    def getState(self) :
        return self.__to
        
    '''
        @brief get action event
        @return event
    '''            
    def getEvents(self) :
        return self.__events
        
    '''
        @brief remove action event
        @param index the event index
    '''            
    def removeEvent(self, index) :
        del self.__events[index]
        
    '''
        @brief add action event
        @param event, the new event
    '''            
    def addEvent(self, event) :
        self.__events.append(event)
        
    '''
        @brief get action job
        @return job
    '''            
    def getJob(self) :
        return self.__job
    
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = ""
        if len(self.__events):
            output += self.__events[0]["name"]
            for event in self.__events[1:]:
                output += " | " + event["name"]
        return "on ("+ output + ")-> " + str(self.__to) +" do "+str(self.__job)
    

class State():

    '''
        @brief build state with selected name
        @param name the state's name
        @param comment some information on state
        @param enterBrief if not empty the state has action on enter
        @param exitBrief if not empty the state has action on exit
    '''
    def __init__(self, name, comment, enterBrief, exitBrief):
        self.__name = name
        self.__comment = comment
        self.__enter = enterBrief
        self.__exit = exitBrief
        self.__actions = []
        
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
        @brief append a action
        @param state the state object
    '''            
    def appendAction(self, action):
        self.__actions.append( action )

    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = "State(" + self.__name +"): Actions( "
        
        for action in self.__actions :
            output += str(action)
            
        return output + ")"
        

