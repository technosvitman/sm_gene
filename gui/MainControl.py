
import wx


class MainControl(wx.Panel):

    '''
        @brief initialize main control gui panel
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)        
        box = wx.StaticBox(self, wx.ID_ANY, "General",
            style=wx.ST_NO_AUTORESIZE)
        bsizer = wx.StaticBoxSizer(box, wx.VERTICAL)
        
        text = wx.StaticText(self, -1, "Output name:")
        bsizer.Add(text)
        
        self.__output = wx.TextCtrl(self, -1, size=(140,-1), style=wx.ST_NO_AUTORESIZE)
        self.__output.SetValue('')
        bsizer.Add(self.__output)
        
        text = wx.StaticText(self, -1, "Template file:")
        bsizer.Add(text)
        
        self.__template = wx.DirPickerCtrl(self, -1, size=(220,-1))
        bsizer.Add(self.__template)
        
        self.__generate = wx.Button(self, wx.ID_OK, "Generate")
        bsizer.Add(self.__generate)
        
        border = wx.BoxSizer()
        border.Add(bsizer, 1, wx.FIXED_MINSIZE, 25)
        
        bsizer.SetSizeHints(box)
        bsizer.Fit(box)
        border.SetSizeHints(self)
        self.SetSizerAndFit(border)
        size = self.GetEffectiveMinSize()
        self.SetMaxSize(size)
        self.SetMinSize(size)
        self.SetSize(size)
        self.Layout()
    
    '''
        @brief binf on generate button click
    '''
    def bindGenerate(self, clbk):
        self.Bind(wx.EVT_BUTTON, clbk, self.__generate)
    
    '''
        @brief get output value
    '''
    def getOutput(self):
        return str(self.__output.GetValue())
        
    '''
        @brief get template file name
    '''
    def getTemplate(self):
        return self.__template.GetPath()