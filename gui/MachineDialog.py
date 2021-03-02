
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
    def __init__(self, parent, title, machine=None) :
        wx.Dialog.__init__(self, parent, title=title)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = wx.StaticText(self, -1, "Machine name:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND) 
        
        self.__mname = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        if machine :
            self.__mname.SetValue(machine.getName())
        else:
            self.__mname.SetValue('')
        
        sizer.Add(self.__mname, flag=wx.ALL | wx.EXPAND) 
        
        text = wx.StaticText(self, -1, "Machine description:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND) 
        
        self.__entry = StateComboBox(self, machine)
        if machine :
            self.__entry.SetValue(machine.getEntry())
        else:
            self.__entry.SetValue('')
            
        sizer.Add(self.__entry, flag=wx.ALL | wx.EXPAND) 
        
        self.SetSizer(sizer)
        
        
    def ShowModal(self) :
        super(MachineDialog, self).ShowModal()
        return str(self.__mname.GetValue()), self.__entry.GetValue()
        
