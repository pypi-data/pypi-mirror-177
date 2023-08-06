"""Implementation of the NetworkX libraries for pyRDTP
"""
import networkx as nx
import matplotlib.pyplot as plt


def generate(mol, voronoi=False):
    """Generate a graph using the given molecule, the connectivity between the
    atoms of the molecule is needed in order to create the graph.

    Args:
        mol (obj:`pyRDTP.molecule.Molecule`): Molecule object that will be used
            to generate the graph.
        voronoi (bool, optional): If True, a Voronoi connectivity search will
            be performed before computing the graph. Defaults to False

    Returns:
        graph (obj:`nx.Graph`) containing the generated graph for the given
        molecule.
    """
    if voronoi:
        mol.connectivity_search_voronoi()

    graph = nx.Graph()
    for atom in mol:
        graph.add_node(atom, elem=atom.element)
        for connection in atom.connections:
            graph.add_edge(atom, connection)
    return graph


def generate_layer(mol, voronoi=False, layer_ax='z'):
    """Works like generate function but splits the different layers creating
    no connection between them

    Args:
        mol (obj:`pyRDTP.molecule.Molecule`): Molecule object that will be used
            to generate the graph.
        voronoi (bool, optional): If True, a Voronoi connectivity search will
            be performed before computing the graph. Defaults to False
        layer_ax (str): Axis of the layer. Defaults to 'z'.

    Returns:
        graph (obj:`nx.Graph`) containing the generated graph for the given
        molecule without taking into account the interlayer connection.
    """
    if voronoi:
        mol.connectivity_search_voronoi()

    graph = nx.Graph()
    for atom in mol:
        for connection in atom.connections:
            if atom.grid[layer_ax] == connection.grid[layer_ax]:
                graph.add_edge(atom, connection)
    return graph


def elem_inf(graph):
    elem_lst = [atom.element for atom in graph.nodes]
    elem_uniq = [elem for numb, elem in enumerate(elem_lst)
                 if elem_lst.index(elem) == numb]
    elem_count = []
    for elem in elem_uniq:
        elem_count.append(elem_lst.count(elem))
    return dict(zip(elem_uniq, elem_count))


def plot(graph):
    """Plot the current graph and show it in interactive mode.

    Args:
        graph (obj:`nx.Graph`): Graph that will be plotted.
    """
    nx.draw(graph)
    plt.show()
