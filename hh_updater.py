"""
Hutton Helper News
"""

""" Other Imports """
import os
import sys
import zipfile
import semantic_version

""" HH Imports """
from hh_version import HH_VERSION
import xmit

HH_PLUGIN_DIRECTORY = os.path.dirname(os.path.realpath(__file__))
RELEASE_CYCLE = 60 * 1000 * 60  # 1 Hour
DEFAULT_URL = 'https://api.github.com/repos/aarronc/helper-reloaded-edmc/releases/latest'
INCLUDE_EXTENSIONS = set(['.py','.md'])


class hh_updater():

    def __init__(self):

        self.last_check = 
        self.release_info = []

    def process_event(self, cmdr, is_beta, system, station, entry, state) -> None:
        "Check RELEASE_CYCLE passed since last check"

    def delete_current_version(self, here=HH_PLUGIN_DIRECTORY):
        "SCARY."

        for filename in sorted(os.listdir(here)):
            if os.path.splitext(filename)[1] in INCLUDE_EXTENSIONS:
                if is2:
                    sys.stderr.write("Deleting {}...\r\n".format(filename))
                else:
                    logger.info("Deleting {}...".format(filename))
                os.remove(os.path.join(here, filename))


    def unzip_new_version(self, s, here=HH_PLUGIN_DIRECTORY):
        "Slightly less scary."
        
        f = BytesIO(s)

        z = zipfile.ZipFile(f, 'r')
        with z:
            for filename in sorted(z.namelist()):
                if is2:
                    sys.stderr.write("Extracting {}...\r\n".format(filename))
                else:
                    logger.info("Extracting {}...".format(filename))
                z.extract(filename, path=here)

    
    def update(self, zipfile_url):
        "Update using the ZIP file at ``zipfile_url``"

        s = xmit.get(zipfile_url, parse=False)
        self.delete_current_version()
        self.unzip_new_version(s)


    def release_check(self):
        "Check GitHub for new release"
        self.release_info = xmit.get(DEFAULT_URL)
        if self.release_info:
            if semantic_version(self.release_info['tag_name']) > semantic_version(HH_VERSION):
                self.update(self.release_info['zipball_url']) 
