from fast_partition_refinement import *
# from new_color_refinement import *
from time import time
import collections


def union(G, H):
    return G + H


def get_color_class(dict_colornum_vertices):
    for colornum, vertex_list in dict_colornum_vertices.items():
        if len(vertex_list) >= 2:
            color_class = colornum

    return color_class  # mathematical certainty that it will be assigned a value


def have_common_edge(vertex1, vertex2):
    return vertex1.is_adjacent(vertex2)


def have_same_neighborhood_no_other(vertex1, vertex2):
    neighborhood_vertex1 = vertex1.neighbours
    neighborhood_vertex1.remove(vertex2)
    neighborhood_vertex2 = vertex2.neighbours
    neighborhood_vertex2.remove(vertex1)

    return collections.Counter(neighborhood_vertex1) == collections.Counter(neighborhood_vertex2)


def have_exactly_same_neighborhood(vertex1, vertex2):
    neighborhood_vertex1 = vertex1.neighbours
    neighborhood_vertex2 = vertex2.neighbours

    return collections.Counter(neighborhood_vertex1) == collections.Counter(neighborhood_vertex2)


def are_twins(vertex1, vertex2):
    return have_common_edge(vertex1, vertex2) and have_same_neighborhood_no_other(vertex1, vertex2)


def are_twins_or_false_twins(vertex1: "Vertex", vertex2: "Vertex"):
    return have_exactly_same_neighborhood(vertex1, vertex2) or are_twins(vertex1, vertex2)


# Branching algorithm with twin pruning.
# The general idea is the same with what was presented on the lecture.
# But we misunderstood something and built a very cool thing. We are not counting twins and comparing them;
# we are storing the twins of all the vertices and if for one of the twins if we have computed to automorphism count
# we use that solution for the other twin as well. As the coarsest stable coloring should satisfy the neighbours
# and twins have the same neighbourhood.
def ind_ref(D, I, U, y_to_its_false_twins):
    alpha = fast_refinement(D, I, U)

    if not is_balanced(alpha):
        return 0
    if is_bijection(alpha):
        return 1

    color_class = get_color_class(alpha[0])     # TODO: improve
    x = alpha[0][color_class][0]                # TODO: improve

    y_to_automorphism_count = dict()
    for i in range(len(U.vertices) // 2, len(U.vertices)):
        y_to_automorphism_count[U.vertices[i]] = -1
    num = 0
    for y in alpha[1][color_class]:              # vertices in the second graph with color `color_class`
        if y_to_automorphism_count[y] != -1:
            num = num + y_to_automorphism_count[y]
            continue
        D_ = D + [x]
        I_ = I + [y]
        temp_sol = ind_ref(D_, I_, U, y_to_its_false_twins)
        for twin_of_y in y_to_its_false_twins[y]:
            y_to_automorphism_count[twin_of_y] = temp_sol
        num = num + temp_sol
    return num


def is_bijection(alpha: [dict]):
    for key in alpha[0].keys():
        if len(alpha[0][key]) != 1:
            return False
    return True


def is_balanced(alpha: [dict]):
    for key in alpha[0].keys():
        if len(alpha[0][key]) != len(alpha[1][key]):
            return False
    return True


def build_false_twins(H):
    y_to_its_false_twins = dict()

    for i in range(len(H.vertices) // 2, len(H.vertices)):
        y_to_its_false_twins[H.vertices[i]] = list()

    for i in range(len(H.vertices) // 2, len(H.vertices)):
        for j in range(i + 1, len(H.vertices)):
            if are_twins_or_false_twins(H.vertices[i], H.vertices[j]):
                y_to_its_false_twins[H.vertices[i]].append(H.vertices[j])
                y_to_its_false_twins[H.vertices[j]].append(H.vertices[i])
    return y_to_its_false_twins


def find_isomorphic_graphs(graphs):
    isomorphic_graphs_groups = []
    group = []  # list of isomorphic graphs

    # the graphs that were already added to the groups, should not be compared again to other graphs
    selected = [False] * len(graphs)

    for index_graph1 in range(0, len(graphs) - 1):
        if selected[index_graph1]:
            continue

        group_count_automorphism = 0

        for index_graph2 in range(index_graph1 + 1, len(graphs)):
            if index_graph1 != index_graph2:
                U = graphs[index_graph1] + graphs[index_graph2]
                y_to_its_false_twins = build_false_twins(U)
                count_automorphism = ind_ref([], [], U, y_to_its_false_twins)

                if count_automorphism:  # if the number of automorphisms is more than 0
                    group_count_automorphism = count_automorphism
                    group.append(index_graph2)
                    selected[index_graph2] = True

        if len(group) != 0 and not selected[index_graph1]:
            group.append(index_graph1)
            isomorphic_graphs_groups.append((group, group_count_automorphism))

        group = []

    return isomorphic_graphs_groups


def iso_print(isomorphic_graphs_groups):
    print('Answer:')
    for group, count_automorphism in isomorphic_graphs_groups:
        print(sorted(group), count_automorphism)


def execute(file_path):
    with open(file_path) as f:
        L = load_graph(f, read_list=True)
        graphs = L[0]

        isomorphic_graphs_groups = find_isomorphic_graphs(graphs)
        iso_print(isomorphic_graphs_groups)


if __name__ == '__main__':
    start = time()

    graph_name = "cubes5"
    file_path = f'SampleGraphSetBranching//{graph_name}.grl'
    execute(file_path)

    print(time() - start)
