"""
This is only to be used as a bridge to go from version
1.0 to version 2.0 and beyond.  Scripts should use the
modern version 2.0 interface as described in the warning
message
"""

from warnings import warn

import MultiPyVu as mpv


class old_MultiVuDataFile():
    def __init__(self):
        self.TScaleType = mpv.TScaleType
        self.TStartupAxisType = mpv.TStartupAxisType
        self.TTimeUnits = mpv.TTimeUnits
        self.TTimeMode = mpv.TTimeMode

    def MultiVuDataFile(self):
        msg = '\n|DEPRECATION WARNING: Instantiating this class using this '
        msg += 'method has been deprecated.  Rather than importing the module '
        msg += 'using:\n'
        msg += '|\tfrom MultiVuDataFile import MultiVuDataFile as mvd\n'
        msg += 'and then instantiating it using:\n'
        msg += '|\ts = mvd.MultiVuDataFile())\n'
        msg += '|\ts.open()\n'
        msg += '|---------------------------------------\n'
        msg += '|Use the following simpler method:\n'
        msg += '|\timport MultiPyVu as mpv\n'
        msg += '|\ts = mpv.DataFile()\n'
        msg += '|---------------------------------------\n\n'
        warn(msg, FutureWarning, stacklevel=2)
        return mpv.DataFile()


MultiVuDataFile = old_MultiVuDataFile()
