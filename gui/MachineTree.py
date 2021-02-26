
import wx


class MachineTree(wx.Panel):

    '''
        @brief initialize main control gui panel
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)        
        box = wx.StaticBox(self, wx.ID_ANY, "Machine explorer")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.__tree = wx.TreeCtrl(self)
        self.__tree.SetMinSize(wx.Size(100,400))
        bsizer.Add(self.__tree, flag=wx.ALL | wx.EXPAND)
        
        border = wx.BoxSizer()
        border.Add(bsizer, 1, flag=wx.ALL | wx.EXPAND)
        
        bsizer.SetSizeHints(box)
        bsizer.Fit(box)
        border.SetSizeHints(self)
        self.SetSizerAndFit(border)
        size = self.GetEffectiveMinSize()
        self.SetMinSize(size)
        self.Layout()

    '''
        @brief append state in tree
    '''
    def __appendState(self, parent, state, name):
        state_def = self.__tree.AppendItem(parent, name)
        self.__tree.SetItemHasChildren(state_def)
                    
        sub = self.__tree.AppendItem(state_def, "OnEnter : "+state.getEnter())
        
        sub = self.__tree.AppendItem(state_def, "OnExit : "+state.getExit())
        
        for action in state.getActions() :
            action_def = self.__tree.AppendItem(state_def, "Action")
            self.__tree.SetItemHasChildren(action_def)
            
            sub = self.__tree.AppendItem(action_def, "To : "+str(action.getState()))
            
            sub = self.__tree.AppendItem(action_def, "Job : "+str(action.getJob()))
            
            lenevents = len(action.getEvents())
            sub = self.__tree.AppendItem(action_def, "Events(%d)"%(lenevents))
            if lenevents :
                self.__tree.SetItemHasChildren(sub)
            
            for event in action.getEvents() :
                evt = self.__tree.AppendItem(sub, event["name"])
            self.__tree.Expand(action_def)
                
    '''
        @brief display machine
    '''
    def display(self, machine):
    
        self.__tree.DeleteAllItems()
    
        root = self.__tree.AddRoot("Machine : "+machine.getName())
        
        self.__appendState(root, machine.getGlobal(), "Global")
        
        for state in machine.getStates() :             
            self.__appendState(root, state, "State :" + state.getName())
                
        self.__tree.Expand(root)
    