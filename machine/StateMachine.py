
from .State import State
from .StateAction import StateAction

import yaml

class StateMachine():

    INDENT_STRING = "    "
    
    '''
        @brief build state machine with selected name
        @param name the state machine's name
        @param entry the entry state name
    '''
    def __init__(self, name="", entry=""):
        self.__name = name
        self.__entry = entry
        self.__events = {}
        self.__states = []
        self.__global = State("global")
        
    '''
        @brief get machine name
        @return name
    '''            
    def getName(self) :
        return self.__name
        
    '''
        @brief get entry state
        @return the entry state name
    '''            
    def getEntry(self) :
        return self.__entry
        
    '''
        @brief get machine name
        @param name the name
    '''            
    def setName(self, name) :
        self.__name = name
        
    '''
        @brief set entry state
        @param entry the entry state name
    '''            
    def setEntry(self, entry) :
        self.__entry = entry
        
    '''
        @brief get event name and comment list
        @return the list
    '''            
    def getEvents(self) :
        infos = []
        for event, comment in self.__events.items():
            infos.append({"name":event, "comment":comment})
        return infos
        
    '''
        @brief get event name and comment list
        @return the list
    '''            
    def getEventNames(self) :
        infos = []
        for event, comment in self.__events.items():
            infos.append(event)
        return infos
        
    '''
        @brief get event comment
        @param event the event
    '''            
    def getEventComment(self, event) :
        if event not in self.__events:
            return ""
        return self.__events[event]
        
    '''
        @brief set event comment
        @param event the event
        @param comment the comment
    '''               
    def setEventComment(self, event, comment) :
        self.__events[event] = comment
        
    '''
        @brief get state list
        @return the list
    '''            
    def getStates(self) :
        return self.__states
        
    '''
        @brief remove state from list
        @return the list
    '''            
    def removeState(self, index) :
        sname = self.__states[index].getName()        
        del self.__states[index]    
        for state in self.__states : 
            for action in state.getActions():
                if action.getState() == sname:
                    del action
                
    '''
        @brief get state's name and comment list
        @return the list
    '''            
    def getStateInfo(self) :
        infos = []
        for state in self.__states:
            infos.append({"name":state.getName(), "comment":state.getComment()})
        return infos
                
    '''
        @brief get state's name list
        @return the list
    '''            
    def getStateNames(self) :
        infos = []
        for state in self.__states:
            infos.append(state.getName())
        return infos
        
    '''
        @brief append an event to the machine
        @param event the event name to append
        @param comment the event comment
    '''            
    def appendEvent(self, event, comment):
        if event in self.__events:
            if comment!="": 
                self.__events[event] = comment
        else :
            events = {}
            keys = list(self.__events.keys())
            keys.append(event)
            keys.sort()
            pos = keys.index(event)
            for k in keys[:pos] :
                events[k] = self.__events[k]
            self.__events[event] = comment
            for k in keys[pos:] :
                events[k] = self.__events[k]
            self.__events = events
        
    '''
        @brief clean up machine content
    '''            
    def cleanUp(self):
        events = []
        states = []
        for state in self.__states :
            for action in state.getActions():
                if action.getState() not in self.getStateNames():
                    states.append(action.getState())
                for event in action.getEvents() :
                    if event not in events :
                        events.append(event)
        todel = []
        for event, comment in self.__events.items():
            if event not in events :
                todel.append(event)
        for td in todel : 
            del self.__events[td]
        
    '''
        @brief set global state action
        @param state the state object that represent global action
    '''            
    def setGlobal(self, state):
        self.__global = state
        
    '''
        @brief return global state action
    '''            
    def getGlobal(self):
        return self.__global
        
    '''
        @brief append a state to the machine
        @param state the state object
    '''            
    def appendState(self, state):
        if state not in self.__states:
            self.__states.append(state)
            
    '''
        @brief extract state from yaml
        @param state_def yaml definition
        @param name state name
    '''
    def extractState(self, state_def, name):
    
        if name == "" :
            name = "global"
            comment = "Global action"
        else:
            comment = state_def.get('comment', '')
            assert comment != None, "state may have comment"
        
        hasenter = state_def.get('enter')
        assert hasenter != None, "state may have enter information"
        
        hasexit = state_def.get('exit')
        assert hasexit != None, "state may have exit info"
        
        
        state = State(name, comment, hasenter, hasexit)
        
        action_event = []
        action_state = []
        used_states = []
        
        actions = state_def.get('actions')
        assert actions != None, "state may have action list( also if empty) " 
        
        for action in actions :
            events = action.get('events')
            assert events != None, "action may have event list"
                        
            to = action.get('to', "")
            job = action.get('job', "")
            
            assert not (to == "" and job == ""), "an action may at least have an action or a target state"            
           
            eventnames = []
            for e in events :
                ename = e.get("name", None)
                assert ename, "event name should be set"
                eventnames.append(ename)
                self.appendEvent(ename, e.get("comment", ""))
                        
            state.appendAction(StateAction(eventnames, to, job))
                    
        if name == "global" :            
            self.setGlobal(state)
        else :            
            self.appendState(state)
        
        return used_states
        
    '''
        @brief build StateMachine from file
        @param file the file name
        @return the machine
    '''
    def fromFile(file):
        yaml_content = yaml.load(file, Loader=yaml.FullLoader)
        
        machine = yaml_content.get('machine')
        assert machine != None, "machine may have a name (field 'machine')"
        
        entry = yaml_content.get('entry')
        assert entry != None, "machine may have an entry state"
        
        machine = StateMachine(machine, entry)
        
        declared_states = []
        used_states = []
                
        global_action = yaml_content.get('global', None)
        if global_action :
            used_states += machine.extractState(global_action, "")
        
        states = yaml_content.get('states')
        
        assert states != None, "machine may have state list"
        
        for state_def in states :
            name = state_def.get('name')
            assert name != None, "state may have name"
            assert name not in declared_states, 'state cannot be declared twice %s'.arg(name)
            declared_states.append(name)
            used_states += machine.extractState(state_def, name)
        
        for used_state in used_states :
            assert used_state in declared_states, 'a transition uses a not declared state : '+used_state        
        
        return machine
    
    '''
        @brief json string for dictionary
        @param structure the arrray
        @param indent the indent character to use
    '''        
    def __dictToFile(structure, indent=""):
        output = "%s{\n"%indent
        for key,val in structure.items() :
            subindent = indent+StateMachine.INDENT_STRING
            output += "%s\"%s\": "%(subindent, key)
            subindent+=StateMachine.INDENT_STRING
            
            if isinstance(val, str):
                output += "\"%s\""%val
            elif isinstance(val, dict):
                output += "\n" + StateMachine.__dictToFile(val, subindent) 
            elif isinstance(val, list):
                output += "\n" + StateMachine.__arrayToFile(val, subindent) 
            output += ",\n"
        return output + "%s}"%indent
    
    '''
        @brief json string for array
        @param structure the arrray
        @param indent the indent character to use
    '''    
    def __arrayToFile(structure, indent=""):
        output = "%s[\n"%indent
        for val in structure :
            subindent = indent+StateMachine.INDENT_STRING
            if isinstance(val, dict):
                output += StateMachine.__dictToFile(val, subindent) 
            output += ",\n"
        return output + "%s]"%indent
        
    '''
        @brief build event yaml
        @param event the event to output
        @param already already sets event
    '''
    def __eventToFile(self, event, already, indent=""):
        output = {"name": event}
            
        if event not in already:
            output["comment"]=self.getEventComment(event)
            already.append(event)
        return output, already
        
    '''
        @brief build action yaml
        @param action the action to output
        @param already already sets event
    '''
    def __actionToFile(self, action, already, indent=""):
        events=[]
        for event in action.getEvents():
            e, already = self.__eventToFile(event, already)
            events.append(e)   
        output = {
            "job": action.getJob(),
            "to" : action.getState(),
            "events" : events }
        return output, already
        
    '''
        @brief build state yaml
    '''
    def __stateToFile(self, state, already=[]):
        actions = []
        for action in state.getActions():
            a, already = self.__actionToFile(action, already)
            actions.append(a)
        
        output = {
            "actions" : actions,
            "enter": state.getEnter(),
            "exit" :state.getExit() }
        return output, already
    
    '''
        @brief build machine yaml file
    '''
    def toFile(self) :
        st, already = self.__stateToFile(self.__global, [])
        
        output = { 
            "machine":self.__name, 
            "entry": self.__entry,
            "global" : st}
            
        states = []
        for state in self.__states:
            s = {
                "name": state.getName(),
                "comment": state.getComment() }
            st, already = self.__stateToFile(state, already)
            s.update(st)
            states.append(s)
        output["states"]=states
        
        return StateMachine.__dictToFile(output)
        
        
    '''
        @brief string represtation for statemachine
        @return the string
    '''  
    def __str__(self):
        output = "Statemachine(" + self.__name +", Entry: "+self.__entry+"): \n  - Events:\n"
        
        for event in self.__events : 
            output += "    - " +event + "\n"
            
        output += "  - States:\n"
        
        for state in self.__states : 
            output += "    - " +str(state) + "\n"
            
        return output
