from graph import *
from graph_io import *
from color_refinement import *

'''
Disjoint union of two graphs
'''


def union(G, H):
    return G + H


'''
Individual color refinement
'''


def ind_ref(D, I, U, vertex_num):
    # if D, I not empty -> color x and y and others 0
    # else color normally
    num = 0

    alpha = color_refinement(D, I, U)

    if is_bijection(U):
        return 1
    if not is_balanced(alpha, vertex_num):
        return 0

    color_class = 0
    for colornum, vertex_list in alpha.items():
        if len(vertex_list) >= 4:
            color_class = colornum
            break

    # TODO:
    # pick x
    # iterate y
    # recursion

    return num


'''
If 2 graphs are discrete
'''


def is_bijection(G):
    list_of_color_nums = []
    for v in G.vertices:
        list_of_color_nums.append(v.color_num)

    list_of_color_nums = sorted(list_of_color_nums)  # sort thee list, so we can compare it to {1,...,k}

    for i in range(len(list_of_color_nums) - 1):
        if list_of_color_nums[i] == list_of_color_nums[i + 1]:
            return False

    return True


'''
If 2 graphs are possibly isomorphic
'''


def is_balanced(alpha, vertex_num):
    for key, val in alpha.items():
        graph1 = 0
        graph2 = 0
        for v in val:
            if v.label // vertex_num == 0:
                graph1 += 1
            else:
                graph2 += 1
        if graph1 != graph2:
            return False
    return True


if __name__ == '__main__':
    G = Graph(False, 4)
    gv = sorted(list(G.vertices), key=lambda v: v.label)
    D = []
    I = []
    D.append(gv[0])
    I.append(gv[1])

    ind_ref(D, I, G, 0)
