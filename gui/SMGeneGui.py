
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
        
        sizer = wx.GridBagSizer()
        
        self.__main = MainControl(self)
        self.__main.bindGenerate(self.generate)
        sizer.Add(self.__main, wx.GBPosition(0, 0), wx.GBSpan(), wx.ALL | wx.EXPAND)   
        
        self.__outputGraph = GraphView(self)
        sizer.Add(self.__outputGraph, wx.GBPosition(0, 1), wx.GBSpan(1, 2), wx.LEFT | wx.TOP | wx.EXPAND)  
        
        self.__tree = MachineTree(self)
        sizer.Add(self.__tree, wx.GBPosition(1, 0), wx.GBSpan(), wx.ALL | wx.EXPAND)
        
        self.SetSizer(sizer)
        
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
            machine = self.__gene.loadMachine(dlg.GetPath())
            self.__tree.display(machine)
        dlg.Destroy()
        
        
    '''
       @brief generate and display state machine
    '''
    def generate(self, event) :
        output = self.__main.getOutput()
        self.__gene.setOutput(output)
        template = self.__main.getTemplate()
        self.__gene.setTemplate(template)
        self.__gene.compute()
        self.__outputGraph.drawUml(self.__gene.getGraph())
