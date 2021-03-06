import time

from graph import *
from graph_io import *
import math


def pre_neighbours_id(U):
    neighbours = {}
    for vertex in U.vertices:
        neighbours[vertex.label] = vertex.neighbours

    return neighbours


def pre_neighbours(U):
    neighbours = {}
    for vertex in U.vertices:
        neighbours[vertex] = vertex.neighbours

    return neighbours


def is_graph_tree(G: Graph):
    visited = [0] * len(G.vertices)
    neighbours = pre_neighbours(G)

    if has_cycles(G, neighbours, G.vertices[0], visited, None):

        return False

    for v_id in range(0, len(G.vertices)):
        if not visited[v_id]:
            return False

    return True


def has_cycles(G: Graph, neighbours: {Vertex: [Vertex]}, v: Vertex, visited: [bool], parent: Vertex):
    visited[v.label] = 1

    for neighbour in neighbours[v]:
        if not visited[neighbour.label]:
            if has_cycles(G, neighbours, neighbour, visited, v):
                return True
        elif parent is not None and neighbour.label != parent.label:
            return True
    return False


def tree_centers(tree: Graph, neighbours: {Vertex: [Vertex]}):
    incidence = [0] * len(tree.vertices)
    leaves = []

    for vertex in tree.vertices:
        v_id = vertex.label
        incidence[v_id] = vertex.degree
        if incidence[v_id] == 0 or incidence[v_id] == 1:
            leaves.append(vertex)
            incidence[v_id] == 0
    visited_vertices = len(leaves)

    while visited_vertices < len(tree.vertices):
        leaves1 = []
        for leaf_node in leaves:
            for neighbour in neighbours[leaf_node.label]:
                n_id = neighbour.label
                incidence[n_id] -= 1
                if incidence[n_id] == 1:
                    leaves1.append(neighbour)

            incidence[leaf_node.label] == 0
        visited_vertices += len(leaves1)
        leaves = leaves1

    return leaves


def root_tree(tree: Graph, center: Vertex, parent: Vertex, neighbours: {Vertex: [Vertex]}):
    center.parent = None
    center.children = []

    for neighbour in neighbours[center.label]:
        if parent is not None and neighbour.label == parent.label:
            continue
        neighbour.parent = center
        neighbour.children = []
        center.children.append(neighbour)
        root_tree(tree, neighbour, center, neighbours)
    return center


def ahu_encoding(root: Vertex):
    if root is None:
        return ""
    labels = []

    for child in root.children:
        labels.append(ahu_encoding(child))

    labels = sorted(labels)

    result = ""
    for label in labels:
        result += str(label)

    encoding = int(f"1{result}0")
    root.encoding = encoding
    return encoding


def ahu_iso(G: Graph, U: Graph):
    neighbours_g = pre_neighbours_id(G)
    neighbours_u = pre_neighbours_id(U)

    g_centers = tree_centers(G, neighbours_g)

    u_centers = tree_centers(U, neighbours_u)

    g_root = root_tree(G, g_centers[0], None,  neighbours_g)

    g_encoded = ahu_encoding(g_root)

    for center in u_centers:
        u_root = root_tree(U, center, None, neighbours_u)
        u_encoded = ahu_encoding(u_root)

        if g_encoded == u_encoded:
            return True, g_centers

    return False, g_centers


def exec_aut(centers: [Vertex], G: Graph):
    root = None
    if len(centers) > 1:
        edges = centers[0].incidence
        for edge in edges:
            if edge.other_end(centers[0]) is centers[1]:
                root = create_new_root(G, centers[0], centers[1], edge)
    else:
        root = centers[0]

    aut_trees(root)
    return root.aut


def create_new_root(G, ex_root1, ex_root2, root_bridge):
    new_root = Vertex(G, len(G.vertices), 1)
    G += new_root
    edge1 = Edge(new_root, ex_root1)
    edge2 = Edge(new_root, ex_root2)
    G += edge1
    G += edge2

    G.del_edge(root_bridge)

    new_root.children = [ex_root1, ex_root2]
    new_root.parent = None
    ex_root1.parent = new_root
    ex_root2.parent = new_root

    if ex_root2 in ex_root1.children:
        ex_root1.children.remove(ex_root2)

    if ex_root1 in ex_root2.children:
        ex_root2.children.remove(ex_root1)

    return new_root


def aut_trees(root: Vertex):
    aut, leaves = 1, 0

    root_classification = {}

    for child in root.children:

        child_enc = child.encoding
        if child_enc != 10:
            if child_enc not in root_classification.keys():
                root_classification[child_enc] = [child]
            else:
                root_classification[child_enc].append(child)
        else:
            leaves += 1

    for child_enc, roots in root_classification.items():
        multiplicty = len(roots)
        aut *= math.factorial(len(roots)) * (aut_trees(roots[0]) ** len(roots))

    root.aut = aut
    return math.factorial(leaves) * aut


def exec_is_tree(file_path):
    with open(f'SampleGraphSetBranching//{file_path}.grl') as f:
        L = load_graph(f, read_list=True)
        G = L[0][0]
        U = L[0][2]

        with open(f'Colored//{file_path}.dot', 'w') as d:
             write_dot(G, d)

        if is_graph_tree(G):
            return True, G, U
        else:
            return False, G, U


def exec_ahu_trees_pair(G, H):
    iso, centers = ahu_iso(G, H)
    if iso:
        return iso, exec_aut(centers, G)
    else:
        return iso, 0


#does not include an is_tree check for the graphs
#inludes printing
def exec_ahu_trees_file(file_path):
    with open(file_path) as f:
        L = load_graph(f, read_list=True)
        graphs = L[0]

        iso_groups = {}
        auto_list = []
        for g_id in range(0, len(graphs)):
            for h_id in range(g_id + 1, len(graphs)):
                G = graphs[g_id]
                H = graphs[h_id]

                iso, auto = exec_ahu_trees_pair(G, H)

                if iso:
                    graph_already_iso_bool, group = graph_already_iso(g_id, iso_groups.values())
                    if not graph_already_iso_bool and g_id not in iso_groups.keys():
                        iso_groups[g_id] = [h_id]
                        auto_list.append(auto)

                    elif g_id in iso_groups.keys():
                        iso_groups[g_id].append(h_id)
                    else:
                        key = list(iso_groups.keys())[list(iso_groups.values()).index(group)]
                        iso_groups[key].append(h_id)

        print("Isomorphic groups of tree graphs:")
        i = 0
        for key, value in iso_groups.items():
            print_iso_groups(key, value, auto_list, i)
            i += 1


#includes is_tree check
#does not include printing
def exec_ahu_trees_graphs(graphs):
    iso_groups = {}
    auto_list = []
    graphs_id_to_remove = []
    for g_id in range(0, len(graphs)):
        for h_id in range(g_id + 1, len(graphs)):
            G = graphs[g_id]
            H = graphs[h_id]

            if is_graph_tree(G) and is_graph_tree(H):

                iso, auto = exec_ahu_trees_pair(G, H)

                if iso:
                    graph_already_iso_bool_g, group = graph_already_iso(g_id, iso_groups.values())

                    if not graph_already_iso_bool_g and g_id not in iso_groups.keys():
                        iso_groups[g_id] = [h_id]
                        graphs_id_to_remove.append(g_id)
                        graphs_id_to_remove.append(h_id)
                        auto_list.append(auto)

                    elif g_id in iso_groups.keys():
                        iso_groups[g_id].append(h_id)
                        graphs_id_to_remove.append(h_id)
                    else:
                        key = list(iso_groups.keys())[list(iso_groups.values()).index(group)]
                        if not graph_already_iso_value(h_id, iso_groups[key]):
                            iso_groups[key].append(h_id)
                            graphs_id_to_remove.append(h_id)

            elif is_graph_tree(G) and g_id not in graphs_id_to_remove:
                graphs_id_to_remove.append(g_id)

            elif is_graph_tree(H) and h_id not in graphs_id_to_remove:
                graphs_id_to_remove.append(h_id)

    if len(iso_groups.keys()) != 0:
        isomorphic_graphs_groups = []

        i = 0
        for key, value in iso_groups.items():
            iso_group_auto_tuple = tuple_creator(key, value, auto_list, i)
            isomorphic_graphs_groups.append(iso_group_auto_tuple)
            i += 1

        return isomorphic_graphs_groups, graphs_id_to_remove
    return [], graphs_id_to_remove


def graph_already_iso_value(h_id: int, values: [int]):
    return h_id in values


def tuple_creator(key: int, values: [int], auto_list: [int], i: int):
    iso_group = [key]

    for value in values:
        iso_group.append(value)

    iso_group_auto_tuple = (iso_group, auto_list[i])

    return iso_group_auto_tuple


def print_iso_groups(key: int, values: [int], auto_list: [int], i: int):
    values_str = ""
    for value in values:
        values_str += f', {str(value)}'
    print(f"[{key}{values_str}] automorphisms: {auto_list[i]}")


def graph_already_iso(g_id: int, iso_graphs: [[int]]):
    for groups in iso_graphs:
        if g_id in groups:
            return True, groups
    return False, []


def exec_ahu_trees_2_graphs(file_path):
    with open(file_path) as f:
        L = load_graph(f, read_list=True)
        graphs = L[0]
        G = graphs[1]
        H = graphs[5]

        iso, auto = exec_ahu_trees_pair(G, H)
        print(auto)


if __name__ == '__main__':
    #exec_ahu_trees_file(f'SampleGraphSetBranching//bigtrees3.grl')
    exec_ahu_trees_graphs()

