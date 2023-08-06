from itertools import combinations, product
from .combinations import SystemCombination
import numpy as np

def performance_anhilation(system, substitutions, bonds):
    accepted = [SystemCombination(system, None, None, None)]

    for elem_old, elem_new, numb in substitutions:
        comb_lst = [[] for i in range(numb)]
        equiv_new = [[] for i in range(numb)]
        for conf in accepted:
            atoms_index_lst = conf.structure.atom_element_filter(elem_old,
                                                                 option='index')
            brothers = []
            for comb_numb in range(1, numb + 1):
                comb_array = np.asarray(list(combinations(atoms_index_lst,
                                                          comb_numb)))
                for combination in comb_array:
                    equiv_new[comb_numb-1] = (np.unique(bonds[:, combination, 1], axis=0))
                    comb_pvt = []
                    accepted_pvt = []
                    for equiv_old in comb_lst[comb_numb-1]:
                        for row_old, row_new in product(equiv_old[1:],
                                                        equiv_new[comb_numb-1]):
                            print(row_old, row_new)
                            if np.all(np.isin(row_old, row_new)):
                                print('broken')
                                break
                        else:
                            print('not broken')
                            continue
                        break
                    else:
                        comb_pvt.append(equiv_new[comb_numb-1])
                        new_structure = conf.structure.copy()
                        for subs in equiv_new[comb_numb-1][0]:
                            new_structure.atoms[subs].element = elem_new
                        new_structure = SystemCombination(new_structure, elem_old, elem_new, comb_numb)
                        new_structure.father_add(conf)
                        brothers.append(new_structure)
                        accepted_pvt.append(new_structure)
                    comb_lst[comb_numb-1] += comb_pvt
                    print(comb_lst)

            for family in brothers:
                family.brother_add(brothers)
                family.brothers.remove(family)
        accepted += accepted_pvt
    return accepted

def performance_anhilation_local(system, substitutions, bonds):
    identifier = 0
    accepted = [SystemCombination(system, None, None, None, identifier=identifier)]

    for elem_old, elem_new, numb in substitutions:
        comb_arrays = []
        print(elem_old, elem_new, numb)
        for conf in accepted:
            candidates = []
            atoms_index = conf.structure.atom_element_filter(elem_old,
                                                             option='index')
            elem_arr = conf.structure.elem_array()
            for comb_numb in range(numb):
                print(conf.identifier, len(comb_arrays), len(accepted), end='\r')
                for combination in combinations(atoms_index, comb_numb + 1):
                    expanded = np.unique(bonds[:, combination, 1], axis=0)
                    for subs in expanded:
                        new_arr = np.copy(elem_arr)
                        new_arr[subs] = elem_new
                        for old_array in comb_arrays:
                            if np.all(new_arr == old_array):
                                break
                        else:
                            continue
                        break
                    else:
                        comb_arrays.append(new_arr)
                        new_structure = conf.structure.copy()
                        for subs in combination:
                            new_structure.atoms[subs].element = elem_new
                        identifier += 1
                        new_structure = SystemCombination(new_structure, elem_old, elem_new, comb_numb, identifier=identifier)
                        new_structure.father_add(conf)
                        candidates.append(new_structure)
            accepted += candidates
    return accepted

def performance_anhilation_unique(system, elem_old, elem_new, numb, bonds):
    accepted = [SystemCombination(system, None, None, None)]
    atoms_index = system.atom_element_filter(elem_old,
                                             option='index')
    comb_lst = []
    for combination in combinations(atoms_index, numb):
        print(len(accepted), end='\r')
#        equiv_new = (np.unique(bonds[:, combination, 1], axis=0))
        equiv_new = np.asarray(combination)
        comb_pvt = []
        accepted_pvt = []
        for equiv_old in comb_lst:
            for row_old in equiv_old:
                if np.all(np.isin(row_old, equiv_new)):
                    break
            else:
                continue
            break
        else:
            comb_pvt.append(equiv_new)
            new_structure = system.copy()
            for subs in equiv_new:
                new_structure.atoms[subs].element = elem_new
            new_structure = SystemCombination(new_structure, elem_old, elem_new, numb)
            new_structure.father_add(system)
            accepted_pvt.append(new_structure)
        comb_lst += comb_pvt
        accepted += accepted_pvt
    return accepted

def performance_anhilation_unique2(system, elem_old, elem_new, numb, bonds):
    accepted = [SystemCombination(system, None, None, None)]
    atoms_index = system.atom_element_filter(elem_old,
                                             option='index')
    comb_lst = []
    objective = (len(list(combinations(atoms_index, numb))))
    for combination in combinations(atoms_index, numb):
        equiv_new = (np.unique(bonds[:, combination, 1], axis=0))
        print(objective, len(comb_lst), equiv_new, end='\r')
        for equiv_old in comb_lst:
            for row_old, row_new in product(equiv_old, equiv_new):
                print(row_old, row_new)
                if np.all(np.isin(row_old, row_new, assume_unique=True)):
                    break
            else:
                continue
            break
        else:
            comb_lst.append(equiv_new)

    print('finished, generating structures...')
    for subs in comb_lst:
        new_structure = system.copy()
        for element in subs:
            for item in element:
                new_structure.atoms[item].element = elem_new
        new_structure = SystemCombination(new_structure, elem_old, elem_new, numb)
        new_structure.father_add(system)
        accepted.append(new_structure)

    return accepted

def performance_anhilation_unique3(system, elem_old, elem_new, numb, bonds):
    accepted = [SystemCombination(system, None, None, None)]
    atoms_index = system.atom_element_filter(elem_old,
                                             option='index')
    comb_lst = []
    objective = (np.array(list(combinations(atoms_index, numb))))
    deletion = True
    while len(objective) > 0:
#        print(len(comb_lst)/(len(objective))*100, end='\r')
        comb_lst.append(objective[0])
        equiv_new = (np.unique(bonds[:, objective[0], 1], axis=0))
        for vector in equiv_new:
            objective = np.delete(objective, np.argwhere(np.isin(objective, vector).all(axis=1)), axis=0)

    print('finished, generating structures...')
    for subs in comb_lst:
        new_structure = system.copy()
        for element in subs:
            new_structure.atoms[element].element = elem_new
        new_structure = SystemCombination(new_structure, elem_old, elem_new, numb)
        new_structure.father_add(system)
        accepted.append(new_structure)

    return accepted
