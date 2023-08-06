"""Operations to obtain different combinations of a molecular system.
"""
from itertools import combinations


def conf_defect_create_multiple(system, substitutions, opt='mult'):
    """Given a determined system, create all the possible combinations of its
    atoms.

    Args:
        system (obj:`molecule.Molecule`): Molecule in which the substitutions
            will be performed.
        substitutions (tuple of tuples): Tuple containing tuples of three
            items defining: the element to substitute, the new element and
            the max number of substitutions.
        opt (str, optional) = 'mult' or 'single'. If mult, all the combinations
            of substitutions starting for 1 will be performed using the numb
            value as max value. If single, one single combination will be
            performed with the number of substitutions specified in numb.
            Defaults to mult.
    """
    sys_lst = []
    sys_lst.append(SystemCombination(system, None, None, 0))
    sys_lst[0].identifier = 0
    for elem_old, elem_new, numb in substitutions:
        sys_pvt = []
        for sys_crt in sys_lst:
            sys_bef = conf_defect_create_single(sys_crt.structure, elem_old,
                                                elem_new, numb, opt)
            for sys_child in sys_bef:
                sys_child.father_add(sys_crt)
                sys_crt.sons_add(sys_child)
            sys_pvt += sys_bef
        sys_lst += sys_pvt
    for identifier, conf in enumerate(sys_lst):
        conf.identifier = identifier
    return sys_lst


def conf_defect_create_single(system, elem_old, elem_new, numb, opt='mult'):
    """Given a determined system, substitute all the atoms with a given
    element for another element, extracting all the possible configurations.

    Args:
        system (obj:`molecule.Molecule`): Molecule in which the substitutions
            will be performed.
        elem_old (str): Element that will be replaced.
        elem_new (str): New element to substitute.
        numb (int): Number of substitutions.
        opt (str, optional). 'mult' or 'single'. If mult, all the combination
            of substitutions starting for 1 will be performed using the numb
            value as max value. If single, one single combination will be
            performed with the number of substitutions specified in numb.
    """

    configurations_lst = []
    atoms_index_lst = system.atom_element_filter(elem_old, option='index')
    if opt == 'mult':
        start = 1
    elif opt == 'single':
        start = numb
    else:
        raise NotImplementedError

    for comb_numb in range(start, numb+1):
        for comb_single in combinations(atoms_index_lst, comb_numb):
            mol_new = system.copy()
            for atom_index in comb_single:
                mol_new.atoms[atom_index].element = elem_new

            per_new = SystemCombination(mol_new, elem_old,
                                        elem_new, comb_numb)
            configurations_lst.append(per_new)

    for configuration in configurations_lst:
        brothers = list(configurations_lst)
        brothers.remove(configuration)
        configuration.brother_add(brothers)
        for kindred in configurations_lst:
            if kindred.comb_numb < configuration.comb_numb:
                configuration.brothers_old_add(kindred)

    return configurations_lst


class SystemCombination:
    """ Single combination of a system, containing dependencies and the
    substituted elements. Used to perform AIT combination systems.

    Args:
        structure (obj:`molecule.Molecule`): Structure of the combination.
        elem_old (str): Substituted element.
        elem_new (str): Substitution element.
        combs (int): Number of the combination.
        identifier (int, optional): ID to identify the combination. Defaults
            to None.

    Attributes:
        structure (obj:`molecule.Moledule`): Structure of the combination
        elem_old (str): Substituted element.
        elem_new (str): Substitution element.
        comb_numb (int): Number of the combination.
        father (obj:`SystemCombination`): Father structure of the combination.
        brothers (list of obj:`SystemCombination`): List containing the
            brothers of the combination.)
        identifier (int): ID to identify the combination.
    """

    def __init__(self, structure, elem_old, elem_new, combs, identifier=None):
        self.name = None
        self.structure = structure
        self.elem_old = elem_old
        self.elem_new = elem_new
        self.comb_numb = combs
        self.father = None
        self.sons = []
        self.brothers_old = []
        self.brothers = []
        self.identifier = identifier
        self.denied = False

    def brother_add(self, brother):
        """Add a brother dependency to the current combinations.

        Args:
            brother(obj:`SystemCombination` or lst): Brother combination.
        """
        if isinstance(brother, list):
            self.brothers += brother
        else:
            self.brothers.append(brother)

    def father_add(self, father):
        """Add a father dependency to the current combination.

        Args:
            father(obj:`SystemCombination`): Father combination.
        """
        self.father = father

    def sons_add(self, sons):
        """Add a sons dependency to the current combination.

        Args:
            sons(obj:`SystemCombination` or list): Sons combination.
        """
        if isinstance(sons, (tuple, list)):
            self.sons += sons
        else:
            self.sons.append(sons)

    def brothers_old_add(self, brothers_old):
        """Add old brothers dependency to the current combination.

        Args:
            brothers_old(obj:`SystemCombination` or list): Brothers_old combination.
        """
        if isinstance(brothers_old, (tuple, list)):
            self.sons += brothers_old
        else:
            self.sons.append(brothers_old)

    def dependencies_obtain(self, opt='id'):
        """Returns a tuple containing all the dependencies of the combination.

        Args:
            opt (str, optional): 'obj' or 'id'. If 'obj', the returned
                tuple will contain obj:`SystemCombination`. If 'id',
                the returned tuple will contain the identifiers of the
                dependencies. Defaults to 'id'

        Returns:
            Tuple containing the dependencies of the combination.
        """
        if self.father:
            if opt == 'obj':
                dependencies = [self.father]
            elif opt == 'id':
                dependencies = [self.father.identifier]
        else:
            dependencies = []

        for brother in self.brothers:
            if brother.comb_numb == (self.comb_numb - 1):
                if opt == 'obj':
                    dependencies.append(brother)
                elif opt == 'id':
                    dependencies.append(brother.identifier)
        return tuple(dependencies)

