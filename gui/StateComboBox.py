
from . import *

import wx
import os
import sys
sys.path.append("..")
from machine import *

'''
  @brief machine dialog definition
'''
class StateComboBox(wx.ComboBox):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, machine) :
        if machine :
            wx.ComboBox.__init__(self, parent, choices=machine.getStateNames())
        else :
            wx.ComboBox.__init__(self, parent)
        
        
        
