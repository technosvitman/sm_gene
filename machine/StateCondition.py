

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
        @param other the other object to compare with
    '''
    def __eq__(self, other):
        if isinstance(other, str):
            return self.__event == other
        if not isinstance(other, StateCondition):
            return False
        if self.__event != other.getEvent():
            return False
        if self.__cond != other.getCond():
            return False
        return True
        
    '''
        @brief check too much proximity between conditions
        @param other the other condition to compare
        @return true on success, false on warning
    '''
    def check(self, other) :
        if self.__event !=  other.getEvent():
            return True

        if self.__cond == "" or \
            other.getCond() == "" :
            return False

        return self.__cond != other.getCond()

    '''
        @brief get action event
        @return event
    '''            
    def getEvent(self) :
        return self.__event
        
    '''
        @brief has transition condition
        @return true if not empty
    '''            
    def hasCond(self) :
        return ( self.__cond != "" )
        
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
    