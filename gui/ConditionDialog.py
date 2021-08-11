
from . import *

import wx
import os
import sys
sys.path.append("..")
from machine import *
from .StateComboBox import StateComboBox

'''
  @brief condition dialog definition
'''
class ConditionDialog(wx.Dialog):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, title, machine, cond, alreadySets) :
        wx.Dialog.__init__(self, parent, title=title)
        
        self.__machine = machine
        self.__cond = cond
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = wx.StaticText(self, -1, "Event name:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__eventName = EventComboBox(self, machine, alreadySets)
        self.__eventName.SetValue(cond.getEvent())
            
        sizer.Add(self.__eventName, flag=wx.ALL | wx.EXPAND, border=5) 
        
        text = wx.StaticText(self, -1, "Event description :")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__desc = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__desc.SetValue(machine.getEventComment(cond.getEvent()))
        self.__eventName.Bind(wx.EVT_COMBOBOX, self.onEventChanged)
        
        sizer.Add(self.__desc, flag=wx.ALL | wx.EXPAND, border=5) 
        
        bsizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(bsizer)
        
        self.SetSizerAndFit(sizer)
        
        self.__eventName.SetFocus()
        
        
    def onEventChanged(self, event) :        
        self.__desc.SetValue(self.__machine.getEventComment(self.__eventName.GetValue()))
        
        
    def ShowModal(self) :
        old = str(self.__desc.GetValue())
        ret= super(ConditionDialog, self).ShowModal()
        if ret == wx.ID_OK:
            self.__cond = StateCondition(self.__eventName.GetValue())
            new = str(self.__desc.GetValue())
            if new != old :
                self.__machine.setEventComment(self.__cond.getEvent(), str(self.__desc.GetValue()))            
        return ret, self.__cond
        
