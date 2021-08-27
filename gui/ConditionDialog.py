
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
        @param parent the parent container
        @param title the dialog title
        @param machine the state machine
        @param cond the condition to edit
        @param alreadySets the list of event already used
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
        
        text = wx.StaticText(self, -1, "Condition (optional) :")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND, border=5) 
        
        self.__conds = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__conds.SetValue(cond.getCond())
        
        sizer.Add(self.__conds, flag=wx.ALL | wx.EXPAND, border=5) 
        
        bsizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(bsizer)
        
        self.SetSizerAndFit(sizer)
        
        self.__eventName.SetFocus()
        
    
    '''
        @brief on event changed in list
        @param event the GUI event produced
    '''
    def onEventChanged(self, event) :        
        self.__desc.SetValue(self.__machine.getEventComment(self.__eventName.GetValue()))
        
    '''
        @see wx.Dialog
        @return super ShowModal return and condition
    '''
    def ShowModal(self) :
        old = str(self.__desc.GetValue())
        ret= super(ConditionDialog, self).ShowModal()
        if ret == wx.ID_OK:
            self.__cond = StateCondition(self.__eventName.GetValue(), \
                                        self.__conds.GetValue())
            new = str(self.__desc.GetValue())
            if self.__cond not in self.__machine.getEventNames():
                self.__machine.appendEvent(self.__cond.getEvent(), new)
            elif new != old :
                self.__machine.setEventComment(self.__cond.getEvent(), str(self.__desc.GetValue()))            
        return ret, self.__cond
        
