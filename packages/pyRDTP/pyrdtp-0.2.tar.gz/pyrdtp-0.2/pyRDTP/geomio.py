"""This module provide the necessary tools to read and write different geometry
formats including the molecule object format of pyRDPT

Attributes:
    GENERIC_CELL (obj:`np.ndarray[3,3]`): Generic cell parameters used to
        generate cell parameters if they are not defined in the given format.
    FORMATS_DIC (dict): Dict containing the associated extensions to every
        class. These keys will be added during the class declaration.
"""
from abc import abstractmethod
from itertools import chain, repeat
import json
import os
import sys
import inspect
from shutil import move
from warnings import warn
import numpy as np
from pyRDTP.molecule import Atom, Bulk, Molecule

GENERIC_CELL = np.array([[20., 0., 0.],
                         [0., 20., 0.],
                         [0., 0., 20.]])


def convert(coord_obj, extension):
    """Convert the given obj:`AbsCoord` in another obj:`AbsCoord` of different
    format.

    Args:
        coord_obj (obj:`AbsCoord`): Coord object.
        extension (str): Extension of the format in wich the object will be
        converted

    Returns:
        obj:`AbsCoord` of the specified format.
    """
    universal = coord_obj.universal_convert()
    new_obj = FORMAT_DICT[extension]()
    new_obj.universal_read(universal)
    return new_obj


def file_read(filename, extension):
    """Read a file of a given format and return the associated obj:`AbsCoord`.

    Args:
        filename (str): Path of the file.
        extension (str): Format of the file.

    Returns:
        obj:`AbsCoord` with the information of the file.
    """
    new_obj = FORMAT_DICT[extension]()
    new_obj.file_read(filename)
    return new_obj


def file_write(coord_obj, filename, extension=None):
    """Write the given obj:`AbsCoord` to the given file

    Args:
        coord_obj (obj:`AbsCoord`): Coord object.
        filename (str): Path of the file.
        extension (str, optional): If specified, the format will be converted
            before write the file.
    """
    if extension:
        write_obj = convert(coord_obj, extension)
    else:
        write_obj = coord_obj

    write_obj.file_write(filename)


def file_to_mol(filename, extension, bulk=False):
    """Read the given filename and convert it to a obj:`Molecule`.

    Args:
        filename (str): Path of the file.
        extension (str): Format of the file.
        bulk (bool): If true Bulk object will be returned instead of Molecule
            object.

    Returns:
        obj:`Molecule` converted from the readed file.
    """
    coord_obj = file_read(filename, extension)
    univ_obj = coord_obj.universal_convert()
    mol_tmp = MolObj()
    mol_tmp.universal_read(univ_obj)
    return mol_tmp.write(bulk=bulk)


def mol_to_file(mol, filename, extension):
    """Convert the given molecule to abs coordinates and print in a file
    with the following extension.

    Args:
        mol(obj:pyRDTP.Molecule): Molecule object.
        filename (str): Path of the file.
        extension (str): Extension of the new file.
    """
    try:
        coord_obj = MolObj()
        coord_obj.read(mol)
    except AttributeError:
        coord_obj = CatObj()
        coord_obj.read(mol)
    universal_coord = coord_obj.universal_convert()
    new_obj = FORMAT_DICT[extension]()
    new_obj.universal_read(universal_coord)
    new_obj.file_write(filename)


def _pack_elements(elements_array):
    """From an array of elements, return the repeated number of elements and
    the number of times that each elements is repeated. If the elements are not
    ordered, the function will count the consecutive blocks of every element.

    Args:
        elements_array(iterable of str): Iterable object containing the
            elements strings.

    Returns:
        obj:`np.ndarray` of str containing each block of elements and
        obj:`np.ndarray` of int containing the number of times that each
        element is repeated. Both arrays have the same length.
    """
    count_lst = []
    elem_lst = []
    count = 1
    for element, element_next in zip(elements_array[:-1], elements_array[1:]):
        if element == element_next:
            count += 1
        else:
            count_lst.append(count)
            elem_lst.append(element)
            count = 1
    count_lst.append(count)
    elem_lst.append(elements_array[-1])
    return np.asarray(elem_lst), np.asarray(count_lst)


def _unpack_elements(elem_lst, count_lst):
    """From an iterable containing a list of elements and an iterable
    containing the number that each element is repeated, create an array of
    elements.

    Args:
        elem_lst(iterable of strings): Iterable containing the unique elements.
        count_lst(iterable of int): Iterable containing the number of
            repetitions of every element.

    Returns:
        obj:`np.ndarray` of str with all the generated elements.

    Notes:
        See _pack_elements for further information.
    """
    return np.asarray(list(chain.from_iterable(map(repeat, elem_lst,
                                                   count_lst))))


def _sort_coords(elements, coords, z_sort=False, elem_sort=False, freeze=None):
    """Sort coordinates depending on an element array and coordinates.

    Args:
        elements (iterable of str): Iterable containing the element array.
        coords (np.ndarray[n,3] of floats): Array containing the associated
            coordinates to every element.
        z_sort (bool, optional): If true, sort the elements by the z
            coordinate. Defaults to False.
        elem_sort (bool, optional): If true, alphabetically sort the elements
            and consequently the coords. Defaults to False.
        freeze (iterable of bool): If given, order and return a freeze array.
            Defaults to None.

    Returns:
        dict containing the following keys as obj:`np.ndarray`:
            elem_arr: Sorted element array.
            coords  : Sorted coords.
            a_elem  : Sorted unique elements.
            a_numb  : Sorted repetitions of every element.
            freeze  : Sorted freeze array.


    Notes:
        Element sort will be performed always before z sort.
        elements and coords must be of the same size.
    """
    if elem_sort:
        new_order = np.argsort(elements)
        new_elements = elements.copy()
        new_elements = new_elements[new_order]
        new_coords = coords.copy()
        new_coords = new_coords[new_order]
        if freeze is not None:
            new_freeze = freeze.copy()
            new_freeze = new_freeze[new_order]
    else:
        new_coords = coords.copy()
        new_elements = elements.copy()
        if freeze is not None:
            new_freeze = freeze.copy()

    if z_sort:
        atom_elem, atom_numb = _pack_elements(new_elements)
        order_arr = np.zeros((len(atom_numb), 2), dtype=int)
        order_arr[:, 1] = np.cumsum(atom_numb)
        order_arr[1:, 0] = order_arr[:-1, 1]
        for start, end in order_arr:
            indexes = np.argsort(new_coords[start:end, 2])
            new_coords[start:end] = new_coords[start:end][indexes]
            if freeze is not None:
                new_freeze[start:end] = new_freeze[start:end][indexes]

    return_dict = {'elem_arr': new_elements,
                   'coords': new_coords,
                   'a_elem': atom_elem,
                   'a_numb': atom_numb}
    if freeze is not None:
        return_dict['freeze'] = new_freeze
    return return_dict


class UniversalCoord:
    """Universaal coordinate class that will be used as a nexus between
    different coordinate systems.

    Attributes:
        name (str): Name of the geometry.
        n_atoms (int): Number of atoms of the geometry.
        elements (iterable of str): Iterable containing the elements of the
            geometry.
        coords (obj:`np.ndarray[n,3]` of floats): Array containing cartesian
            coordinates of the molecule.
        additional_inf (dict): Dictionary containing additional information
            that maybe will be used for different formats.
    """

    def __init__(self):
        self.name = None
        self._n_atoms = None
        self.elements = None
        self.coords = None
        self.additional_inf = {}

    @property
    def n_atoms(self):
        if self._n_atoms is None:
            return len(self.coords)
        else:
            return self._n_atoms

    @n_atoms.setter
    def n_atoms(self, other):
        self._n_atoms = other


class AbsCoord:
    """Parent class defining the needed functions for a coordinate format.

    Attributes:
        The attributes depends of the child class.

    Args:
        obj (str, obj:`UniversalCoord` or object, optional): If an object is
        given as input, __init__ will try to read and convert the given input
        into the format of the class. str will try to read a file,
        obj:`UniversalCoord` will trigger universal_read function and an object
        will trigger read function. If None value is given, __init__ will only
        create the object. Defaults to None

    Properties:
        extension (str): Extension associated with the class.
    """

    def __init__(self, obj=None):
        if isinstance(obj, str):
            self.file_read(obj)
        elif isinstance(obj, UniversalCoord):
            self.universal_read(obj)
        elif isinstance(obj, AbsCoord):
            _ = obj.universal_convert()
            self.universal_read(_)
        elif obj is None:
            pass
        else:
            self.read(obj)

    def __str__(self):
        return self.write()

    def file_read(self, filename):
        """Extract the content from a file and give it to read function.

        Args:
            filename (str): Path of the file.
        """
        with open(filename, 'r') as file_open:
            content = file_open.readlines()
        self.read(content)

    def file_write(self, filename, **kwargs):
        """Write the output of the write function into a given file.

        Args:
            filename (str): Path of the file.
            **kwargs: Options depending on the child class.
        """
        if os.path.isfile(filename):
            warn("Old " + filename + " found, moving the file to " + filename +
                 '.bak!')
            move(filename, filename + '.bak')

        with open(filename, 'w') as file_open:
            file_open.write(self.write(**kwargs))

    @abstractmethod
    def read(self, content):
        """Read a string and store the information in the object attributes

        Args:
            content (str): Content that will be parsed.
        """
        pass

    @abstractmethod
    def write(self, **kwargs):
        """Write an string in the associated format.

        Args:
            **kwargs: Options depending on the child class.

        Returns:
            str containing the information in the class file format.
        """
        pass

    @abstractmethod
    def universal_convert(self):
        """Create an obj:`UniversalCoord`, translate the attributes of the
        current class to the attributes of the new object and return the new
        object.

        Returns:
            obj:`UniversalCoord` containing the geometry information.
        """
        pass

    @abstractmethod
    def universal_read(self, universal):
        """Fill the attributes of this class with the information of an
        obj:`UniversalCoord` class.

        Args:
            universal (obj:`UniversalCoord): Object containing the information
                of a geometry.
        """
        pass


class VaspContcar(AbsCoord):
    """POSCAR/CONTCAR format class.

    Attributes:
        name (str): Name of the system.
        multiplier (float): Direct coords multiplier.
        cell_p (obj:`np.ndarray[3,3]`): Cell parameters of the given system.
        a_elem (obj:`np.ndarray[n]` of str): Unique elements of the system.
        a_numb (obj:`np.ndarray[n]` of int): Number of times that every element
            is repeated.
        coords (obj:`np.ndarray[n,3]` of floats): Array containing cartesian
            coordinates of the molecule.
        dcoords (obj:`np.ndarray[n,3]` of floats): Array containing direct
            coordinates of the molecule.
        freeze (obj:`np.ndarray[n,3]` of str): Array containing the freeze
            status of the coordinates.
    """

    extension = 'contcar'

    def __init__(self, obj=None):
        self.name = None
        self.multiplier = None
        self.cell_p = None
        self.a_elem = None
        self.a_numb = None
        self.n_atoms = None
        self.coords = None
        self.dcoords = None
        self.freeze = None
        super().__init__(obj)

    def read(self, content):
        content = [line.strip() for line in content]
        self.name = content[0]
        self.multiplier = float(content[1])
        self.cell_p = np.asarray([line.split() for line in content[2:5]],
                                 dtype=float)
        if (self.cell_p == 0).all():
            self.cell_p = GENERIC_CELL
        self.a_elem = tuple(content[5].split())
        self.a_numb = tuple((int(number) for number in content[6].split()))
        self.n_atoms = sum(self.a_numb)

        coord_indexes = [content.index(match) for match in content[1:] if
                         'configuration' in match]

        if coord_indexes:
            all_confs = [(start+1, end) for start, end in
                         zip(coord_indexes[:-1], coord_indexes[1:])]
            if 'Cartesian' in content[all_confs[0][0] - 1]:
                coord_type = 'cartesian'
            elif 'Direct' in content[all_confs[0][0] - 1]:
                coord_type = 'direct'
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

            finish_at = self.n_atoms + start_at
            all_confs = [(start_at, finish_at)]

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
            if coord_type == 'cartesian':
                self.coords = coords
                ainv = np.linalg.inv(self.cell_p)
                self.dcoords = np.dot(coords, ainv)
            elif coord_type == 'direct':
                self.dcoords = coords
                self.coords = np.dot(coords, self.cell_p) * self.multiplier
            self.freeze = np.asarray(freeze)

    def write(self, direct=True, elem_sort=False, z_sort=False):
        if direct:
            sel_coords = self.dcoords
            body_inf = 'Selective\nDirect\n'
        else:
            sel_coords = self.coords
            body_inf = 'Selective\nCartesian\n'

        if elem_sort or z_sort:
            _ = _unpack_elements(self.a_elem, self.a_numb)
            pact_dict = _sort_coords(_, sel_coords, elem_sort=elem_sort,
                                     z_sort=z_sort)
            a_numb = pact_dict['a_numb']
            a_elem = pact_dict['a_elem']
            sel_coords = pact_dict['coords']
        else:
            a_numb = self.a_numb
            a_elem = self.a_elem

        cell_p_tmp = " {: .16f} {: .16f} {: .16f}\n"
        coord_tmp = " {} {} {}  {} {} {}\n"
        header_str = "{}\n{:.2f}\n".format(self.name, self.multiplier)
        cell_p = cell_p_tmp * 3
        cell_p = cell_p.format(*self.cell_p.flatten())
        elem_inf = (' '.join(a_elem) + '\n' +
                    ' ' + ' '.join(map(str, a_numb)) + '\n')

        coord_format = np.char.mod('% .16f', sel_coords)
        merge = np.concatenate((coord_format, self.freeze), axis=1)
        body_coords = (coord_tmp * self.n_atoms).format(*merge.flatten())

        assemble = header_str + cell_p + elem_inf + body_inf + body_coords
        return assemble

    def universal_convert(self):
        universal = UniversalCoord()
        universal.name = self.name
        universal.n_atoms = self.n_atoms
        universal.elements = _unpack_elements(self.a_elem, self.a_numb)
        universal.elements = np.asarray(universal.elements)
        universal.coords = self.coords
        bool_freeze = self.freeze == ['T']
        if 1 > self.multiplier or 1 < self.multiplier:
            cell_p_tmp = self.cell_p * self.multiplier
        else:
            cell_p_tmp = self.cell_p
        universal.additional_inf = {'dcoords': self.dcoords,
                                    'freeze': bool_freeze,
                                    'cell_p': cell_p_tmp,
                                    'multiplier': self.multiplier}
        return universal

    def universal_read(self, universal):
        self.name = universal.name
        self.n_atoms = universal.n_atoms
        self.coords = universal.coords
        self.a_elem, self.a_numb = _pack_elements(universal.elements)

        if universal.additional_inf.get('multiplier') is not None:
            self.multiplier = universal.additional_inf.get('multiplier')
        else:
            self.multiplier = 1.

        if universal.additional_inf.get('cell_p') is not None:
            self.cell_p = universal.additional_inf.get('cell_p')
        else:
            self.cell_p = GENERIC_CELL

        if universal.additional_inf.get('dcoords') is not None:
            self.dcoords = universal.additional_inf.get('dcoords')
        else:
            self.dcoords = np.dot(self.coords, np.linalg.inv(self.cell_p))

        if universal.additional_inf.get('freeze') is not None:
            freeze = universal.additional_inf.get('freeze')
            str_freeze = np.ones(freeze.shape, dtype=str)
            str_freeze[freeze] = 'T'
            str_freeze[~freeze] = 'F'
            self.freeze = str_freeze
        else:
            self.freeze = np.asarray([['T', 'T', 'T']] * self.n_atoms)


class XYZ(AbsCoord):
    """POSCAR/CONTCAR format class.

    Attributes:
        name (str): Name of the system.
        elements (iterable of str): Iterable containing the elements of the
            geometry.
        n_atoms (int): Number of atoms of the geometry.
        coords (obj:`np.ndarray[n,3]` of floats): Array containing cartesian
            coordinates of the molecule.
    """

    extension = 'xyz'

    def __init__(self, obj=None):
        self.name = None
        self.elements = None
        self.n_atoms = None
        self.coords = None
        super().__init__(obj)

    def read(self, content):
        content = [line.strip() for line in content]
        self.n_atoms = int(content[0])

        if content[1]:
            self.name = content[1]
        else:
            self.name = 'unnamed'

        atoms_coords_raw = content[2:self.n_atoms+2]
        atoms_elements = []
        atoms_coords = []

        for line in atoms_coords_raw:
            line = line.split()
            atoms_elements.append(line[0])
            atoms_coords.append(line[1:4])

        self.elements = np.asarray(atoms_elements)
        self.coords = np.asarray(atoms_coords, dtype=float)

    def write(self):
        xyz_str = ''
        xyz_str += '{:d}\n'.format(self.n_atoms)
        xyz_str += '{:s}\n'.format(self.name)
        coords_lst = self.coords.tolist()
        for element, coords in zip(self.elements, coords_lst):
            xyz_str += '{:s}  {:.16f}  {:.16f}  {:.16f}\n'.format(element,
                                                                  *coords)
        return xyz_str

    def universal_convert(self):
        universal = UniversalCoord()
        universal.name = self.name
        universal.n_atoms = self.n_atoms
        universal.elements = self.elements
        universal.coords = self.coords
        return universal

    def universal_read(self, universal):
        self.name = universal.name
        self.n_atoms = universal.n_atoms
        self.elements = universal.elements
        self.coords = universal.coords


class MolObj(AbsCoord):
    """POSCAR/CONTCAR format class.

    Attributes:
        name (str): Name of the system.
        cell_p (obj:`np.ndarray[3,3]`): Cell parameters of the given system.
            is repeated.
        coords (obj:`np.ndarray[n,3]` of floats): Array containing cartesian
            coordinates of the molecule.
        dcoords (obj:`np.ndarray[n,3]` of floats): Array containing direct
            coordinates of the molecule.
        system_type (str): System type of the molecule.
        freeze (obj:`np.ndarray[n,3]` of bool): Array containing the freeze
            status of the coordinates.
    """

    extension = 'molobj'

    def __init__(self, obj=None):
        self.name = None
        self.cell_p = None
        self.elements = None
        self.n_atoms = None
        self.system_type = None
        self.coords = None
        self.dcoords = None
        self.freeze = None
        super().__init__(obj)

    def __str__(self):
        return None

    def file_read(self, filename):
        raise NotImplementedError

    def read(self, content):
        self.name = content.name
        self.cell_p = content.cell_p.direct
        self.elements = content.elem_array()
        self.n_atoms = content.atom_numb
        self.coords = content.coords_array('cartesian')
        self.dcoords = content.coords_array('direct')
        self.freeze = np.asarray(content.freeze_array())
        if isinstance(content, Molecule):
            self.system_type = 'molecule'
        elif isinstance(content, Bulk):
            self.system_type = 'bulk'

    def write(self, bulk=False):
        if bulk:
            mol_obj = Bulk(self.name)
        else:
            mol_obj = Molecule(self.name)

        atom_lst = []
        for index in range(self.n_atoms):
            new_atom = Atom(self.elements[index],
                            coords=self.coords[index],
                            freeze=self.freeze[index],
                            dcoords=self.dcoords[index])
            atom_lst.append(new_atom)
        mol_obj.cell_p_add(self.cell_p)
        mol_obj.atom_add_list(atom_lst)
        return mol_obj

    def universal_convert(self):
        universal = UniversalCoord()
        universal.name = self.name
        universal.n_atoms = self.n_atoms
        universal.elements = self.elements
        universal.coords = self.coords
        universal.additional_inf = {'cell_p': self.cell_p,
                                    'dcoords': self.dcoords,
                                    'freeze': self.freeze,
                                    'system_type': self.system_type}
        return universal

    def universal_read(self, universal):
        if universal.name:
            self.name = universal.name
        else:
            self.name = 'unnamed'
        self.n_atoms = universal.n_atoms
        self.elements = universal.elements
        self.coords = universal.coords
        cell_p_tmp = universal.additional_inf.get('cell_p')
        if cell_p_tmp is not None and not (cell_p_tmp == 0).all():
            self.cell_p = universal.additional_inf.get('cell_p')
        else:
            self.cell_p = GENERIC_CELL

        if universal.additional_inf.get('dcoords') is not None:
            self.dcoords = universal.additional_inf.get('dcoords')
        else:
            self.dcoords = np.dot(self.coords, np.linalg.inv(self.cell_p))

        if universal.additional_inf.get('freeze') is not None:
            self.freeze = universal.additional_inf.get('freeze')
        else:
            self.freeze = np.asarray([[True, True, True]] * self.n_atoms)

        if universal.additional_inf.get('system_type') is not None:
            self.system_type = universal.additional_inf.get('system_type')


class JsonMol(AbsCoord):
    """JSON file format

    Attributes:
        name (str): Name of the geometry.
        n_atoms (int): Number of atoms of the geometry.
        elements (iterable of str): Iterable containing the elements of the
            geometry.
        coords (obj:`np.ndarray[n,3]` of floats): Array containing cartesian
            coordinates of the molecule.
        additional_inf (dict): Dictionary containing additional information
            that maybe will be used for different formats.
    """

    extension = 'json'

    def __init__(self, obj=None):
        self.name = None
        self.n_atoms = None
        self.elements = None
        self.coords = None
        self.additional_inf = {}
        super().__init__(obj)

    def read(self, content):
        self.name = content['name']
        self.n_atoms = content['n_atoms']
        self.elements = content['elements']
        self.coords = content['coords']
        self.additional_inf = content['additional_inf']

    def write(self):
        json_string = json.dumps(self.__dict__, separators=(',', ':'),
                                 sort_keys=True, indent=4)
        return json_string

    def universal_convert(self):
        universal = UniversalCoord()
        universal.name = self.name
        universal.n_atoms = self.n_atoms
        universal.elements = np.asarray(self.elements)
        universal.coords = np.asarray(self.coords)
        for key, value in self.additional_inf.items():
            if isinstance(value, list):
                universal.additional_inf[key] = np.asarray(value)
            else:
                universal.additional_inf[key] = value
        return universal

    def universal_read(self, universal):
        self.name = universal.name
        self.n_atoms = universal.n_atoms
        self.elements = universal.elements.tolist()
        self.coords = universal.coords.tolist()
        for key, value in universal.additional_inf.items():
            if isinstance(value, np.ndarray):
                self.additional_inf[key] = value.tolist()
            else:
                self.additional_inf[key] = value


class CatObj(AbsCoord):
    def __init__(self, obj=None):
        self.name = None
        self.cell_p = None
        self.n_atoms = None
        self.molecules = []
        self.surface = None
        self.z_sort = False
        self.mol_join = False
        super().__init__(obj)

    def __str__(self):
        return None

    def read(self, content):
        self.name = content.name
        self.n_atoms = content.count_atoms()
        self.surface = MolObj()
        self.surface.read(content.surface)
        self.cell_p = content.surface.cell_p.direct
        for mol in content.molecules:
            mol_obj = MolObj()
            mol_obj.read(mol)
            self.molecules.append(mol_obj)

    def write(self):
        raise NotImplementedError

    def universal_convert(self):
        universal = UniversalCoord()
        universal.additional_inf['cell_p'] = self.cell_p
        universal.n_atoms = self.n_atoms

        if self.mol_join:
            tmp_inf = {}
            ord_elem = []
            checker = True
            mol_lst = [self.surface] + [mol for mol in self.molecules]
            for mol_obj in mol_lst:
                for index, element in enumerate(mol_obj.elements):
                    tmp_coords = mol_obj.coords[index]
                    tmp_freeze = mol_obj.freeze[index]
                    try:
                        tmp_coords = np.append(tmp_inf[element]['coords'],
                                               [tmp_coords], axis=0)
                        tmp_freeze = np.append(tmp_inf[element]['freeze'],
                                               [tmp_freeze], axis=0)
                        tmp_inf[element]['coords'] = tmp_coords
                        tmp_inf[element]['freeze'] = tmp_freeze
                    except KeyError:
                        ord_elem.append(element)
                        tmp_inf[element] = {'coords': np.asarray([tmp_coords]),
                                            'freeze': np.asarray([tmp_freeze])}
                if not self.z_sort:
                    continue
                if self.z_sort and checker:
                    for element in ord_elem:
                        tmp_elem = [element] * len(tmp_inf[element]['coords'])
                        tmp_elem = np.asarray(tmp_elem)
                        tmp_dict = _sort_coords(tmp_elem,
                                                tmp_inf[element]['coords'],
                                                z_sort = True, elem_sort = False,
                                                freeze=tmp_inf[element]['freeze'])
                        tmp_inf[element]['coords'] = tmp_dict['coords']
                        tmp_inf[element]['freeze'] = tmp_dict['freeze']
                        checker = False

            universal.elements = np.empty([self.n_atoms], dtype='<U4')
            universal.coords = np.zeros([self.n_atoms, 3])
            universal.additional_inf['freeze'] = np.zeros([self.n_atoms, 3],
                                                          dtype=bool)
            index = 0
            for element in ord_elem:
                for coord, freeze in zip(tmp_inf[element]['coords'],
                                         tmp_inf[element]['freeze']):
                    universal.elements[index] = element
                    universal.coords[index, :] = coord
                    universal.additional_inf['freeze'][index, :] = freeze
                    index += 1
#                tmp_elem = np.asarray([element] *
#                                      len(tmp_inf[element]['coords']))
#
#                universal.elements = np.append(universal.elements, tmp_elem, axis=0)
#                print(universal.coords.shape)
#                print(tmp_inf[element]['coords'].shape)
#                universal.coords = np.append(universal.coords,
#                                             tmp_inf[element]['coords'], axis=0)
#                universal.additional_inf['freeze'] = np.append(universal.coords, tmp_inf[element]['freeze'], axis=0

        else:
            universal.elements = self.surface.elements
            universal.coords = self.surface.coords
            universal.additional_inf['freeze'] = self.surface.freeze
            for mol in self.molecules:
                universal.elements = np.append(universal.elements,
                                               mol.elements)
                universal.coords = np.append(universal.coords, mol.coords,
                                             axis=0)
                universal.additional_inf['freeze'] = np.append(universal.additional_inf['freeze'],
                                                               mol.freeze, axis=0)
            if self.z_sort:
                tmp_dict = _sort_coords(universal.elements,
                                        universal.coords, z_sort = True,
                                        elem_sort = False,
                                        freeze=universal.additional_inf['freeze'])
                universal.elements = tmp_dict['elem_arr']
                universal.coords = tmp_dict['coords']
                universal.additional_inf['freeze'] = tmp_dict['freeze']
        return universal

    def universal_read(self, universal):
        raise NotImplementedError


class ASEAtoms(AbsCoord):

    extension = 'ase'

    def __init__(self, obj=None):
        self.name = None
        self.cell_p = None
        self.elements = None
        self.coords = None
        super().__init__(obj)

    def read(self, obj):
        self.name = obj.get_chemical_formula()
        self.cell_p = obj.cell.array
        self.elements = obj.get_chemical_symbols()
        self.coords = obj.get_positions()

    def file_read(self, filename):
        raise NotImplementedError

    def write(self):
        from ase import Atoms
        ase_atoms = Atoms(self.elements,
                          positions=self.coords,
                          cell=self.cell_p,
                          pbc=[1., 1., 1])
        return ase_atoms

    def universal_convert(self):
        universal = UniversalCoord()
        universal.name = self.name
        universal.elements = self.elements
        universal.coords = self.coords
        universal.additional_inf = {'cell_p': self.cell_p}
        return universal

    def universal_read(self, universal):
        if universal.name:
            self.name = universal.name
        else:
            self.name = 'unnamed'
        self.elements = universal.elements
        self.coords = universal.coords
        if universal.additional_inf.get('cell_p') is not None:
            self.cell_p = universal.additional_inf.get('cell_p')
        else:
            self.cell_p = GENERIC_CELL


FORMAT_DICT = inspect.getmembers(sys.modules[__name__], inspect.isclass)
FORMAT_DICT = {form[1].extension: form[1] for form in FORMAT_DICT if
               hasattr(form[1], 'extension')}
