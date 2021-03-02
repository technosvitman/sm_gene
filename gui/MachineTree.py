
import wx
import sys
sys.path.append("..")
from machine import *
from .StateDialog import StateDialog


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
        self.__tree.SetMinSize(wx.Size(200,450))
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
        @brief append event in tree
    '''
    def __appendEvent(self, parent, event):
        self.__tree.AppendItem(parent, event, data={"type":MachineTree.EVENT, "content":event})

    '''
        @brief append event in tree
    '''
    def __setEvents(self, events, action):
        self.__tree.SetItemText(events, "Events(%d)"%(len(action.getEvents())))

    '''
        @brief append state in tree
    '''
    def __appendAction(self, parent, action):
        action_def = self.__tree.AppendItem(parent, "Action", data={"type":MachineTree.ACTION, "content":action})
        self.__tree.SetItemHasChildren(action_def)
        
        sub = self.__tree.AppendItem(action_def, "To : "+str(action.getState()))
        
        sub = self.__tree.AppendItem(action_def, "Job : "+str(action.getJob()))
        
        lenevents = len(action.getEvents())
        sub = self.__tree.AppendItem(action_def, "")
        self.__setEvents(sub, action)
        if lenevents :
            self.__tree.SetItemHasChildren(sub)
        
        for event in action.getEvents() :
            self.__appendEvent(sub, event['name'])          
        self.__tree.Expand(sub)
        self.__tree.Expand(action_def)
        
    '''
        @brief append state in tree
    '''
    def __updateState(self, state_def, state):
        self.__tree.DeleteChildren(state_def)
        self.__tree.SetItemHasChildren(state_def)
                    
        self.__tree.AppendItem(state_def, "OnEnter : "+state.getEnter())
        
        self.__tree.AppendItem(state_def, "OnExit : "+state.getExit())
        
        for action in state.getActions() :
            self.__appendAction(state_def, action)            
        
        self.__tree.Expand(state_def)
        return state_def
        
    '''
        @brief append state in tree
    '''
    def __appendState(self, parent, state, name, type_item):
        state_def = self.__tree.AppendItem(parent, name, 
                        data={"type":type_item, "content":state})
        return self.__updateState(state_def, state)

    '''
        @brief display machine
    '''
    def display(self, machine):
        self.__machine = machine
        self.__tree.DeleteAllItems()
    
        root = self.__tree.AddRoot("Machine : "+machine.getName(), 
                        data={"type":MachineTree.MACHINE, "content":machine.getName()})
        
        self.__appendState(root, machine.getGlobal(), "Global", MachineTree.GLOBAL)
        
        for state in machine.getStates() :             
            self.__appendState(root, state, "State :" + state.getName(), MachineTree.STATE)
                
        self.__tree.Expand(root)
    
    '''
       @brief on item right click
    '''
    def __onRightClick(self, event):
        # Get TreeItemData
        item = event.GetItem()
        itemData = self.__tree.GetItemData(item)
        if itemData == None :
            return
        typeitem = itemData['type']
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
            wrapper = lambda event: self.addEvent(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem) 
        
        if typeitem == MachineTree.STATE or typeitem == MachineTree.ACTION or typeitem == MachineTree.EVENT: 
            menuItem = popupmenu.Append(-1, 'Remove')
            wrapper = lambda event: self.remove(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem)
            

        # Show menu
        self.PopupMenu(popupmenu, event.GetPoint())
        
    '''
        @brief find state index from item
        @param item
    '''        
    def __findStateIndex(self, item):
        index = -2
        while item.IsOk() :
            item=self.__tree.GetPrevSibling(item)
            index+=1
        return index
        
    '''
        @brief find action index from item
        @param item
    '''        
    def __findActionIndex(self, item):
        index = -3
        while item.IsOk() :
            item=self.__tree.GetPrevSibling(item)
            index+=1
        return index
        
    '''
        @brief find event index from item
        @param item
    '''        
    def __findEventIndex(self, item):
        index = -1
        while item.IsOk() :
            item=self.__tree.GetPrevSibling(item)
            index+=1
        return index
        
                
    '''
        @brief remove item
    '''
    def remove(self, event, item):
        typeitem = self.__tree.GetItemData(item)['type']
        
        if typeitem == MachineTree.STATE :
            self.__machine.removeState(self.__findStateIndex(item))
            self.__tree.Delete(item)
            
        elif typeitem == MachineTree.ACTION :
            index = self.__findActionIndex(item)
            p=self.__tree.GetItemParent(item)
            self.__tree.Delete(item)
            state = self.__tree.GetItemData(p)["content"]
            state.removeAction(index)
            
        elif typeitem == MachineTree.EVENT :
            event = self.__findEventIndex(item)
            p=self.__tree.GetItemParent(item)
            self.__tree.Delete(item)
            item=self.__tree.GetItemParent(p)
            action = self.__findActionIndex(item)
            item=self.__tree.GetItemParent(item)
            state = self.__tree.GetItemData(item)["content"]
            action = state.getActions()[action]
            action.removeEvent(event)
            self.__setEvents(p, action)
        self.__machine.cleanUp()
        
    '''
        @brief edit item
    '''
    def edit(self, event, item):
        typeitem = self.__tree.GetItemData(item)['type']
        
        if typeitem == MachineTree.MACHINE :
            popup = MachineDialog(self, "Edit machine", self.__machine)
            if popup.ShowModal() == wx.ID_OK:
                self.display(self.__machine)
        
        elif typeitem == MachineTree.STATE or typeitem == MachineTree.GLOBAL :
            state = self.__tree.GetItemData(item)['content']
            old = state.getName()
            popup = StateDialog(self, "Edit", state)
            
            if popup.ShowModal() == wx.ID_OK:
                if typeitem == MachineTree.STATE :
                    self.__tree.SetItemText(item, "State :" + state.getName())
                if self.__machine.getEntry() == old:
                    self.__machine.setEntry(state.getName())
                self.__updateState(item, state)

                
    '''
        @brief add state to machine
    '''
    def addState(self, event, item):
        #todo popup state
        state = State("")
        popup = StateDialog(self, "New state", state)
        if popup.ShowModal() == wx.ID_OK:
            self.__machine.appendState(state)
            self.__appendState(item, state, "State :" + state.getName(), MachineTree.STATE)
            

                
    '''
        @brief add action to state
    '''
    def addAction(self, event, item):
        #todo popup action
        action = StateAction()
        state = self.__tree.GetItemData(item)['content']
            
        state.appendAction(action)
        self.__appendAction(item, action)

                
    '''
        @brief add event to action
    '''
    def addEvent(self, event, item):
        #todo popup event
        action = self.__tree.GetItemData(item)['content']
        action.addEvent({"name":"test"})
        item = self.__tree.GetLastChild(item)
        self.__setEvents(item, action)
        self.__appendEvent(item, "test")
    