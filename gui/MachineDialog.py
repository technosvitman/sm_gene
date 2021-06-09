
from . import *

import wx
import os
import sys
sys.path.append("..")
from machine import *
from .StateComboBox import StateComboBox

'''
  @brief machine dialog definition
'''
class MachineDialog(wx.Dialog):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, title, machine) :
        wx.Dialog.__init__(self, parent, title=title)
        
        self.__machine = machine
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = wx.StaticText(self, -1, "Machine name:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__mname = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__mname.SetValue(machine.getName())
        
        sizer.Add(self.__mname, flag=wx.ALL | wx.EXPAND, border=5) 
        
        text = wx.StaticText(self, -1, "Entry state:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__entry = StateComboBox(self, machine)
        self.__entry.SetValue(machine.getEntry())
            
        sizer.Add(self.__entry, flag=wx.ALL | wx.EXPAND, border=5) 
        
        bsizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(bsizer)
        
        self.SetSizerAndFit(sizer)
        
        self.__mname.SetFocus()       
    
    '''
        @see wx.Dialog
    '''    
    def ShowModal(self) :
        ret= super(MachineDialog, self).ShowModal()
        if ret == wx.ID_OK:
            entry = self.__entry.GetValue()
            self.__machine.setName(str(self.__mname.GetValue()))
            if entry not in self.__machine.getStateNames() :
                self.__machine.appendState(State(entry))
            self.__machine.setEntry(entry)
        return ret
        
