
import wx


class MachineTree(wx.Panel):
    MACHINE=0
    GLOBAL=1
    STATE=2
    ACTION=3
    EVENT=4

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
        self.__tree.Bind(wx.EVT_TREE_ITEM_RIGHT_CLICK, self.__onRightClick)
        self.Layout()
        
        self.__machine = None

    '''
        @brief append state in tree
    '''
    def __appendState(self, parent, state, name, type_item):
        state_def = self.__tree.AppendItem(parent, name, 
                        data={type_item, state})
        self.__tree.SetItemHasChildren(state_def)
                    
        sub = self.__tree.AppendItem(state_def, "OnEnter : "+state.getEnter())
        
        sub = self.__tree.AppendItem(state_def, "OnExit : "+state.getExit())
        
        for action in state.getActions() :
            action_def = self.__tree.AppendItem(state_def, "Action", data={MachineTree.ACTION, action})
            self.__tree.SetItemHasChildren(action_def)
            
            sub = self.__tree.AppendItem(action_def, "To : "+str(action.getState()))
            
            sub = self.__tree.AppendItem(action_def, "Job : "+str(action.getJob()))
            
            lenevents = len(action.getEvents())
            sub = self.__tree.AppendItem(action_def, "Events(%d)"%(lenevents))
            if lenevents :
                self.__tree.SetItemHasChildren(sub)
            
            for event in action.getEvents() :
                evt = self.__tree.AppendItem(sub, event["name"], data={MachineTree.EVENT, event['name']})
            self.__tree.Expand(action_def)
        return state_def
    
    '''
       @brief on item right click
    '''
    def __onRightClick(self, event):
        # Get TreeItemData
        item = event.GetItem()
        itemData = self.__tree.GetItemData(item)
        if itemData == None :
            return
        typeitem, content = itemData
        # Create menu
        popupmenu = wx.Menu()
        menuItem = popupmenu.Append(-1, 'Edit')
        wrapper = lambda event: self.edit(event, item)
        self.Bind(wx.EVT_MENU, wrapper, menuItem)
        if typeitem == MachineTree.MACHINE :
            menuItem = popupmenu.Append(-1, 'Add state')  
            wrapper = lambda event: self.addState(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem)     
        elif typeitem == MachineTree.STATE or typeitem == MachineTree.GLOBAL : 
            menuItem = popupmenu.Append(-1, 'Add action')
            wrapper = lambda event: self.addAction(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem)
        elif typeitem == MachineTree.ACTION : 
            menuItem = popupmenu.Append(-1, 'Add event')
            wrapper = lambda event: self.addItem(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem) 
        
        if typeitem == MachineTree.STATE or typeitem == MachineTree.ACTION or typeitem == MachineTree.EVENT: 
            menuItem = popupmenu.Append(-1, 'Remove')
            wrapper = lambda event: self.remove(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem)
            

        # Show menu
        self.PopupMenu(popupmenu, event.GetPoint())
                
    '''
        @brief remove item
    '''
    def remove(self, event, item):
        itemData = self.__tree.GetItemData(item)
        typeitem, content = itemData
        
        if typeitem == MachineTree.STATE :
            c=item
            s = 0
            while c.IsOk() :
                c=self.__tree.GetPrevSibling(c)
                s+=1
            self.__machine.removeState(s-2)
        self.display(self.__machine)
        
        
    '''
        @brief edit item
    '''
    def edit(self, event, item):
        print(str(event))
        print(str(item))

                
    '''
        @brief add state to machine
    '''
    def addState(self, event, item):
        print(str(event))
        print(str(item))

                
    '''
        @brief add action to state
    '''
    def addAction(self, event, item):
        print(str(event))
        print(str(item))

                
    '''
        @brief add event to action
    '''
    def addEvent(self, event, item):
        print(str(event))
        print(str(item))

    '''
        @brief display machine
    '''
    def display(self, machine):
        self.__machine = machine
        self.__tree.DeleteAllItems()
    
        root = self.__tree.AddRoot("Machine : "+machine.getName(), 
                        data={MachineTree.MACHINE, machine.getName()})
        
        self.__appendState(root, machine.getGlobal(), "Global", MachineTree.GLOBAL)
        
        for state in machine.getStates() :             
            self.__appendState(root, state, "State :" + state.getName(), MachineTree.STATE)
                
        self.__tree.Expand(root)
    