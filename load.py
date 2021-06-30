"""
Hutton Helper RELOADED

re-write/re-imagination of HH
"""

""" EDMC Imports """
import logging
import semantic_version
import myNotebook as nb
from config import appname, appversion, config

""" Tkinter Imports """
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.font as tkFont
from ttkHyperlinkLabel import HyperlinkLabel

""" Other Imports """
from typing import Optional
import traceback
import uuid
import zlib
import os
import json

""" HH Imports """
from big_dicts import *
import xmit

PLUGIN_NAME = "Hutton Helper RELOADED"

plugin_dir = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f"{appname}.{plugin_dir}")

UUID = str(uuid.uuid4())

class HuttonHelper:
    """
    Hutton-Helper-RELOADED

    The hutton helper re-written to be more managable and easier to understand
    """

    def __init__(self) -> None:
        # Instantiate Class.  when decoraters are used we wont be able to do this ! 
        logger.info(f"{PLUGIN_NAME} instantiated")

    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.
        It is the first point EDMC interacts with our code after loading our module.
        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        return PLUGIN_NAME

    def on_unload(self) -> None:
        """
        on_unload is called by plugin_stop below.
        It is the last thing called before EDMC shuts down. Note that blocking code here will hold the shutdown process.
        """
        self.on_preferences_closed("", False)  # Save our prefs

    def setup_preferences(self, parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
        """
        setup_preferences is called by plugin_prefs below.
        It is where we can setup our own settings page in EDMC's settings window. Our tab is defined for us.
        :param parent: the tkinter parent that our returned Frame will want to inherit from
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        :return: The frame to add to the settings window
        """
        current_row = 0
        frame = nb.Frame(parent)

        return frame

    def on_preferences_closed(self, cmdr: str, is_beta: bool) -> None:
        """
        on_preferences_closed is called by prefs_changed below.
        It is called when the preferences dialog is dismissed by the user.
        :param cmdr: The current ED Commander
        :param is_beta: Whether or not EDMC is currently marked as in beta mode
        """
 
    def setup_main_ui(self, parent: tk.Frame) -> tk.Frame:
        """
        Create our entry on the main EDMC UI.
        This is called by plugin_app below.
        :param parent: EDMC main window Tk
        :return: Our frame
        """
        current_row = 0
        frame = tk.Frame(parent)


        current_row += 1


        return frame

    def process_event(self, cmdr, is_beta, system, station, entry, state) -> None:
        """
        E:D client made a journal entry
        :param cmdr: The Cmdr name, or None if not yet known
        :param system: The current system, or None if not yet known
        :param station: The current station, or None if not docked or not yet known
        :param entry: The journal entry as a dictionary
        :param state: A dictionary containing info about the Cmdr, current ship and cargo
        :return:
        """
        self.cmdr = cmdr

    def error_report(self, description=None):
        "Handle failure."

        logger.error("ERROR: {}".format(description or ''))
        logger.error("{}".format("\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))))

        errorreport = {}
        errorreport['cmdr'] = self.cmdr
        errorreport['huttonappversion'] = HH_VERSION
        errorreport['edmcversion'] = appversion
        errorreport['modulecall'] = description or ''
        errorreport['traceback'] = traceback.format_exception(exc_type, exc_value, exc_traceback)
        error_data = zlib.compress(json.dumps(errorreport).encode('utf-8'))
        xmit.post('/errorreport', error_data, headers=xmit.COMPRESSED_OCTET_STREAM)


hh = HuttonHelper()


# Note that all of these could be simply replaced with something like:
# plugin_start3 = hh.on_load
def plugin_start3(plugin_dir: str) -> str:
    return hh.on_load()


def plugin_stop() -> None:
    return hh.on_unload()


def plugin_prefs(parent: nb.Notebook, cmdr: str, is_beta: bool) -> Optional[tk.Frame]:
    return hh.setup_preferences(parent, cmdr, is_beta)


def prefs_changed(cmdr: str, is_beta: bool) -> None:
    return hh.on_preferences_closed(cmdr, is_beta)


def plugin_app(parent: tk.Frame) -> Optional[tk.Frame]:
    return hh.setup_main_ui(parent)


def journal_entry(cmdr, is_beta, system, station, entry, state) -> None:
    return hh.process_event(cmdr, is_beta, system, station, entry, state)