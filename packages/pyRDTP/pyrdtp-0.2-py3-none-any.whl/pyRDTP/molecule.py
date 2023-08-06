"""Atoms and Molecules module.

This module contains a series of tools and functions in order to create and
handle molecules in a different ways

Attributes:
    DIM_DICT (:obj`dict`): translation dict for cartesian coordinate system
"""
import warnings
from itertools import product
from collections import OrderedDict, namedtuple
import numpy as np
from scipy.spatial import Voronoi
from pyRDTP import geometry
from pyRDTP.data import radius


DIM_DICT = {'x': 0, 'y': 1, 'z': 2}  # Axis translation Dic

class Atom:
    """Atom Class type, defines a single atom.

    Note:
        Coordinates are optional, but at least one type of coordinates is
        necessary in order to execute some methods.

    Args:
        element (str): Element of the atom.
        freeze (tuple): Allowed movement of the dimensions.
        coords (tuple of floats, optional): Cartesian position coordinates.
        dcoords (tuple of floats, optional): Direct position coordinates.

    Attributes:
        element (str): Element of the atom object.
        freeze (tuple of 3 bool): Allowed movement of the dimensions.
        coords (:obj`np.ndarray` of floats, optional): Cartesian coordinates.
        dcoords (:obj`np.ndarray` of floats, optional): Direct coordinates.
    """
#    __slots__ = ('element', 'freeze', 'coords', 'dcoords', 'grid',
#                 'connections', 'index')

    def __init__(self, element, coords=None, freeze=[True, True, True],
                 dcoords=None):
        self.element = element

        for item in (coords, dcoords):
            try:
                item = np.asarray(item, dtype=float)
            except TypeError:
                if item is not None:
                    item = None

        self.coords = coords
        self.dcoords = dcoords
        if not isinstance(freeze, list):
            new_freeze = list(freeze).copy()
        else:
            new_freeze = freeze.copy()
        for index, item in enumerate(new_freeze):
            if isinstance(item, str):
                if item in ['T', 'True', 'true', 'TRUE']:
                    new_freeze[index] = True
                elif item in ['F', 'False', 'false', 'FALSE']:
                    new_freeze[index] = False
        self.freeze = list(new_freeze)
        self.connections = []
        self.grid = {}
        self.grid['x'] = None
        self.grid['y'] = None
        self.grid['z'] = None
        self.index = None

#    def __eq__(self, other):
#        _validate = self.coords == other.coords and \
#                    self.freeze == other.freeze and \
#                    self.element == other.element
#
#        return _validate

    def __str__(self):
        coords = " ".join(format(coord, "10.8f") for coord in self.coords)
        freeze = " ".join(str(self.freeze))
        string = "{0} {1} {2}"
        printable = string.format(self.element, coords, freeze)
        return printable

    def __repr__(self):
        string = "({0}) {1} |{2}|"
        freeze = "| |".join(map(str, self.freeze))
        printable = string.format(self.element, self.coords, freeze)
        return printable

    def copy(self):
        """Creates a copy of the atom that calls the method.

        Returns:
            (:obj`atom`) a copy of the original atom.
        """

        new_element = self.element
        new_freeze = self.freeze
        if isinstance(self.coords, np.ndarray):
            new_coords = self.coords.copy()
        if isinstance(self.dcoords, np.ndarray):
            new_dcoords = self.dcoords.copy()
        new_atom = Atom(new_element, coords=new_coords, freeze=new_freeze,
                        dcoords=new_dcoords)
        return new_atom

    def move_to(self, coords_new, system='cartesian'):
        """Move an atom to the given cartesian or direct coords.

        Args:
            coords_new (tuple of floats or ints): New coords of the atom.
            system (str, optional): Coordinate system of the new coords.
                Defaults to 'cartesian'.

        Examples:
            >>> atom.move_to((3.,2.,4.), system='direct')
        """
        if not all(isinstance(coord, (float, int)) for coord in coords_new):
            return TypeError('coords_new: Must contain only floats or ints')
        if len(coords_new) != 3:
            return ArithmeticError('coords_new: Must contain only 3 values')

        coords_array = np.asarray(coords_new, dtype=float)

        if system == 'cartesian':
            self.coords = coords_array
        elif system == 'direct':
            self.dcoords = coords_array
        else:
            return ValueError('system argument must be cartesian or direct')

        return None

    def connection_add(self, other_atom):
        """Bond two atoms

        Args:
            other_atom (:obj`Atom`): Atom that will be bonded.
        """
        if other_atom not in self.connections:
            self.connections.append(other_atom)
        if self not in other_atom.connections:
            other_atom.connections.append(self)

    def connection_remove(self, other_atom):
        """Remove a bond between two atoms.

        Args:
            other_atom (:obj`Atom`): Atom that will be unbonded.
        """
        if other_atom in self.connections:
            self.connections.remove(other_atom)
        if self in other_atom.connections:
            other_atom.connections.remove(self)

    def connection_remove_all(self):
        """Remove all the connections of this atom.
        """
        for other_atom in self.connections:
            self.connection_remove(other_atom)


class Molecule:
    """Molecule class. Container of atoms.

    Args:
        name (str): Name of the molecule.

    Attributes:
        name (str): Name of the molecule.
        atoms (list of :obj`atoms`): Atoms of the molecule.
        cell_p (:obj`CellParameters`): Object containing the cell parameters
        atom_numb (int): Number of atoms that contains the molecule.
        formula (str): Unordered formula of the molecule.
    """
    def __init__(self, name):
        self.name = name
        self.atoms = []
        self.cell_p = None
        self.atom_numb = 0
        self.pairs = None
        self._elems_numb = None
        self._elems = None
        self._elems_array = None

    def __add__(self, other):
        if isinstance(other, Atom):
            self.atom_add(other)
            return self
        if isinstance(other, list):
            self.atom_add_list(other)
            return self

        return NotImplemented

    def __eq__(self, other):
        try:
            test_1 = np.all(self.coords_array() == other.coords_array())
            test_2 = np.all(self.elem_array() == other.elem_array())
            test_3 = np.all(self.cell_p == other.cell_p)
            return all((test_1, test_2, test_3))
        except ValueError:
            return False

    def __in__(self, other):
        return other in self.atoms

    def __str__(self):
        repr_str = '{} ({}) [{}]'.format(self.name,
                                         self.formula, str(self.atom_numb))
        return repr_str

    def __repr__(self):
        return str(self)

    def __len__(self, choice=None):
        return len(self.atoms)

    def __getitem__(self, choice):
        if isinstance(choice, int):
            return self.atoms[choice]
        elif isinstance(choice, str):
            val = [atom for atom in self.atoms if atom.element == choice]
        elif isinstance(choice, (list, tuple)):
            val = []
            for item in choice:
                if isinstance(item, int):
                    val.append(self.atoms[item])
                if isinstance(item, str):
                    val += [atom for atom in self.atoms if
                            atom.element == item]
        else:
            try:
                val = self.atoms[choice]
            except TypeError:
                raise TypeError
        val = self.select(val, mol_obj = True)
        return val

    def __iter__(self):
        return iter(self.atoms)

    def __abs__(self):
        return self.find_centroid()

    def atom_add(self, atom):
        """Add a single atom object

        Args:
            atom (:obj`Atom`): Atom to add to the molecule.

        Note:
            If Cell Parameters are setted, this function will try to convert
            the atom to the missing coordinate system.
        """
        self.atoms.append(atom)
        self.atom_numb += 1

        if atom.dcoords is None and self.cell_p is not None:
            atom.dcoords = np.dot(atom.coords, self.cell_p.inverse)
        elif atom.coords is None and self.cell_p is not None:
            atom.coords = np.dot(atom.dcoords, self.cell_p.direct)

        if self._elems is not None:
            if atom.element in self._elems:
                self._elems_numb[atom.element] += 1
            else:
                self._elems.add(atom.element)
                self._elems_numb[atom.element] = 1

    @property
    def coords(self):
        return self.coords_array('cartesian')

    @coords.setter
    def coords(self, other):
        self.coords_update(other, 'cartesian')
        self.coords_convert_update('direct')

    @property
    def dcoords(self):
        return self.coords_array('direct')

    @dcoords.setter
    def dcoords(self, other):
        self.coords_update(other, 'direct')
        self.coords_convert_update('cartesian')

    @property
    def centroid(self):
        return self.find_centroid()

    @centroid.setter
    def centroid(self, other):
        new_centroid = np.asarray(other)
        self.move_to(new_centroid, system='cartesian', origin='centroid')

    @property
    def plane(self):
        return self.find_plane(system='cartesian')

    @plane.setter
    def plane(self, other):
        self.align_to_plane(other)


    def atom_add_list(self, atom_list):
        """Add a list of atoms to the molecule object.

        Args:
            atom_list (list of :obj`atoms`): A list containing all the
                atoms that will be added to the molecule.
        """
        for _atom in atom_list:
            self.atom_add(_atom)

    def atom_remove(self, atom):
        """Removes the selected atom from the molecules.

        Args:
            atom (:obj`Atom`): Atom to remove.
        """
        if isinstance(atom, int):
            atom = self.atoms[atom]
        self.atoms.remove(atom)
        self.atom_numb -= 1
        for conn in atom.connections:
            conn.connections.remove(atom)
        if self._elems_numb is not None:
            self._elems_numb[atom.element] -= 1
            if self._elems_numb[atom.element] == 0:
                del self._elems_numb[atom.element]
                if self._elems is not None:
                    self._elems.remove(atom.element)

    def atom_remove_list(self, list):
        """Remove the atoms on a list.

        Args:

            list of :obj:`Atom`: List with the atoms that will be removed.
        """
        new_list = []
        for item in list:
            if isinstance(item, int):
                new_list.append(self.atoms[item])
            else:
                new_list.append(item)
        for atom in new_list:
            self.atom_remove(atom)


    def atom_remove_by_element(self, element):
        """Removes from the current molecule all the atoms of the given element

        Args:
            element (str): Element of the atoms to remove
        """
        trash = []
        for atom in self.atoms:
            if atom.element == element:
                trash.append(atom)
        for atom in trash:
            self.atom_remove(atom)

    def atom_sort(self):
        """Sort the atoms of the molecule using the element in alphabetical
        order
        """
        self.atoms.sort(key=lambda atom: atom.element, reverse=False)

    def atom_element_filter(self, element, option='atom', invert=False):
        """Return a list containing the atoms or the atom index of all the
        atoms of a given element

        Args:
            element (str, or list of str): Element that will be filtered.
            option (str, option): 'atom' or 'index'. If 'atom', returns a list
                filled with 'Atom' objects. If 'index' then the method will
                return the index of the matching atoms in the molecule
            invert(bool, optional): Return the atoms that do not match with
                the given elements instead of the ones that match.

        Returns:
            list of `obj:Atom` or int containing the reference to the atoms
            with the given element.
        """
        if isinstance(element, str):
            element = [element]

        if option == 'atom':
            if invert:
                atom_lst = [atom for atom in self.atoms
                            if atom.element not in element]
            else:
                atom_lst = [atom for atom in self.atoms
                            if atom.element in element]
        elif option == 'index':
            if invert:
                atom_lst = [self.atoms.index(atom) for atom in self.atoms
                            if atom.element not in element]
            else:
                atom_lst = [self.atoms.index(atom) for atom in self.atoms
                            if atom.element in element]
        else:
            raise NotImplementedError
        return atom_lst

    def atom_obtain_lowest(self, dimension='z', add_inf=False, highest=False):
        """Return the lowest atom of the molecule. If coords is True, a tuple
        containing the coords and direct coords of the atom will be returned
        instead.

        Args:
            dimension (str, optional): 'x', 'y' or 'z'. Dimension in which
                search for the lowest atom. Defaults to 'z'.
            coords (bool, optional): If True a tuple containing the atom,
                index, coords and direct coords will be returned instead of the
                atom object.
            highest (bool, optional): If True, the highest atom will be
                returned instead of the lowest.

        Returns:
            If coords is False, the lowest obj:`Atom` in the specified
            dimension will be returned. If coords is True a tuple containing
            the atom, index, cartesian and direct coords will be returned.
        """
        dim_numb = DIM_DICT[dimension]
        coords = self.coords_array('cartesian')
        if highest:
            minimum_index = np.argmax(coords[:, dim_numb])
        else:
            minimum_index = np.argmin(coords[:, dim_numb])
        atom = self.atoms[minimum_index]
        if add_inf:
            Coordinates = namedtuple('Coords', 'atom index cartesian direct')
            return Coordinates(atom, minimum_index, atom.coords, atom.dcoords)

        return atom

    def align(self, mol_at, vector=None, atoms=None):
        """Align the current molecule using two atoms of the molecule and a
        vector or two atoms from another molecule.

        Args:
            mol_at (list of int or obj:`Atoms`): If the value is an int the
                atom index will be used, if the value is an obj:`Atom` then
                this atom will be used.
            vector (list, tuple or np.ndarray): Vector that will be used to
                align the molecule.
            atoms (list of obj:`Atoms`): Atoms that will be used to calculate
                the vector that will be used to align the molecule.
        """
        atom_pair = []
        for item in mol_at:
            if isinstance(item, int):
                atom_pair.append(self.atoms[item])
            elif isinstance(item, Atom):
                atom_pair.append(item)
            else:
                raise NotImplementedError("""A list containing two integers
                                          or two atoms is needed in order
                                          to perform the the alignment!""")

        if len(atom_pair) > 2:
            warnings.warn("""More than 2 atoms used to generate the vector,
                          only the first and the second will be used!""")
        elif len(atom_pair) < 2:
            raise NotImplementedError("""Two atoms are needed to align the
                                      molecule""")

        if not vector:
            if not atoms:
                raise TypeError("""A vector or two atoms are needed to perform
                                the alignment!""")

            vector = atoms[1].coords - atoms[0].coords

        own_vector = atom_pair[1].coords - atom_pair[0].coords
        cosine = np.dot(own_vector / np.linalg.norm(own_vector),
                        vector / np.linalg.norm(vector))
        angle = np.arccos(cosine)

        rot_mat = geometry.rotation_matrix(own_vector, angle)
        self.rotate(matrix=rot_mat, origin=atom_pair[0].coords)

    def align_to_plane(self, plane_norm):
        """Rotate the molecule to align its plane with the given one. For more
        information about the plane calculation see the find_plane() function.

        Args:
            plane_norm (vector-like of dimension 3): Norm of the plane.
        """
        mol_plane = self.find_plane()
        plane_norm_tmp = np.asarray(plane_norm)
        rot_axis = np.cross(plane_norm_tmp, mol_plane)
        rot_angle = geometry.angle_between(plane_norm_tmp, mol_plane)
        rot_mat = geometry.rotation_matrix(rot_axis, rot_angle)
        self.rotate(matrix=rot_mat)

    def cell_p_add(self, cell_p):
        """Add a CellParameters object to the molecule.
            It is needed in order to perform coordinate conversions.

        Args:
            cell_p (:obj`CellParameters`): Cell parameters of the molecule.

        """
        checker = False
        if self.cell_p is not None:
            checker = True

        param = CellParameters(cell_p)
        self.cell_p = param

        if checker:
            self.coords_convert_update('direct')

    def connection_clear(self):
        """Clear all the bonds between all the atoms of the molecule.
        """
        for atom in self.atoms:
            atom.connection_remove_all()

    def coords_array(self, system='cartesian'):
        """Return a numpy array depending of the system value

        Args:
            system (str, optional): coordinate system, must be
                direct or cartesian. Defaults to 'cartesian'.

        Returns:
            array_out (:obj`np.ndarray`): Array containing the coordinates of
                all atoms in the given coordinate system.
        """
        if system == 'cartesian':
            array_out = np.vstack(tuple(atom.coords for atom in self.atoms))
        elif system == 'direct':
            array_out = np.vstack(tuple(atom.dcoords for atom in self.atoms))
        return array_out

    def coords_convert(self, convert_to):
        """Return a np in with the coordinates of the specified system

        Args:
            contert_to (str): Coordinate system wanted. Value must be 'direct'
                or 'cartesian'.

        Returns:
            _coords (:obj`np.ndarray`): Array containing the coordinates in the
                new coordinate system, converted from the other.
        """
        if convert_to == 'cartesian':
            _coords = self.coords_array('direct').dot(self.cell_p.direct)
            return _coords
        if convert_to == 'direct':
            _coords = self.coords_array('cartesian').dot(self.cell_p.inverse)
            return _coords

        raise ValueError('system argument must be cartesian or direct')

    def coords_convert_update(self, convert_to):
        """Convert the coordinates into the given system and
        update the coordinates of the atoms of the molecule

        Args:
            convert_to (str): Coordinate system to update. Value must be
                'direct' or 'cartesian'.
        """
        array_converted = self.coords_convert(convert_to)
        self.coords_update(array_converted, convert_to)

    def coords_update(self, array, system):
        """Update direct/cartesian coords using a new array

        Args:
            array (:obj`np.ndarray`): Array containing the new positions.
            system (str, optional): coordinate system, must be direct or
                cartesian.
        """

        _atom_list = array.tolist()
        if system == 'cartesian':
            point_to = 'coords'
        elif system == 'direct':
            point_to = 'dcoords'
        else:
            raise ValueError('System argument must be cartesian or direct')

        for position, _atom in enumerate(self):
            setattr(_atom, point_to, np.asarray(_atom_list[position]))

    def copy(self):
        """Generates a copy of the current molecule.

        Returns:
            :obj`Molecule` copy of the molecule
        """
        atoms_copy = [atom.copy() for atom in self.atoms]
        cell_p_copy = self.cell_p.copy()

        connect_lst = []
        for atom in self.atoms:
            connect_lst.append([self.atoms.index(cone) for cone in
                                atom.connections])

        molecule_copy = Molecule(self.name)
        molecule_copy.atom_add_list(atoms_copy)
        molecule_copy.cell_p = cell_p_copy

        for atom, connects in zip(molecule_copy.atoms, connect_lst):
            atom.connections = [molecule_copy[index] for index in connects]

        return molecule_copy

    def dcoords_correct(self):
        """Correct the direct coords coordinates to be in the center of the
        box"""
        for atom in self.atoms:
            atom.dcoords[atom.dcoords < 0.] += 1
            atom.dcoords[atom.dcoords > 1.] -= 1

    def distance(self, atom_1, atom_2,
                 system='cartesian', minimum=False, obj=False):
        """Calculates the distance between two atoms of the molecule.

        Args:
            atom_1 (int): Index of the first atom of the molecule.
            atom_2 (int): Index of the second atom of the molecule.
            system (str, optional): 'cartesian' or 'direct'. Defaults to
                'cartesian'.
            minimum (bool, optional): Uses PBC to compute the minimum distance
                between the two atoms. Defaults to False.
            obj (bool, optiona): Use atom object instead atom indexes. Defaults
                to False.
        """
        if not obj:
            atom_1 = self.atoms[atom_1]
            atom_2 = self.atoms[atom_2]

        if system == 'cartesian' and not minimum:
            vector = atom_1.coords - atom_2.coords
        else:
            vector = atom_1.dcoords - atom_2.dcoords
            if minimum:
                for index, axis in enumerate(vector):
                    if axis >= 0.5:
                        vector[index] -= 1.
                    elif axis <= -0.5:
                        vector[index] += 1.
            if system == 'cartesian':
                vector = np.dot(vector, self.cell_p.direct)
        return np.linalg.norm(vector)

    def coordination_analysis(self, comp_dist=False):
        """Returns a dictionary containing the atom elements and the
        coordination values for every element.

        Args:
            comp_dist (bool, optional): If True, the voronoi method will be
                used to compute the bonds before the bond analysis.

        Returns:
            dict containing the coordination number of every element
        """
        if comp_dist:
            self.connectivity_search_voronoi()
        coord_elem_dict = {}
        for atom in self.atoms:
            if atom.element not in coord_elem_dict:
                coord_elem_dict[atom.element] = []
            coord_elem_dict[atom.elemen].append(len(atom.connections))
        return coord_elem_dict

    def elem_inf(self, opt='ordered'):
        """Returns a dictionary containing the number of atoms with every
        element of the molecule. The dict is sorted by element apparence.

        Args: opt(str, optional): 'ordered' or 'disordered'. If ordered,
            an ordered dict will be returned. If disordered, a normal
            dict will be returned.

        Returns:
            mol_dict (dict): Keys are the element and values are the
                number of aoms with the element that the molecule contains.
        """
        elem_lst = [atom.element for atom in self.atoms]
        elem_uniq = [elem for numb, elem in enumerate(elem_lst)
                     if elem_lst.index(elem) == numb]
        elem_count = []
        for elem in elem_uniq:
            elem_count.append(elem_lst.count(elem))
        if opt == 'ordered':
            mol_dic = OrderedDict(zip(elem_uniq, elem_count))
        elif opt == 'disordered':
            mol_dic = dict(zip(elem_uniq, elem_count))
        return mol_dic

    def elem_array(self):
        """Return a numpy array containing the elements of the current atoms.

        Returns:
            np.ndarray containing a with all the elements of the atom.
        """
        array = np.asarray([atom.element for atom in self.atoms])
        self._elems_array = array
        return array

    @property
    def elements_number(self):
        """Return a disordered dict containing the elements and the numbers
        of atom per element.

        Returns:
            dict with the elements as keys and the number of atoms of every
            element.
        """
        if self._elems_numb is None:
            self._elems_numb = self.elem_inf(opt='disordered')
        return self._elems_numb

    @property
    def elements_list(self):
        """Return a numpy array containing the elements of every atoms.

        Returns:
            numpy.ndsarray containing a list with the elements of the atoms.
        """
        if self._elems_array is None:
            self._elems_array = self.elem_array()
        return self._elems_array

    @property
    def elements(self):
        """Return a set containing the diferent elements of the molecule.

        Returns:
            set containing the unique elements of the molecule.
        """
        if self._elems is None:
            self._elems = set(self.elem_inf(opt='disordered').keys())
        return self._elems

    def find_centroid(self, system='cartesian'):
        """Find the centroid of the molecule object.

        Args:
            system (str, optional): Coordinate system of the centroid, must be
                'direct' or 'cartesian'. Defaults to cartesian.

        Returns:
            centroid (:obj`np.ndarray` 3x1): The point of the centroid in
                the given coordinates.
        """
        centroid = np.zeros(3, dtype=float)
        for atom in self:
            if system == 'cartesian':
                centroid = [xx + yy for xx, yy in zip(atom.coords, centroid)]
            elif system == 'direct':
                centroid = [xx + yy for xx, yy in zip(atom.dcoords, centroid)]
            else:
                return ValueError('system must be cartesian or direct')
        centroid = np.asarray([xx/len(self) for xx in centroid], dtype=float)
        return centroid

    def find_lower_atom(self, dimension='z'):
        """Returns the lower atom in the given dimension

        Args:
            dimension (str, optional): 'x', 'y' or 'z'. Dimension in which
                find the lowest atom. Defaults to 'z'.
        """
        coords_array = self.coords_array(system='direct')
        index = np.argmin(coords_array[:, DIM_DICT[dimension]])
        return self.atoms[index]

    def find_upper_atom(self, dimension='z'):
        """Returns the lower atom in the given dimension

        Args:
            dimension (str, optional): 'x', 'y' or 'z'. Dimension in which
                find the lowest atom. Defaults to 'z'.
        """
        coords_array = self.coords_array(system='direct')
        index = np.argmax(coords_array[:, DIM_DICT[dimension]])
        return self.atoms[index]

    def find_plane(self, system='cartesian'):
        """Get the norm of the plane that adjust better to all the atoms of
        the molecule.

        Args:
            system (str, optional): 'cartesian' or 'direct'. Defines the
                coordinates system in which the norm of the plane will be
                returned. Defaults to cartesian.

        Returns:
            obj:`np.ndarray` of dtype float and dimension (3) with the norm of
            the adjusted plane.
        """
        _, norm = geometry.plane_fit(self.coords_array(system=system))
        return norm

    @property
    def formula(self):
        """Returns a string containing the chemical formula of the molecule
        without a specific order.

        Returns:
            str containing the unordered formula of the molecule.
        """
        formula = ''
        for element, number in self.elements_number.items():
            formula += element + str(number)
        return formula

    def freeze_array(self):
        """Returns the current freeze status of the atoms.

            Returns:
                freeze_tuple (:obj`tuple` of strings): Tuple containing all the
                    freeze tuples.
        """
        freeze_tuple = tuple([atom.freeze for atom in self.atoms])
        return freeze_tuple

    def invert(self):
        """Apply the invert operation symmetry to the molecules object
        """

        centroid = self.find_centroid(system='cartesian')
        coords = self.coords_array(system='cartesian')
        coords -= centroid
        coords = np.negative(coords)
        coords += centroid
        self.coords_update(coords, 'cartesian')
        self.coords_convert_update('direct')

    def atom_change_mov_all(self, option):
        """Freeze all atoms of the current molecule.

        Args:
            option (str): 'freeze' or 'release'.
        """
        if option == 'freeze':
            new_mov = tuple([False] * 3)
        elif option == 'release':
            new_mov = tuple([True] * 3)
        else:
            raise NotImplementedError

        for atom in self.atoms:
            atom.freeze = new_mov

    def atom_change_element_all(self, element_old, element_new):
        """Search for all the atoms with a given element and substitute all
        these atoms with another element.

        Args:
            element_old (str): Element to substitute. If this argument takes
                "all" as a value, it will perform the element substitution
                for all atoms.
            element_new (str): New element of the selected atoms.
        """
        for atom in self.atoms:
            if element_old in [atom.element, 'all']:
                atom.element = element_new

    def atom_index(self):
        """Index all the atoms of the molecules"""

        for index, atom in enumerate(self.atoms):
            atom.index = index

    def move_to(self, coords_new, system='cartesian', origin='centroid',
                lock=None):
        """Moves the molecule object to the given point, using the centroid
           as reference.

        Args:
            coords_new (:obj`tuple` of floats): New x, y and z positions
                of the centroid.
            system (str): Coords system of the given position. Must be
                'cartesian' or direct'.
            origin (str or tuple 3, option): The origin point of the move
                vector. Defaults to 'centroid'.
            lock (list of str, opt): Lock the given coordinates during the
                movement. Defaults to an empty list.

        Examples:
            >>> molecule.move_to((3.,1.,2.), origin=(3.,2.,0.))
        """
        if not all(isinstance(coord, (float, int)) for coord in coords_new):
            return TypeError('coords_new: Must contain only floats or ints')
        if len(coords_new) != 3:
            return ArithmeticError('coords_new: Must contain only 3 values')

        coords_array = np.asarray(coords_new, dtype=float)
        if isinstance(origin, str):
            if origin == 'centroid':
                origin_point = self.find_centroid(system)
        else:
            origin_point = np.asarray(origin)

        move_vector = coords_array - origin_point
        coords_old = self.coords_array(system)

        if lock is not None:
            for dimension in lock:
                move_vector[DIM_DICT[dimension]] = 0

        coords_new = coords_old + move_vector
        self.coords_update(coords_new, system)

        if system == 'cartesian':
            self.coords_convert_update('direct')
        elif system == 'direct':
            self.coords_convert_update('cartesian')
        else:
            return ValueError('system argument must be cartesian or direct')

        return None

    def move_to_center(self):
        """Moves the molecule to 0,0,0 in cartesian coordinates.
        """
        self.move_to((0, 0, 0), system='cartesian', origin='centroid')

    def move_to_box_center(self):
        """Moves the molecule to the center of the direct coordinates,
        0.5, 0.5, 0.5."""
        box_center = np.asarray([.5] * 3, dtype=float)
        box_center = box_center.dot(self.cell_p.direct)
        self.move_to(box_center, system='cartesian', origin='centroid')

    def move_vector(self, mov_vec, system='cartesian'):
        """Apply the given movement vector to the molecule.

        Args:
            mov_vec (lst, tuple or array of size 3): Vector in which the
                molecule atom will be moved.
            system (str, optional): 'cartesian' or 'direct'. Coordinate system
                of the vector. Defaults to 'cartesian'.
        """
        mov_vec = np.asarray(mov_vec, dtype=float)
        coords = self.coords_array(system)
        new_coords = coords + mov_vec
        self.coords_update(new_coords, system=system)
        if system == 'cartesian':
            self.coords_convert_update('direct')
        elif system == 'direct':
            self.coords_convert_update('cartesian')

    def repair(self):
        """Try to repair the molecule in direct coordinates.
        WARNING: Only should be used with molecules smaller than the half
                 of the cell.
        """
        for dimension in range(0, 3):
            val_max = max([atom.dcoords[dimension] for atom in self.atoms])
            for atom in self.atoms:
                if abs(atom.dcoords[dimension] - val_max) >= 0.5:
                    atom.dcoords[dimension] += 1.
        self.coords_convert_update('cartesian')

    def rotate(self, axis=None, angle=None, origin=None, matrix=None):
        """Rotate the current molecule.

        Args:
            axis (tuple of 3 floats, optional): Tuple containing the rotation
                vector that will be used as an axis. Defaults to None.
            angle (float, optional): Rotation angle. Defaults to None.
            origin (tuple of 3 floats): Origin point to rotate the molecule in
                cartesian coordinates, if None, centroid will be used.
                Defaults to None.
            matrix (obj:`np.ndarray`, optional): If specified, use a rotation
                matrix instead of generating one. Defaults to None.
        """
        if origin is None:
            origin = self.find_centroid('cartesian')
        else:
            origin = np.asarray(origin, dtype=float)

        if matrix is not None:
            rotation_mat = matrix
        else:
            rotation_mat = geometry.rotation_matrix(axis, angle)

        coords_old = self.coords_array('cartesian')
        coords_old -= origin
        coords_new = np.dot(coords_old, rotation_mat)
        coords_new += origin
        self.coords_update(coords_new, system='cartesian')
        self.coords_convert_update('direct')

    def select(self, item_lst, copy=False, mol_obj=False):
        """Return a list or a molecule containing the selected atoms by index.

        Args:
            item_lst (list or tuple of integers or atoms): List containing the
                index or the atoms that will be selected.
            copy (bool, optional): If true a copy of the atoms will be created
                instead of returning a pointer to the atoms of the original
                molecule. Defaults to False.
            mol_obj (bool, optional): Returns an obj:Molecule instead of a list
                containing the selected atoms of the molecule. Defaults to
                False.

        Returns:
            List of obj:`molecule.Atom` or obj:`molecule.Molecule` with the
            selected atoms.
        """
        selected = []
        for item in item_lst:
            if isinstance(item, int):
                selected.append(self.atoms[item])
            elif isinstance(item, Atom):
                selected.append(item)

        if copy:
            selected = [atom.copy() for atom in selected]

        if mol_obj:
            new_mol = Molecule('Selection')
            new_mol.atom_add_list(selected)
            new_mol.cell_p_add(self.cell_p)
            return new_mol
        return selected

    def to_bulk(self):
        """Generate an obj:`Bulk` with the same data of the original object.

        Returns:
            obj:`Bulk` with the same data of the molecule.
        """
        bulk = Bulk(self.name)
        atoms = [atom.copy() for atom in self.atoms]
        cell_p = self.cell_p
        bulk.atom_add_list(atoms)
        bulk.cell_p_add(cell_p)
        return bulk

    def vacuum_add(self, distance=12., dimension='z'):
        """Add vacuum to the bulk setted in the catalytic system.

        Args:
            distance (float, optional): Distance between the highest point
                of the bulk and the final point of the vacuum. Defaults to 12.

            dimension (str, 'x', 'y' or 'z', optional): Dimension to which
                the vacuum id added. Defaults to 'z'.

        Examples:
            >>> catsys.vacuum_add(distance=13., dimension='y')
        """
        dimension_numb = DIM_DICT[dimension]

        vec_dim = self.cell_p.direct[dimension_numb]
        vec_norm = np.linalg.norm(vec_dim)
        vec_exp = (vec_norm + distance) / vec_norm
        exp_attr = {dimension: vec_exp}
        self.cell_p.expand(**exp_attr)

        self.coords_convert_update('direct')

    def connectivity_search_voronoi(self, tolerance=0.25, center=False):
        """Perform a connectivity search using the voronoi method. The method
        uses periodic boundary conditions and CORDERO Radius.

        Args:
            tolerance (float, optional): Tolerance that will be added to the
                medium distance between two atoms.
            center (bool, optional): If True, the direct coordinates array of
                the molecule will be centered before the bond calculation to
                avoid errors in far from the box molecules. The coordinates
                of the molecule will not change.
        
        Notes:
            self.pairs will be fullfilled after the use of this method.

        Cite:
            Isayev, O. et al. Universal fragment descriptors for predicting
                properties of inorganic crystals. Nat. Commun. 8, 15679
                doi: 10.1038/ncomms15679 (2017).
        """
        if len(self.atoms) == 1:
            return []

        if center:
            cartesian_old = np.copy(self.coords_array('cartesian'))
            direct_old = np.copy(self.coords_array('direct'))
            self.move_to_box_center()

        coords_arr = np.copy(self.coords_array('direct'))
        coords_arr = np.expand_dims(coords_arr, axis=0)
        coords_arr = np.repeat(coords_arr, 27, axis=0)

        mirrors = [-1, 0, 1]
        mirrors = np.asarray(list(product(mirrors, repeat=3)))
        mirrors = np.expand_dims(mirrors, 1)
        mirrors = np.repeat(mirrors, coords_arr.shape[1], axis=1)

        corrected_coords = np.reshape(coords_arr + mirrors,
                                      (coords_arr.shape[0] * coords_arr.shape[1],
                                       coords_arr.shape[2]))
        corrected_coords = np.dot(corrected_coords, self.cell_p.direct)

        translator = np.tile(np.arange(coords_arr.shape[1]),
                             coords_arr.shape[0])
        vor_bonds = Voronoi(corrected_coords)

        pairs_corr = translator[vor_bonds.ridge_points]
        pairs_corr = np.unique(np.sort(pairs_corr, axis=1), axis=0)
        true_arr = pairs_corr[:, 0] == pairs_corr[:, 1]
        true_arr = np.argwhere(true_arr)
        pairs_corr = np.delete(pairs_corr, true_arr, axis=0)
        dst_d = {}
        pairs_lst = []
        for pair in pairs_corr:
            elements = [self.atoms[index].element for index in pair]
            fr_elements = frozenset(elements)
            if fr_elements not in dst_d:
                dst_d[fr_elements] = radius.CORDERO[elements[0]]
                dst_d[fr_elements] += radius.CORDERO[elements[1]]
                dst_d[fr_elements] += tolerance
            if dst_d[fr_elements] >= self.distance(*pair, system='cartesian',
                                                   minimum=True):
                pairs_lst.append(pair)
                self.atoms[pair[0]].connection_add(self.atoms[pair[1]])
        self.pairs = np.asarray(pairs_lst)

        if center:
            self.coords_update(cartesian_old, 'cartesian')
            self.coords_update(direct_old, 'direct')
        return self.pairs


class Bulk(Molecule):
    """This class determines either a bulk system and a surface

    Init method inherited from Molecule object. See Molecule object
    for more information
    """

    def copy(self):
        """Generates a copy of the current bulk.

        Returns:
            :obj`Bulk` copy of the bulk
        """
        atoms_copy = [atom.copy() for atom in self.atoms]
        cell_p_copy = self.cell_p.copy()

        connect_lst = []
        for atom in self.atoms:
            connect_lst.append([self.atoms.index(cone) for cone in
                                atom.connections])

        bulk_copy = Bulk(self.name)
        bulk_copy.atom_add_list(atoms_copy)
        bulk_copy.cell_p = cell_p_copy

        for atom, connects in zip(bulk_copy.atoms, connect_lst):
            atom.connections = [bulk_copy[index] for index in connects]

        return bulk_copy

    def layer_detect(self, threshold, dimension):
        """Try to detect layers of atoms in the given dimension. The layer
        position will be added to the atom.grid attribute.

        Args:
            threshold (float): Threshold which determines the thickness of
                the layer.
            dimension (str): Dimension in which detect the layers. Must be 'x'
                'y' or 'z'

        Examples:
            >>> bulk.layer_detect(0.1, 'x')
        """
        dim_numb = DIM_DICT[dimension]
        th_vec = threshold * self.cell_p.inverse[:, [dim_numb]]
        th_direct = np.linalg.norm(th_vec)
        fragment = np.array([0., th_direct], dtype=float)

        current_layer = 0
        while fragment[1] < 1.:
            for atom in self.atoms:
                dcoords_dim = atom.dcoords[dim_numb]
                if fragment[0] <= dcoords_dim <= fragment[1]:
                    atom.grid[dimension] = current_layer
            current_layer += 1
            fragment += th_direct

    def layer_detect_smart(self, threshold=0.01, thickness=1, dimension='z'):
        """Try to detect layers of a certain atom thickness. The number of the
        layer of every Atom will be added to the Atom.grid attribute.

        Args:
            threshold (float, optional): Threshold of the thickness
                of the layer, in direct coordinates. Defaults to a
                1/100 (0.01) partition of the box.
            thickness (int, optional): Thickness of every layer, in atoms.
                Defaults to 1.
            dimension (str, optional): Dimension in which try to detect
                layers. Defaults to 'z'.

        Returns:
            int containing the number of layers detected.

        Examples:
            >>> bulk.layer_detect_smart(thickness=2, dimension='x')
            ...
            >>> bulk.layer_detect_smart(threshold=0.1, dimension='y')
        """
        layer_lst = []
        atom_ref = []
        counter = 0
        for atom in self.atoms:
            dcoords_dim = atom.dcoords[DIM_DICT[dimension]]
            for layer, identifier in layer_lst:
                tolerance = [layer - threshold, layer + threshold]
                if tolerance[0] <= dcoords_dim <= tolerance[1]:
                    atom_ref.append([atom, identifier])
                    break
            else:
                layer_lst.append([dcoords_dim, counter])
                atom_ref.append([atom, counter])
                counter += 1

        layer_lst.sort(key=lambda x: x[0])
        pos_lst = [column[1] for column in layer_lst]

        for atom, identifier in atom_ref:
            atom.grid[dimension] = pos_lst.index(identifier)

        if thickness > 1:
            for atom, _ in atom_ref:
                atom.grid[dimension] = (atom.grid[dimension] // thickness)
        return counter

    def layer_get(self, layer_numb, atom_lst=False, copy=False, axis='z'):
        """Create a molecule containing only the atoms of the selected surface.

        Args:
            layer_numb (int, lst): Number of the layer to extract. If is a list
                or a tuple of integers all the layers in the list will be.
                obtained.
            atom_lst (bool, optional): If True, return a list of atoms
                containing the atoms of the layers instead of a molecule.
                Defaults to False.
            copy (bool, optional): If True, the atoms of the new molecule will
                be a copy of the original ones instead of the originals.
                Defaults to False.
            axis (str, optional): Axis in which the layers are defined.
                Defaults to 'z'.

        Returns:
            obj:`Molecule` if atom_lst is False or list of obj:`Atom` if
            atom_lst is True.
        """
        if isinstance(layer_numb, int):
            atoms_lst = [atom for atom in self.atoms
                         if atom.grid[axis] == layer_numb]
        elif isinstance(layer_numb, (list, tuple)):
            atoms_lst = [atom for atom in self.atoms
                         if atom.grid[axis] in layer_numb]
        if copy:
            new_lst = []
            for atom in atoms_lst:
                new_lst.append(atom.copy())
            atoms_lst = new_lst

        if atom_lst:
            return atoms_lst

        new_mol = Molecule(self.name + '{{}}'.format(str(layer_numb)))

        if copy:
            new_mol.cell_p.add(self.cell_p.copy())
        else:
            new_mol.cell_p_add(self.cell_p)

        new_mol.atom_add_list(atoms_lst)

        return new_mol

    def expand(self, **expansion):
        """Expands the unit cell trhough the given axes.

        Args:
            **expansion: Axis and dimension expansion, only x, y, z values
                with an integer expansion are allowed.
            grid (bool, optional): If True a Grid will be added. Defaults to
                False.

        Examples:
            >>> bulk1.expand(x=3, y=2)
        """

        try:
            self.coords_array('direct')
        except AttributeError:
            self.coords_convert_update('direct')

        def single_expansion(self, dimension, multiplier):
            """ Expands the in system one dimension

            Args:
                dimension (int): dimension to expand, 0, 1 or 2
                multiplier (int): multiplier factor
            """

            new_atom_list = []  # Append atoms generated after loop
            for atom in self.atoms:
                atom.dcoords[dimension] /= multiplier  # Direct system new pos
                for act_mult in range(1, multiplier):
                    new_atom = atom.copy()
                    sum_factor = act_mult/multiplier
                    new_atom.dcoords[dimension] += sum_factor
                    new_atom_list.append(new_atom)
            self.atom_add_list(new_atom_list)

        for dim, mult in expansion.items():
            if mult > 1:
                single_expansion(self, DIM_DICT[dim], mult)
            else:
                pass
        self.cell_p.expand(**expansion)  # Expand the cell tensor first ...
        self.coords_convert_update('cartesian')  # ... then update to cartesian

    def highest_point(self, system='cartesian'):
        """Returns the coordinates of the higher point of the surface.

        Args:
            system (str): Coordinate system of the coords returned. Must
                be 'cartesian' or 'direct'. Defaults to cartesian.

        Returns:
            float numb containing the coordinates of the highger atom in
                the bulk.
        """

        if system == 'cartesian':
            max_value = max([atom.coords[2] for atom in self.atoms])
        elif system == 'direct':
            max_value = max([atom.dcoords[2] for atom in self.atoms])
        return max_value

    def connection_search_brute(self, threshold=1.4, pbt=False):
        """Search the connection between the atoms of the bulk using brute
        force. This method will connect all the atoms within a distance
        shorter than the threshold.

        threshold (float, optional): Threshold distance to consider a
            connection. Defaults to 1.4.
        pbt (bol, optional): If True, periodic boundary conditions will be
            used to determine connectivity. Defaults to False.
        """
        if pbt:
            coords = self.coords_array(system='direct')
            for ii in range(len(coords)):
                for jj in range(ii + 1, len(coords)):
                    diff = coords[ii] - coords[jj]
                    for kk in range(3):
                        if abs(diff[kk]) > 0.5:
                            if diff[kk] < 0:
                                diff[kk] += 1.
                            else:
                                diff[kk] -= 1.
                    if np.linalg.norm(np.dot(diff, self.cell_p.direct)) < threshold:
                        self.atoms[ii].connection_add(self.atoms[jj])
        else:
            coords = self.coords_array(system='cartesian')
            for ii in range(len(coords)):
                for jj in range(ii + 1, len(coords)):
                    diff = coords[ii] - coords[jj]
                    if np.linalg.norm(diff) < threshold:
                        self.atoms[ii].connection_add(self.atoms[jj])

    def surface_center(self):
        """Returns the coordinates of the middle point at surface.

        Note:
            The middle point is computed using the direct coordinates
            and then is translate to cartesian using the CellParams.
            To do so, this function relies in cell_p attribute of
            Molecule class. If no cell_p is set, set one using the
            cell_p_add method.

        Returns:
            :obj`np.ndarray` containing the coordinates of the middle
                point.
        """
        if self.cell_p is None:
            raise NoSurfaceError

        max_point = self.highest_point(system='direct')
        middle_point = np.array([0.5, 0.5, max_point])
        return middle_point.dot(self.cell_p.direct)

    def atom_change_mov_layer(self, dimension, layers, option='freeze'):
        """Freeze or release the atoms corresponding to the given layers.

        Args:
            dimension (str): Dimension of the layers. Must be 'x', 'y' or 'z'.
            layers (list or tuple of int, int): Layers that will be frozen.
            option (str, optional): 'freeze' or 'release' the atoms. Default
                to freeze.

        Notes:
            Note that a layer identification must be used before this function.
            For more information look at Bulk.layer_detect or
            Bulk.layer_detect_smart.
        """
        if option == 'freeze':
            new_mov = tuple([False] * 3)
        elif option == 'release':
            new_mov = tuple([True] * 3)
        else:
            raise NotImplementedError

        if isinstance(layers, (tuple, list)):
            for atom in self.atoms:
                if atom.grid[dimension] in layers:
                    atom.freeze = new_mov
        elif isinstance(layers, int):
            for atom in self.atoms:
                if atom.grid[dimension] == layers:
                    atom.freeze = new_mov
        else:
            msg = 'Only int, tuple or list of int are allowed as a argument'
            raise NotImplementedError(msg)

    def split_by_layer(self, layer_number, dimension='z'):
        """Split the actual bulk into a CatalyticSystem containing a surface
        and an a molecule. The layers of the bulk must be used before
        splitting the system. Items below the layer number will be part
        of the surface and items above the layer_numb will form a molecule.

        Args:
            layer_numb (int): Number of layers that will be used to create
                the surface.
            dimension (str, optiona): 'x', 'y' or 'z'. Dimension in which the
                layers are splitted. Defaults to 'z'.
        """
        layers = tuple(range(layer_number))
        surface_atoms = []
        mol_atoms = []
        for atom in self.atoms:
            if atom.grid[dimension] in layers:
                surface_atoms.append(atom)
            else:
                mol_atoms.append(atom)

        new_bulk = Bulk('BLK')
        new_bulk.atom_add_list(surface_atoms)
        new_bulk.cell_p_add(self.cell_p)

        caty = CatalyticSystem('CAT')
        caty.surface_set(new_bulk)

        if mol_atoms:
            new_mol = Molecule('SPL')
            new_mol.atom_add_list(mol_atoms)
            new_mol.cell_p_add(self.cell_p)
            caty.molecule_add(new_mol)

        return caty

    def split_by_element(self, elements, invert=False):
        """Split the actual bulk into a CatalyticSystem containing a surface
        and an a molecule. The elements of the bulk must be specified.

        Args:
            elements (lst of str): List containing the elements of the bulk
                that will be splitted.
            invert (bool, optional): If True, the atoms of the bulk will be
                the ones that do not match with the ones in the elements list.
                Defaults to False.
        """
        if isinstance(elements, str):
            elements = [elements]
        surface_atoms = []
        mol_atoms = []
        for atom in self.atoms:
            if atom.element in elements:
                surface_atoms.append(atom)
            else:
                mol_atoms.append(atom)

        new_bulk = Bulk('BLK')
        new_bulk.atom_add_list(surface_atoms)
        new_bulk.cell_p_add(self.cell_p)

        caty = CatalyticSystem('CAT')
        caty.surface_set(new_bulk)

        if mol_atoms:
            new_mol = Molecule('SPL')
            new_mol.atom_add_list(mol_atoms)
            new_mol.cell_p_add(self.cell_p)
            caty.molecule_add(new_mol)

        return caty

    def move_to_bottom(self):
        """"Move the bulk to the bottom of the cell parameters"""
        move_vec = np.zeros(3)
        for axis in range(3):
            move_vec[axis] = np.min(self.coords_array('direct')[:, axis])
        self.move_vector(-move_vec, system='direct')


class CatalyticSystem:
    """Class that contains the whole catalytic system, including the surface
    and multiple molecules.

    Args:
        name (str): Name of the catalytic system.

    Attributes:
        name (str): Name of the catalytic system.
        surface (:obj`Surface`): Surface of the system.
        molecules (list of :obj`Molecule`): Molecules in the system.
        mol_num (int): Number of molecules in the system.
    """
    def __init__(self, name):
        self.name = name
        self._surface = None
        self.molecules = []
        self.mol_num = 0
        self._cell_p = None

    def __add__(self, other):
        if isinstance(other, Molecule):
            self.molecule_add(other)
        elif isinstance(other, list) and all(isinstance(molecule, Molecule)
                                             for molecule in other):
            self.molecule_add_list(other)
        else:
            return NotImplemented
        return self

    def __len__(self):
        return self.mol_num

    def __in__(self, other):
        bool_out = other in (self.molecules + [self.surface])
        return bool_out

    def __getitem__(self, choice):
        if choice == 'surface':
            selection = self.surface
        else:
            for _molecule in self.molecules:
                if _molecule.name == choice:
                    selection = _molecule
                    break
            else:
                selection = None
        return selection

    def __iter__(self):
        return iter(self.molecules)

    def __str__(self):
        repr_str = '{}\nSurface: {}\n'.format(self.name, str(self.surface))
        repr_str += 'Molecules[{}]: '.format(str(self.mol_num))
        if self.molecules:
            for molecule in self.molecules:
                repr_str += str(molecule) + ', '
            repr_str = repr_str[:-2]
        return repr_str

    def __repr__(self):
        return str(self)

    @property
    def cell_p(self):
        """Cell parameters of the system.
        """
        return self._cell_p

    @cell_p.setter
    def cell_p(self, value):
        if isinstance(value, CellParameters):
            self._cell_p = value
        else:
            self._cell_p = CellParameters(value)
        self.surface.cell_p = self._cell_p
        self.cell_p_update(item='all', system='direct')

    @property
    def surface(self):
        """Surface of the system, must be an obj:`molecule.Bulk`.
        """
        return self._surface

    @surface.setter
    def surface(self, value):
        self.surface_set(value)

    @surface.deleter
    def surface(self):
        del self._surface

    def cell_p_update(self, item='molecules', system='cartesian'):
        """Updates the direct coordinates of all the molecules of the system
        to the new Cell Parameters.

        Args:
            item (str): Items of the system to update. Must be 'molecules',
                'surface' or 'all'. Defaults to 'all'.
            system (str): Coordinate system of the coords returned. Must
                be 'cartesian' or 'direct'. Defaults to cartesian.

        Examples:
            >>> catsys.cell_p_update(item='all', system='direct')
            ...
            >>> catsys.cell_p_update(item='molecules', system='cartesian')
            ...
            >>> catsys.cell_p_update(item='surface')
        """
        if item in ('molecules', 'all'):
            for _molecule in self:
                _molecule.cell_p = self.cell_p
                _molecule.coords_convert_update(system)
        if item in ('surface', 'all'):
            self.surface.coords_convert_update(system)

    def count_atoms(self):
        """Count the number of atoms in the system.

        Returns:
            int with the number of atoms of the system.
        """

        atom_number = 0
        if self.surface:
            atom_number += self.surface.atom_numb
        for molecule in self.molecules:
            atom_number += molecule.atom_numb
        return atom_number

    def layer_add(self, layer, dimension='z'):
        """Adds a layer at the top of one of the three dimensions of the
        surface of the catalytic system.

        Args:
            layer (:obj`molecule`): Layer to add to the top of the surface.
            dimension (str, optional): Dimension where the layer will be
                added. Must be x, y or z. Defaults to z.

        Notes:
            - Both, the layer and the current object must have a cell_p.
            - Like the molecules or the surface, the layer added should not
                be part of the catalytic system after the addition.

        Examples:
            >>> catsys.layer_add(molecule, dimension='x')
        """
        d_num = DIM_DICT[dimension]
        center_low = np.array([.5, .5, .5])
        center_low[d_num] = 0.
        center_low_c = center_low.dot(layer.cell_p.direct)
        center_high = np.array([.5, .5, .5])
        center_high[d_num] = 1.
        center_high_c = center_high.dot(self.cell_p.direct)

        layer.move_to(center_high_c, system='cartesian', origin=center_low_c)

        norm_self = np.linalg.norm(self.cell_p.direct[d_num])
        cell_p_factor = norm_self + np.linalg.norm(layer.cell_p.direct[d_num])
        cell_p_factor /= norm_self

        exp_attr = {dimension: cell_p_factor}
        self.cell_p.expand(**exp_attr)
        self.cell_p_update('all', system='direct')

        self.molecule_add(layer)  # Adding the layer to the system

    def molecule_add(self, _molecule):
        """Add a single molecule to the catalytic system.

        Args:
            _molecule (:obj`Molecule`): Single molecule to add to the system.

        Note:
            If a surface is setted, the cell_p attribute of the molecule will
            change. Moreover, the direct coordinates of the atoms will be
            recalculated using the new cell_p.
        """
        for molecule_c in self.molecules:
            if molecule_c is _molecule:
                _molecule = molecule_c.copy()
                break

        if isinstance(_molecule, Molecule):
            while self[_molecule.name] is not None:
                new_name = _molecule.name + "_"
                msg = "Two molecules with the same name, changing the name " \
                      "of " + _molecule.name + " to " + new_name
                warnings.warn(msg, UserWarning)
                _molecule.name = new_name

            if self.surface is not None:  # If the surface is setted ...
                _molecule.cell_p = self.cell_p  # ... Change the cell_p
                _molecule.coords_convert_update('direct')

            self.molecules.append(_molecule)
            self.mol_num += 1
        else:
            msg = 'The molecule argument shold belong to Molecule class!'
            raise TypeError(msg)

    def molecule_add_list(self, molecules_list):
        """Add a list of molecules to the catalytic system.

        Args:
            molecules_list (:obj`list` of :obj`Molecule`): List filled with
                molecules.
        """
        conditional_list = isinstance(molecules_list, list)
        conditional_molecules = all(isinstance(molecule, Molecule)
                                    for molecule in molecules_list)

        if conditional_list and conditional_molecules:
            for molecule in molecules_list:
                self.molecule_add(molecule)
        else:
            msg = 'Argument must be a list that only contains molecules!'
            raise TypeError(msg)

    def move_over_surface_center(self, molecule, distance, origin='centroid'):
        """Moves the selected molecule over the middle point of the surface.

        Args:
            molecule (:obj`molecule`): Molecule of the system to move.
            distance (float): Distance between the centroid of the
                molecule and the highest point of the surface.
                In Armstrongs.
        """
        new_point = self.surface.surface_center()
        new_point[2] += distance
        molecule.move_to(new_point, system='cartesian', origin=origin)

    def move_over_atom(self, molecule, atom, distance,
                       dimension='z', origin='centroid'):
        """Move the selected molecule at a specified distance over an atom
        of the bulk.

        Args:
            molecule (:obj`Molecule`): Molecule in the catalytic to move.
            atom (:obj`Atom`): Atom of the surface in which the molecule
                will be moved over.
            distance (float): Distance between the atom and the centroid
                of the molecule.
            dimension (str, optional): 'x', 'y' or 'z'. Dimension in which
                add the molecule. Defaults to 'z'.
        """
        displacement = np.zeros(3)
        displacement[DIM_DICT[dimension]] = distance
        coordinates = atom.coords + displacement
        molecule.move_to(coordinates, system='cartesian', origin=origin)

    def move_over_bridge(self, molecule, atoms, distance,
                         dimension='z', origin='centroid'):
        """Move the selected molecule of the CatalyticSystem over a bridge
        between two atoms of the bulk.

        Args:
            molecule (:obj`Molecule`): Molecule to move over the bridge.
            atoms (tuple with 2 :obj`Atom`): Atoms of the surface that
                form the bridge over which the molecule will be moved.
            distance (float): Distance between the atom and the centroid
                of the molecule.
            dimension (str, optional): 'x', 'y' or 'z'. Dimension in which
                add the molecule. Defaults to 'z'.
        """
        displacement = np.zeros(3)
        displacement[DIM_DICT[dimension]] = distance
        bridge = (atoms[1].coords - atoms[0].coords) / 2.
        bridge = atoms[0].coords + bridge
        coordinates = bridge + displacement
        molecule.move_to(coordinates, system='cartesian', origin=origin)

    def move_over_multiple_atoms(self, molecule, atoms, distance=None,
                                 dimension='z', origin='centroid'):
        """Move the selected molecule of the CatalyticSystem over the central
        point of 3 different atoms.

        Args:
            molecule(:obj`Molecule`): Molecule to move over the bridge.
            atoms (tuple with multiple :obj`Atoms`): Atoms of the surface that
                will be used to calculate the middle point.
            distance (float, optional): Distance between the centroid of the
                selected atoms and the new position of the molecule. If None,
                molecule will preserve its original axis direction.
            dimension (str, optional): 'x', 'y', or 'z'. Dimension along the
                distance will be applied. Defaults to 'z'.
            origin (str, optional): Origin of the molecule in which apply the
                movement vector. Defaults to 'centroid'
        """
        coords = np.asarray([atom.coords for atom in atoms])
        atoms_centroid = np.sum(coords, axis=0) / coords.shape[0]
        displacement = np.zeros(3)
        if distance is None:
            molecule.move_to(atoms_centroid, system='cartesian', origin=origin,
                             lock=[dimension])
        else:
            displacement[DIM_DICT[dimension]] = distance
            new_point = displacement + atoms_centroid
            molecule.move_to(new_point, system='cartesian', origin=origin)

    def surface_set(self, surface):
        """Set the surface object to the catalytic system.

        Args:
            surface (:obj`Surface`): Surface of the system.

        Note:
            Adding a surface will cause the CatalyticSystem cell_p
            to change to the cell_p of the surface. The molecules
            of the system will be updated to change their cell_p.
        """
        if isinstance(surface, Bulk):
            self._surface = surface
        else:
            msg = 'The surface arguments should belong to Bulk class!'
            raise TypeError(msg)

        self._cell_p = surface.cell_p
        self.cell_p_update(item='molecules', system='direct')

    def vacuum_add(self, distance=12., dimension='z'):
        """Add vacuum to the bulk setted in the catalytic system.

        Args:
            distance (float, optional): Distance between the highest point
                of the bulk and the final point of the vacuum. Defaults to 12.

            dimension (str, 'x', 'y' or 'z', optional): Dimension to which
                the vacuum id added. Defaults to 'z'.

        Examples:
            >>> catsys.vacuum_add(distance=13., dimension='y')
        """
        dimension_numb = DIM_DICT[dimension]

        vec_dim = self.cell_p.direct[dimension_numb]
        vec_norm = np.linalg.norm(vec_dim)
        vec_exp = (vec_norm + distance) / vec_norm
        exp_attr = {dimension: vec_exp}
        self.cell_p.expand(**exp_attr)

        self.cell_p_update(item='all', system='direct')


class CellParameters:
    """Object containing the direct cell parameters and the inverse
    matrix associated to perform changes of the coordinate system.

    Args:
        cell_p (list or np.ndarray 3x3): Direct cell tensor or the system.

    Attributes:
        direct (:obj`np.ndarray`): Array containing the cell tensor
            of the system.
        inverse (:obj`np.ndarray`): Array containing the inverse cell tensor
            of the system.
    """

    def __init__(self, cell_p):
        if isinstance(cell_p, (list, tuple, np.ndarray)):
            self.direct = np.array(cell_p, dtype=float)
            self.inverse = self.invert()
        elif isinstance(cell_p, CellParameters):
            self.direct = np.copy(cell_p.direct)
            self.inverse = np.copy(cell_p.inverse)
        else:
            raise NotImplementedError

    def __pos__(self):
        return self.direct

    def __neg__(self):
        return self.inverse

    def __eq__(self, other):
        return self.direct == other.direct

    def __repr__(self):
        return str(self.direct)

    def copy(self):
        """Copy the CellParameters object.

        Returns:
            :obj`CellParameters` copy of the Cell Parameters.
        """
        cell_p_copy = CellParameters(self.direct)
        return cell_p_copy

    def invert(self):
        """ Returns the inverse np array of the cell parameters.

        Returns:
            np.ndarray 3x3: Inverse cell tensor
        """
        return np.linalg.inv(self.direct)

    def expand(self, **expansion):
        """ Expand the cell parameters trhough the given dimensions.

        Args:
            **expansion: Axis and dimension expansion, only x, y, z values
                with an integer expansion are allowed.
        """
        for dim, mult in expansion.items():
            self.direct[DIM_DICT[dim]] *= mult
        self.inverse = self.invert()    # Update the inverse matrix

    def size(self):
        """Returns the norm of the three vectors of the box.

        Returns:
            :obj`np.ndarray` containing the norm of the three vectors.
        """
        size = np.ones(3)
        for dimension, row in enumerate(self.direct):
            size[dimension] = np.linalg.norm(row)
        return size

    @property
    def lattice_parameters(self):
        """Lattice constants of the cell.

        Returns:
            dict containig the lattice parameters of the current cell.
        """
        keys = ['a', 'b', 'c', 'alpha', 'beta', 'gamma']
        param_tmp = np.linalg.norm(self.direct, axis=0)
        angle_tmp = np.zeros(3)
        for axis in range(3):
            matrix_tmp = np.delete(self.direct, axis, axis=0)
            norm_tmp = np.delete(param_tmp, axis)
            angle_pvt = np.dot(*matrix_tmp) / np.prod(norm_tmp)
            angle_pvt = np.arccos(angle_pvt)
            angle_pvt = (angle_pvt * 180) / np.pi
            angle_tmp[axis] = angle_pvt
        return dict(zip(keys, np.append(param_tmp, angle_tmp)))


class NoSurfaceError(Exception):
    """No Surface error.
    """
    def __init__(self, catsys):
        self.catsys = catsys
        self.str = 'No surface found in' + str(catsys)

    def __repr__(self):
        return self.str


class NoCellPError(Exception):
    """No CellP error.
    """
    def __init__(self):
        pass

    def __repr__(self):
        return 'No CellParameters found'
