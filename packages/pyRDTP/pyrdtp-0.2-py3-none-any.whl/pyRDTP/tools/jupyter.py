import numpy as np
import py3Dmol
from pyRDTP import geomio
from pyRDTP.molecule import Molecule


def show_molecule(molecule, center=True, index=False):
    uni_obj = geomio.MolObj(molecule)
    xyz_obj = geomio.XYZ(uni_obj)
    if center:
        center = molecule.find_centroid('cartesian')
        vector = np.zeros(3) - center
        xyz_obj.coords += vector
    xyz_coords = str(xyz_obj)
    view = py3Dmol.view()
    view.addModel(xyz_coords, 'xyz')
    view.setStyle({'sphere': {'color': 'spectrum'}})
    if index:
        for numb, item in enumerate(xyz_obj.coords):
            view.addLabel(str(numb), {'position': {'x': item[0], 'y': item[1],
                                                   'z': item[2]},
                                      'backgroundColor': 0x800080,
                                      'backgroundOpacity': 0.8})
    return view


def j_show(self, center=True, index=False):
    return show_molecule(self, center, index)


Molecule.j_show = j_show
