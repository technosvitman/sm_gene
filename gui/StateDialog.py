
from . import *

import wx
import os
import sys
sys.path.append("..")
from machine import *

'''
  @brief state dialog definition
'''
class StateDialog(wx.Dialog):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, parent, title, state) :
        wx.Dialog.__init__(self, parent, title=title)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        self.__state = state
        
        if state.getName() == "global" :
            self.__sname = None
        else:
            print("pouet")
            text = wx.StaticText(self, -1, "State name:")
        
            sizer.Add(text, flag=wx.ALL | wx.EXPAND) 
        
            self.__sname = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
            self.__sname.SetValue(state.getName())
        
            sizer.Add(self.__sname, flag=wx.ALL | wx.EXPAND) 
        
        text = wx.StaticText(self, -1, "State description:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND) 
        
        self.__desc = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__desc.SetValue(state.getComment())
        
        sizer.Add(self.__desc, flag=wx.ALL | wx.EXPAND) 
        
        text = wx.StaticText(self, -1, "On enter:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND) 
        
        self.__enter = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__enter.SetValue(state.getEnter())
        
        sizer.Add(self.__enter, flag=wx.ALL | wx.EXPAND) 
        
        text = wx.StaticText(self, -1, "On exit:")
        
        sizer.Add(text, flag=wx.ALL | wx.EXPAND) 
        
        self.__exit = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__exit.SetValue(state.getExit())
        
        sizer.Add(self.__exit, flag=wx.ALL | wx.EXPAND) 
        
        bsizer = self.CreateButtonSizer(wx.OK|wx.CANCEL)
        sizer.Add(bsizer)
        
        self.SetSizerAndFit(sizer)
        
        
    def ShowModal(self) :
        ret= super(StateDialog, self).ShowModal()
        if ret == wx.ID_OK:
            if self.__sname :
                self.__state.setName(str(self.__sname.GetValue()))
            self.__state.setComment(str(self.__desc.GetValue()))
            self.__state.setEnter(str(self.__enter.GetValue()))
            self.__state.setExit(str(self.__exit.GetValue()))
        return ret   
