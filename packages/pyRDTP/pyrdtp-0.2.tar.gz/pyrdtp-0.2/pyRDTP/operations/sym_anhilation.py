from itertools import combinations
from combinations import SystemCombination
import symmetry
import numpy as np

def performance_anhilation(system, substitutions, bonds):
    origin = SystemCombination(system, None, None, None, identifier=0)
    for elem_old, elem_new, number in substitutions:
        atoms_index_lst = system.atom_element_filter(elem_old, option='index')
        for substitution in range(1, number + 1):
            for comb_single in combinations(atoms_index_lst, comb_numb):

def performance_anhilation_single(system, substitutions, bonds):
    for comb_numb in range(1, substitutions[3] + 1):
        atoms_index_lst = system.atom_element_filter(elem_old, option='index')
        comb_arr = np.asarray(list(combinations(atom_index_lst, comb_numb)))
        eqv_lst = []
        for combination in comb_array:
            equiv_new = append(np.unique(bonds[:, combination, 1], axis=0))
            for equiv_old in comb_lst:
                for row_old in equiv_old[1:]:
                    for row_new in equiv_old[1:]:
                        if not np.all(np.isin(row_old, row_new)):
