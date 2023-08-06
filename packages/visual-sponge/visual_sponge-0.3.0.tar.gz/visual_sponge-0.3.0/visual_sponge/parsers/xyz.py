from pathlib import Path

from . import Parser
from .. import Model


class XYZParser(Parser, formats="xyz"):
    @staticmethod
    def Model_Parse(m, **kwargs):
        guess_bond = kwargs.get("guess_bond", False)
        as_first_frame = kwargs.get("as_first_frame", True)
        if guess_bond:
            raise NotImplementedError
        with open(m) as f:
            num = int(f.readline())
            atoms = [{} for i in range(num)]
            if as_first_frame:
                crds = [None for i in range(num)]
            else:
                crds = None
            name = f.readline().strip()
            for i in range(num):
                line = f.readline()
                words = line.split()
                atoms[i]["elem"] = words[0]
                if as_first_frame:
                    crds[i] = [float(words[j + 1]) for j in range(3)]
        return atoms, Model(name=name, atoms=atoms, crds=[crds])
    
    @staticmethod
    def Traj_Parse(traj, **kwargs):
        frames = kwargs.get("frames", 1)
        crds = [None] * frames
        with open(traj) as f:
            for frame in range(frames):
                num = int(f.readline())
                crd = [None] * num
                f.readline()
                for i in range(num):
                    line = f.readline()
                    words = line.split()
                    crd[i] = [float(words[j + 1]) for j in range(3)]
                crds[frame] = crd
        return crds