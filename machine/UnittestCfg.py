
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
