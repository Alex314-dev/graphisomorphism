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
    print(alpha)

    if not is_balanced(alpha):
        return 0
    if is_bijection(alpha):
        return 1

    color_class = 0
    for colornum, vertex_list in alpha[0].items():
        if len(vertex_list) >= 2:
            color_class = colornum      # the first coloring with more than 4 vertices in `U` ~ TODO: improve
            break

    x = alpha[0][color_class][0]        # the first vertex in G with color `color_class` ~ TODO: improve
    num = 0
    for y in alpha[1][color_class]:     # vertices in H with color `color_class`
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


if __name__ == '__main__':
    G = complete_graph(4)
    H = complete_graph(4)
    U = union(G, H)
    D = list()
    I = list()
    print(ind_ref(D, I, U))
