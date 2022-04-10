from graph import *
from graph_io import *
from new_color_refinement import pre_neighbours


def pre_neighbours_id(U):
    neighbours = {}
    for vertex in U.vertices:
        neighbours[vertex.label] = vertex.neighbours

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

def root_tree(tree: Graph, center: Vertex):
    return

def ahu_encoding(rooted_tree: Graph):
    return


def ahu_iso(G: Graph, U: Graph):
    neighbours_g = pre_neighbours_id(G)
    neighbours_u = pre_neighbours_id(U)

    g_centers = tree_centers(G, neighbours_g)
    u_centers = tree_centers(U, neighbours_u)

    g_rooted = root_tree(G, g_centers[0])
    g_encoded = ahu_encoding(g_rooted)

    for center in u_centers:
        u_rooted = root_tree(U, center)
        u_encoded = ahu_encoding(u_rooted)

        if g_encoded == u_encoded:
            return True
    return False

def exec_is_tree(file_path):
    with open(f'SampleGraphSetBranching//{file_path}.grl') as f:
        L = load_graph(f, read_list=True)
        G = L[0][0]

        with open(f'Colored//{file_path}.dot', 'w') as d:
             write_dot(G, d)

        neighbours_g = pre_neighbours_id(G)

        return tree_centers(G, neighbours_g)
        #return is_graph_tree(G)

if __name__ == '__main__':
    print(exec_is_tree(f'trees36'))

