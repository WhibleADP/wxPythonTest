import wx
import cv2
from cv2 import cv


class ShowCapture(wx.Panel):
    def __init__(self, parent, capture, fps=50):
        super(ShowCapture, self).__init__(parent)

        self.capture = capture
        ret, frame = self.capture.read()

        self.height, self.width = frame.shape[:2]
        self.SetInitialSize((self.width, self.height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        self.bmp = wx.BitmapFromBuffer(self.width, self.height, frame)

        self.timer = wx.Timer(self)
        self.timer.Start(1000./fps)

        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)

    def OnEraseBackground(self, evt):
        # This is intentionally empty, because we are using
        # an empty OnEraseBackground event to reduce flicker
        pass

    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)

    def NextFrame(self, event):
        ret, frame = self.capture.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.bmp.CopyFromBuffer(frame)
            self.Refresh()


class ShowCamera(ShowCapture):
    def __init__(self, parent, fps=15):
        capture = cv2.VideoCapture(0)
        capture.set(cv.CV_CAP_PROP_FRAME_WIDTH, 640)
        capture.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 480)
        super(ShowCamera, self).__init__(parent, capture, fps)


if __name__ == '__main__':
    app = wx.App()
    frame = wx.Frame(None)
    cap = ShowCamera(frame, fps=50)
    frame.Show()
    app.MainLoop()
