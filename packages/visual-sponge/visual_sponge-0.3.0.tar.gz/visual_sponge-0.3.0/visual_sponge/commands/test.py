from .. import MACROS, Model


def TEST():
    name = MACROS.localization("Water For Test")
    atoms = [{"elem":"O", "bonds":[1,2]}, {"elem":"H"}, {"elem":"H"}]
    crds = [[[0,0,0],[1.0,0,0],[0,1.0,0]],
            [[0,0,0],[1.5,0,0],[0,1.5,0]],
            [[0,0,0],[2.0,0,0],[0,2.0,0]],
            [[0,0,0],[1.5,0,0],[0,1.5,0]]]
    model = Model(name=name, atoms=atoms)
    model.crds.extend(crds)
    Model.WORKING = model
    MACROS.CMD = [{"cmd":"MODEL", "atoms":atoms, "name":name},
                  {"cmd":"TRAJ", "mid":model.id, "crds":crds},
                  {"cmd":"DEFAULT", "mid":Model.WORKING.id}]
    return model
