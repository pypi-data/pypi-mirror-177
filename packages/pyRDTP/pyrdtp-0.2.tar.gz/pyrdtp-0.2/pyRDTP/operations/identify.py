"""This module aims to provide the necessary tools to identify defects and
position candidates at bulks and slabs"""
from collections import namedtuple
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

Position = namedtuple('Position', 'type dcoords coords')
Atom_A = namedtuple('Atom_A', 'atom atom_index position distance correction')
DIM_DICT = {'x': 0, 'y': 1, 'z': 2}  # Axis translation Dic


def ident_hcp_111(bulk, upper_layer, dimension='z', all_fcc=False):
    """Search for the position candidates in a hcp (1 1 1) slab.

    Args:
        bulk (obj:`molecule.Bulk`): Bulk object in which the positions will
            be identified.
        upper_layer (int): Layer in which identify the positions.
        dimension (str, optional): 'x', 'y' or 'z'. Dimension of the layer.
            Defaults to 'z'.
        all_fcc (bool, optional): If True, all the defects will be identified
            as fcc. Defaults to False.

    Returns:
        List of namedtuples containing the type of position (hcp of fcc), a
        np.ndarray containing the direct coordinates and a np.ndarray
        containing the cartesian coordinates.
    """
    means = []
    sets = []
    atoms_surf = []
    atoms_low = []
    for atom in bulk.atoms:
        if atom.grid[dimension] == upper_layer:
            atoms_surf.append(atom)
        elif atom.grid[dimension] == (upper_layer - 1):
            atoms_low.append(atom.dcoords)

    for atom in atoms_surf:
        neighs_sel = [neighbour for neighbour in atom.connections
                      if neighbour.grid[dimension] == upper_layer]
        for neighbour in neighs_sel:
            connection_sel = [connect for connect in neighbour.connections
                              if connect.grid[dimension] == upper_layer]
            for connection in connection_sel:
                if atom in connection.connections:
                    setting = set((atom, neighbour, connection))
                    coords_arr = [atom.dcoords for atom in setting]
                    coords_arr = np.asarray(coords_arr)
                    if setting not in sets:
                        act_mean = np.mean(coords_arr, axis=0)
                        sets.append(setting)
                        nearest = np.argmin(np.linalg.norm(atoms_low - act_mean, axis=1))
                        point = Point(atoms_low[nearest])
                        pivot = coords_arr.copy()
                        pivot[:, DIM_DICT[dimension]] = atoms_low[nearest][DIM_DICT[dimension]]
                        polygon = Polygon(pivot)
                        coords = np.dot(act_mean, bulk.cell_p.direct)
                        if polygon.contains(point) and not all_fcc:
                            defect_type = 'hcp'
                        else:
                            defect_type = 'fcc'
                        means.append(Position(defect_type, act_mean, coords))
    return means


def ident_bridges_2d(bulk, layer, dimension='z'):
    """Identify the bridge positions in a single layer.

    Args:
        bulk (obj:`molecule.Bulk`): Bulk in which the bridges will be
            identified.
        layer (int): Number of the layer in which the positions will be
            identified.
        dimension (str, optional): 'x', 'y' or 'z'. Dimension of the layer.
            Defaults to 'z'.

    Returns:
        List of namedtuples containing the type of position (bridge), a
        np.ndarray containing the direct coordinates and a np.ndarray
        containing the cartesian coordinates.
    """
    atom_pairs = []
    for atom in bulk.atoms:
        for connection in atom.connections:
            if atom.grid[dimension] == layer and connection.grid[dimension] == layer:
                if (atom, connection) not in atom_pairs and (connection, atom) not in atom_pairs:
                    atom_pairs.append((atom, connection))
    bridge = []
    for pair in atom_pairs:
        dcoords = np.mean([atom.dcoords for atom in pair], axis=0)
        coords = np.mean([atom.coords for atom in pair], axis=0)
        bridge.append(Position('bridge', dcoords, coords))
    return bridge


def atoms_positions(bulk, layer, dimension='z'):
    """Identify the top positions in a single layer.

    Args:
        bulk (obj:`molecule.Bulk`): Bulk in which the bridges will be
            identified.
        layer (int): Number of the layer in which the positions will be
            identified.
        dimension (str, optional): 'x', 'y' or 'z'. Dimension of the layer.
            Defaults to 'z'.

    Returns:
        List of namedtuples containing the type of position (top), a
        np.ndarray containing the direct coordinates and a np.ndarray
        containing the cartesian coordinates.
    """
    positions_lst = []
    for atom in bulk:
        if atom.grid[dimension] == layer:
            positions_lst.append(Position('top', atom.dcoords, atom.coords))
    return positions_lst


def lower_atom_positions(cat_sys, positions, natoms, dimension='z', mol_sel=None):
    """Return the nearest defect for the specified number of atom, prioritizing
    the lowest atoms of the molecules

    Args:
        cat_sys (obj:`molecule.CatalyticSystem`): Catalytic system containing
            the molecule and the bulk to calculate the nearest positions.
        positions (lst of namedtuples): List of tuples containing the
            positions information.
        natoms (int): Number of atoms that will be used in the calculations.
        dimension (str, optional): 'x', 'y' or 'z'. Dimension of the layer.
            Defaults to 'z'.
        mol_sel (obj:`molecule.Molecule`, optional): Molecule that will be
            used to calculate the nearest distances.

    Returns:
        List of namedtuples containing the atom, atom index, position in
        cartesian coordinates and distance in angstroms.
    """
    dim_numb = DIM_DICT[dimension]
    position_coords = np.asarray([item[2] for item in positions])

    if mol_sel is None:
        mol_sel = cat_sys.molecules[0]

    coords = mol_sel.coords_array('cartesian')

    try:
        if len(mol_sel.atoms) == natoms:
            lower_index = np.argsort(coords[:, dim_numb])
            selected = coords[lower_index[:natoms]]
        else:
            lower_index = np.argpartition(coords[:, dim_numb], natoms)
            selected = coords[lower_index[:natoms]]
    except ValueError:
        lower_index = np.asarray([0])
        selected = np.asarray([coords[0]])
    pairs_lst = []
    for index, selection in enumerate(selected):
        pos_index = np.argmin(np.linalg.norm(position_coords - selection, axis=1))
        atom_sel = mol_sel.atoms[lower_index[index]]
        position_sel = positions[pos_index]
        distance = abs(atom_sel.coords[dim_numb] - position_sel[2][dim_numb])
        correction = np.ones(3)
        correction = position_sel[2]
        correction -= atom_sel.coords
        correction[dim_numb] = 0
        tupled = Atom_A(atom_sel, lower_index[index], position_sel, distance, correction)
        pairs_lst.append(tupled)
    return pairs_lst


def transfer(cat_sys, mol_sel, mol_a, positions, opt_rot=False, use_ori=False):
    """Generate a copy a molecule and transfer them to the nearest positions in
    a CatalyticSystem.

    Args:
        cat_sys (obj:`molecule.CatalyticSystem`): CatalyticSystem to which the
            selected molecule will be moved.
        mol_sel (obj:`molecule.Molecule`): Molecule that will be copied and
            moved to the Catalytic System.
        mol_a (lst of tuples): Tuples containing the connection between atoms
            of the molecule and positions of the bulk. See lower_atom_positions
            for more information.
        positions (lst of tuples): Tuples containing the position candidates of
            the bulk
        opt_rot (bool, optional): If used, the molecule will be rotated within
            a second atom. Defaults to False.
        use_ori (bool, optional): Use the nearest position of the direct
            coords instead of the center of the cell.
    """
    mol_used = mol_sel.copy()
    lesser_position = mol_a[0][2][0]
    dcoords = np.asarray([item[1] for item in positions if
                          item[0] == lesser_position])
    coords = np.asarray([item[2] for item in positions if
                         item[0] == lesser_position])
    if use_ori:
        middle_arr = mol_a[0][2][1]
    else:
        middle_arr = np.ones(3) - 0.5
    middle_index = np.linalg.norm(dcoords - middle_arr, axis=1)
    middle_index = np.argmin(middle_index, axis=0)
    distance = np.zeros(3)
    distance[2] += mol_a[0][3]
    mol_used.move_to(coords[middle_index] + distance,
                     system='cartesian',
                     origin=(mol_used[mol_a[0][1]].coords + mol_a[0][4]))
    if opt_rot:
        lesser_coords = mol_used.atoms[mol_a[0][1]].coords
        atom_coords = mol_used.atoms[mol_a[1][1]].coords
        second_position = mol_a[1][2][0]
        coords_second = np.asarray([item[2] for item in positions if
                                    item[0] == second_position])
        second_index = np.linalg.norm(coords_second - atom_coords, axis=1)
        second_index = np.argmin(second_index, axis=0)
        pos_coords = coords_second[second_index] + mol_a[1][4]

        vector_old = atom_coords - lesser_coords
        vector_new = pos_coords - lesser_coords

        dot = np.dot(vector_old[:2], vector_new[:2])
        if dot != 0:
            angle = dot / (np.linalg.norm(vector_old[:2])
                           * np.linalg.norm(vector_new[:2]))
            angle = np.arccos(angle)
            mol_used.rotate(axis=[0, 0, 1], angle=angle, origin=lesser_coords)

    cat_sys.molecule_add(mol_used)
