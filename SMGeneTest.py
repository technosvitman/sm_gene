
from machine import *

import argparse
import os
import yaml

'''
  @brief tester for generator class
''' 
class SMGeneTest():
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
    
    '''
        @brief build empty machine
    '''
    def createMachine(self):   
        self.__machine = StateMachine()
        return self.__machine
    
    '''
        @brief build input machine from file
        @param input_file the machine file
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
        @brief compute test unit for loaded state machine
        @param config the configuration filename
    '''
    def unittest(self, config):    
        assert self.__machine != None, "call loadMachine before"
        
        testcases = self.__machine.unittest()
        
        tester = Unittest()
        
        config = UnittestCfg.fromFile(open(config, 'r'))
        
        tester.build(config)
        tester.unitest(config, testcases, self.__machine)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='SMGeneTest : statemachine tester')
    parser.add_argument("-i", type=str, default=None)
    parser.add_argument("-u", type=str, default=None)
    parser.add_argument("-v", default=False, action="store_true")
    
    args = parser.parse_args()
    gene = SMGeneTest()
    if args.i==None:
        args.i = "machine_example.yml"
    machine = gene.loadMachine(args.i)
    if args.v:
        print(machine)
    if args.u:
        gene.unittest(args.u)
