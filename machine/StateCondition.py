

class StateCondition():
    '''
        @brief build state action condition
        @param event the event title
        @param cond the linked condition
    '''
    def __init__(self, event, cond=""):
        self.__cond = cond
        self.__event = event
        
    '''
        @brief equality implementation
    '''
    def __eq__(self, other):
        if self.__event != other.getEvent():
            return False
        if self.__cond != other.getCond():
            return False
        return True
        
    '''
        @brief get action event
        @return event
    '''            
    def getEvent(self) :
        return self.__event
        
    '''
        @brief get transition condition
        @return condition
    '''            
    def getCond(self) :
        return self.__cond
        
    '''
        @brief set condition
        @param cond the condition
    '''            
    def setCond(self, cond) :
        self.__cond = cond
    
    '''
        @brief string represtation for state condition
        @return the string
    '''  
    def __str__(self):
        output = self.__event
        if self.__cond != "":
            output += " [ " + self.__cond + " ]"
        return output
    