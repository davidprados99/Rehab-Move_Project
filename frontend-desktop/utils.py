import os
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller."""
    try:
        # PyInstaller creates a temporary folder and stores the path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        # If not running in a .exe, use the normal path
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)