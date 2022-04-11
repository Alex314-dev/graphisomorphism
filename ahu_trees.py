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
    visited = [False] * len(G.vertices)
    neighbours = pre_neighbours(G)

    if is_cyclic(G, neighbours, G.vertices[0], visited, None):

        return False

    for i in range(0, len(G.vertices)):
        if not visited[i]:
            return False

    return True


def is_cyclic(G: Graph, neighbours: {Vertex: [Vertex]}, v: Vertex, visited: [bool], parent: Vertex):
    visited[v.label] = True

    for neighbour in neighbours[v]:
        if not visited[neighbour.label]:
            if is_cyclic(G, neighbours, neighbour, visited, v):
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
        # labels = sorted(labels)
        # encoding = ""
        # for label in labels:
        #     encoding += str(label)
        # child.aut = int(encoding)
        # print(child.aut)

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
    print(f"Roots G: {len(g_centers)}")
    u_centers = tree_centers(U, neighbours_u)

    g_root = root_tree(G, g_centers[0], None,  neighbours_g)

    g_encoded = ahu_encoding(g_root)

    for center in u_centers:
        u_root = root_tree(U, center, None, neighbours_u)
        #print(f"Root U: {g_root.label}")
        u_encoded = ahu_encoding(u_root)

        if g_encoded == u_encoded:
            if len(g_centers) > 1:
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
    new_root = Vertex(G, len(G.vertices) + 1, 1)
    G += new_root
    edge1 = Edge(new_root, ex_root1)
    edge2 = Edge(new_root, ex_root2)
    G += edge1
    G += edge2

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
        #print(f"Child {child} of {root} encoding: {child.encoding}")
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

        # neighbours_g = pre_neighbours_id(G)
        #
        # g_centers = tree_centers(G, neighbours_g)
        # g_root = root_tree(G, g_centers[0], None, neighbours_g)
        # g_encoded = ahu_encoding(g_root)
        #root = None
        iso, centers = ahu_iso(G, U)

        return exec_aut(centers, G)
        # print(f"Isomorphic: {iso} \n"
        #       f"Automorphisms: {root.aut}")
        #for v in range(0, len(G.vertices)):
            #print(G.vertices[v].aut)

        #return tree_centers(G, neighbours_g)
        #return is_graph_tree(G)

if __name__ == '__main__':
    print(exec_is_tree(f'bigtrees3'))

