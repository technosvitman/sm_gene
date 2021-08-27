
from pyctest import *

'''
    @see PycTestCase
'''
class UnittestCase(PycTestCase):
    '''
        @brief init UnittestCase
        @param config test input configuration
    '''
    def __init__(self, config):    
        super(PycTestCase, self).__init__()
        self._config=config
    
    '''
        @brief return current machine state
    '''
    def _getState(self):
        return getattr(self, "c_"+self._config.machine).current_state
       

'''
    @brief test path through state machine
'''
class UnittestTestPath(UnittestCase): 
    '''
        @brief init UnittestCase
        @param path the path to test
        @param config test input configuration
    '''
    def __init__(self, path, config):    
        super(UnittestTestPath, self).__init__(config)
        self.__path=path
        
    '''
        @brief string representation
    '''
    def __str__(self):
        return "Path : "+str(self.__path)
    
    '''
        @brief return state code from path step
        @param step the path step
    '''
    def __toStateCode(self, step):
        return getattr(self, "c_"+self._config.states[step.getState()])    
    
    '''
        @brief call state machine compute event
        @param event the event code to compute
    '''
    def __compute(self, event):
        evt = getattr(self, "c_"+self._config.events[event])
        self.call(self._config.compute, (evt, self.NULL()))    
    
    '''
        @brief get next state code from step
        @param step the path step
    '''    
    def __toNewStateCode(self, step):
        return getattr(self, "c_"+self._config.states[step.getDst()])
        
    '''
        @brief get alias condition
        @param cond the condition
    '''
    def __cond(self, cond):        
        return getattr(self, "c_"+self._config.conds[cond])
    
    '''
        @brief set condition to true
        @param cond the condition to set
    '''
    def __setCond(self, cond):        
        self.__cond(cond)[0] = 1        
    
    '''
        @brief set condition to false
        @param cond the condition to clear
    '''
    def __clearCond(self, cond):        
        self.__cond(cond)[0] = 0                
    
    '''
        @see PycTestCase
    '''
    def runTest(self):
        self.call(self._config.init)
        
        #check entry
        entry = self.__path[0]
        
        self.assertEqual(self._getState(), \
                self.__toStateCode(entry))
        
        for step in self.__path: 
            cond = step.getCond()
            
            # if has condition set it
            if cond.hasCond() :
                self.__setCond(cond.getCond())
        
            #compute transition
            self.__compute(cond.getEvent()) 
            
            # if has condition clear it
            if cond.hasCond() :
                self.__clearCond(cond.getCond())           
            
            #check new state
            self.assertEqual(self._getState(), \
                    self.__toNewStateCode(step))

'''
    @brief test state definition
'''
class UnittestTestStateDefinition(UnittestCase): 
    '''
        @brief init UnittestCase
        @param state the machine state to test
        @param config test input configuration
    '''
    def __init__(self, state, config):    
        super(UnittestTestStateDefinition, self).__init__(config)
        self.__state=state
        
    '''
        @brief string representation
    '''
    def __str__(self):
        return "Check state declaration ( %s ){entry:%s, exit:%s}"%(\
            self.__state.getName(), \
            self.__state.hasEnter(), \
            self.__state.hasExit())
        
    '''
        @brief return state code from name
    '''
    def __toStateCode(self):
        return getattr(self, "c_"+self._config.states[self.__state.getName()])  
        
    '''
        @brief return states table
    '''
    def __getStates(self):
        return getattr(self, "c_"+self._config.machine).states  
        
    '''
        @brief return state structure
    '''
    def __toStateDef(self):
        return self.__getStates()[self.__toStateCode()]    
    
    '''
        @see PycTestCase
    '''
    def runTest(self):
        self.call(self._config.init)
        
        state_def = self.__toStateDef()
        
        if self.__state.hasEnter():
            self.assertNotEqual(state_def.on_enter, self.NULL())
        else:
            self.assertEqual(state_def.on_enter, self.NULL())
        
        self.assertNotEqual(state_def.do_job, self.NULL())
        
        if self.__state.hasExit():
            self.assertNotEqual(state_def.on_exit, self.NULL())
        else:
            self.assertEqual(state_def.on_exit, self.NULL())

'''
    @brief test global action definition
'''
class UnittestTestGlobalDefinition(UnittestCase): 
    '''
        @brief init UnittestCase
        @param state the machine state to test
        @param config test input configuration
    '''
    def __init__(self, global_action, config):    
        super(UnittestTestGlobalDefinition, self).__init__(config)
        self.__global=global_action
        
    '''
        @brief string representation
    '''
    def __str__(self):
        return "Check global declaration ( %s ){entry:%s, do:%s, exit:%s}"%(\
            self.__global.getName(), \
            self.__global.hasEnter(), \
            len(self.__global.getActions())==0,\
            self.__global.hasExit())
        
    '''
        @brief return global enter action
    '''
    def __globalEnter(self):
        return getattr(self, "c_"+self._config.machine).global_on_enter  
        
    '''
        @brief return global enter action
    '''
    def __globalExit(self):
        return getattr(self, "c_"+self._config.machine).global_on_exit 
        
    '''
        @brief return global enter action
    '''
    def __globalDo(self):
        return getattr(self, "c_"+self._config.machine).global_do_job  
    
    '''
        @see PycTestCase
    '''
    def runTest(self):
        self.call(self._config.init)
        
        state_def = self.__globalEnter()
        
        if self.__global.hasEnter():
            self.assertNotEqual(self.__globalEnter(), self.NULL())
        else:
            self.assertEqual(self.__globalEnter(), self.NULL())
            
        if len(self.__global.getActions()) != 0:
            self.assertNotEqual(self.__globalDo(), self.NULL())
        else:
            self.assertEqual(self.__globalDo(), self.NULL())
        
        if self.__global.hasExit():
            self.assertNotEqual(self.__globalExit(), self.NULL())
        else:
            self.assertEqual(self.__globalExit(), self.NULL())
        
        
        