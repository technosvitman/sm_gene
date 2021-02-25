
import wx


class MainControl(wx.Panel):

    '''
        @brief initialize main control gui panel
    '''
    def __init__(self, parent):
        wx.Panel.__init__(self,parent)
        self.__generate = wx.Button(self, wx.ID_CLEAR, "Generate")
    
    '''
        @brief binf on generate button click
    '''
    def bindGenerate(self, clbk):
        self.Bind(wx.EVT_BUTTON, clbk, self.__generate)
    