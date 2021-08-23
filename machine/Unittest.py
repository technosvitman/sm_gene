
'''
    @brief this class reflect transition for path and test case
'''
class UnittestStep():
    '''
        @brief init UnittestStep
        Build it from transition action and current state
        @param state state name to check
        @param action original action
    '''
    def __init__(self, state, action):
        self.__action = action
        self.__state = state  
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__action)
    
    '''
        @brief compare UnittestStep with string
        @param other the string to compare
    '''
    def __eq__(self, other):
        if isinstance(other, str) : 
            return self.__state == other
        else:
            return False

    '''
        @brief get action state target
        @return state name
    '''            
    def getAction(self) :
        return self.__action
            
    '''
        @brief return string representation
    '''
    def __str__(self):
        output = "="+self.__state+"( "
        for cond in self.__action :
            output += str(cond)+" "
        output += ") " 
        return output+"=>"
        
'''
    @brief this class reflect unitest path for initial condition
'''
class UnittestPath():
    '''
        @brief UnittestPath
        @param origin initialise the test path with origin path
    '''
    def __init__(self, origin=None):
        self.__path = []
        self.__last = None
        if origin:
            self.__path = list(origin.getList())           
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__path)         
        
    '''
        @brief get path as list 
    '''
    def getList(self):
        return self.__path
        
    '''
        @brief return step to unittestpath
        @param step the step to add
    '''
    def append(self, step):
        self.__last=step
        self.__path.append(step)
            
    '''
        @brief return string representation
    '''
    def __str__(self):
        output = ""
        if len(self.__path):
            for e in self.__path:
                output += "%s "%str(e)
        return output + self.__last.getAction().getState()
        
'''
    @brief this class reflect unitest paths collection
'''
class UnittestPaths():
    '''
        @brief UnittestPaths
    '''
    def __init__(self, paths=None):
        self.__paths = []
        if paths:
            self.__paths = list(paths)
        
    '''
        @brief get iterator
    '''
    def __iter__(self):
        return iter(self.__paths)
        
    '''
        @brief return paths as list
    '''
    def getList(self):
        return self.__paths
            
    '''
        @brief add list
    '''
    def __add__(self, other):
        content = list(self.__paths)
        content += other.getList()
        output = UnittestPaths( content )
        return output
    
    '''
        @brief append path to collection
        @param path the unittestpath to add
    '''
    def append(self, path):
        self.__paths.append(path)
    
    '''
        @brief return string representation
    '''
    def __str__(self):
        output = "{"
        if len(self.__paths):
            output += "\n"
            for e in self.__paths:
                output += "%s\n"%str(e)
        return output + "}"
        
    