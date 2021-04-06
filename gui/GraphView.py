
import wx


class GraphView(wx.ScrolledWindow):

    '''
        @brief initialize main control gui panel
    '''
    def __init__(self, parent):
        wx.ScrolledWindow.__init__(self, parent)
        self.__bp = wx.StaticBitmap(self)
        self.EnableScrolling(True, True)
        
    '''
        @brief draw image
    '''
    def drawUml(self, path):
        im = wx.Image(path, wx.BITMAP_TYPE_ANY)
        self.__bp.SetBitmap(wx.Bitmap(im))
        
        w, h = im.GetSize()
        self.SetClientSize(w,h)
        self.SetScrollbars(20, 20, w/20, h/20)
        self.EnableScrolling(True, True)
        self.AdjustScrollbars()
        
    