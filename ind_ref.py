from color_refinement import *

'''
Disjoint union of two graphs
'''


def union(G, H):
    return G + H


'''
Individual color refinement
'''


def ind_ref(D, I, U):
    alpha = color_refinement(D, I, U)

    if not is_balanced(alpha):
        return 0
    if is_bijection(alpha):
        return 1

    color_class = 0
    for colornum, vertex_list in alpha[0].items():
        if len(vertex_list) >= 2:
            color_class = colornum  # the first coloring with more than 4 vertices in `U` ~ TODO: improve
            break

    x = alpha[0][color_class][0]  # the first vertex in G with color `color_class` ~ TODO: improve
    num = 0
    for y in alpha[1][color_class]:  # vertices in H with color `color_class`
        D_ = D + [x]
        I_ = I + [y]
        num = num + ind_ref(D_, I_, U)
    return num


'''
If 2 graphs are discrete
'''


def is_bijection(alpha: [dict]):
    for key in alpha[0].keys():
        if len(alpha[0][key]) != 1:
            return False
    return True


'''
If 2 graphs are possibly isomorphic
'''


def is_balanced(alpha: [dict]):
    for key in alpha[0].keys():
        if len(alpha[0][key]) != len(alpha[1][key]):
            return False
    return True


'''
Testing purposes - K_n
'''


def complete_graph(n: int) -> Graph:
    G = Graph(False, n)
    if n <= 1:
        return G

    gv = sorted(list(G.vertices), key=lambda v: v.label)
    for i in range(0, len(gv)):
        for j in range(i + 1, len(gv)):
            G.add_edge(Edge(gv[i], gv[j]))
    return G


def find_isomorphic_graphs(graphs):
    isomorphic_graphs_groups = []
    group = []  # list of isomorphic graphs

    # the graphs that were already added to groups, should not be compared again to other graphs
    selected = [False] * len(graphs)

    for index_graph1 in range(0, len(graphs) - 1):
        if selected[index_graph1]:
            continue

        group_count_automorphism = 0

        for index_graph2 in range(index_graph1 + 1, len(graphs)):
            if index_graph1 != index_graph2:
                U = graphs[index_graph1] + graphs[index_graph2]
                count_automorphism = ind_ref([], [], U)

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
    print('Sets of possibly isomorphic graphs:')
    for group, count_automorphism in isomorphic_graphs_groups:
        print(sorted(group), count_automorphism)


def exec(file_path):
    with open(file_path) as f:
        L = load_graph(f, read_list=True)
        graphs = L[0]

        isomorphic_graphs_groups = find_isomorphic_graphs(graphs)
        iso_print(isomorphic_graphs_groups)


if __name__ == '__main__':
    graph_name = "wheeljoin14"
    file_path = f'SampleGraphSetBranching//{graph_name}.grl'
    exec(file_path)

"""
    G = complete_graph(5)
    H = complete_graph(5)
    U = union(G, H)
    D = list()
    I = list()
    print(ind_ref(D, I, U))
"""
