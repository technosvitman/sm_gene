
from machine import *
from codegene import *
from gui import *

import argparse
import os
import wx
import yaml

'''
  @brief main generator class
''' 
class SMGene():
    DEFAULT_INPUT = os.path.dirname(os.path.realpath(__file__))+"/machine_example.yml"
    DEFAULT_TEMPLATE = os.path.dirname(os.path.realpath(__file__))+"/templates"
    DEFAULT_OUTPUT="machine"

    '''
        @brief initialize generator
    '''
    def __init__(self):
        self.__machine = None
        self.__indentChar = "    "
        self.__input = None
        self.__output = None
        self.__template = None
    
    '''
        build empty machine
    '''
    def createMachine(self):   
        self.__machine = StateMachine()
        return self.__machine
    
    '''
        build input machine from file
    '''
    def loadMachine(self, input_file):                
        if input_file == None:
            input_file = SMGene.DEFAULT_INPUT
        self.__input = input_file
        yaml_file = open(self.__input, 'r')
        self.__machine = StateMachine.fromFile(yaml_file)  
        yaml_file.close()        
        return self.__machine
    
    '''
        save input machine file
    '''
    def saveMachine(self, input_file):                
        assert input_file != ""
        self.__input = input_file
        yaml_file = open(self.__input, 'w+')
        yaml_file.write(self.__machine.toFile())
        yaml_file.close()
    
    '''
        @brief get graph path
    '''
    def getGraph(self):
        return Plantuml.getUMLGraph(self.__output)
    
    '''
        @brief check machine
    '''
    def check(self):
        return self.__machine.check()
    
    '''
        @brief set output basename
    '''
    def setOutput(self, output):
        self.__output = output
    
    '''
        @brief set template path
    '''
    def setTemplate(self, template):
        self.__template = template
    
    '''
        @brief compute test unit for loaded state machine
    '''
    def unittest(self, verbose):    
        assert self.__machine != None, "call loadMachine before"
        
        testcases = self.__machine.unittest()
        
        if verbose:
            print(testcases)
        
        tester = Unittest()
        
        config = UnittestCfg(\
                "output/machine_example.c",\
                "output/machine_example.h",\
                "example_machine",\
                "example_machine_Init",\
                "example_machine_Compute")
                
        config.appendCond("Condition example", "Condition example")
        config.appendCond("Another condition", "Another condition")
        
        config.appendState("State1", "example_machine_state_eSTATE1")
        config.appendState("State2", "example_machine_state_eSTATE2")
        config.appendState("State3", "example_machine_state_eSTATE3")
        config.appendState("State4", "example_machine_state_eSTATE4")
                
        config.appendEvent("Event1", "example_machine_event_eEVENT1")
        config.appendEvent("Event2", "example_machine_event_eEVENT2")
        config.appendEvent("Event3", "example_machine_event_eEVENT3")
        config.appendEvent("Event4", "example_machine_event_eEVENT4")
        config.appendEvent("Event5", "example_machine_event_eEVENT5")
        config.appendEvent("Event6", "example_machine_event_eEVENT6")
        config.appendEvent("Event7", "example_machine_event_eEVENT7")
        
        tester.build(config)
        tester.unitest(testcases, config)
        
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self, withuml=True):
    
        assert self.__machine != None, "call loadMachine before"
                
        if self.__template == None or self.__template == "":
            self.__template = SMGene.DEFAULT_TEMPLATE
        
        if self.__output == None or self.__output == "":
            if self.__input :
                head, tail = os.path.split(self.__input)
                self.__output = os.path.splitext(tail)[0]
            else :
                self.__output = SMGene.DEFAULT_OUTPUT
        
        gene = Source(self.__machine, self.__template)
        gene.compute(self.__output)
        gene = Header(self.__machine, self.__template)
        gene.compute(self.__output)
        if withuml:
            gene = Plantuml(self.__machine, self.__template)
            gene.compute(self.__output)
    
    '''
        @brief start and run gui
    '''        
    def gui(self):
        app = wx.App()
        frame = SMGeneGui(self)
        app.SetTopWindow(frame)
        frame.Show()
        frame.Maximize(True)
        app.MainLoop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SMGene : statemachine generator')
    parser.add_argument("-i", type=str, default=None)
    parser.add_argument("-o", type=str, default=None)
    parser.add_argument("-u", default=False, action="store_true")
    parser.add_argument("-v", default=False, action="store_true")
    parser.add_argument("-t", type=str, default=None)
    
    args = parser.parse_args()
    gene = SMGene()
    if args.i==None and not args.u and not args.v:
        gene.gui()
    else:        
        if args.i==None:
            args.i = "machine_example.yml"
        machine = gene.loadMachine(args.i)
        if args.v:
            print(machine)
        gene.setOutput(args.o)
        gene.setTemplate(args.o)
        gene.compute(not args.u)
        if args.u:
            gene.unittest(args.v)
