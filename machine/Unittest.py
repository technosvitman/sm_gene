
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
    @see PycTestCase
'''
class UnittestCase(PycTestCase):

    def __init__(self, path, config):    
        super(PycTestCase, self).__init__()
        self.__path=path
        self.__config=config
        
    def __str__(self):
        return "Case : "+str(self.__path)
        
    def runTest(self):
        self.call(self.__config.init)
        
        #check entry
        entry = self.__path[0]
        print(entry)
        
        #self.assertEqual(getState(self), \
        #        self.c_test_machine_state_eSTATE1)
        
        for step in self.__path:
            print("*")
            #check new state
            
            
'''
    @brief configuration for test
'''
class UnittestCfg:
    '''
        @brief unittest input configuration
        @param source the source file to test
        @param header the header file to test
        @param init the initialisation method name
    '''    
    def __init__(self, source, header, init):
        self.source = source
        self.header = header
        self.init = init
        self.conds = {}
    
    
    def append(self, condition, alias, code):
        
        self.conds[condition]={"alias":alias,"code":code}
       
        
        
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
        
        for key,e in config.conds.items():
                
            self.__loader.load_source(\
            "int %s_v = 0;\nint * %s = &%s_v;\n"%(\
            e["alias"], e["alias"], e["alias"])); 
            
            src = src.replace(e["code"], e["alias"]+"_v")
                
            self.__loader.load_header(\
            "extern int * %s;\n"%(e["alias"])); 
        
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