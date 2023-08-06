from collections import namedtuple
import numpy as np
import warnings

def lambda_calc(dist, pdist, constraint, mass1, mass2, t_step):
    num = pdist**2 - constraint**2
    den = 4*(mass1**-1 + mass2**-1) * t_step**2 * np.dot(pdist, dist)
    return num/den

class Shake:
    """Perform a constrained molecular dynamic using the verlet integrator and
    the shake algorithm.

    Attributes:
        pairs (list of 2 obj:`pyRDTP.molecule.Atom`): List containing all
            the bonded atom pairs of the molescule.
        dists (obj:`np.ndarray` of size npairs,3,3): Array containing the
            cartesian vectors between all the pairs. First index of the array
            contains the previous step distances, the second index contains
            the actual distances and the third index constains the values
            of the distances for the next step.
        coords (obj:`np.ndarray` of size natoms,3,3): Array containing the
            cartesian coordinates of every molecule.First index of the array
            contains the previous step distances, the second index contains
            the actual distances and the third index constains the values
            of the distances for the next step.
        masses (obj:`np.ndarray` of size natoms,1): Vector containing the
            atomic masses of every atom in the molecule.
        timestep (float): Timestep that will be used by the verlet integrator.
        time (float): Time passed during the molecule dynamic.

    Refs:
        Verlet integrator:
            Verlet, L. Computer “Experiments” on Classical Fluids. I.
            Thermodynamical Properties of Lennard-Jones Molecules. Physical
            Review 1967, 159 (1), 98–103.
            https://doi.org/10.1103/physrev.159.98.
        SHAKE algorithm:
            Ryckaert, J.-P.; Ciccotti, G.; Berendsen, H. J. Numerical
            Integration of the Cartesian Equations of Motion of a System with
            Constraints: Molecular Dynamics of n-Alkanes. Journal of
            Computational Physics 1977, 23 (3), 327–341.
    """
    def __init__(self):
        self.pairs = None
        self.dists = None
        self.coords = None
        self.constraints = None
        self.forces = None
        self.forcefield = None
        self.molecule = None
        self.masses = None
        self.timestep = None
        self.time = 0
        self._lambdas = None
        self._correction = None

    @classmethod
    def from_molecule(cls, mol, pairs=None, constraints='all',
                      forcefield=None):
        """Create a constrained molecular dynamic starting from an
        obj:`pyRDTP.molecule.Molecule`.

        Args:
            mol (obj:`pyRDTP.molecule.Molecule`): Molecule that will be used
                as the starting point in the molecular dynamic.
            pairs (list of lists of 2 ints, optional): List containing the
                index of the pairs. If the list is empty, mol.pairs attribute
                will be used to determine the pairs.
            constraints (obj:`np.ndarray` of size npairs,1, optional): Vector
                of the same size than the number of pairs containing the
                constraint distance for every pair in order. If all, all the
                bonds will be fixed with the initial distances. Defaults to
                all.
            forcefield (func, optional): Function that takes as input an
                obj:`pyRDTP.Molecule.molecule` and returns an obj:`np.nadarray`
                of size natoms,3 with the computed forces for every atom.

        Returns:
            obj:`Shake` enveloping the molecular dynamic.
        """
        # Initialize Shake object
        shk = cls()
        shk.dists = []
        shk.constraints = []

        shk.molecule = mol

        if not all([atom.index is not None for atom in mol.atoms]):
            mol.atom_index()

        if pairs is None:
            shk.pairs = mol.pairs

        # Create forces matrix
        shk.forces = np.zeros((mol.atom_numb, 3), dtype=float)
        shk.coords = np.zeros((3, mol.atom_numb, 3), dtype=float)
        shk.dists = np.zeros((3, len(shk.pairs), 3), dtype=float)
        shk.masses = np.ones(mol.atom_numb)

        if constraints != 'all':
            shk.pairs = np.asarray(constraints)

        shk.coords[[0, 1]] = mol.coords_array(system='cartesian')

        # Compute distances
        dists = []
        for index, pair in enumerate(shk.pairs):
            r_vec = mol.atoms[pair[0]].coords - mol.atoms[pair[1]].coords
            dists = np.linalg.norm(r_vec)

            shk.dists[0:2, index] = r_vec
            shk.constraints.append(dists)

        # Add forfecield
        if forcefield is not None:
            shk.forcefield = forcefield

        shk.constraints = np.asarray(shk.constraints, dtype=float)
        return shk

    def force_change(self, index, vector):
        """Change the force vector associated to a single atom of the
        molecules.

        Args:
            index (int): Index of the atom mol.
            vector (obj:`np.ndarray` of size 1,3): Force vector that will be
                applied to the selected atom.
        """
        self.forces[index] = np.asarray(vector)

    def verlet_step(self):
        """Compute the next coordinates and pair distances and update the
        pertinent matrixes.

        Returns: obj:`np.ndarray` of natoms,3 containing the computed
            coordinates
        """

        step_matrix = np.zeros(self.coords[1].shape, dtype=float)
        step_matrix = (2*self.coords[1] - self.coords[0] +
                       (np.divide(self.forces, self.masses.repeat(3).reshape(self.forces.shape[0], 3)) * self.timestep**2))
        self.coords[2] = step_matrix

        new_dist = -1. * (np.diff(self.coords[2][self.pairs], axis=1))
        self.dists[2] = np.reshape(new_dist, self.dists[0].shape)

        return self.coords[2]

    def lambda_calc(self):
        """Compute the constraint lambdas for the next step

        Returns:
            obj:`np.ndarray` of npairs,3 containing the computed lambdas.
        """
        num = np.linalg.norm(self.dists[2], axis=1)**2 - self.constraints**2
        den = 4 * np.sum(self.masses[self.pairs]**-1, axis=1)
        den *= self.timestep**2
        dots = np.zeros(den.shape)
        for index in range(den.shape[0]):
            dots[index] = np.dot(self.dists[2][index], self.dists[0][index])

        self._lambdas = num/(den*dots)
        return self._lambdas

    def lambda_correct(self):
        """Compute the SHAKE correction for the new coordinates.

        Returns:
            obj:`np.ndarray` of size npairs,2,3 containing the lambda
            correction for all the atoms.
        """
        n_pairs = self.pairs.shape[0]
        corr = self.dists[1] * 2
        corr *= (np.reshape(self._lambdas, (self._lambdas.shape[0], 1))
                 * self.timestep**2)

        sign_mat = np.asarray([[1], [-1]] * n_pairs, dtype=float)
        sign_mat = np.repeat(corr, 2, axis=0) * sign_mat
        sign_mat = np.reshape(sign_mat, [n_pairs, 2, 3])

        self._correction = sign_mat

        return self._correction

    def lambda_apply(self):
        """Apply the lambda correction to the new coordinates and update
        the new coordinates.

        Returns:
            obj:`np.ndarray` of size natoms,3 containing the corrected
            coordinates.
        """
        for index, pair in enumerate(self.pairs):
            self.coords[2][pair[0]] += self._correction[index][0]
            self.coords[2][pair[1]] += self._correction[index][1]
        new_dist = np.diff(self.coords[2][self.pairs], axis=1)
        self.dists[2] = np.reshape(new_dist, self.dists[0].shape)
        self.coords[0] = np.copy(self.coords[1])
        self.dists[0] = np.copy(self.dists[1].copy())
        self.coords[1][self.pairs] = np.copy(self.coords[2][self.pairs])
        self.dists[1] = np.copy(self.dists[2])
        return self.coords[2]

    def lambda_cycle(self):
        """Perform a full lambda cycle, calculating the SHAKE lambdas, the
        given corrections and then applying them to the calculated new
        coordinates.
        """
        self.lambda_calc()
        self.lambda_correct()
        self.lambda_apply()

    def shake_cycle(self, threshold=5, max_steps=5):
        """Perform a full shake cycle, performing a verlet step and then
        calculating the lambda corrections and applying them until the
        constrains are fulfilled.

        Args:
            threshold (int): 10^-x type threshold. Shake cycle will be applied
                until the difference of all the squares of the distances and
                the squares of the constraints are below this threshold.
            max_steps (int): 10^x type. Max lambda steps can be applied before
                the convergence.

        Returns:
            obj:`np.ndarray` vector of size npairs containing the computed
            square deviation between the constraints and the new distances.
        """
        max_steps = 10**max_steps
        thresh = 10**-threshold
        dist_mod = np.linalg.norm(self.dists[2], axis=1)**2
        dist_mod -= self.constraints**2
        step = 0

        while not (abs(dist_mod) < thresh).all():
            self.lambda_cycle()
            dist_mod = np.linalg.norm(self.dists[2], axis=1)**2
            dist_mod -= self.constraints**2
            step += 1
            if step > max_steps:
                print('WARNING')
                warnings.warn('Max number of shake steps reached!')
                break

        return dist_mod

    def full_cycle(self, cycles=1, return_mol=False):
        """Create a generator with a given number of steps that apply the
        Verlet+SHAKE algorithms.

        Args:
            cycles (int, optional): Number of Verlet+SHAKE cycles that the
                generator contains. Defaults to 1.
            return_mol (bool, optional): If True, return a
                obj:`pyRDTP.molecule.Molecule` instead of a new cartesian
                coordinates matrix. Defaults to False.

        Returns:
            Generator that yields: If return_mol is True:
                obj:`pyRDTP.molecule.Molecule` containing the new molecule,
                else: obj:`np.ndarray` of size natoms,3 containing the new
                computed coordinates.
        """
        if self.forcefield is not None:
            self.forces = self.forcefield(self.molecule)
        count = 0
        while count < cycles:
            self.verlet_step()
            self.shake_cycle()
            if return_mol:
                yield self.update_mol(direct=False)
            else:
                self.update_mol(direct=True)
                yield self.coords[1]
            count += 1

    def update_mol(self, direct=False):
        """Update the stored molecule with the actual coords
        """
        self.molecule.coords_update(self.coords[1], system='cartesian')
        if direct:
            self.molecule.coords_convert_update('direct')
        return self.molecule
