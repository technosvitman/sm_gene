
import yaml

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
        @brief build UnittestCfg from file
        @param file the file
        @return the config
    '''
    def fromFile(file):
        yaml_content = yaml.load(file, Loader=yaml.FullLoader)
        
        source = yaml_content.get('source')
        assert source != None, "source file to analyse should set(field 'source')"
        
        header = yaml_content.get('header')
        assert header != None, "header file to analyse should set(field 'header')"
        
        machine = yaml_content.get('machine')
        assert machine != None, "machine variable should be identified(field 'machine')"
        
        init = yaml_content.get('init')
        assert init != None, "init function should be identified(field 'init')"
        
        compute = yaml_content.get('compute')
        assert compute != None, "compute function should be identified(field 'compute')"
        
        cfg = UnittestCfg(source, header, machine, init, compute)
        
        conds = yaml_content.get('conds')
        
        assert conds != None, "configuration should define a dictionnary to translate conditions name and condition code"
        
        for cond_def in conds :
            cond = cond_def.get('cond')
            assert cond != None, "condition may have a conditions name('cond')"
            code = cond_def.get('code')
            assert code != None, "condition may have a code('ode')"
            cfg.appendCond(cond, code)
        
        states = yaml_content.get('states')
        
        assert states != None, "configuration should define a dictionnary to translate state name and state code"
        
        for state_def in states :
            state = state_def.get('state')
            assert state != None, "state may have a conditions name('state')"
            code = state_def.get('code')
            assert code != None, "state may have a code('ode')"
            cfg.appendState(state, code)
        
        events = yaml_content.get('events')
        
        assert events != None, "configuration should define a dictionnary to translate event name and event code"

        for event_def in events :
            event = event_def.get('event')
            assert event != None, "event may have a eventitions name('event')"
            code = event_def.get('code')
            assert code != None, "event may have a code('ode')"
            cfg.appendEvent(event, code)            
        
        return cfg
