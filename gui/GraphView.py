
import wx

'''
    @brief panel to display UML graph
'''
class GraphView(wx.ScrolledWindow):

    '''
        @brief initialize main control gui panel
        @param parent the parent container
    '''
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        
        self.__bp = wx.StaticBitmap(self)
        self.Layout()
        
    '''
        @brief draw image
        @param path the image path
    '''
    def drawUml(self, path):
        im = wx.Image(path, wx.BITMAP_TYPE_ANY)
        
        self.__bp.SetBitmap(wx.Bitmap(im))        
        pw, ph = self.GetSize()
        
        w, h = im.GetSize()
        self.SetClientSize(w,h)
        self.Fit()
        self.SetScrollbars(20, 20, w/20, h/20)
        self.EnableScrolling(True, True)
        self.SetSize(w+20, ph)
        
    