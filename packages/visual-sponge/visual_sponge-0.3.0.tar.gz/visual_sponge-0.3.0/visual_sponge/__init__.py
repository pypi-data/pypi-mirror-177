from configparser import ConfigParser
from pathlib import Path
from importlib import import_module
from collections import OrderedDict
import Xponge

__version__ = "0.3.0"

Configure = ConfigParser()
ConfigurePath = Path(__file__).parent / "conf.ini"

class Model():
    id = 0
    models = OrderedDict()
    WORKING = None
    def __init__(self, name, atoms, crds=None):
        self.name = name
        self.id = Model.id
        self.atoms = atoms
        if crds is None:
            self.crds = []
        else:
            self.crds = crds
        Model.models[self.id] = self
        Model.id += 1

    def __repr__(self):
        return f"Model(name={self.name}, id={self.id}, frame={len(self.crds)}{', default' if self is Model.WORKING else ''})"

    def __str__(self):
        return repr(self)


class MACROS:
    VERSION = __version__
    PACKAGE = "Visual Sponge"
    PORT = 10696
    DEBUG_MODE = False
    APP = None
    CMD = None
    TEXT = ""
    TEMP = None

def initialize():
    Configure.read(ConfigurePath)

    translation = import_module(".translation." + Configure.get("DEFAULT", "language", fallback="chinese"), __name__).translation
    
    def localization(key):
        return translation.get(key, key)
    MACROS.localization = localization
    
initialize()