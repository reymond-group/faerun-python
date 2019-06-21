import os
from faerun.faerun import Faerun
from faerun.web import host

_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_asset(path):
    """Gets the path to the assets folder
    
    Arguments:
        path {str} -- The path of the asset within the asset folder
    
    Returns:
        str -- The full path to the asset
    """
    return os.path.join(_ROOT, 'assets', path)