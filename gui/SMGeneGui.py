
from . import *

import wx
import os

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
        
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        toolbar = self.CreateToolBar()
        
        toolbar.AddSeparator()        
        
        text = wx.StaticText(toolbar, -1, "Output name:")
        toolbar.AddControl(text)
        
        self.__output = wx.TextCtrl(toolbar, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__output.SetValue('')
        toolbar.AddControl(self.__output)
        
        toolbar.AddSeparator()        
        
        text = wx.StaticText(toolbar, -1, "Template file:")
        toolbar.AddControl(text)
        
        self.__template = wx.DirPickerCtrl(toolbar, -1, size=(220,-1))
        toolbar.AddControl(self.__template)
        
        generate = toolbar.AddTool(wx.ID_ANY, "Generate",
                    wx.Bitmap(os.path.dirname(os.path.realpath(__file__))+"/icon/iconfinder-hammer-builder-build-labor-4622503_122420.png"))
        toolbar.AddSeparator()        
        toolbar.Bind(wx.EVT_TOOL, self.generate, generate)
        toolbar.Realize() 
        
        self.__tree = MachineTree(self)
        sizer.Add(self.__tree, flag=wx.ALL | wx.EXPAND)
        
        self.__outputGraph = GraphView(self)
        sizer.Add(self.__outputGraph, flag=wx.ALL | wx.EXPAND) 
        
        self.SetSizer(sizer)
        
        self.SetSize((350, 250))
        
        self.Centre()
        
        nit_id = wx.NewId()
        oit_id = wx.NewId()
        sit_id = wx.NewId()
        f5_id = wx.NewId()
        self.Bind(wx.EVT_MENU, self.__on_new_file, id=nit_id)
        self.Bind(wx.EVT_MENU, self.__on_open_file, id=oit_id)
        self.Bind(wx.EVT_MENU, self.__on_save_file, id=sit_id)
        self.Bind(wx.EVT_MENU, self.generate, id=f5_id)
        
        accel_tbl = wx.AcceleratorTable([
                                        (wx.ACCEL_CTRL, ord('N'), nit_id),
                                        (wx.ACCEL_CTRL, ord('O'), oit_id),
                                        (wx.ACCEL_CTRL, ord('S'), sit_id),
                                        (wx.WXK_NONE, wx.WXK_F5, f5_id)
                                        ])
        self.SetAcceleratorTable(accel_tbl)
        
    '''
        @brief create the menu bar
    '''
    def __create_menu(self):
        menu_bar = wx.MenuBar()
        
        file_menu = wx.Menu()
        menu_bar.Append(file_menu, '&File')
        
        new_file_item = file_menu.Append(
            wx.ID_ANY, 'New...', 
            'New statemachine'
        )
        
        self.Bind(
            event=wx.EVT_MENU, 
            handler=self.__on_new_file,
            source=new_file_item,
        )
        
        open_file_item = file_menu.Append(
            wx.ID_ANY, 'Open...', 
            'Open statemachine yaml file'
        )
        
        self.Bind(
            event=wx.EVT_MENU, 
            handler=self.__on_open_file,
            source=open_file_item,
        )
        
        save_file_item = file_menu.Append(
            wx.ID_ANY, 'Save...', 
            'Save statemachine yaml file'
        )
        
        self.Bind(
            event=wx.EVT_MENU, 
            handler=self.__on_save_file,
            source=save_file_item,
        )
        self.SetMenuBar(menu_bar)
        
    
    '''
       @brief on open file selected
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
       @brief on save file selected
       @todo add file selection
    '''
    def __on_save_file(self, event) :
        self.__on_save_as_file(event)
    
    '''
       @brief on save file selected
       @todo add file selection
    '''
    def __on_save_as_file(self, event) :
        title = "Save as:"
        dlg = wx.FileDialog(self, title, wildcard="YAML File (*.yml) | *.yml",
                           style=wx.FD_SAVE)
        if dlg.ShowModal() == wx.ID_OK:
            self.__gene.saveMachine(dlg.GetPath())
        dlg.Destroy()
        
    
    '''
       @brief on new selected
    '''
    def __on_new_file(self, event) :
        machine = self.__gene.createMachine()
        popup = MachineDialog(self, "New machine", machine)
        if popup.ShowModal() == wx.ID_OK:
            self.__tree.display(machine)
        
        
    '''
       @brief generate and display state machine
    '''
    def generate(self, event) :
        check = self.__gene.check()
        if check == {} :
            output = str(self.__output.GetValue())
            self.__gene.setOutput(output)
            template = self.__template.GetPath()
            self.__gene.setTemplate(template)
            self.__gene.compute()
            self.__outputGraph.drawUml(self.__gene.getGraph())
        else:
            content = "Too much proximity in transitions : \n\n"
            for key,val in check.items() :
                content += "- In state %s\n"%key
                for entry in val:
                    to1, to2, conds = entry
                    content += "  - between transition to %s and %s\n"%(to1, to2)
                    for c in conds :
                        content += "    - %s with %s\n"%(c)

            dlg = wx.MessageDialog(self,
                    content,
                    caption="Please check your Machine",
                    style=wx.OK)
            dlg.ShowModal()
