
from .CodeGenerator import CodeGenerator

class Source(CodeGenerator):
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self, basename):
                
    
        # add includes files        
        inc_files = "#include \"statemachine.h\"\n#include \""+basename+".h\"\n"
        
        # add globales variables
        glbvar = "/**\n" 
        glbvar += " * @brief the machine state\n"
        glbvar += " */\n"
        glbvar += "statemachine_t "+self._prefix+";\n"
        
        # add states callbacks declaration
        clbks = "\n/*****************************************************************"
        clbks += "\n *                  States Callbacks section                     *"
        clbks += "\n *****************************************************************/\n\n"
        
        clbks += "/**\n" 
        clbks += " * @brief set machine state\n"
        clbks += " */\n"
        clbks += "static inline void " + self._prefix + "_set_state( "
        clbks += self._prefix + "_state_t state )\n"
        clbks += "{\n"
        clbks += CodeGenerator.INDENT_CHAR+"statemachine_Set_state( &" + self._prefix + ", state);\n"
        clbks += "}\n\n"
        
        global_action = self._machine.getGlobal()
        
        if global_action :
            clbks += self.__buildStateCallbacks(global_action);
        
        declaration = ""
        
        for state in self._machine.getStates() :
            clbks += self.__buildStateCallbacks(state)
            declaration += self.__buildStateDeclaration(state)+",\n"
                
        # add states declaration
            
        states = "\n/*****************************************************************"
        states += "\n *                    States declaration                         *"
        states += "\n *****************************************************************/\n\n"
        
        states += "\n/**\n"
        states += " * @brief states declaration for "+self._machine.getName()+" machine\n"
        states += " */\n"
        states += "const statemachine_state_t "+self._prefix+"_states["+self._prefix+"_state_eCOUNT]={\n"
        states += declaration
        states += "};\n"
        
        
        #write init and compute function
        func = "\n/**\n"
        func += " * @brief intitialize "+self._machine.getName()+" machine\n"
        func += " */\n"
        func += "\nvoid "+self._prefix+"_Init( void )"
        func += "\n{"
        func += "\n"+CodeGenerator.INDENT_CHAR+"statemachine_Init(&"+self._prefix+", "
        func += self._prefix+"_state_e"+self._machine.getEntry().upper()+", "+self._prefix+"_states);\n"
        func += "\n"+CodeGenerator.INDENT_CHAR+"statemachine_Start(&"+self._prefix+");\n"
        
        if global_action :
            declaration = self.__buildStateDeclaration(global_action)
            func += "\n"+CodeGenerator.INDENT_CHAR+"statemachine_Set_global(&"+self._prefix+", "+declaration+");\n"
            
        
        func += "}\n"
        
        func += "\n/**\n"
        func += " * @brief compute "+self._machine.getName()+" machine\n"
        func += " * @param event the "+self._machine.getName()+" event\n"
        func += " * @brief data attached event's data or NULL\n"
        func += " */\n"
        func += "\nvoid "+self._prefix+"_Compute( "+self._prefix+"_event_t event, void * data )"
        func += "\n{"
        func += "\n"+CodeGenerator.INDENT_CHAR+"statemachine_Compute(&"+self._prefix+", event, data);"
        func += "\n}\n"
                
        template = self.getTemplate("template_source.c")
        
        output = CodeGenerator.getFile(basename+".c")
        output.write(
            template.safe_substitute(
                statemachine_includes=inc_files,
                statemachine_globales=glbvar,
                statemachine_states_clbk=clbks,
                statemachine_states=states,
                statemachine_func=func))

    
    '''
        @brief compute state do job callback
        @param state the state
        @return the string containing the callback
    ''' 
    def __buildStateDoJob(self, state):
        output = ""
        name = state.getName()
        state_name = self._prefix+"_"+name
        
        output += "/**\n"
        output += " * @brief do job for state "+name+"\n"
        output += " */\n"
        output += "statemachineDO_JOB_CLBK("+state_name+")\n"
        output += "{\n"
        output += CodeGenerator.INDENT_CHAR+"statemachineNO_DATA(); //Remove this line to use data\n\n"
        output += CodeGenerator.INDENT_CHAR+"switch(statemachineEVENT_ID())\n"
        output += CodeGenerator.INDENT_CHAR+"{\n"
        
        for action in state.getActions():
            job = action.getJob()
            to = action.getState()
            for event in action.getEvents(): 
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"case "+self._prefix+"_event_e"+event.upper()+":\n"
                if job :
                    output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"/* "+job+" */\n"
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"//TODO write your code here\n"
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR
                if to :
                    output += CodeGenerator.INDENT_CHAR+self._prefix+"_set_state( "+self._prefix+"_state_e"+to.upper()+" );\n"
                output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"break;\n\n"
        
        output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"default:\n"
        output += CodeGenerator.INDENT_CHAR+CodeGenerator.INDENT_CHAR+"break;\n"
        output += CodeGenerator.INDENT_CHAR+"}\n"
        output += "}\n\n"
        
        return output
        
    '''
        @brief compute state callbacks
        @param state the state
        @return the string containing the callbacks
    ''' 
    def __buildStateCallbacks(self, state):
        output = ""
        name = state.getName()            
        state_name = self._prefix+"_"+name
                        
        if state.hasEnter() :
            output += "/**\n"
            output += " * @brief on enter state "+name+"\n"
            output += " */\n"
            output += "statemachineON_ENTER_CLBK("+state_name+")\n"
            output += "{\n"
            output += CodeGenerator.INDENT_CHAR+"/* "+state.getEnter()+" */\n"
            output += CodeGenerator.INDENT_CHAR+"//TODO write your code here\n"
            output += "}\n\n"
            
        output += self.__buildStateDoJob(state)
                
        if state.hasExit() :
            output += "/**\n"
            output += " * @brief on exit state "+name+"\n"
            output += " */\n"
            output += "statemachineON_EXIT_CLBK("+state_name+")\n"
            output += "{\n"
            output += CodeGenerator.INDENT_CHAR+"/* "+state.getExit()+" */\n"
            output += CodeGenerator.INDENT_CHAR+"//TODO write your code here\n"
            output += "}\n\n"
            
        return output
        
    '''
        @brief compute state declaration
        @param state the state
        @return the string containing the declaration
    ''' 
    def __buildStateDeclaration(self, state):
        output = CodeGenerator.INDENT_CHAR+"statemachineSTATE("   
        output += self._prefix+"_"+state.getName()+", "
        
                        
        if state.hasEnter() :
            output += "I"
            
        output += "D"
                
        if state.hasExit() :
            output += "O"
        
        output += " )"
            
        return output
        