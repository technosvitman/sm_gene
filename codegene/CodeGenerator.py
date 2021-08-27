
from machine import StateMachine
import os
from string import Template

'''
    @brief generic code generator from machine
'''
class CodeGenerator():

    INDENT_CHAR = "    " 

    '''
        @brief initialize generator
        @param machine the state machine to compute
        @param template the template directory
    '''
    def __init__(self, machine, template):
        self._machine = machine   
        self.__template = template
        self._prefix = self._machine.getName() + "_machine"
    
    '''
        @brief compute output state machine files from input machine
        @param basename the file basename
    '''
    def compute(self, basename):
        pass    
        
    '''
        @biref get template content
        @param filename the template filename
    '''
    def getTemplate(self, filename):
        template=open(self.__template+"/"+filename, 'r')
        return Template(template.read())
        
    '''
        @biref get write access to output file
        @param filename the the filname
    '''
    def getFile(filename):
        return open(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output/"+filename, 'w+')
        
    '''
        @biref get write access to output file
        @param filename the the filname
    '''
    def getBinaryFileName(filename):
        return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))+"/output/"+filename
        
    '''
        @biref get write access to output file
        @param filename the the filname
    '''
    def getBinaryFile(filename):
        return open(CodeGenerator.getBinaryFileName(filename), 'wb+')