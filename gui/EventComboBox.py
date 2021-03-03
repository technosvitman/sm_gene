
from . import *

import wx
import os
import sys
sys.path.append("..")
from machine import *

'''
  @brief machine dialog definition
'''
class EventComboBox(wx.ComboBox):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, machine, without=[]) :
        if machine :
            events = machine.getEventNames()
            for e in without : 
                events.remove(e)
            wx.ComboBox.__init__(self, parent, choices=events)
        else :
            wx.ComboBox.__init__(self, parent)
        
        
        
