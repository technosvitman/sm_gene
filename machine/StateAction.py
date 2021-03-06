

class StateAction():
    '''
        @brief build state action
        @param event the event triggering the transition
        @param to the target state if any
        @param job the job to do if any
    '''
    def __init__(self, event=[], to="", job=""):
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
        @brief set action state target
        @param to state name
    '''            
    def setState(self, to) :
        self.__to = to
        
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
        if event not in self.__events :
            self.__events.append(event)
        
    '''
        @brief update action event
        @param event, the current event
        @param newEvent, the new event
    '''            
    def updateEvent(self, event, newEvent) :
        self.__events.remove(event)
        if newEvent not in self.__events :
            self.__events.append(event)
            return True
        return False
        
    '''
        @brief get action job
        @return job
    '''            
    def getJob(self) :
        return self.__job
        
    '''
        @brief set action job
        @param job the job
    '''            
    def setJob(self, job) :
        self.__job = job
        
    '''
        @brief get if action is a well formed action
        @return True if ok
    '''            
    def isOk(self) :
        if len(self.__events) == 0:
            return False
        if self.__job=="" and self.__to == "":
            return False
        return True
    
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = ""
        if len(self.__events):
            output += self.__events[0]
            for event in self.__events[1:]:
                output += " | " + event
        return "on ("+ output + ")-> " + str(self.__to) +" do "+str(self.__job)
    