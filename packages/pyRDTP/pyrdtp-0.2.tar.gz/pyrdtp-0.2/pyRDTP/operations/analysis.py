import numpy as np

BOND_ORDER = {'C': 4,
              'O': 2}

def bond_analysis(mol, comp_dist=False):
    """Returns a dictionary of frozen tuples containing information about
    the bond distances values between the different bonds of the molecule.

    Args:
        comp_dist (bool, optional): If True, the voronoi method will be
            used to compute the bonds before the bond analysis.
        bond_num (bool, optional): Take into account the number of bonds
            of every atom and separate the different distances.

    Returns:
        dict of frozentuples containing the minimum distances between
        different atoms.
    """
    if comp_dist:
        mol.connectivity_search_voronoi()
    package = BondPackage()
    for atom in mol.atoms:
        for connection in atom.connections:
            atom_set = set((connection, atom))
            if atom_set in package:
                continue
            norm = mol.distance(atom, connection, minimum=True, obj=True)
            new_bond = Bond(atom, connection, norm)
            package.bond_add(new_bond)
    return package


def insaturation_matrix(mol, voronoi=False):
    """Generate the insaturation bond matrix for an organic molecule.

    Args:
        mol (:obj`pyRDTP.Molecule`): Organic molecule that will be analyzed to
            create the bond matrix.
        voronoi (bool, optional): If True, a voronoi connectivity analysis
            will be performed before creating the bond matrix. Defaults to
            False.

    Returns:
        :obj`np.ndarray` of size (n_noHatoms, n_noHatoms) containing the bonds
        between different atoms and the insaturations in the diagonal.

    Notes:
        At the moment only works with C and O, discarding the H.
        If Voronoi is True, all the previous bonds will be deleted from the
        molecule.
    """
    if voronoi:
        mol.connection_clear()
        mol.connectivity_search_voronoi()
    not_h = mol.atom_element_filter('H', invert=True)
    bond_mat = np.zeros((len(not_h), len(not_h)), dtype=int)

    for index, atom in enumerate(not_h):
        avail_con = BOND_ORDER[atom.element]
        for connection in atom.connections:
            avail_con -= 1
            if not connection.element == 'H':
                bond_mat[index, not_h.index(connection)] = 1
        bond_mat[index, index] = avail_con
    return bond_mat


def insaturation_solver(bond_mat):
    """Solve the insaturation matrix distributing all the avaliable bonds
    between the different atoms of the matrix.

    bond_mat (:obj`np.ndarray`): Bond matrix containing the information of the
        bonds and insaturations. See insaturation_matrix()  function for
        further information.

    Returns:
        :obj`np.ndarray` containing the insaturation matrix.
    """
    ori_mat = bond_mat.copy()
    new_mat = bond_mat.copy()
    while True:
        for row, value in enumerate(new_mat):
            if [new_mat[row] == 0][0].all():
                continue
            elif new_mat[row, row] == 0:
                new_mat[row] = 0
                new_mat[:, row] = 0
                break
            elif new_mat[row, row] < 0:
                continue
            bool_mat = [value != 0][0]
            bool_mat[row] = False
            if np.sum(bool_mat) == 1:
                col = np.argwhere(bool_mat)[0]
                new_mat[row, row] -= 1
                new_mat[col, col] -= 1
                new_mat[row, col] += 1
                new_mat[col, row] += 1

                ori_mat[row, row] -= 1
                ori_mat[col, col] -= 1
                ori_mat[row, col] += 1
                ori_mat[col, row] += 1
                break
        else:
            break
    return ori_mat


def insaturation_check(mol):
    """Check if all the bonds from an organic molecule are fullfilled.

    Returns:
        True if all the electrons are correctly distributed and False
        if the molecule is a radical.
    """
    bond_mat = insaturation_matrix(mol)
    bond_mat = insaturation_solver(bond_mat)
    return not np.diag(bond_mat).any()


class Bond:
    def __init__(self, atom_1, atom_2, distance):
        self.atoms = frozenset((atom_1, atom_2))
        self.elements = frozenset((atom_1.element, atom_2.element))
        self.distance = distance
        self.bond_order = frozenset(((atom_1.element, len(atom_1.connections)),
                                     (atom_2.element, len(atom_2.connections))))
    def __repr__(self):
        atoms = list(self.atoms)
        rtr_str = '{}({})-{}({}) [{:.4f}]'.format(atoms[0].element,
                                                  len(atoms[0].connections),
                                                  atoms[1].element,
                                                  len(atoms[1].connections),
                                                  self.distance)
        return rtr_str


class BondPackage:
    def __init__(self):
        self.name = None
        self.bonds = []
        self.bond_types = []
        self.bond_elements = {}
        self.orders = {}

    def __contains__(self, item):
        new_set = frozenset(item)
        for sg_bond in self.bonds:
            if sg_bond.atoms == new_set:
                return True
        else:
            return False

    def __getitem__(self, choice):
        if isinstance(choice, int):
            selection = self.bonds[choice]
        elif isinstance(choice, str):
            selection = self.element_search(choice)
        elif isinstance(choice, (list, tuple)):
            selection = self.bond_search(choice)
        return selection

    def __len__(self):
        return len(self.bonds)

    def bond_add(self, bond):
        if isinstance(bond, (list, tuple)):
            for item in bond:
                self._bond_add(item)
        elif isinstance(bond, Bond):
            self._bond_add(bond)
        else:
            raise NotImplementedError

    def _bond_add(self, bond):
        if bond.elements not in self.bond_elements:
            self.bond_elements[bond.elements] = []
        if bond.bond_order not in self.bond_types:
            self.bond_types.append(bond.bond_order)
            self.bond_elements[bond.elements].append(bond.bond_order)
        for atom in bond.atoms:
            element_type = (atom.element, len(atom.connections))
            if atom.element not in self.orders:
                self.orders[atom.element] = []
            elif element_type in self.orders[atom.element]:
                continue
            self.orders[atom.element].append(element_type)
        self.bonds.append(bond)

    def sum_bonds(self, other):
        bonds = other.bonds.copy()
        self.bond_add(bonds)

    def _compute_average(self, sub_pack):
        dist_arr = np.asarray([sg_bond.distance for sg_bond in sub_pack])
        return np.average(dist_arr)

    def type_average(self, elements):
        return np.average(np.asarray([sg_bond for sg_bond in self.bonds if
                                      sg_bond.elements == frozenset(elements)]))

    def element_search(self, element):
        selection = [sg_bond for sg_bond in self.bonds if
                     element in sg_bond.elements]
        return selection

    def element_order_search(self, element_type):
        selection = [sg_bond for sg_bond in self.bonds if
                     element_type in sg_bond.bond_order]
        return selection

    def bond_search(self, elements):
        frz_set = frozenset(elements)
        selection = [sg_bond for sg_bond in self.bonds if
                     frz_set == sg_bond.elements]
        return selection

    def bond_order_search(self, bond_type):
        frz_set = frozenset(bond_type)
        selection = [sg_bond for sg_bond in self.bonds if
                     frz_set == sg_bond.bond_order]
        return selection

    def analysis_element(self):
        rtr_dic = {}
        for key, value in self.orders.items():
            sub_typ = []
            for item in value:
                arr_pvt = self.element_order_search(item)
                sub_typ.append({'order': item,
                                'average': self._compute_average(arr_pvt)})

            avg_el = np.average(np.array([elem['average'] for elem in sub_typ]))
            rtr_dic[key] = {'sub_types': sub_typ,
                            'total_average': avg_el}
        return rtr_dic

    def analysis_bond(self):
        rtr_dic = {}
        for key, value in self.bond_elements.items():
            sub_typ = []
            avg_tot = 0
            for item in value:
                arr_pvt = self.bond_order_search(item)
                lst_pvt = list(item)
                weight = len(arr_pvt)
                sub_typ.append({'elements': lst_pvt,
                                'average': self._compute_average(arr_pvt),
                                'weight': weight})
                avg_tot += weight

            avg_el = np.array([elem['average'] * float(elem['weight'])
                               for elem in sub_typ])
            avg_el = np.sum(avg_el / avg_tot)
            avg_norm = np.average(np.array([elem['average'] for elem in sub_typ]))
            lst_pvt = list(key)
            rtr_dic[key] = {'sub_types': sub_typ,
                            'weighted_average': avg_el,
                            'total_average': avg_norm,
                            'bond_total': avg_tot}
        return rtr_dic
