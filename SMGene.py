
from machine import StateMachine
from codegene import *

import argparse
import os
import wx

'''
  @brief main gui frame definition
'''
class SMGeneGui(wx.Frame):
        
    '''
        @brief gui initialize
    '''
    def __init__(self) :
        wx.Frame.__init__(self, parent=None, title='SMGene : state machine generator')

'''
  @brief main generator class
''' 
class SMGene():
    DEFAULT_INPUT = os.path.dirname(os.path.realpath(__file__))+"/machine_example.yml"
    DEFAULT_TEMPLATE = os.path.dirname(os.path.realpath(__file__))+"/templates"

    '''
        @brief initialize generator
    '''
    def __init__(self, input_file, output, template):
        self.__machine = None
        self.__indentChar = "    "
        self.__input = input_file
        self.__output = output
        self.__template = template
    
    '''
        build input machine from file
    '''
    def __loadMachine(self):
        yaml_file = open(self.__input, 'r')
        self.__machine = StateMachine.fromFile(yaml_file)
    
    '''
        @brief compute output state machine files from input machine
    '''
    def compute(self):
                
        if self.__input == None:
            self.__input = SMGene.DEFAULT_INPUT
            
        self.__loadMachine()
    
        assert len(self.__machine.getEvents()) != 0, 'Event list cannot be empty'
        print( self.__machine )
                
        if self.__template == None:
            self.__template = SMGene.DEFAULT_TEMPLATE
        
        if self.__output == None:
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
        frame = SMGeneGui()
        frame.Show()
        app.MainLoop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SMGene : statemachine generator')
    parser.add_argument("-i", type=str, default=None)
    parser.add_argument("-o", type=str, default=None)
    parser.add_argument("-t", type=str, default=None)
    
    args = parser.parse_args()
    gene = SMGene(args.i, args.o, args.t)
    if args.i==None :
        gene.gui()
    else:        
        gene.compute()
