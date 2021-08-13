
import wx
import sys
sys.path.append("..")
from machine import *
from . import *


class MachineTree(wx.Panel):
    MACHINE=0
    GLOBAL=1
    STATE=2
    ACTION=3
    COND=4
    SUB=0xFF

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
        self.__tree.Bind(wx.EVT_KEY_DOWN, self.__onKey)
        self.__tree.Bind(wx.EVT_LEFT_DCLICK, self.__onDblClick)
        self.Layout()
        
        self.__machine = None

    '''
        @brief append condition in tree
    '''
    def __appendCond(self, parent, cond):
        return self.__tree.AppendItem(parent, str(cond), data={"type":MachineTree.COND, "content":cond})

    '''
        @brief append cond in tree
    '''
    def __setConds(self, conds, action):
        self.__tree.SetItemText(conds, "Conds(%d)"%(len(action.getConds())))

    '''
        @brief update action in tree
    '''
    def __updateAction(self, action_def, action):        
        self.__tree.DeleteChildren(action_def)
        self.__tree.SetItemHasChildren(action_def)
        
        sub = self.__tree.AppendItem(action_def, "To : "+str(action.getState()), data={"type":MachineTree.SUB})
        
        sub = self.__tree.AppendItem(action_def, "Job : "+str(action.getJob()), data={"type":MachineTree.SUB})
        
        lenconds = len(action.getConds())
        sub = self.__tree.AppendItem(action_def, "", data={"type":MachineTree.SUB})
        self.__setConds(sub, action)
        if lenconds :
            self.__tree.SetItemHasChildren(sub)
        
        for cond in action.getConds() :
            self.__appendCond(sub, cond)          
        self.__tree.Expand(sub)
        self.__tree.Expand(action_def)

    '''
        @brief append action in tree
    '''
    def __appendAction(self, parent, action):
        action_def = self.__tree.AppendItem(parent, "Action", data={"type":MachineTree.ACTION, "content":action})
        self.__updateAction(action_def, action)
        return action_def
        
    '''
        @brief update state in tree
    '''
    def __updateState(self, state_def, state):
        self.__tree.DeleteChildren(state_def)
        self.__tree.SetItemHasChildren(state_def)
                    
        self.__tree.AppendItem(state_def, "OnEnter : "+state.getEnter(), data={"type":MachineTree.SUB})
        
        self.__tree.AppendItem(state_def, "OnExit : "+state.getExit(), data={"type":MachineTree.SUB})
        
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
       @brief on item key pressed
    '''
    def __onKey(self, event):
        # Get TreeItemData
        item = self.__tree.GetFocusedItem()
        if item == None or not item.IsOk():
            event.Skip()
        itemData = self.__tree.GetItemData(item)
        if itemData == None :
            event.Skip()
        typeitem = itemData['type']
        if typeitem == MachineTree.SUB :
            item = self.__tree.GetItemParent(item)
            itemData = self.__tree.GetItemData(item)  
            if itemData == None :
                event.Skip()
            typeitem = itemData['type']
            
        key = event.GetKeyCode() 
        if key == wx.WXK_DELETE:
            if typeitem == MachineTree.STATE or typeitem == MachineTree.ACTION or typeitem == MachineTree.COND: 
                self.remove(event, item)
        elif key == 13:
            self.edit(event, item)
        elif key == wx.WXK_SPACE:            
            if typeitem == MachineTree.MACHINE :
                self.addState(event, item)                
            elif typeitem == MachineTree.STATE or typeitem == MachineTree.GLOBAL : 
                self.addAction(event, item)                
            elif typeitem == MachineTree.ACTION :
                self.addCond(event, item)
        else:            
            event.Skip()
    
    '''
       @brief on item right click
    '''
    def __onRightClick(self, event):
        # Get TreeItemData
        item = event.GetItem()        
        if not item.IsOk():
            return
        itemData = self.__tree.GetItemData(item)
        if itemData == None :
            return
        typeitem = itemData['type']
        if typeitem == MachineTree.SUB :
            item = self.__tree.GetItemParent(item)
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
            menuItem = popupmenu.Append(-1, 'Add condition')
            wrapper = lambda event: self.addCond(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem) 
        
        if typeitem == MachineTree.STATE or typeitem == MachineTree.ACTION or typeitem == MachineTree.COND: 
            menuItem = popupmenu.Append(-1, 'Remove')
            wrapper = lambda event: self.remove(event, item)
            self.Bind(wx.EVT_MENU, wrapper, menuItem)
            

        # Show menu
        self.PopupMenu(popupmenu, event.GetPoint())
        
        
    
    '''
       @brief on item left double click
    '''
    def __onDblClick(self, event):
        # Get TreeItemData
        item = self.__tree.GetFocusedItem()        
        if not item.IsOk():
            return
        itemData = self.__tree.GetItemData(item)
        if itemData == None :
            return
        typeitem = itemData['type']
        if typeitem == MachineTree.SUB :
            item = self.__tree.GetItemParent(item)
            itemData = self.__tree.GetItemData(item)  
            if itemData == None :
                return      
            typeitem = itemData['type']    
        self.edit(event, item)        
        
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
    def __findCondIndex(self, item):
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
            
        elif typeitem == MachineTree.COND :
            cond = self.__findCondIndex(item)
            p=self.__tree.GetItemParent(item)
            self.__tree.Delete(item)
            item=self.__tree.GetItemParent(p)
            action = self.__findActionIndex(item)
            item=self.__tree.GetItemParent(item)
            state = self.__tree.GetItemData(item)["content"]
            action = state.getActions()[action]
            action.removeCond(cond)
            self.__setConds(p, action)
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
                
        elif typeitem == MachineTree.ACTION :         
            action = self.__tree.GetItemData(item)['content']
            popup = ActionDialog(self, "Edit action", self.__machine, action)
            ret, hasnew = popup.ShowModal()
            if ret == wx.ID_OK:
                if hasnew:
                    self.display(self.__machine)
                else:
                    self.__updateAction(item, action)
                
        elif typeitem == MachineTree.COND :         
            cond = self.__tree.GetItemData(item)['content']
            parent = self.__tree.GetItemParent(item)
            parent = self.__tree.GetItemParent(parent)
            action = self.__tree.GetItemData(parent)['content']
            popup = ConditionDialog(self, "Edit condition", self.__machine, cond, action.getConds())
            ret, newcond = popup.ShowModal()
            if ret == wx.ID_OK:
                item = self.__tree.SetItemText(item, str(newcond))
                action.updateCond(cond, newcond)        
        if item:
            self.__tree.SelectItem(item)
                
    '''
        @brief add state to machine
    '''
    def addState(self, event, item):
        state = State("")
        popup = StateDialog(self, "New state", state)
        if popup.ShowModal() == wx.ID_OK:
            self.__machine.appendState(state)
            item = self.__appendState(item, state, "State :" + state.getName(), MachineTree.STATE)
            self.__tree.SelectItem(item)
            

                
    '''
        @brief add action to state
    '''
    def addAction(self, event, item):
        action = StateAction()
        state = self.__tree.GetItemData(item)['content']
                
        popup = ActionDialog(self, "New action", self.__machine, action)
        ret, hasnew = popup.ShowModal()
        if ret == wx.ID_OK:
            state.appendAction(action)
            item = self.__appendAction(item, action) 
            if hasnew:
                self.display(self.__machine)
            self.__tree.SelectItem(item)
            

                
    '''
        @brief add cond to action
    '''
    def addCond(self, cond, item):
        cond=StateCondition("NewEvent")
        action = self.__tree.GetItemData(item)['content']
                
        popup = ConditionDialog(self, "New condition", self.__machine, cond, action.getConds())
        ret, cond = popup.ShowModal()
        if ret == wx.ID_OK:
            item = self.__tree.GetLastChild(item)
            action.addCond(cond)
            self.__setConds(item, action)
            item = self.__appendCond(item, cond)
            self.__tree.SelectItem(item)
    