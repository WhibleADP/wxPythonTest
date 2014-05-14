import wx
from math import hypot, sin, cos, pi


class Star(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, style=wx.FRAME_SHAPED |
                                                         wx.SIMPLE_BORDER |
                                                         wx.FRAME_NO_TASKBAR)



        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

        if wx.Platform == '__WXGTK__':
            self.Bind(wx.EVT_WINDOW_CREATE, self.OnWindowCreate)
        else: self.OnWindowCreate()

        self.Centre()
        self.Show(True)

    def OnPaint(self, event):
        dc = wx.PaintDC(self)

        dc.SetPen(wx.Pen('#424242'))
        size_x, size_y = self.GetClientSizeTuple()
        dc.SetDeviceOrigin(size_x / 2, size_y / 2)

        points = (((0, 85), (75, 75), (100, 10), (125, 75), (200, 85),
                   (150, 125), (160, 190), (100, 150), (40, 190), (50, 125)))

        region = wx.RegionFromPoints(points)
        dc.SetClippingRegionAsRegion(region)

        radius = hypot(size_x / 2, size_y / 2)
        angle = 0

        while (angle < 2 * pi):
            x = radius * cos(angle)
            y = radius * sin(angle)
            dc.DrawLinePoint((0, 0), (x, y))
            angle = angle + 2 * pi / 360

        dc.DestroyClippingRegion()

    def OnWindowCreate(self):
        points = (((0, 85), (75, 75), (100, 10), (125, 75), (200, 85),
                   (150, 125), (160, 190), (100, 150), (40, 190), (50, 125)))
        region = wx.RegionFromPoints(points)
        self.SetShape(region)

    def OnLeftDown(self, event):
        x, y = self.ClientToScreen(event.GetPosition())
        ox, oy = self.GetPosition()
        dx = x - ox
        dy = y - oy
        self.delta = ((dx, dy))

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            x, y = self.ClientToScreen(event.GetPosition())
            fp = (x - self.delta[0], y - self.delta[1])
            self.Move(fp)

app = wx.App()
Star(None, -1, 'Star')
app.MainLoop()
