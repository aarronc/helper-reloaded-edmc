"""
Hutton Helper News
"""

""" EDMC Imports """
import logging
import semantic_version
from config import appname

""" Tkinter Imports """
import tkinter.messagebox as tkMessageBox

""" HH Imports """
from hh_version import HH_VERSION
import xmit

""" Other Imports """
import os
import sys
import zipfile
from io import BytesIO

HH_PLUGIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RELEASE_CYCLE = 60 * 1000 * 60  # 1 Hour
DEFAULT_URL = 'https://api.github.com/repos/aarronc/helper-reloaded-edmc/releases/latest'
INCLUDE_EXTENSIONS = set(['.py','.md'])
UPDATE_MESSAGE = "Hutton Helper Updated to version {}\n\nRelease Info:\n'{}'\n\nPlease Restart EDMC to use new version"

plugin_name = os.path.basename(os.path.dirname(__file__))
logger = logging.getLogger("{}.{}".format(appname,plugin_name))

lastcheck = ""

def delete_current_version(here=HH_PLUGIN_DIRECTORY):
    "SCARY."

    for filename in sorted(os.listdir(here)):
        if os.path.splitext(filename)[1] in INCLUDE_EXTENSIONS:
            logger.info("Deleting {}...".format(filename))
            os.remove(os.path.join(here, filename))


def unzip_new_version(s, here=HH_PLUGIN_DIRECTORY):
    "Slightly less scary."
    
    f = BytesIO(s)
    z = zipfile.ZipFile(f, 'r')
    with z:
        #for filename in sorted(z.namelist()):
        #    logger.info("Extracting {}...".format(filename))
        #    z.extract(filename, path=here)
        for zip_info in z.infolist():
            if zip_info.filename[-1] == '/':
                continue
            zip_info.filename = os.path.basename(zip_info.filename)
            z.extract(zip_info, here)


def update(zipfile_url):
    "Update using the ZIP file at ``zipfile_url``"

    s = xmit.get(zipfile_url, parse=False)
    delete_current_version()
    unzip_new_version(s)


def release_check():
    "Check GitHub for new release"
        
    release_info = xmit.get(DEFAULT_URL)
    if release_info:
        if semantic_version.Version(release_info['tag_name']) == semantic_version.Version(HH_VERSION):
            return  # Current Version do nothing

        elif semantic_version.Version(release_info['tag_name']) > semantic_version.Version(HH_VERSION):
            update(release_info['zipball_url'])
            tkMessageBox.showinfo("Hutton Helper Updated to version {}".format(release_info['tag_name']) , UPDATE_MESSAGE.format(release_info['tag_name'],release_info['body']))
