
'''
    @brief this class reflect action decision regarding condition
'''
class EventAction():
    '''
        @brief build event action
        @param cond the conditions to perform the action
        @param to the target state if any
        @param job the job to do if any
    '''
    def __init__(self, cond="", to="", job=""):
        self.__to = to
        self.__job = job
        self.__cond = cond
        
    '''
        @brief get action state target
        @return state name
    '''            
    def getState(self) :
        return self.__to
        
    '''
        @brief has transition condition
        @return true if not empty
    '''            
    def hasCond(self) :
        return ( self.__cond != "" )
        
    '''
        @brief get action conditions
        @return condition
    '''            
    def getCond(self) :
        return self.__cond
        
    '''
        @brief get action job
        @return job
    '''            
    def getJob(self) :
        return self.__job
    
    '''
        @brief string represtation for state action
        @return the string
    '''  
    def __str__(self):
        return "Act( %s, %s, %s )"%(self.__to, self.__job, self.__cond)
        
'''
    @brief this class reflect the output switch on event received regarding condition and action to perform
'''
class EventCase():
    '''
        @brief build event case
        @param event the event title
    '''
    def __init__(self, event):
        self.__event = event
        self.__acts = []
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__acts)
        
    '''
        @brief equality implementation
        @param other the other element to compare with
    '''
    def __eq__(self, other):
        if isinstance(other, str):
            return self.__event == other
        if not isinstance(other, EventCase):
            return False
        if self.__event != other.getEvent():
            return False
        return True
        
    '''
        @brief get action event
        @return event
    '''            
    def getEvent(self) :
        return self.__event
        
    '''
        @brief add action 
        @param act the new action
    '''            
    def addAct(self, act) :
        if act not in self.__acts:
            self.__acts.append(act)
            
    '''
        @brief string represtation for state action
        @return the string
    '''  
    def __str__(self):
        output = "Event( %s ) { "%self.__event
        if len(self.__acts):
            output += "\n"
            for act in self.__acts:
                output += "%s\n"%str(act)
        return output + "}"
    
'''
    @brief this class store all event case for a state
'''
class EventCaseList():
    
    '''
        @brief build event case list
    '''
    def __init__(self):
        self.__events = []
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__events)
        
    '''
        @brief append from StateAction
        @param act the state action
    '''
    def append(self, act):
        for cond in act.getConds():
            evt = None
            a = EventAction(cond=cond.getCond(),\
                            to=act.getState(),\
                            job=act.getJob())
            for e in  self.__events:
                if e == cond.getEvent():
                    evt = e
                    break
            if not evt: 
                evt = EventCase(cond.getEvent())
                self.__events.append(evt)
            evt.addAct(a)
        
    '''
        @brief append from State
        @param state the state
    '''
    def appendState(self, state):
        for act in state.getActions():
            self.append(act)        
    
    '''
        @brief string represtation for state action
        @return the string
    '''  
    def __str__(self):
        output = "{ "
        if len(self.__events):
            output += "\n"
            for e in self.__events:
                output += "%s\n"%str(e)
        return output + "}"