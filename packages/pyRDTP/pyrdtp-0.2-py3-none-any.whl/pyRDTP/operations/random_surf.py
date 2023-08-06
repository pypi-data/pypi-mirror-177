"""Operations to fill a surface randomly with different molecules. A template
with a simple configuration to use this module can be found in templates
"""
import json
import random
from collections import namedtuple
import numpy as np
from .. import vaspio
from .. import molecule

SEED = None


def parse_molecules(file_loc):
    """Parse the specification file containing the information about the
    parameters in the random generator

    Args:
        file_loc (str): String containg the location of the specifications
            file.

    Returns:
        Namedtuple containing the mol packages, surface and layer used
        in the system.
    """

    with open(file_loc) as jfile:
        data = json.load(jfile)

    global SEED
    SEED = data['seed']

    mol_packages = []
    surf_data = data['surface']
    surface = vaspio.read_from_file_vasp(surf_data['name'], definition='bulk')
    surface.layer_detect_smart()
    surface.connection_search_brute(threshold=surf_data['bond_thresh'],
                                    pbt=surf_data['pbt'])
    for package in data['molecules']:
        mol = vaspio.read_from_file_vasp(package['name'])
        if 'inverse' in package:
            inverse = package['inverse']
        else:
            inverse = None
        tupled = (mol, package['quantity'], package['form'],
                  package['distance'], package['pvector'],
                  package['priority'], inverse)
        mol_packages.append(MolPackage(*tupled))

    System = namedtuple('System', 'mol_pkg surface layer')
    return System(mol_packages, surface, surf_data['layer'])


def prepare_surface_grid(mol_packages, surface, layer):
    """Prepare the surface grid to perform the random filling.

    Args:
        mol_packages (list of :obj`MolPackage`): List containing the molecules
            that will be attached to the system.
        surface (:obj`molecule.Bulk`): Surface in which deploy the molecules.
        layer (int): Number of layer associated to the surface.

    Returns:
        List containing all the atoms of the selected layer and a list
        containing the index of the neighbours of every atom in atoms_slct
        using the index of the first list.

    Notes:
        This grid only considers neighbours in 2 dimensions at the surface.
    """
    neigh_numb = max([len(molecule.pvector) for molecule in mol_packages])
    atoms_slct = [atom for atom in surface.atoms if atom.grid['z'] == layer]
    neigh_atoms = [[] for item in range(neigh_numb)]
    neigh_index = [[] for item in range(neigh_numb)]

    for atom in atoms_slct:
        atoms_pvt = np.asarray([atoms_slct.index(neigh) for neigh
                                in atom.connections if neigh.grid['z'] == layer])
        neigh_index[0].append(atoms_pvt)
        neigh_atoms[0].append([atoms_slct[index] for index in atoms_pvt])

    for distance in range(1, neigh_numb):
        for neigh_pack in neigh_atoms[distance - 1]:
            pvt_atom = []
            pvt_index = []
            for atom_single in neigh_pack:
                for connection in atom_single.connections:
                    pvt_atom.append(connection)
                    pvt_index.append(atoms_slct.index(connection))
            neigh_atoms[distance].append(pvt_atom)
            neigh_index[distance].append(np.asarray(pvt_index))

    Associations = namedtuple('Associations', 'atoms neighbours')

    return Associations(atoms_slct, neigh_index)


def surface_randomize(mol_packages, surface, layer, atoms_slct, neigh_index):
    """ Deploy the selected molecules over the surface using random algorithm.

    Args:
        mol_packages (list of :obj`MolPackage`): List containing the molecules
            that will be attached to the system.
        surface (:obj`molecule.Bulk`): Surface in which deploy the molecules.
        layer (int): Layer number of the surface.
        atoms_slct (list of :obj`molecule.Atom`): List containing the atoms of
            the surface. Generated using the prepare_surface_grid() function.
        neigh_index (list of int): List containing the neighbour of every atom
            in the atoms_slct list

    Returns:
        :obj`molecule.CatalyticSystem` containing the the surface with all the
        molecules deployed.
    """
    random.seed(SEED)

    tower = np.asarray([item.quantity for item in mol_packages])
    tower.sort()
    mol_packages_ord = [pkg for _, pkg in sorted(zip(list(tower), mol_packages))]
    atoms_total = np.sum(tower)
    tower = tower / atoms_total
    tower = np.cumsum(tower[::-1])

    vacants = np.ones(len(atoms_slct), dtype=bool)
    p_vector = np.ones(len(atoms_slct), dtype=float)
    if any(pkg.idistance for pkg in mol_packages_ord):
        p_vector_i = np.ones(len(atoms_slct), dtype=float)

    def tower_obtain():
        rand_numb = random.random()
        for index, item in enumerate(tower):
            if rand_numb <= item:
                return_val = mol_packages_ord[index]
                break

        return return_val

    def vacant_obtain(bridge=False, invert=False):
        avail = np.argwhere(vacants)
        if invert:
            vector_pvt = p_vector_i
        else:
            vector_pvt = p_vector
        while True:
            index = avail[random.randrange(avail.shape[0])][0]
            rand = random.random()
            if vector_pvt[index] >= rand:
                if bridge:
                    neighs = neigh_index[0][index]
                    avail_2 = np.argwhere(vacants[neighs])
                    if np.any(avail_2):
                        index_2 = avail_2[random.randrange(avail_2.shape[0])][0]
                        index_2 = neighs[index_2]
                        if vector_pvt[index_2] >= random.random():
                            vacants[index] = False
                            vacants[index_2] = False
                            return (index, index_2)
                else:
                    vacants[index] = False
                    return index

    def update_p_vec(package, atoms, bridge, invert=False):
        if invert:
            vector_pvt = p_vector_i
        else:
            vector_pvt = p_vector
        if bridge:
            for index, probability in enumerate(package.pvector):
                vector_pvt[neigh_index[index][atoms[0]]] *= probability
                vector_pvt[neigh_index[index][atoms[1]]] *= probability
        else:
            for index, probability in enumerate(package.pvector):
                vector_pvt[neigh_index[index][atoms]] *= probability

    cat_sys = molecule.CatalyticSystem('name')
    cat_sys.surface_set(surface)

    prioritize = [pkg for pkg in mol_packages if pkg.priority > 0]
    prioritize.sort(key=lambda pkg: pkg.priority, reverse=True)

    while atoms_total > 0:
        if prioritize:
            if prioritize[0].quantity == 0:
                prioritize.pop(0)
                continue
            else:
                molecule_pkg = prioritize[0]
                molecule_pkg.quantity -= 1
        else:
            molecule_pkg = tower_obtain()
            if molecule_pkg.quantity == 0:
                continue
            else:
                molecule_pkg.quantity -= 1

        if molecule_pkg.ichange is not None and random.random() < molecule_pkg.ichange:
            invert_bool = True
        else:
            invert_bool = False

        bridge_bool = molecule_pkg.form == 'Bridge'
        vacant_slc = vacant_obtain(bridge=bridge_bool, invert=invert_bool)
        print(vacant_slc)
        update_p_vec(molecule_pkg, vacant_slc, bridge_bool, invert=invert_bool)
        if bridge_bool:
            atom = (atoms_slct[vacant_slc[0]], atoms_slct[vacant_slc[1]])
        else:
            atom = atoms_slct[vacant_slc]

        molecule_pkg.deploy(cat_sys, atom, invert=invert_bool)
        atoms_total -= 1

    return cat_sys


class MolPackage:
    """Class to group the informations of the molecules that will be deployed
    in the surface.

    Args:
        mol (:obj`molecule.Molecule`): Molecule geometry to deploy.
        quantity (int): Quantity of this molecule that will be deployed in the
            surface.
        distance (float): Surface distance from the molecules from the surface
            in angstroms.
        form (str): Type of deployment. At the moment only accepts 'Bridge' for
            a deployment at the middle point between two atoms or 'Top' for a
            deployment over 1 atom.
        pvector (lst or tuple of floats): List containing the probability to a
            neighbour to accept a deployment near to this kind of molecules.
            Every position of the list represent a level of neighbours, being
            the [0] index the nearest neighbours, the [1] item the neighbours
            of the neighbours, etc.
        priority (int, optional): Priority of the deployment. Higher priority
            packages will be deployed first. 0 priority packages will be
            deployed randomly. Defaults to 0.
        inverse (dic, optional): Must contain the keys 'distance' and 'chance'
            for the inverse distance and the cance to invert the molecule.
            Defaults to None.

    Attributes:
        Same as Args.
    """
    def __init__(self, mol, quantity, form, distance, pvector, priority=0, inverse=None):
        self.molecule = mol
        self.quantity = quantity
        self.form = form
        self.distance = distance
        self.pvector = pvector
        self.priority = priority
        if inverse:
            self.idistance = inverse['distance']
            self.ichange = inverse['chance']
            imol = mol.copy()
            imol.invert()
            self._imolecule = imol
        else:
            self.idistance = None
            self.ichange = None

    def deploy(self, system, atom, invert=False):
        """Generates a copy of the molecule attribute and deploy them over a
        surface.

        system (:obj`molecule.CatalyticSystem`): Catalytic system containing
            a surface to deply the molecules.
        atom (:obj`molecule.Atom`): Atom of the surface upside the molecule
            will be deployed.
        invert(bool, optional): If True the molecule will be deployed inverted.
            To perform this operation the package must be initialized with the
            inverse argument. Defaults to false.
        """
        if invert:
            new_mol = self._imolecule.copy()
            distance = self.idistance
        else:
            new_mol = self.molecule.copy()
            distance = self.distance
        system.molecule_add(new_mol)

        if self.form == 'Bridge':
            system.move_over_bridge(new_mol, atom, distance)
        if self.form == 'Top':
            if invert:
                ori = new_mol.find_upper_atom()
            else:
                ori = new_mol.find_lower_atom()
            system.move_over_atom(new_mol, atom, distance, origin=ori.coords)
