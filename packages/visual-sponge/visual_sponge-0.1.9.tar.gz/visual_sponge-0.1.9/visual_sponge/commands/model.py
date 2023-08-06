from pathlib import Path

from .. import MACROS, Model
from ..parsers import Parser

def MODEL(m, format_=None, **kwargs):
    """MODEL(m, format_=None, **kwargs)
  Get a new Model instance

  :return: a new Model instance
  :param m: the model
  :param format_: the model format. If not given, the format will be guessed.
  :param **kwargs: options specified to the format.
    xyz
      guess_bond=False
        whether to guess the bonded information based on distance
      as_first_frame=True
        whether to use the coordinates in the file as the coordinates in the first frame
    """
    if format_ is None:
        if isinstance(m, str):
            path = Path(m)
            suffix = path.suffix
            if suffix != "txt":
                format_ = suffix[1:]
            else:
                raise NotImplementedError
        else:
            raise TypeError
    parser = Parser(format_)
    atoms, model = parser.Model_Parse(m, **kwargs)
    Model.WORKING = model
    MACROS.CMD = [{"cmd":"MODEL", "atoms": atoms, "name": model.name, "crds": model.crds},
                  {"cmd":"DEFAULT", "mid":Model.WORKING.id}]
    return model
