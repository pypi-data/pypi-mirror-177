import pandas as pd
from sklearn.linear_model import LinearRegression

class BensonGroup:
    """Definition of every Benson group consistint in a main atom bonded to
    other atoms.

    Args:
        main (str, optional): Element of the central atom of the group.
            Defaults to None.
        connections (dict of str and ints, optional): dictionary containing
            the other atoms bonded to the central one as the keys and the
            number of bonds as the value.
    """
    def __init__(self, main=None, connections=None):
        self.main = main
        self.connections = connections

    def __str__(self):
        return self.to_str()

    def __eq__(self, other):
        return str(self) == str(other)

    def __hash__(self):
        return hash(self.to_str())

    @classmethod
    def from_atom(cls, atom):
        """Construct a BensonGroup for a single atom and return the new object.

        Args:
            atom (obj:`pyRDTP.molecule.Atom`): Atom object with the pertinent
                connections that will be used as the main element of the group.
        """
        main = atom.element
        connect_dict = {}
        for neighbour in atom.connections:
            if neighbour.element not in connect_dict:
                connect_dict[neighbour.element] = 1
            else:
                connect_dict[neighbour.element] += 1
        return cls(main=main, connections=connect_dict)

    def to_str(self):
        """Convert the BensonGroup into a readable str.

        Retruns:
            str of the form AxByCz where A is the main element, B and C are the
            neighbours and x, y, z are the number of the repetitions of each element.
        """
        ordered_keys = list(self.connections.keys())
        ordered_keys.sort()

        out_str = self.main
        if self.main in ordered_keys:
            ordered_keys.remove(self.main)
            out_str += str(self.connections[self.main] + 1)

        for key in ordered_keys:
            out_str += key
            if self.connections[key] != 1:
                out_str += str(self.connections[key])
        return out_str


class BensonMolecule:
    """Benson molecule type. Contains the groups of a molecule.

    Args:
        molecule (obj:`pyRDTP.molecule.Molecule`, optional): Molecule object
            described in the BensonMolecule object. Defaults to None.
        groups (len of obj:`BensonGroup`, optional): Groups contained in the
            molecule.
        energy (float, opt): Energy of the molecule. Defaults to None.
    """
    def __init__(self, molecule=None, groups=None, energy=None):
        self.molecule = molecule
        self.groups = groups
        self.energy = energy

    def __len__(self):
        return len(self.groups)

    @classmethod
    def from_molecule(cls, molecule, elements=None, voronoi=True, energy=None):
        """Create a BensonMolecule from a current molecule object.

        Args:
            molecule (obj:`pyRDTP.molecule.Molecule`): Molecule object that will
                be converted to a BensonMolecule object
            elements (list of str, optional): List of elements that can be
                computed as the main atom. If None all the elements are possible
                candidates for be the main element of the BensonGroup. Defaults
                to None.
            voronoi (bool, optional): If True, a connectivity search using the
                voronoi method will be performed to the molecule before
                extracting the groups
            energy (float, optional): Energy of the molecule. Defaults to None.

        Returns:
            obj:`BensonMolecule` filled with the molecule and the groups
            calculated for the given molecule.
        """
        new_obj = cls(molecule=molecule.copy(), energy=energy)
        new_obj.extract_groups_from_molecule(elements=elements,
                                             voronoi=voronoi)
        return new_obj

    def extract_groups_from_molecule(self, elements=None, voronoi=False):
        """If molecule attribute is not None, try to extract the BensonGroups
        from the molecule object.

        Args:
            elements (list of str, optional): List of elements that can be
                computed as the main atom. If None all the elements are possible
                candidates for be the main element of the BensonGroup. Defaults
                to None.
            voronoi (bool, optional): If True, a connectivity search using the
                voronoi method will be performed to the molecule before
                extracting the groups. Defaults to True.
        """
        self.groups = {}
        if self.molecule is None:
            raise AttributeError("Molecule Attribute is empty!")

        if voronoi:
            self.molecule.connectivity_search_voronoi()

        if elements is None:
            atom_lst = self.molecule.atoms
        else:
            atom_lst = [atom for atom in self.molecule.atoms if atom.element in
                        elements]

        for atom in atom_lst:
            new_group = str(BensonGroup.from_atom(atom))
            if new_group not in self.groups:
                self.groups[new_group] = 1
            else:
                self.groups[new_group] += 1

    def as_series(self, include_ener=True):
        """Exports the obtained groups and its number into a Pandas Series
        object.

        Args:
            include_ener (bool, optional): If True and the energy of the
                molecule is not None, the energy will be added to the series
                included at the series. Defaults to True.

        Returns:
            obj:`pd.Series` with the labels of the group and the number of
            groups found.

        """
        out_series = pd.Series(self.groups)
        if include_ener and self.energy is not None:
            out_series = out_series.append(pd.Series({'energy': self.energy}))
        return out_series


class BensonPack:
    """Object that contains a group of BensonMolecule and methods to perform
    different analysis to the molecules.

    Args:
        b_molecules (list of obj:`BensonMolecule`): List containing all the
        BensonMolecules that will be analyzed.
    """
    def __init__(self, b_molecules=None):
        self.b_molecules = b_molecules

    def __len__(self):
        return len(self.b_molecules)

    @property
    def dataframe(self):
        return self.as_dataframe()

    @property
    def energies(self):
        df_full = self.as_dataframe()
        return df_full['energy']

    @property
    def groups(self):
        df_full = self.as_dataframe()
        return df_full.loc[:, df_full.columns != 'energy']

    @classmethod
    def from_molecule_list(cls, molecule_lst, elements=None, voronoi=True,
                           energy_lst=None):
        """Create a BensonPack from a list of molecules. The molecules will be
        first converted to a obj:`BensonMolecule`. For more information see
        the BensonMolecule.from_molecule method.

        Args:
            molecule_lst (list of obj:`pyRDTP.molecule.Molecule`): list
                containing all the molecules that will be added to the Pack.
            elements (list of str, optional): List of elements that can be
                computed as the main atom. If None all the elements are possible
                candidates for be the main element of the BensonGroup. Defaults
                to None.
            energy_lst (list of floats): List containing the energy for every
                molecule. If None, the energies of the molecules will not be
                computed. Defaults to None.
            voronoi (bool, optional): If True, a connectivity search using the
                voronoi method will be performed to the molecule before
                extracting the groups. Defaults to True.
        """
        b_molecules_lst = []
        if energy_lst is None:
            energy_lst = [None] * len(molecule_lst)
        for molecule, energy in zip(molecule_lst, energy_lst):
            b_molecule_tmp = BensonMolecule.from_molecule(molecule,
                                                          elements=elements,
                                                          voronoi=voronoi,
                                                          energy=energy)
            b_molecules_lst.append(b_molecule_tmp)
        return cls(b_molecules_lst)

    def as_dataframe(self):
        """Convert all the obj:`BensonMolecules` into a obj:`pd.DataFrame`
        containing the information about the groups and the energy of every
        molecule.

        Returns:
            obj:`pd.DataFrame` with the information contained in the
            obj:`BensonPack`
        """
        series_lst = [b_molecule.as_series() for b_molecule in self.b_molecules]
        out_df = pd.concat(series_lst, axis=1)
        out_df = out_df.fillna(0)
        return out_df.transpose()

    def multi_linear_regression(self):
        """Perform a multilinear with all the groups and the energies from the
        molecules in the pack.
        """
        df_full = self.as_dataframe()
        lin_reg = LinearRegression()
        group_set = df_full.loc[:, df_full.columns != 'energy']
        energy_set = df_full['energy']
        lin_reg.fit(group_set, energy_set)
        return lin_reg
