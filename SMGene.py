
from machine import StateMachine
from codegene import *
from gui import *

import argparse
import os
import wx

'''
  @brief main generator class
''' 
class SMGene():
    DEFAULT_INPUT = os.path.dirname(os.path.realpath(__file__))+"/machine_example.yml"
    DEFAULT_TEMPLATE = os.path.dirname(os.path.realpath(__file__))+"/templates"

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
        build input machine from file
    '''
    def loadMachine(self, input_file):                
        if input_file == None:
            input_file = SMGene.DEFAULT_INPUT
        self.__input = input_file
        yaml_file = open(self.__input, 'r')
        self.__machine = StateMachine.fromFile(yaml_file)    
        assert len(self.__machine.getEvents()) != 0, 'Event list cannot be empty'
        print( self.__machine )
    
    '''
        @brief get graph path
    '''
    def getGraph(self):
        return Plantuml.getUMLGraph(self.__output)
    
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
        @brief compute output state machine files from input machine
    '''
    def compute(self):
    
        assert self.__input != None, "call loadMachine before"
                
        if self.__template == None or self.__template == "":
            self.__template = SMGene.DEFAULT_TEMPLATE
        
        if self.__output == None or self.__output == "":
            head, tail = os.path.split(self.__input)
            self.__output = os.path.splitext(tail)[0]
        
        gene = Source(self.__machine, self.__template)
        gene.compute(self.__output)
        gene = Header(self.__machine, self.__template)
        gene.compute(self.__output)
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
    parser.add_argument("-t", type=str, default=None)
    
    args = parser.parse_args()
    gene = SMGene()
    if args.i==None :
        gene.gui()
    else:        
        gene.loadMachine(args.i)
        gene.setOutput(args.o)
        gene.setTemplate(args.o)
        gene.compute()
