

class StateAction():
    '''
        @brief build state action
        @param conds the conditions triggering the transition
        @param to the target state if any
        @param job the job to do if any
    '''
    def __init__(self, conds=None, to="", job=""):
        self.__to = to
        self.__job = job
        if conds : 
            self.__conds = conds
        else:
            self.__conds = []
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__conds)

    '''
        @brief check too much proximity between conditions of 2 actions
        @param other the other action to compare
        @return tupple list with each 2 conditions in case of error, empty list otherwise
    '''
    def check(self, other) :
        output = []
        for c in self.__conds :
            for co in other:
                if self.__to != "" and \
                    other.getState() != "" and \
                    not c.check(co):
                    output.append((str(c), str(co)))
        return output

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
        @brief get action conditions
        @return conditions
    '''            
    def getConds(self) :
        return self.__conds
        
    '''
        @brief remove action condition
        @param index the condition index
    '''            
    def removeCond(self, index) :
        del self.__conds[index]
        
    '''
        @brief add action condition
        @param cond the new event
    '''            
    def addCond(self, cond) :
        if cond not in self.__conds :
            self.__conds.append(cond)
        
    '''
        @brief update action condition
        @param cond the current condition
        @param newCond the new condition
    '''            
    def updateCond(self, cond, newCond) :
        self.__conds.remove(cond)
        if newCond not in self.__conds :
            self.__conds.append(newCond)
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
        if len(self.__conds) == 0:
            return False
        if self.__job=="" and self.__to == "":
            return False
        return True
    
    '''
        @brief string represtation for state action
        @return the string
    '''  
    def __str__(self):
        output = ""
        if len(self.__conds):
            output += str(self.__conds[0])
            for cond in self.__conds[1:]:
                output += " || " + str(cond)
        return "on ( "+ output + " )-> " + str(self.__to) +" do "+str(self.__job)
    