import tkinter as tk
from gui.configure import *


class Button(tk.Button):
    def __init__(self, top):
        tk.Button.__init__(self, top)
        self.configure(borderwidth=0,
                       highlightthickness=0,
                       cursor="hand2")


class TopMenuButton(Button):
    def __init__(self, top):
        Button.__init__(self, top)
        self.configure(background=TMB_BG,
                       width=TMB_WIDTH)


class LeftMenuButton(Button):
    def __init__(self, top):
        Button.__init__(self, top)
        self.configure(background=LMB_BG,
                       wrap=LMB_wrap,
                       width=LMB_width,
                       foreground=LMF_TEXT_COLOR)