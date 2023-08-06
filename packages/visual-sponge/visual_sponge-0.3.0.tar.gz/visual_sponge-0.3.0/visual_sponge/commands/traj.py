from pathlib import Path

from .. import MACROS, Model
from ..parsers import Parser

def TRAJ(traj, format_=None, m=None, append=False, **kwargs):
    """TRAJ(traj, format_=None, m=None, append=False, **kwargs)
  Load trajectory to the model

  :return: None
  :param traj: the trajectory
  :param format_: the trajectory format. If not given, the format will be guessed.
  :param m: the model to load. If not given, the working model will be used.
  :param append: whether to append or replace the trajectory in model
  :param **kwargs: options specified to the format.
    xyz
      frame=1
        the number of frames in the trajectory
    """
    if m is None:
        m = Model.WORKING
        if m is None:
            raise ValueError
    elif isinstance(m, int):
        m = Model.models[m]
    if format_ is None:
        if isinstance(traj, str):
            path = Path(traj)
            suffix = path.suffix
            if suffix != "txt":
                format_ = suffix[1:]
            else:
                raise NotImplementedError
        else:
            raise TypeError
    parser = Parser(format_)
    crds = parser.Traj_Parse(traj, **kwargs)
    if append:
        m.crds.extend(crds)
    else:
        m.crds = crds
    MACROS.CMD = [{"cmd":"TRAJ", "crds":crds, "append":append, "mid":m.id}]
    return m

