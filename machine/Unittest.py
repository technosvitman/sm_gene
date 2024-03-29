
from pyctest import *
from .UnittestCase import *

'''
    @brief Tester
'''    
class Unittest:
    MODULE_FILE="statemachine/statemachine"

    '''
        @brief build tester
    '''
    def __init__(self):
        self.__loader = PycTester()
    
    '''
        @brief build library from c file
        @param config the unittest configuration
    '''
    def build(self, config):    
    
        self.__loader.load_source(\
        "#define UNITTEST_STATEMACHINE 1\n"); 
        
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
        @param config the unittest configuration
        @param paths unittest cases path
        @param machine the machine to check
    '''
    def unitest(self, config, paths, machine):
        print("================Unitary Test==============")  

        print("Generate test cases")
        for state in machine.getStates():
            self.__loader.appendTest(UnittestTestStateDefinition(state, config))  
        self.__loader.appendTest(UnittestTestGlobalDefinition(machine.getGlobal(), config))  
        for path in paths:
            self.__loader.appendTest(UnittestTestPath(path, config))  
            
        self.__loader.run(config.output)       