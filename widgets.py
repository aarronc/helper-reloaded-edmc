"""
Various display widgets.
"""

""" Tkinter Imports """
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from ttkHyperlinkLabel import HyperlinkLabel

""" Other Imports """
import collections


class StyleCaptureLabel(ttk.Label):
    """
    A label that captures style information when EDMC applies its theme.

    USE ONLY ONCE.
    """

    def __init__(self, *args, **kwargs):
        "Initialise the ``StyleCaptureLabel``."

        ttk.Label.__init__(self, *args, **kwargs)
        self.__style = ttk.Style()  # acts like a singleton

    def configure(self, *args, **kwargs):
        "Reconfigure the ``StyleCaptureLabel``. Capture the details."

        if 'font' in kwargs:  # capture full font details
            font = kwargs['font']

            if isinstance(font, str):
                kwargs['font'] = tkFont.nametofont(font)

            elif isinstance(font, collections.Iterable):
                kwargs['font'] = tkFont.Font(font=font)

        ttk.Label.configure(self, *args, **kwargs)
        self.__style.configure('HH.TCheckbutton', **kwargs)
        self.__style.configure('HH.TLabel', **kwargs)
        

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
