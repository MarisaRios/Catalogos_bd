# main.py
import wx
from login import LoginFrame

if __name__ == "__main__":
    app = wx.App(False)
    login_frame = LoginFrame()
    app.MainLoop()