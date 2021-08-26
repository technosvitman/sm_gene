
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
        @param parent the parent container
        @param machine the state machine
        @param without the event list to not display
    '''
    def __init__(self, parent, machine, without=[]) :
        if machine :
            events = machine.getEventNames()
            for e in without : 
                events.remove(e)
            wx.ComboBox.__init__(self, parent, choices=events)
        else :
            wx.ComboBox.__init__(self, parent)
        
        
        
