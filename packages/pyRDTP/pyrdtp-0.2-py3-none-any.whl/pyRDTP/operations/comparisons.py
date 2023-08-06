"""Operations to perform comparisons between two different molecule systems."""
import numpy as np
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
from scipy.linalg import svd


def molecule_compare(mol1, mol2, options='vacuum',
                     excluded=False, threshold=0.05):
    """Compare two different molecules that are in a similar space position.

    Args:
        mol1 (obj:`molecule`): First molecule to compare.
        mol2 (obj:`molecule`): Second molecule to compare.
        options (str, optional): 'vacuum' or 'pbc'. pbc apply the minimum image
            convention while vacuum does not.
        excluded (bol, optional): If True, the excluded atom indexs will be
            returned in addition to bond indexes. Defaults to false.
        threshold (float, optional): If an atom is moved more than the
            specified threshold (direct cell parameters unit) then this
            atom will be counted as a movement.

    Returns:
        obj:`np.ndarray` containing the indexes of linked molecules.
        Excluded values (tuple of int, optional) tuple containing the exluded
            atom indexes.

    Raises:
        ValueError if exluded have a value different to True or False
    """
    matrixes = np.ones(2)
    matrixes = np.asarray((mol1.coords_array('direct'),
                           mol2.coords_array('direct')))
    matrixes = np.asarray((np.expand_dims(matrixes[0], 2),
                           np.expand_dims(matrixes[1], 2)))

    atom_diff = abs(matrixes[0].shape[0] - matrixes[1].shape[0])

    if np.argmax((matrixes[0].shape[0], matrixes[1].shape[0])) == 1:
        matrixes = np.flip(matrixes)
        swap = True
    else:
        swap = False

    matrixes = np.asarray((matrixes[0].repeat(matrixes[1].shape[0], axis=2),
                           matrixes[1].repeat(matrixes[0].shape[0], axis=2)))

    matrixes[1] = matrixes[1].swapaxes(0, 2)
    matrixes[1] = np.flip(matrixes[1], axis=2)

    diff = matrixes[0] - matrixes[1]

    if options == 'pbc':
        true_box = abs(diff) >= 0.5
        true_box = true_box * 1
        true_box_sign = diff < 0.
        true_box_sign = true_box_sign * 1
        true_box_sign[true_box_sign == 0] = -1.

        diff = true_box * true_box_sign - diff

    diff = np.linalg.norm(diff, axis=1)

    curated = diff[:, ::-1]

    if atom_diff != 0:
        maxs = np.argsort(np.amin(curated, axis=1))[-atom_diff:]
    else:
        maxs = np.asarray([])

    mins = np.argmin(curated, axis=1)
    ordmins = np.argsort(np.amin(curated, axis=1))
    equivalences = np.array(tuple(zip(range(0, diff.shape[0]), mins)))
    equivalences = equivalences[ordmins]
    builder = np.ones([diff.shape[0], 2], dtype=int) * (diff.shape[0] + 1)
    movements = []
    maxs_index = np.where(np.in1d(equivalences[:, 0], maxs))
    equivalences = np.delete(equivalences, maxs_index, axis=0)
    for atom1, atom2 in equivalences:
        count = 0
        while atom2 in builder[:, 0]:
            count += 1
            curated[atom1, atom2] = np.argmax(curated[atom1])
            atom2 = np.argmin(curated[atom1])
        if curated[atom1, atom2] > threshold:
            movements.append((atom2, atom1))

        builder[atom1] = np.array((atom2, atom1))

    curated = builder[builder[:, 0] != (diff.shape[0] + 1)]

    if swap:
        curated = np.flip(curated)
        movements = tuple(np.flip(np.asarray(movements)))

    if excluded is False:
        return curated
    if excluded is True:
        return curated, maxs, movements

    msg = '"excluded" argument must be True or False'
    raise ValueError(msg)


def molecule_change_elements(mol1, mol2, options='vacuum'):
    """Compare the positions of the atoms, search for differences between
    elements and then update the elements of the second molecule with the
    elements of the first molecule.

    Args:
        mol1 (obj:`pyRDTP.molecule.Molecule`): Base molecule that will serve
            as an element pattern.
        mol2 (obj:`pyRDTP.molecule.Molecule`): Base molecule that will serve
            as a position pattern.
        options (str, optional): 'vacuum' or 'pbc'. pbc apply the minimum image
            convention while vacuum does not.

    Returns:
        obj:`pyRDTP.molecule.Molecule` with the elements of the first molecule
        and the positions of the second molecule.

    Note:
        Take into account, that if there is one atom present in mol1 and not in
        mol2, the atom of mol1 will be copied directly to mol2. As opposed, if
        mol2 contains an atom that is not in mol1, this atom will be removed.
    """
    bonds, excluded, mov = molecule_compare(mol1, mol2, options, excluded=True)
    for atom1, atom2 in bonds:
        print(atom2, mol1.atoms[atom2], atom1, mol2.atoms[atom1])
    print('')
    mol_new = mol2.copy()
    for atom1, atom2 in bonds:
        if mol1.atoms[atom2].element != mol_new.atoms[atom1].element:
            mol_new.atoms[atom1].element = mol1.atoms[atom2].element
            mol_new.atoms[atom1].freeze = mol1.atoms[atom2].freeze

        # Origin freeze
        mol_new.atoms[atom1].freeze = mol1.atoms[atom2].freeze

    if mov:
        for pair in mov:
            mol_new.atoms[pair[0]].dcoords = (np.asarray(mol1.atoms[pair[1]].dcoords))
            mol_new.atoms[pair[0]].freeze = mol1.atoms[pair[1]].freeze
        mol_new.coords_convert_update('cartesian')

    if excluded.size > 0:
        atom_excluded = []
        for exclusion in excluded:
            if len(mol_new) > len(mol1):
                atom_excluded.append(mol_new.atoms[int(exclusion)])
            else:
                atom_excluded.append(mol1.atoms[int(exclusion)])
        for atom in atom_excluded:
            if len(mol_new) < len(mol1):
                mol_new.atom_add(atom.copy())
            else:
                mol_new.atoms.remove(atom)

    return mol_new


def obtain_pairs(molecule_base, molecule_choice, pbc=False, elem_use=True, min_path=False):
    """Given two molecules with the same number of atom and composition,
    pair the nearest atom and reorder one of them with the same order of
    the nearest atoms in the base structure.

    Args:
        base_molecule (obj:`molecule.Molecule`): Molecule that will be use
            as a pattern to calculate the distances.
        choice_molecule (obj:`molecule.Molecule`): Molecule that will be
            reordered using the base molecule.
        pbc (bool, optional): Use the Periodic Boundary Condition correction
            to obtain the minimum points.
        elem_use (bool, optional): Take into account the elements of the atoms
            to calculate the pairs.
    """
    if elem_use:
        molecule_base.atom_sort()
        molecule_choice.atom_sort()
        elements = molecule_base.elem_array()
        atom_pairs = np.zeros((elements.shape[0], elements.shape[0]), dtype=object)
        for ii in range(elements.shape[0]):
            for jj in range(elements.shape[0]):
                atom_pairs[ii, jj] = (molecule_base.atoms[ii], molecule_choice.atoms[jj])

    elem_sym, elem_numb = np.unique(elements, return_counts=True)
    elem_bool = {}
    for element_sing in elem_sym:
        zero_mat = np.zeros([elements.shape[0], elements.shape[0]], dtype=bool)
        true_mat = elements == element_sing
        zero_mat[true_mat] = true_mat
        elem_bool[element_sing] = zero_mat

    base = molecule_base.coords_array('cartesian')
    coordinates = molecule_choice.coords_array('cartesian')

    if pbc:
        base_direct = molecule_base.coords_array('direct')
        coordinates_direct = molecule_choice.coords_array('direct')
        cell_p = molecule_base.cell_p.direct

    if not pbc:
        rms_actual = cdist(coordinates, base, metric='euclidean')

    else:
        matrixes = np.ones(2)
        matrixes = np.asarray((base_direct, coordinates_direct))
        matrixes = np.asarray((np.expand_dims(matrixes[0], 2),
                               np.expand_dims(matrixes[1], 2)))

        matrixes = np.asarray((matrixes[0].repeat(matrixes[1].shape[0], axis=2),
                               matrixes[1].repeat(matrixes[0].shape[0], axis=2)))

        matrixes[1] = matrixes[1].swapaxes(0, 2)
        matrixes[1] = np.flip(matrixes[1], axis=2)

        diff = matrixes[0] - matrixes[1]
        diff = np.flip(diff, 2)

        true_box = abs(diff) >= 0.5
        true_box = true_box * 1
        true_box_sign = diff < 0.
        true_box_sign = true_box_sign * 1
        true_box_sign[true_box_sign == 0] = -1.

        diff = true_box * true_box_sign + diff
        pbc_pivot = np.expand_dims(cell_p, axis=1)
        pbc_pivot = np.repeat(pbc_pivot, diff.shape[0], axis=1)
        for item in np.arange(diff.shape[2]):
            diff[:, :, item] = np.dot(diff[:, :, item], cell_p)

        rms_actual = np.linalg.norm(diff, axis=1)
    if elements is not None:
        rms_lst = np.ones(elements.shape[0])
        pairs_lst = np.zeros((elements.shape[0], 2), dtype=object)
        counter = 0
        for counts, element in zip(elem_numb, elem_sym):
            elem_rms = rms_actual[elem_bool[element]]
            atom_rms = atom_pairs[elem_bool[element]]
            elem_rms = np.reshape(elem_rms, (counts, counts))
            atom_rms = np.reshape(atom_rms, (counts, counts))
            if min_path:
                mins = linear_sum_assignment(elem_rms)
                for atom1, atom2 in zip(mins[0], mins[1]):
                    pairs_lst[counter] = atom_rms[atom1, atom2]
                    counter += 1
            else:
                for ii in range(elem_rms.shape[0]):
                    min_val = divmod(elem_rms.argmin(), elem_rms.shape[1])
                    rms_lst[ii] = elem_rms[min_val[0], min_val[1]]
                    pairs_lst[counter] = (atom_rms[min_val[0], min_val[1]])
                    elem_rms = np.delete(elem_rms, min_val[1], axis=1)
                    elem_rms = np.delete(elem_rms, min_val[0], axis=0)
                    atom_rms = np.delete(atom_rms, min_val[1], axis=1)
                    atom_rms = np.delete(atom_rms, min_val[0], axis=0)
                    counter += 1
    return pairs_lst

#        rms[index_act] = np.sqrt(np.sum(rms_lst**2) / total)
#    else:
#        rms[index_act] = np.sqrt(np.sum(np.min(rms_actual, axis=1)**2) / total)


def kabsch_alg(molecule_1, molecule_2, elem_wise=False):
    """Use the kabsch_algorithm to reduce the RMS between two different
    molecules.

    Args:
        molecule_1 (obj:`Molecule`): Molecule that will be used as a base for
            the kabsch algorithm. This object will not be changed after the
            algorithm
        molecule_2 (obj:`Molecule`): Molecule that will be rotated after the
            application of the algorithm.
    """
    molecule_2.move_to(molecule_1.find_centroid())

    p_matrix = np.asarray(molecule_1.coords_array('cartesian'), dtype=float)
    q_matrix = np.asarray(molecule_2.coords_array('cartesian'), dtype=float)

    if elem_wise:
        elem_1 = molecule_1.elem_array()
        elem_2 = molecule_2.elem_array()
        h_matrix = np.ones((3, 3))
        for dim_i in range(3):
            for dim_j in range(3):
                h_pvt = 0
                for atom, _ in enumerate(elem_1):
                    if elem_1[atom] == elem_2[atom]:
                        h_pvt += np.dot(p_matrix[atom, dim_i],
                                        q_matrix[atom, dim_j])
                h_matrix[dim_i, dim_j] = h_pvt
    else:
        h_matrix = np.asarray(np.dot(p_matrix.transpose(),
                                     q_matrix), dtype=float)

    u_matrix, _, vt_matrix = svd(h_matrix)
    d_val = np.linalg.det(np.dot(vt_matrix.transpose(),
                                 u_matrix.transpose()))

    imp_corr = np.array([[1., 0, 0],
                         [0, 1., 0],
                         [0, 0, d_val]], dtype=float)

    r_matrix = np.dot(np.dot(vt_matrix.transpose(),
                             (imp_corr)), u_matrix.transpose())
    molecule_2.rotate(matrix=r_matrix)
    return r_matrix
