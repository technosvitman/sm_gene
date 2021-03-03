
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
class ActionDialog(wx.Dialog):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, title, machine, action) :
        wx.Dialog.__init__(self, parent, title=title)
        
        self.__machine = machine
        self.__action = action
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = wx.StaticText(self, -1, "Job:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__job = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__job.SetValue(action.getJob())
        
        sizer.Add(self.__job, flag=wx.ALL | wx.EXPAND, border=5) 
        
        text = wx.StaticText(self, -1, "Destination state:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__to = StateComboBox(self, machine)
        self.__to.SetValue(action.getState())
            
        sizer.Add(self.__to, flag=wx.ALL | wx.EXPAND, border=5) 
        
        bsizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(bsizer)
        
        self.SetSizerAndFit(sizer)
        
        
    def ShowModal(self) :
        ret= super(ActionDialog, self).ShowModal()
        newstate=False
        if ret == wx.ID_OK:
            to = self.__to.GetValue()
            self.__action.setJob(str(self.__job.GetValue()))
            if to!="":
                if to not in self.__machine.getStateNames() :
                    self.__machine.appendState(State(to))
                    newstate=True
            self.__action.setState(to)
        return ret, newstate
        
