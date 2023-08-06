# pyRDTP

<!-- vim-markdown-toc GitLab -->

	* [The 5+1 W](#the-51-w)
	* [Installation](#installation)
		* [Dependencies](#dependencies)
		* [Manual installation](#manual-installation)
		* [Automatic installation](#automatic-installation)
		* [Jupyter-Lab integration](#jupyter-lab-integration)
	* [Usage](#usage)
		* [Basic usage](#basic-usage)
			* [Reading VASP files](#reading-vasp-files)
			* [Transformations](#transformations)
			* [Merging different molecules](#merging-different-molecules)
			* [Writing VASP files](#writing-vasp-files)
		* [Advanced usage](#advanced-usage)
			* [Graphs](#graphs)
			* [Notebook integration](#notebook-integration)
			* [Scripts](#scripts)
* [Author](#author)

<!-- vim-markdown-toc -->

## The 5+1 W
1. What?
- pyRDTP is a Python library designed to manipulate and analyze chemical geometries mainly for heterogeneous catalysis.
2. Why?
- Some computational chemistry projects involve a large number of species that are connected between them. The main purpose of pyRDTP is to ease the generation of these structures to calculate them with VASP or another software.
3. How?
- pyRDTP contains different packages to transform different formats into molecules and write these objects back into different formats. It also includes different modules that compare, manipulate and analyze these objects. 
4. When?
- Right now! pyRDTP is still in development, but some modules work perfectly at this moment. Moreover, we will tag stable releases for daily usage.
5. Where?
- At Núria López group (ICIQ, Spain). PyRDTP is designed for the daily tasks that every computational chemist in heterogeneous catalysis has to face.
6. Who?
- The weird guy with the blue keyboard. I'm the main developer of these libraries and I `HIGHLY` appreciate the feedback. If you find a bug, or you need to implement some weird algorithm with these libraries, don't hesitate to contact us.

## Installation
### Pip

```console
pip install pyrdtp
```

### Dependencies

pyRDTP need the following libraries to run correctly:
* `networkx`
* `shapely`
* `numpy`
* `scipy`
* `matplotlib`

Additional libraries are required to visualize molecules with Jupyter-Lab:
* `py3Dmol`

### Jupyter-Lab integration

3Dmol is used to see the molecules in Jupyter-Labs, you will need to install 


## Usage


### Basic usage

#### Reading VASP files

To simply read a molecule from a CONTCAR file you will need to use the `geomio`
module from pyRDTP.

```python
from pyRDTP import geomio

mol_1 = geomio.file_to_mol('./CONTCAR', 'contcar')
```

#### Transformations
Then `mol_1` will store all the information from the CONTCAR file into a
`Molecule` object, different methods of `Molecule` can be used, for example you
can remove all the hydrogen atoms from the molecule:

```python
mol_1.atom_remove_by_element('H')
```
You can also specify that you are reading a `Bulk` which has special methods.

For example, imagine that you have an unit cell and want to perform a 3x3x4
expansion and add vacuum:

```python
bulk_1 = geomio.file_to_mol('./POSCAR', 'contcar', bulk=True)
bulk_1.expand(x=3, y=3, z=4)
bulk_1.vacuum_add(distance=12, dimension='z')
```

#### Merging different molecules
Another useful object is the `CatalyticSystem` that allows to set a `Bulk` as
surface and multiple `Molecules` as an unique system:

```python
from pyRDTP.molecule import CatalyticSystem


caty = CatalyticSystem('dummy')
caty.surface_set(bulk_1)
caty.molecule_add(mol_1)
```

`CatalyticSystem` has his own methods, as for example move a molecule
over 2A at the center of 3 atoms:

```python
atoms = caty.surface[[3,6,7]]
caty.move_over_multiple_atoms(mol_1, atoms, distance=3)
```

#### Writing VASP files

Once you finish you can write the new molecule to a POSCAR file:

```python
geomio.mol_to_file(caty, './POSCAR', 'contcar')
```


### Advanced usage

#### Graphs

pyRDTP uses [NetworkX](https://networkx.github.io) to work with graphs. You can
transform any molecule into a graph using the graph module, `voronoi` option
can be used to automatically detect the bonds:

```python
from pyRDTP.operations import graph

grp_1 = graph.generate(mol_1, voronoi=True)
```

You can also plot your graph:

```python

graph.plot(grp)
```

#### Notebook integration

You can use [3Dmol](https://3dmol.csb.pitt.edu) to visualize your molecules in
Jupyter-Lab.  To do so you need to import the `jupyter` module.

```python
from pyRDTP.tools import jupyter

jupyter.show_molecule(mol_1)
```

#### Scripts

A set of scripts is packed inside the libraries. These scripts are prepared to
perform concrete tasks using the command line. They are located inside the
`scripts` folder. Using:

```console
~/pyrdtp/scripts/somescript --help
```

You can see the purpose and the usage of the script.

# Author

Dr. Sergio P. García Carrillo, PostDoc (sp.garcia@utoronto.ca)

# Mantainers 

Santiago Morandi, PhD Student (smorandi@iciq.es), Oliver Loveday, PhD Student (oloveday@iciq.es)
