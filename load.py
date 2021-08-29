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
import hh_data
import hh_news
from hh_version import HH_VERSION
import xmit
import widgets
import galaxy_regions
from canonnevents import whiteList

PLUGIN_NAME = "Hutton Helper RELOADED"

ADDITIONAL_PATHS_URL = 'http://hot.forthemug.com/event_paths.json'

plugin_dir = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger(f"{appname}.{plugin_dir}")
if not logger.hasHandlers():
    level = logging.INFO  # this level means we can have level info and above So logger.info(...) is equivalent to sys.stderr.write() but puts an INFO tag on it logger.error(...) is possible gives ERROR tag
    logger.setLevel(level)
    logger_channel = logging.StreamHandler()
    logger_channel.setLevel(level)
    logger_formatter = logging.Formatter(f'%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d:%(funcName)s: %(message)s')
    logger_formatter.default_time_format = '%Y-%m-%d %H:%M:%S'
    logger_formatter.default_msec_format = '%s.%03d'
    logger_channel.setFormatter(logger_formatter)
    logger.addHandler(logger_channel)

UUID = str(uuid.uuid4())

def merge_dicts(*dict_args):
    """
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    """
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


class HuttonHelper:
    """
    Hutton-Helper-RELOADED

    The hutton helper re-written to be more managable and easier to understand
    """
    def _cargo_refresh(self, cmdr):
        dump_path = hh_data.get_journal_path('Cargo.json')
        with open(dump_path, 'r') as dump:
            dump = dump.read()
            if dump ==  "":
                return
            dump = json.loads(dump)
            dump['commandername'] = cmdr
            compress_json = json.dumps(dump)
            cargo_data = zlib.compress(compress_json.encode('utf-8'))
            xmit.post('/missioncargo', cargo_data, headers=xmit.COMPRESSED_OCTET_STREAM)


    def __init__(self) -> None:
        # Instantiate Class.  when decoraters are used we wont be able to do this ! 
        self.cmdr = "Not Known Yet"
        logger.info(f"{PLUGIN_NAME} instantiated")


    def on_load(self) -> str:
        """
        on_load is called by plugin_start3 below.
        It is the first point EDMC interacts with our code after loading our module.
        :return: The name of the plugin, which will be used by EDMC for logging and for the settings window
        """
        # Below not working to get additional paths from server and merge the dicts

        #extra_paths = xmit.get(ADDITIONAL_PATHS_URL)
        #nonlocal EVENT_PATHS
        #if extra_paths is not None:
            #EVENT_PATHS = merge_dicts(EVENT_PATHS, extra_paths)

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
        padx, pady = 10, 5  # formatting
        sticky = tk.EW + tk.N  # full width, stuck to the top
        anchor = tk.NW

        # we declare a whitelist object so we can run a timer to fetch the event whitelist from Canonn
        # This is so that we can find out what events to transmit There is no UI associated
        Canonn=whiteList(parent)
        Canonn.fetchData()

        frame = self.frame = tk.Frame(parent)
        frame.columnconfigure(0, weight=1)

        table = tk.Frame(frame)
        table.columnconfigure(1, weight=1)
        table.grid(sticky=sticky)

        HyperlinkLabel(
            table,
            text='Helper:',
            url='https://hot.forthemug.com/',
            anchor=anchor,
        ).grid(row=0, column=0, sticky=sticky)
        self.status = widgets.SelfWrappingLabel(table, anchor=anchor, text="For the Mug!")
        self.status.grid(row=0, column=1, sticky=sticky)

        widgets.StyleCaptureLabel(table, anchor=anchor, text="Hutton News:").grid(row=1, column=0, sticky=sticky)
        hh_news.HuttonNews(table).grid(row=1, column=1, sticky=sticky)

        self.plugin_rows = {}
        self.plugin_frames = {}
        row = 1 # because the table is first

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
        #we are going to send events to Canonn, The whitelist tells us which ones
        try:
            whiteList.journal_entry(cmdr, is_beta, system, station, entry, state,"Hutton-Helper-{}".format(HH_VERSION))
        except:
            self.error_report("Canonn failed, but don't let that stop you")

        if is_beta:
            self.status['text'] = 'Disabled due to beta'
            return

        self.cmdr = cmdr
        hh_news.commander = cmdr

        entry['commandername'] = cmdr
        entry['hhstationname'] = station
        entry['hhsystemname'] = system
        entry['huttonappversion'] = HH_VERSION
        entry['edmcversion'] = str(appversion())
        entry['uuid'] = UUID

        compress_json = json.dumps(entry)
        transmit_json = zlib.compress(compress_json.encode('utf-8'))

        event = entry['event']

        # If we can find an entry in EVENT_PATHS, forward on to right end point
        event_path = EVENT_PATHS.get(event)
        if event_path:
            xmit.post(event_path, data=transmit_json, parse=False, headers=xmit.COMPRESSED_OCTET_STREAM)

        if 'StarPos' in entry:
            entry['StarRegion'] = galaxy_regions.findRegion(entry['StarPos'][0],entry['StarPos'][1],entry['StarPos'][2])

        # If we can find an entry in EVENT_STATUS_FORMATS, fill in the string and display it to the user:
        status_format = EVENT_STATUS_FORMATS.get(entry['event'])
        if status_format:
            self.status['text'] = status_format.format(**entry)

        # Update and Send cargo to server
        if event == 'Cargo':
            self._cargo_refresh(cmdr)

        # For some events, we need our status to be based on translations of the event that string.format can't easily do:
        if event == 'MarketBuy':
            this.status['text'] = "{:,.0f} {} bought".format(float(entry['Count']), ITEM_LOOKUP.get(entry['Type'],entry['Type']))

        elif event == 'MarketSell':
            this.status['text'] = "{:,.0f} {} sold".format(float(entry['Count']), ITEM_LOOKUP.get(entry['Type'],entry['Type']))

        elif event == 'FactionKillBond':
            this.status['text'] = "Kill Bond Earned for {:,.0f} credits".format(float(entry['Reward']))

        elif event == 'Bounty':
            this.status['text'] = "Bounty Earned for {:,.0f} credits".format(float(entry['TotalReward']))
    
        elif event == 'RedeemVoucher':
            # For some events, we need to check another lookup table. There are ways to make the original lookup table
            # do this heavy lifting, too, but it'd make the code above more complicated than a trucker who'd only just
            # learned Python could be expected to maintain.

            redeem_status_format = REDEEM_TYPE_STATUS_FORMATS.get(entry['Type'])
            if redeem_status_format:
                this.status['text'] = redeem_status_format.format(float(entry['Amount']))

        elif event == 'SellExplorationData':
            baseval = entry['BaseValue']
            bonusval = entry['Bonus']
            totalvalue = entry['TotalEarnings']
            this.status['text'] = "Sold ExplorationData for {:,.0f} credits".format(float(totalvalue))

        elif event == 'MultiSellExplorationData':
            baseval = entry['BaseValue']
            bonusval = entry['Bonus']
            totalvalue = entry['TotalEarnings']
            this.status['text'] = "Sold ExplorationData for {:,.0f} credits".format(float(totalvalue))

    def on_cmdr_data(self, data, is_beta):
        """
        E:D client shortly after startup gives dump of information on current commander
        :param data: A dictionary containing info about the Cmdr
        :param is_beta: If game is a beta version
        :return:
        """

        if not is_beta:
            compress_json = json.dumps(dict(data))
            transmit_json = zlib.compress(compress_json.encode('utf-8'))
            xmit.post('/docked', parse=False, data=transmit_json, headers=xmit.COMPRESSED_OCTET_STREAM)


    def error_report(self, description=None):
        "Handle failure."

        logger.error("ERROR: {}".format(description or ''))
        logger.error("{}".format("\n".join(traceback.format_exception(exc_type, exc_value, exc_traceback))))

        errorreport = {}
        errorreport['cmdr'] = self.cmdr
        errorreport['huttonappversion'] = HH_VERSION
        errorreport['edmcversion'] = str(appversion())
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

def cmdr_data(data, is_beta):
    return hh.on_cmdr_data(data, is_beta)