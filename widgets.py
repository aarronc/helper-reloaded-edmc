"""
Various display widgets.
"""

""" Tkinter Imports """
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from ttkHyperlinkLabel import HyperlinkLabel




class SelfWrappingHyperlinkLabel(HyperlinkLabel):
    "Tries to adjust its width."

    def __init__(self, *a, **kw):
        "Init."

        HyperlinkLabel.__init__(self, *a, **kw)
        self.bind('<Configure>', self.__configure_event)

    def __configure_event(self, event):
        "Handle resizing."

        self.configure(wraplength=event.width - 2)


class SelfWrappingLabel(ttk.Label):
    "Tries to adjust its width."

    def __init__(self, *a, **kw):
        "Init."

        ttk.Label.__init__(self, *a, **kw)
        self.bind('<Configure>', self.__configure_event)

    def __configure_event(self, event):
        "Handle resizing."

        self.configure(wraplength=event.width - 2)
