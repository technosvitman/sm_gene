
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
class EventDialog(wx.Dialog):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, title, machine, event, alreadySets) :
        wx.Dialog.__init__(self, parent, title=title)
        
        self.__machine = machine
        self.__event = event
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        text = wx.StaticText(self, -1, "Event name:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__eventName = EventComboBox(self, machine, alreadySets)
        self.__eventName.SetValue(event)
            
        sizer.Add(self.__eventName, flag=wx.ALL | wx.EXPAND, border=5) 
        
        text = wx.StaticText(self, -1, "Description :")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__desc = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__desc.SetValue(machine.getEventComment(event))
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
        ret= super(EventDialog, self).ShowModal()
        if ret == wx.ID_OK:
            self.__event = self.__eventName.GetValue()
            new = str(self.__desc.GetValue())
            if new != old :
                self.__machine.setEventComment(self.__event, str(self.__desc.GetValue()))            
        return ret, self.__event
        
