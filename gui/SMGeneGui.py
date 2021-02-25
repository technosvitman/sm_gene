
from . import *

import wx

'''
  @brief main gui frame definition
'''
class SMGeneGui(wx.Frame):
        
    '''
        @brief gui initialize
    '''
    def __init__(self, generator) :
        wx.Frame.__init__(self, parent=None, title='SMGene : state machine generator')
        self.__gene = generator
        self.__create_menu()
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        self.__main = MainControl(self)
        self.__main.bindGenerate(self.generate)
        hbox.Add(self.__main, wx.ID_ANY, flag=wx.LEFT | wx.TOP)
        
        self.__outputGraph = GraphView(self)
        hbox.Add(self.__outputGraph, wx.ID_ANY,flag=wx.LEFT | wx.TOP | wx.EXPAND)
        
        self.SetSizer(hbox)
        self.Layout()
        
    '''
        @brief create the menu bar
    '''
    def __create_menu(self):
        menu_bar = wx.MenuBar()
        
        file_menu = wx.Menu()
        
        open_file_item = file_menu.Append(
            wx.ID_ANY, 'Open...', 
            'Open statemachine yaml file'
        )
        menu_bar.Append(file_menu, '&File')
        
        self.Bind(
            event=wx.EVT_MENU, 
            handler=self.__on_open_file,
            source=open_file_item,
        )
        self.SetMenuBar(menu_bar)
        
    
    '''
       @brief on file selected
    '''
    def __on_open_file(self, event) :
        title = "Choose a file:"
        dlg = wx.FileDialog(self, title, wildcard="YAML File (*.yml) | *.yml",
                           style=wx.FD_OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.__gene.loadMachine(dlg.GetPath())
        dlg.Destroy()
        
        
    '''
       @brief generate and display state machine
    '''
    def generate(self, event) :
        output = self.__main.getOutput()
        print(output)
        self.__gene.setOutput(output)
        self.__gene.compute()
        self.__outputGraph.drawUml(self.__gene.getGraph())
