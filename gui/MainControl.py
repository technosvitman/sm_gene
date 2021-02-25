
import wx


class MainControl(wx.Panel):

    '''
        @brief initialize main control gui panel
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)        
        box = wx.StaticBox(self, wx.ID_ANY, "General")
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        self.__output = wx.TextCtrl(self, -1, size=(140,-1))
        self.__output.SetValue('custom output name')
        bsizer.Add(self.__output)
        
        self.__generate = wx.Button(self, wx.ID_CLEAR, "Generate")
        bsizer.Add(self.__generate)
        
        border = wx.BoxSizer()
        border.Add(bsizer, 1, wx.EXPAND|wx.ALL, 25)
        self.SetSizer(border)
    
    '''
        @brief binf on generate button click
    '''
    def bindGenerate(self, clbk):
        self.Bind(wx.EVT_BUTTON, clbk, self.__generate)
    
    '''
        @brief binf output value changed
    '''
    def getOutput(self):
        return str(self.__output.GetValue())