#!/usr/bin/env python3
"""This module provide the necessary tools to parse CONTCAR and POSCAR files
and convert them to molecules """
import xml.etree.ElementTree
import itertools
import os
from shutil import move
from collections import namedtuple, Counter
import numpy as np
from pyRDTP import molecule


def read_from_file_vasp(_filename, definition='molecule'):
    """Reads the attributes of the molecule from a given VASP format file.

    Args:
        _filename (str): Direction of the file.

    Returns:
        :obj`molecule.Molecule` molecule object extracted from the file.
    """
    poscar = namedtuple('POSCAR', 'name multiplier cell_p a_elem a_numb '
                        'a_tot type coords freeze')
    with open(_filename) as file_contcar:
        content = file_contcar.readlines()
    content = [line.strip() for line in content]
    name = content[0]
    multiplier = float(content[1])
    cell_p = np.asarray([line.split() for line in content[2:5]], dtype=float)
    a_elem = tuple(content[5].split())
    a_numb = tuple((int(number) for number in content[6].split()))
    a_tot = sum(a_numb)

    coord_indexes = [content.index(match) for match in content[1:] if 'configuration' in match]
    if coord_indexes:
        all_confs = [(start+1, end) for start, end in zip(coord_indexes[:-1], coord_indexes[1:])]
        if 'Cartesian' in content[all_confs[0][0] - 1]:
            coord_type = 'cartesian'
        elif 'Direct' in content[all_confs[0][0] - 1]:
            coord_type = 'direct'
        else:
            raise NotImplementedError

    else:
        try:
            start_at = content.index('Cartesian') + 1
            coord_type = 'cartesian'
        except Exception:
            try:
                start_at = content.index('Direct') + 1
                coord_type = 'direct'
            except Exception:
                print('File must be in Cartesian or Direct coordinates!')

        finish_at = a_tot + start_at
        all_confs = [(start_at, finish_at)]

    mol_lst = []
    for start_at, finish_at in all_confs:
        coords_raw = [line.split() for line in content[start_at:finish_at]]
        coords = []
        freeze = []
        for line in coords_raw:
            coords.append([float(number) for number in line[0:3]])
            if line[3:6]:
                freeze.append([freeze for freeze in line[3:6]])
            else:
                freeze.append(['T', 'T', 'T'])
        coords = np.asarray(coords, dtype=float)
        system_tupled = poscar(name, multiplier, cell_p, a_elem,
                               a_numb, a_tot, coord_type, coords, freeze)
        vp_obj = Vasp(system_tupled)
        if definition == 'molecule':
            mol_obj = vp_obj.convert_to_molecule()
        elif definition == 'bulk':
            mol_obj = vp_obj.convert_to_bulk()
        mol_lst.append(mol_obj)

    if len(mol_lst) == 1:
        mol_lst = mol_obj

    return mol_lst


def read_from_file_vasprun(filename):
    """Read all the images from a vasprun.xml file and return a list
    containing all the image objects.
    """
    vasprun = xml.etree.ElementTree.parse(filename).getroot()
    calculations = vasprun.findall('calculation')
    atominfo = vasprun.find('atominfo')
    atominfo = atominfo.find('array')
    atominfo = atominfo.find('set')
    elem_lst = []
    for element in atominfo:
        elem_lst.append(element[0].text.strip())
    elem_lst = np.asarray(elem_lst)

    freeze = [match for match in vasprun.findall('structure')
              if 'initialpos' in match.attrib.values()]
    freeze = [match for match in freeze[0].findall('varray')
              if 'selective' in match.attrib.values()]
    try:
        freeze = freeze[0].findall('v')
        freeze = [line.text.split() for line in freeze]
    except IndexError:
        freeze = [['T', 'T', 'T'] for element, _ in enumerate(elem_lst)]

    package = CompleteRun()
    for item in calculations:
        forces = item.find('varray')
        forces = [line.text.split() for line in forces]
        forces = np.asarray(forces, dtype=float)

        dcoords = item.find('structure')
        cell_p_pvt = dcoords.find('crystal')
        dcoords = dcoords.find('varray')
        dcoords = [line.text.split() for line in dcoords]
        dcoords = np.asarray(dcoords, dtype=float)

        energy_pvt = item.find('energy').findall('i')
        energy = {}
        for item_pvt in energy_pvt:
            if 'e_fr_energy' in item_pvt.attrib.values():
                energy['fr_energy'] = float(item_pvt.text)
            if 'e_wo_entrp' in item_pvt.attrib.values():
                energy['wo_entrp'] = float(item_pvt.text)
            if 'e_0_energy' in item_pvt.attrib.values():
                energy['0_energy'] = float(item_pvt.text)

        for item_pvt in cell_p_pvt:
            if 'basis' in item_pvt.attrib.values():
                cell_p = [line.text.split() for line in item_pvt]
                cell_p = np.asarray(cell_p, dtype=float)
                break

        package.add_image(Image(energy, forces, cell_p, elem_lst, freeze=freeze, dcoords=dcoords))

    return package


def read_from_file_xyz(_filename):
    """Read the attributes of the molecule from a given xyz format file.

    Args:
        _filename (str): Direction of the file.

    Returns:
        :obj`molecule.Molecule` molecule object extracted from the file.
    """
    xyz = namedtuple('XYZ', 'name elems a_tot coords')
    with open(_filename) as fc:
        content = [line.strip() for line in fc]

    atoms_total = content[0]

    if content[1]:
        name = content[1]
    else:
        name = 'Default'

    atoms_coords_raw = content[2:atoms_total+2]
    atoms_elements = []
    atoms_coords = []

    for line in atoms_coords_raw:
        atoms_elements.append(line[0])
        atoms_coords.append(line[1:4])

    atoms_elements = tuple(atoms_elements)
    atoms_coords = np.asarray(atoms_coords, dtype=float)
    system_tupled = xyz(name, atoms_elements, atoms_total, atoms_coords)
    xyz_obj = Xyz(system_tupled)
    return xyz_obj.convert_to_molecule()


def print_vasp(mol_obj, _filename, coord_type='direct', elem_type='split'):
    """Prints all the molecules in the molecules attribute in vasp POSCAR
    format.

    Args:
        mol_obj (:obj`molecule.Molecule` or :obj`molecule.CatalyticSystem`):
            Object that will be printed.
        _filename (str): Path of the file in which the output
            will be write.
        coord_type (str, optional): Indicates the coordinate system format
            of the output file. Must be 'direct' or 'cartesian'.
            Defaults to 'cartesian'.
        elem_type (str, optional): Writing style of the output. Must be
            'split' or 'join'. 'split' writes the elements of the
            molecules splitted between molecules while 'join' count all
            the atoms of a certain element and then print the coordinates.
            Defaults to 'split'

    Notes:
        The atoms are sorted by the first element in the molecule list.

    Examples:
        Example of the output format for 2 H20 molecules:
        split :
            H O H O
            2 1 2 O
            ...
            H coords
            H coords
            O coords
            ...

        join:
            H O
            4 2
            ...
            H coords
            H coords
            H coords
            ...
    """
    mol_lst = []
    bulk = None
#    for _molecule in self.molecules:
#        if isinstance(_molecule, molecule.Bulk):
#            bulk = _molecule
#            mol_lst.insert(0, _molecule)  # Use the first molecule in case
#        else:                             # that there is no bulk.
#            mol_lst.append(_molecule)
#
#    if not bulk:
#        bulk = self.molecules[0]  # Virtual bulk for cellp and name
    if isinstance(mol_obj, (molecule.Molecule, molecule.Bulk)):
        bulk = mol_obj  # Virtual bulk for cellp and name
        mol_lst.append(bulk)
    elif isinstance(mol_obj, molecule.CatalyticSystem):
        bulk = mol_obj.surface
        mol_lst.append(bulk)
        mol_lst += mol_obj.molecules
    else:
        msg = """ Object type must molecule.Molecule, molecule.Bulk
                  or molecule.CatalyticSystem """
        raise NotImplementedError(msg)

    title = bulk.name
    elem_dicts = [mol.elem_inf() for mol in mol_lst]
    atom_elems = []
    atom_numbers = []
    if elem_type == 'split':
        for dict_c in elem_dicts:
            for elem, numb in dict_c.items():
                atom_elems.append(elem)
                atom_numbers.append(numb)
    elif elem_type == 'join':
        elem_dict_new = Counter({})
        for dict_c in elem_dicts:
            elem_dict_new += Counter(dict_c)
        for elem, numb in elem_dict_new.items():
            atom_elems.append(elem)
            atom_numbers.append(numb)

    atoms_ordered = []
    if elem_type == 'split':
        for dict_c, _molecule in zip(elem_dicts, mol_lst):
            for elem in dict_c.keys():
                atoms_ordered += [atom for atom in _molecule
                                  if atom.element == elem]
    elif elem_type == 'join':
        for elem in atom_elems:
            for _molecule in mol_lst:
                atoms_ordered += [atom for atom in _molecule
                                  if atom.element == elem]

    if os.path.isfile(_filename):
        move(_filename, _filename+'.bak')

    with open(_filename, 'a') as fc:
        print(title, file=fc)
        print('{0:16f}'.format(1), file=fc)
        print_line = '{0:16f} {1:16f} {2:16f}'
        coords_format = ' {:+2.16f}  {:+2.16f}  {:+2.16f}  {:1s}  {:1s}  {:1s}'
        cell_p_format = ' {:.16f}  {:.16f}  {:.16f} '
        for coord in bulk.cell_p.direct:
            print(cell_p_format.format(coord[0], coord[1], coord[2]), file=fc)
        print("", end="", file=fc)
        print(*atom_elems, sep=" ", file=fc)
        print("", end="", file=fc)
        print(*atom_numbers, sep=" ", file=fc)
        print("Selective Dynamics", file=fc)
        if coord_type == 'direct':
            print("Direct", file=fc)
        elif coord_type == 'cartesian':
            print("Cartesian", file=fc)
        for atom in atoms_ordered:
            if coord_type == 'direct':
                coords = atom.dcoords
            elif coord_type == 'cartesian':
                coords = atom.coords
            freeze = []
            for item in atom.freeze:
                if item:
                    freeze.append('T')
                else:
                    freeze.append('F')
            print(coords_format.format(coords[0], coords[1],
                                       coords[2], freeze[0],
                                       freeze[1], freeze[2]), file=fc)


def print_xyz(mol_obj, _filename):
    """Prints a file representing the current catalytic system in .xyz format

    Args:
        mol_obj (:obj`molecule.Molecule` or :obj`molecule.CatalyticSystem`):
            Object that will be printed.
        _filename (str): Direction of the output xyz file

    Raises:
        NotImplementedError if the mol_obj is neither a Molecule or a
            Catalytic System.
    """
    mol_lst = []
    if isinstance(mol_obj, (molecule.Molecule, molecule.Bulk)):
        mol_lst.append(mol_obj)
    elif isinstance(mol_obj, molecule.CatalyticSystem):
        mol_lst.append(mol_obj.surface)
        mol_lst += mol_obj.molecules
    else:
        msg = """ Object type must molecule.Molecule, molecule.Bulk
                  or molecule.CatalyticSystem """
        raise NotImplementedError(msg)

    atoms_total = sum([len(mol) for mol in mol_lst])
    format_b = '{0} {1:10f} {2:10f} {3:10f}'
    with open(_filename, 'a') as fc:
        print(atoms_total, file=fc)
        print('', file=fc)
        for mol in mol_lst:
            for atom in mol.atoms:
                coords = atom.coords
                print(format_b.format(atom.element, coords[0], coords[1],
                                      coords[2]), file=fc)


class Vasp:
    """Vasp object provide the tools to parse and create molecules from
    POSCAR files.

    Attributes:
        raw (str): Raw data obtained from the input file.
        name (str): Name of the given system.
        multiplier (int): Multiplier of the system.
        cell_p (:obj`list` 3x3 of str): Cell parameters of the system.
        a_elem (:obj`list` of str): Elements of the system.
        a_numb (:obj`list` of str): Number of atoms of every atom in the
            system
        a_tot (int) : Total atoms of the system.
        type (str) : Coordinate system of the file, 'Direct' or 'Cartesian'.
        coords (:obj`list` of str): Coordinates of all the atoms in the system.
        freeze (:obj`list` of str): Freeze coordinates status of every atom.
    """

    def __init__(self, data_args):
        self.name = data_args.name
        self.multiplier = data_args.multiplier
        self.cell_p = data_args.cell_p
        self.a_elem = data_args.a_elem
        self.a_numb = data_args.a_numb
        self.a_tot = data_args.a_tot
        self.type = data_args.type
        self.coords = data_args.coords
        self.freeze = data_args.freeze

    def convert_to_molecule(self):
        """ Creates a molecule object using the POSCAR file.

        Returns:
            molecule.Molecule object containing the created molecule.
        """
        _molecule = molecule.Molecule(self.name)
        return self.molecule_fill(_molecule)

    def convert_to_bulk(self):
        """ Creates a bulk object using the POSCAR file

        Returns:
            molecule.Bulk object containing the created bulk.
        """
        bulk = molecule.Bulk(self.name)
        return self.molecule_fill(bulk)

    def read_molecule(self, mol_obj, elem_type='split'):
        mol_lst = []
        bulk = None
        if isinstance(mol_obj, (molecule.Molecule, molecule.Bulk)):
            bulk = mol_obj  # Virtual bulk for cellp and name
            mol_lst.append(bulk)
        elif isinstance(mol_obj, molecule.CatalyticSystem):
            bulk = mol_obj.surface
            mol_lst.append(bulk)
            mol_lst += mol_obj.molecules
        else:
            msg = """ Object type must molecule.Molecule, molecule.Bulk
                      or molecule.CatalyticSystem """
            raise NotImplementedError(msg)

        title = bulk.name
        elem_dicts = [mol.elem_inf() for mol in mol_lst]
        atom_elems = []
        atom_numbers = []
        if elem_type == 'split':
            for dict_c in elem_dicts:
                for elem, numb in dict_c.items():
                    atom_elems.append(elem)
                    atom_numbers.append(numb)
        elif elem_type == 'join':
            elem_dict_new = Counter({})
            for dict_c in elem_dicts:
                elem_dict_new += Counter(dict_c)
            for elem, numb in elem_dict_new.items():
                atom_elems.append(elem)
                atom_numbers.append(numb)

        atoms_ordered = []
        if elem_type == 'split':
            for dict_c, _molecule in zip(elem_dicts, mol_lst):
                for elem in dict_c.keys():
                    atoms_ordered += [atom for atom in _molecule
                                      if atom.element == elem]
        elif elem_type == 'join':
            for elem in atom_elems:
                for _molecule in mol_lst:
                    atoms_ordered += [atom for atom in _molecule
                                      if atom.element == elem]

        if os.path.isfile(_filename):
            move(_filename, _filename+'.bak')

        with open(_filename, 'a') as fc:
            print(title, file=fc)
            print('{0:16f}'.format(1), file=fc)
            print_line = '{0:16f} {1:16f} {2:16f}'
            coords_format = ' {:+2.16f}  {:+2.16f}  {:+2.16f}  {:1s}  {:1s}  {:1s}'
            for coord in bulk.cell_p.direct:
                print(print_line.format(coord[0], coord[1], coord[2]), file=fc)
            print("", end="", file=fc)
            print(*atom_elems, sep=" ", file=fc)
            print("", end="", file=fc)
            print(*atom_numbers, sep=" ", file=fc)
            print("Selective Dynamics", file=fc)
            if coord_type == 'direct':
                print("Direct", file=fc)
            elif coord_type == 'cartesian':
                print("Cartesian", file=fc)
            for atom in atoms_ordered:
                if coord_type == 'direct':
                    coords = atom.dcoords
                elif coord_type == 'cartesian':
                    coords = atom.coords
                freeze = atom.freeze
                print(coords_format.format(coords[0], coords[1],
                                           coords[2], freeze[0],
                                           freeze[1], freeze[2]), file=fc)

    def molecule_fill(self, other):
        """ Fills the needed values to create a molecule object

        Args:
            other (obj:`molecule.Molecule` or subclasses): Molecule object to
                complete using the class attributes.

        Returns:
            other (obj:`molecule.Molecule` or subclasses): Modified molecule
        """
        # Setting the coords type
        elem_list = [list(itertools.repeat(elem, numb))
                     for elem, numb in zip(self.a_elem, self.a_numb)]
        elem_list = list(itertools.chain.from_iterable(elem_list))
        atom_params = zip(elem_list, self.freeze, self.coords)
        if self.type == 'cartesian':
            atoms = [molecule.Atom(elem, freeze, coords=coords)
                     for elem, freeze, coords in atom_params]
        elif self.type == 'direct':
            atoms = [molecule.Atom(elem, freeze, dcoords=coords)
                     for elem, freeze, coords in atom_params]
        other.cell_p_add(self.cell_p)
        other.atom_add_list(atoms)

        return other


class Xyz:
    def __init__(self, data_args):
        self.name = data_args.name
        self.elems = data_args.a_elem
        self.a_tot = data_args.a_tot
        self.coords = data_args.coords

    def convert_to_molecule(self):
        """Convert the Xyz object into a Molecule object.

        Returns:
            :obj`molecule.Molecule` object with the attributes of Xyz format

        Notes:
            Cell Parameters are missing in xyz format, then, a large cell will
            be created in order to supply the cell parameters to the molecules
            library.
            Cartesian coordinates will be used because of the lack of direct
            coordinates in xyz files.
            The freeze parameters are not specified in xyz format, that is why
            the freeze parameters will be always T
        """
        _molecule = molecule.Molecule(self.name)
        freeze = ('T', 'T', 'T')
        cell_p = np.array([20., 0., 0.],
                          [0., 20., 0.],
                          [0., 0., 20.])
        atom_lst = []
        for elem, coords in zip(self.elems, self.coords):
            atom_lst.append(molecule.Atom(elem, freeze, coords=coords))

        _molecule.atom_add_list(atom_lst)
        _molecule.cell_p_add(cell_p)
        return _molecule

class Image:
    def __init__(self, energy, forces, cell_p, elems,
                 freeze=None, coords=None, dcoords=None):
        self._molecule = None
        self.energy = energy
        self.forces = forces
        self._coords = coords
        self.dcoords = dcoords
        self.cell_p = cell_p
        self.elements = elems
        if freeze is None:
            self.freeze = [None] * len(self.elements)
        else:
            self.freeze = freeze

    @property
    def molecule(self):
        if self._molecule is None:
            elems, count = np.unique(self.elements, return_counts=True)
            name = ""
            for sing_elem, number in zip(elems, count):
                name += str(sing_elem) + str(number)
            new_mol = molecule.Molecule(name)
            new_cell_p = molecule.CellParameters(self.cell_p)
            if self.dcoords is None:
                np.dot(self.coords, new_cell_p.invert)
            for dcoords, coords, freeze, atom_elem in zip(self.dcoords,
                                                          self.coords,
                                                          self.freeze,
                                                          self.elements):
                new_atom = molecule.Atom(atom_elem, freeze, dcoords=dcoords)
                new_mol.atom_add(new_atom)
            new_mol.cell_p_add(new_cell_p)
            new_mol.coords_convert_update('cartesian')
            self._molecule = new_mol
        return self._molecule

    @property
    def coords(self):
        if self._coords is None:
            self._coords = np.dot(self.dcoords, self.cell_p)
        return self._coords


class CompleteRun:
    def __init__(self):
        self.images = []
        self.images_numb = 0

    def __len__(self):
        return self.images_numb

    def __getitem__(self, choice):
        return self.images[choice]

    def add_image(self, image):
        self.images.append(image)
        self.images_numb += 1

    def lesser_energy_image(self, energy='wo_entrp'):
        energy_lst = [image.energy[energy] for image in self.images]
        minimum = min(energy_lst)
        index = energy_lst.index(minimum)
        return self.images[index]
