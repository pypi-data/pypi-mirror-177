"""This module contains functions that will help to perform symmetry
operations and anhilations using the point group symmetry matrixes
"""

from fractions import Fraction
from itertools import combinations
import numpy as np

DIM_DICT = {"x": np.asarray((1, 0, 0)), "y": np.asarray((0, 1, 0)),
            "z": np.asarray((0, 0, 1)), "-x": np.asarray((-1, 0, 0)),
            "-y": np.asarray((0, -1, 0)), "-z": np.asarray((0, 0, -1))}


def sgo_parse(sgo_location):
    """This function parses a file containing symmetry operations.

    Args:
        sgo_location (str): Location of the file containing the symmetry
            operations.

    Returns:
        obj:`np.ndarray` containing the matrix form of the simmetry operations.

    Notes:
        The symmetry operations file must be in this format:
            1 x,y,z
            2 -z,x,y
            3 -z,y+1/2,z
            4 -z+3/4,y,z
                ...

        Before returning the symmetry arrays, the program will search and
        purge the repeated arrays.
    """
    with open(sgo_location) as sgo_file:
        sgo_content = sgo_file.read()

    curated = sgo_content.splitlines()
    matrix_lst = []

    for line in curated:
        new_matrix = []
        newline = line.split()
        if len(newline) > 1:
            newline = newline[1]
        newline = newline.split(',')
        for item in newline:
            pivot = item.split('+')
            sub = DIM_DICT[pivot[0]]
            if len(pivot) > 1:
                sub = sub * float(Fraction(pivot[1]))
            new_matrix.append(sub)
        matrix_lst.append(new_matrix)

    return np.unique(np.asarray(matrix_lst), axis=0)


def obtain_unique(system, sgo_lst, threshold=0.05):
    """Search wich matrixes are symmetry operations available for the given
    system. Then, return the atom positions relationship for every matching
    symmetry operation.

    Args:
        system (obj:`SystemCombination`): System combination containing the
            base structure to check the symmetry.
        sgo_lst (np.ndarray): np.ndarray containing the symmetry operations
            in array form. This array can be generated using the sgo_parse()
            function.
        threshold (float, optional): Max distance to accept equality between
            two atoms. Direct units. Defaults to 0.1.
    """

    origin_array = system.coords_array('direct')
    origin_elem = system.elem_array()
    bonds_lst = []
    counter = 0

    for matrix in sgo_lst:

        sum_vec = np.zeros(3)
        if matrix.shape[-1] == 4:
            sum_vec = matrix[:,3]
            matrix = matrix[:,0:3]
        counter += 1
        bonds = []
        match = True
        new_array = np.dot((origin_array - 0.5), matrix)
        new_array = new_array + 0.5 + sum_vec
        mol2 = system.copy()
        mol2.coords_update(new_array, 'direct')
        for old in range(0, len(origin_array)):
            for new in range(0, len(new_array)):
                if origin_elem[old] != origin_elem[new]:
                    pass
                else:
                    distance = origin_array[old] - new_array[new]
                    test1 = abs(distance) >= 0.5
                    test2 = distance < 0
                    test2 = (test2 * 2) - 1
                    distance = distance + (test1 * test2)
                    distance = np.linalg.norm(distance)
                    if distance < threshold:
                        bonds.append((old, new))
                        break
            else:
                match = False

            if not match:
                break
        else:
            bonds_lst.append(bonds)

    return np.unique(np.asarray(bonds_lst), axis=0)

def symmetry_anhilition(system_lst, bonds_lst):

#    denied = []
    counter = 0
    for system in system_lst:
        system.denied = False
    print(len(tuple(combinations(system_lst, 2))))
    for systems in combinations(system_lst, 2):
        counter += 1
        print(counter, end="\r")

        if not systems[0].denied or not systems[1].denied:
            pass

        elem_sets = (systems[0].structure.elements,
                     systems[1].structure.elements)
        elem_dicts = (systems[0].structure.elements_number,
                      systems[1].structure.elements_number)

        if elem_sets[0] != elem_sets:
            pass

        if elem_dicts[0] != elem_dicts[1]:
            pass

        elems = [systems[0].structure.elements_list,
                 systems[1].structure.elements_list]

        for bonds in bonds_lst:
            elems_pivot = elems[1][bonds[:, 1]]
            checker = elems[0] == elems_pivot

            if checker.all():
                ordered = sorted(systems, key=lambda x: x.identifier,
                                 reverse=True)

#                denied.append(ordered[1])
                ordered[1].denied = True
                for son in ordered[1].sons:
                    son.father = ordered[0]
                for brother in ordered[1].brothers:
                    if ordered[1] in brother.brothers:
                        brother.brothers.remove(ordered[1])
                        if ordered[0] in brother.brothers:
                            pass
                        else:
                            brother.brothers.append(ordered[0])

#                for dependency in system_lst:
#                    if dependency.denied:
#                        pass

#                    if dependency.father == ordered[1]:
#                        dependency.father = ordered[0]
#                        pass

#                    if ordered[1] in dependency.brothers:
#                        dependency.brothers.remove(ordered[1])
#                        if ordered[0] in dependency.brothers:
#                            pass
#                        else:
#                            dependency.brothers.append(ordered[0])

                break

    accepted = []
    for item in system_lst:
        if not item.denied:
            accepted.append(item)

    return accepted


def translation_matrixes_gen(x=1, y=1, z=1):
    """Generate the translation matrixes and combinations associated with a
    non fractional unit cell expansion.

    Args:
        x (int, optional): Expansion in x axis. Defaults to 1.
        y (int, optional): Expansion in y axis. Defaults to 1.
        z (int, optional): Expansion in y axis. Defaults to 1.

    Returns:
        obj:`np.ndarray` [n,3,3] where n is the number of all the generated
        arrays.
    """
    matrixes = []
    for axis, mult in enumerate([x, y, z]):
        if mult == 1:
            pass
        else:
            displacements = np.array(range(1, mult)) / mult
            matrixes_axis = []
            for item in displacements:
                matrix_unit = np.zeros(3)
                matrix_unit[axis] += item
                matrixes_axis.append(matrix_unit)

            if matrixes:
                matrixes_new = []
                for old in matrixes:
                    for new in matrixes_axis:
                        matrixes_new.append(old + new)
                matrixes += matrixes_new

            matrixes += matrixes_axis

    matrixes.append(np.zeros(3))  # Zero displacement vector

    return np.array(matrixes)


def translation_matrixes_comb(trans, symm):
    """Combine the translational matrixes and the symmetry matrixes to
    generate a supermatrix containing all the possible geometry operations
    for a supercell

    Args:
        trans (obj:`np.ndarray`): Array containing the translational matrixes.
        symm (obj:`np.ndarray`): Array containing the point group symmetry
            operation matrixes.

    Returns:
        obj:`np.ndarray` containing all the possible combinations between the
        translation and point group symmetry operation matrixes.
    """
    trans_pivot = np.tile(trans, (symm.shape[0], 1))
    symm_pivot = np.repeat(symm, trans.shape[0], axis=0)
    new_arr = np.dstack((symm_pivot, trans_pivot))
    return new_arr
