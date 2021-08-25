
from pyctest import *

'''
    @see PycTestCase
'''
class UnittestCase(PycTestCase):
    '''
        @brief init UnittestCase
        @param path the path to test
        @param config test input configuration
    '''
    def __init__(self, path, config):    
        super(PycTestCase, self).__init__()
        self._path=path
        self._config=config
    
    '''
        @brief return current machine state
    '''
    def _getState(self):
        return getattr(self, "c_"+self._config.machine).c_state
       

'''
    @brief test path
'''
class UnittestTestPath(UnittestCase):   
    '''
        @brief string representation
    '''
    def __str__(self):
        return "Path : "+str(self._path)
    
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
        entry = self._path[0]
        
        self.assertEqual(self._getState(), \
                self.__toStateCode(entry))
        
        for step in self._path: 
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