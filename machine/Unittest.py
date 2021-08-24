
from pyctest import *

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
        @brief return step state
    '''
    def getState(self):
        return self.__state
        
    '''
        @brief return state destination
    '''
    def getTo(self):
        return self.__action.getState()
    
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

    def __getitem__(self, n):
        return self.__path[n]
        
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
            
            
'''
    @brief configuration for test
'''
class UnittestCfg:
    '''
        @brief unittest input configuration
        @param source the source file to test
        @param header the header file to test
        @param init the initialisation method name
        @param compute the compute method name
    '''    
    def __init__(self, source, header, machine, init, compute):
        self.source = source
        self.header = header
        self.machine = machine
        self.init = init
        self.compute = compute
        self.conds = {}
        self.states = {}
        self.events = {}
    
    '''
        @brief append condition alias
        @param condition the original condition in statemachine
        @param code in file code line
    '''
    def appendCond(self, condition, code):        
        self.conds[condition]=code
    
    '''
        @brief append state alias
        @param state the original state in statemachine
        @param code in file code line
    '''
    def appendState(self, state, code):        
        self.states[state]=code
    
    '''
        @brief append event alias
        @param event the original event in statemachine
        @param code in file code line
    '''
    def appendEvent(self, event, code):        
        self.events[event]=code
        
'''
    @see PycTestCase
'''
class UnittestCase(PycTestCase):

    def __init__(self, path, config):    
        super(PycTestCase, self).__init__()
        self.__path=path
        self.__config=config
        
    def __str__(self):
        return "Case : "+str(self.__path)
        
    def __getState(self):
        return getattr(self, "c_"+self.__config.machine).c_state
        
    def __toStateCode(self, step):
        return getattr(self, "c_"+self.__config.states[step.getState()])
        
    def __compute(self, event):
        evt = getattr(self, "c_"+self.__config.events[event])
        self.call(self.__config.compute, (evt, self.NULL()))
    
    def __toNewStateCode(self, step):
        return getattr(self, "c_"+self.__config.states[step.getTo()])
    
    def __cond(self, cond):        
        return getattr(self, "c_"+self.__config.conds[cond])
    
    def __setCond(self, cond):        
        self.__cond(cond)[0] = 1
    
    def __clearCond(self, cond):        
        self.__cond(cond)[0] = 0
            
    def runTest(self):
        self.call(self.__config.init)
        
        #check entry
        entry = self.__path[0]
        
        self.assertEqual(self.__getState(), \
                self.__toStateCode(entry))
        
        for step in self.__path: 
            for cond in step:
                # if has condition set it
                if cond.hasCond() :
                    self.__setCond(cond.getCond())
            
                #compute transition
                self.__compute(cond.getEvent()) 
                
                # if has condition clear it
                if cond.hasCond() :
                    self.__clearCond(cond.getCond())           
                
                #check new state
                self.assertEqual(self.__getState(), \
                        self.__toNewStateCode(step))        
        
class Unittest:
    MODULE_FILE="statemachine/statemachine"

    def __init__(self):
        self.__loader = PycTester()
    
    '''
        @brief build library from c file
        @param config the unittest configuration
    '''
    def build(self, config):  
        
        self.__loader.load_module(Unittest.MODULE_FILE)
        
        src = str(open(config.source).read())
        
        alias = 0
        for key,e in config.conds.items():                
            self.__loader.load_source(\
            "int cond%d_v = 0;\nint * cond%d = &cond%d_v;\n"%(\
            alias, alias, alias)); 
            
            src = src.replace(e, "cond%d_v"%alias)
                
            self.__loader.load_header(\
            "extern int * cond%d;\n"%(alias));
            config.conds[key] = "cond%d"%alias
            alias += 1
                
        self.__loader.load_header(\
        "extern statemachine_t %s;\n"%(config.machine)); 
        
        self.__loader.load_source(src)
        
        self.__loader.load_header_file(config.header)
        
        self.__loader.build("_machine")
        
    '''
        @brief unitary test for C library
        @param paths unittest cases path
        @param config the unittest configuration
    '''
    def unitest(self, paths, config):
        print("================Unitary Test==============")  

        print("Generate test cases")
        for path in paths:
            self.__loader.appendTest(UnittestCase(path, config))   
        self.__loader.run()       