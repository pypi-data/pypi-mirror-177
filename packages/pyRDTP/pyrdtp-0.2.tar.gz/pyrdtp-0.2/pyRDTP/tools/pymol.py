#!/usr/bin/env python3
"""
This tool is intended to serve as nexus between openbabel and pyRDTP. Note
that it uses the vasp file format to read and write from pyRDTP, so many things
will not be preserved when a conversion is performed.
"""

import os
from tempfile import mkstemp
from openbabel import pybel
from pyRDTP import geomio
from pyRDTP.molecule import Molecule, CatalyticSystem


def to_obabel(mol):
    """Converts a molecule object into an openbabel molecule object

    Args:
        mol (obj:`pyRDTP.molecule.Molecule`): Molecule object from pyRDTP.

    Returns:
        (obj:`pybel.Molecule`): Molecule object from openbabel.

    Notes:
        As openbabel fails reading a vasp string, this function creates a
        temporary file as a proxy to avoid the use of an string. The file is
        deleted when this function is completed.
    """
    if isinstance(mol, Molecule):
        wrap_mol = geomio.MolObj(mol)
    elif isinstance(mol, CatalyticSystem):
        wrap_mol = geomio.CatObj(mol)
    else:
        raise NotImplementedError

    _, tmp_path = mkstemp()
    mol_str = geomio.convert(wrap_mol, 'contcar').write()
    with open(tmp_path, 'w', encoding='utf8') as out_f:
        out_f.write(mol_str)
    ob_mol = next(pybel.readfile('vasp', tmp_path))
    os.remove(tmp_path)
    return ob_mol


def to_molobj(omol):
    """Converts and omol molecule into a Molecule object.

    Args:
        omol (obj:`pybel.Molecule`): Molecule object from openbabel.

    Returns:
        (obj:`pyRDTP.molecule.Molecule`) to work with pyRDTP.
    """
    raw_str = omol.write('vasp')
    vasp_obj = geomio.VaspContcar()
    vasp_obj.read(raw_str.splitlines()) # splitlines needed
    return geomio.convert(vasp_obj, 'molobj').write()


def to_smiles(mol):
    """Uses openbabel to convert the given molecule into an smiles string.

    Args:
        mol (obj:`pyRDTP.molecule.Molecule`): Molecule object from pyRDTP.

    Returns
        str containing the smiles code of the molecule.

    """
    omol = to_obabel(mol)
    raw_str = omol.write('smi')

    # openbabel includes the name of the file.
    out_str = raw_str.split('\t')[0]
    return out_str


def smiles_to_obabel(smi_str):
    """Read a smiles string and transform it to an openbabel molecule object

    Args:
        smi_str (str): Smiles string.

    Returns:
        (obj:`pybel.Molecule`): Molecule object from openbabel.
    """
    return pybel.readstring('smi', smi_str)


def from_smiles(smi_str, make3d=True):
    """Read a smiles string and transform it into pyRDTP molecule object

    Args:
        smi_str (str): Smiles string.
        make3d (bool or dict, optional): Tell obabel to perform a 3D
            transformation before converting the molecule te pyRDTP. If a
            dictionary is passed, 'forcefield' and/or 'steps' keys should be
            specified. If True forcefield='mmff94', steps=50 are used by
            default.

    Returns:
        (obj:`pyRDTP.molecule.Molecule`) to work with pyRDTP.
    """
    omol = smiles_to_obabel(smi_str)
    if isinstance(make3d, dict):
        omol.make3D(**make3d)
    elif make3d:
        omol.make3D()

    return to_molobj(omol)
