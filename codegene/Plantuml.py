
from .CodeGenerator import CodeGenerator
from plantweb.render import render as render_uml

class Plantuml(CodeGenerator):

    UML_FILE_EXT=".png"

    '''
        @brief get uml graph file
        @param basename
    '''
    def getUMLGraph(basename):
        return CodeGenerator.getBinaryFileName(basename+Plantuml.UML_FILE_EXT)
    
    '''
        @brief compute output state machine files from input machine
        @param basename the file basename
    '''
    def compute(self, basename):
        #build plantuml
        plantuml = "\n@startuml\n"
        
        name = self._machine.getName().upper()
        
        global_action = self._machine.getGlobal()
        if global_action : 
            plantuml += "\n[*] -> "+name+"\n"
            plantuml += "state "+name+"{\n"
            if global_action.hasEnter():
                plantuml += name+" : **global entry** : __global_on_enter()__\n"
                plantuml += name+" : > " + global_action.getEnter() + "\\n\n"
            if global_action.hasExit():
                plantuml += name+" : **global exit** : __global_on_exit()__\n"
                plantuml += name+" : > " + global_action.getExit() + "\\n\n"
            
            for action in global_action.getActions():
                if action.isOk():
                    conds = str(action.getConds()[0])
                    for cond in action.getConds()[1:] :
                        conds += " || "+str(cond)
                    job = action.getJob()
                    if job :
                        plantuml += name+" : **On** __" + conds
                        plantuml += "__ / //"+job+"//"
                        plantuml += "\n"
                    to = action.getState()
                    if to :
                        plantuml += name+" --> "+to+" : "+ conds +"\n"
                    plantuml += "\n"
            plantuml += "\n"
        
        
        plantuml += "\n[*] -> "+ self._machine.getEntry()+"\n"
        
        for state in self._machine.getStates() :
            plantuml += "\n"
            if state.getComment() != "" :
                plantuml += state.getName()+" : //"+state.getComment()+"//\\n\n"
            if state.hasEnter():
                plantuml += state.getName()+" : **Entry** / __"+state.getName()+"_on_enter()__\n"
                plantuml += state.getName()+" : > " + state.getEnter() + "\\n\n"
            if state.hasExit():
                plantuml += state.getName()+" : **Exit** / __"+state.getName()+"_on_exit()__\n"
                plantuml += state.getName()+" : > " + state.getExit() + "\\n\n"
                
            for action in state.getActions():
                if action.isOk():
                    conds = str(action.getConds()[0])
                    for cond in action.getConds()[1:] :
                        conds += " || "+ str(cond)
                    job = action.getJob()
                    if job :
                        plantuml += state.getName()+" : **On** __" + conds
                        plantuml += "__ / //"+job+"//"
                        plantuml += "\n"
                    to = action.getState()
                    if to :
                        plantuml += state.getName()+" --> "+to+" : "+ conds +"\n"
                    plantuml += "\n"
            plantuml += "\n"
        
        
        if global_action : 
            plantuml += "}\n"
        
        plantuml += "\n@enduml\n"
        
        output = CodeGenerator.getFile(basename+".plantuml")
        output.write(plantuml)
        output.close()
        
        #render uml
        uml = render_uml( plantuml, engine='plantuml', format='png', cacheopts={ 'use_cache': False} )
        
        output = CodeGenerator.getBinaryFile(basename+Plantuml.UML_FILE_EXT)
        
        for b in uml:
            if isinstance(b, bytes):
                output.write(b)
            elif isinstance(b, str):
                output.write(bytes(b, 'UTF8'))
        output.close()
        
    
        