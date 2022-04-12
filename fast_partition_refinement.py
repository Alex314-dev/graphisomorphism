import time
from graph import *
from graph_io import *


def initial_l_coloring(U: "Graph"):     # this function is a menace to human soul, goodness and creativity
    degree_to_Zn = dict()
    unique_degrees = set()
    for v in U.vertices:
        unique_degrees.add(v.degree)
    unique_degrees = list(unique_degrees)
    for d in range(len(unique_degrees)):
        degree_to_Zn[unique_degrees[d]] = d + 1
    for v in U.vertices:
        v.colornum = degree_to_Zn[v.degree]
        v.cdeg = 0
    return len(unique_degrees)


def ind_ref_l_coloring(D, I, U):
    for v in U.vertices:
        v.colornum = 1
        v.cdeg = 0
    for i in range(len(D)):
        D[i].colornum = i + 2
        I[i].colornum = i + 2
    return len(D) + 1


def fast_refinement(D: ["Vertex"], I: ["Vertex"], U: "Graph"):
    # start = time.time()
    C = dict()                                  # Coloring. {int: set(vertex)}
    A = dict()                                  # Adjacent coloring. {int: list(vertex)}
    maxcdeg = dict()                            # Max color degree. {int: int}
    mincdeg = dict()

    if len(D) == 0:
        l = initial_l_coloring(U)
    else:
        l = ind_ref_l_coloring(D, I, U)
    for c in range(1, len(U.vertices) + 1):     # range(1, len(U.vertices) + 1) or range(1, len(U.vertices) // 2 + 1) ?
        C[c] = set()
        A[c] = list()
        maxcdeg[c] = 0
        mincdeg[c] = 0
    for v in U.vertices:
        C[v.colornum].add(v)

    k = l
    s_refine = [i for i in range(1, k + 1)]       # range(1, k) or range(1, k + 1) ?
    colors_adj = set()

    while len(s_refine) != 0:
        r = s_refine.pop()                        # is there any difference in .pop(0) and .pop()
        for v in C[r]:
            for w in v.neighbours:
                w.cdeg = w.cdeg + 1
                if w.cdeg == 1:
                    A[w.colornum].append(w)
                if w.colornum not in colors_adj:
                    colors_adj.add(w.colornum)
                if w.cdeg > maxcdeg[w.colornum]:
                    maxcdeg[w.colornum] = w.cdeg
        # mincdeg = dict()                        # might not be the correct place to define this dict
        for c in colors_adj:
            if len(C[c]) != len(A[c]):
                mincdeg[c] = 0
            else:
                mincdeg[c] = maxcdeg[c]
                for v in A[c]:
                    if v.cdeg < mincdeg[c]:
                        mincdeg[c] = v.cdeg
        colors_split = list()
        for c in colors_adj:
            if mincdeg[c] < maxcdeg[c]:
                colors_split.append(c)
        colors_split.sort()
        for s in colors_split:
            k = split_up_color(s, maxcdeg, mincdeg, C, A, s_refine, k)
        # reset attributes for the next iteration
        for c in colors_adj:
            for v in A[c]:
                v.cdeg = 0
            maxcdeg[c] = 0
            A[c] = list()
        colors_adj = set()

    # print("Coloring time: ", time.time() - start)
    return separate_coloring(C, len(U.vertices) // 2)


def split_up_color(s, maxcdeg, mincdeg, C, A, s_refine, k):
    f = dict()
    numcdeg = dict()
    maxcoldeg = maxcdeg[s]

    for i in range(1, maxcoldeg + 1):
        numcdeg[i] = 0
    numcdeg[0] = len(C[s]) - len(A[s])
    for v in A[s]:
        numcdeg[v.cdeg] = numcdeg[v.cdeg] + 1
    b = 0
    for i in range(1, maxcoldeg + 1):
        if numcdeg[i] > numcdeg[b]:
            b = i
    if s in s_refine:
        in_queue = True
    else:
        in_queue = False
    for i in range(1, maxcoldeg + 1):
        if numcdeg[i] >= 1:
            if i == mincdeg[s]:
                f[i] = s
                if not in_queue and b != i:
                    s_refine.append(f[i])
            else:
                k = k + 1
                f[i] = k
                if in_queue or b != i:
                    s_refine.append(f[i])
    for v in A[s]:
        if f[v.cdeg] != s:
            C[s].remove(v)
            C[f[v.cdeg]].add(v)
            v.colornum = f[v.cdeg]

    return k


def separate_coloring(alpha, vertex_num: int):
    alpha1 = dict()
    alpha2 = dict()

    for key, val in alpha.items():
        if len(val) == 0:
            continue
        alpha1[key] = list()
        alpha2[key] = list()
        for v in val:
            if v.label // vertex_num == 0:
                alpha1[key].append(v)
            else:
                alpha2[key].append(v)

    return [alpha1, alpha2]


# def color_refinement_main(graph_list: ["Graph"]):
#     graph_to_coloring = dict()
#     for i in range(0, len(graph_list)):
#         graph_to_coloring[i] = list()
#
#     G = Graph(False)
#     for g in graph_list:
#         G = G + g
#     vertex_number = len(G.vertices) // len(graph_list)
#     Gv = sorted(list(G.vertices), key=lambda v: v.label)
#
#     fast_refinement([], [], G)
#     for i in range(0, len(Gv)):
#         graph_to_coloring[i // vertex_number].append(Gv[i].colornum)
#     color_refinement_decision(graph_to_coloring)
#
#
# def color_refinement_decision(graph_to_coloring: {int: [int]}):
#     output = (list(), list())
#     skip = list()
#     for i in range(0, len(graph_to_coloring)):
#         if i in skip:
#             continue
#         eq_class = [i]
#         sorted_colors_of_i = sorted(graph_to_coloring[i])
#         isDiscrete = len(set(graph_to_coloring[i])) == len(graph_to_coloring[i])
#         skip.append(i)
#         for j in range(i + 1, len(graph_to_coloring)):
#             if j in skip:
#                 continue
#             if sorted_colors_of_i == sorted(graph_to_coloring[j]):
#                 eq_class.append(j)
#                 skip.append(j)
#         output[0].append(eq_class)
#         output[1].append(isDiscrete)
#     print(output)
#
#
# if __name__ == '__main__':
#     start = time.time()
#     with open("./SampleGraphsFastColorRefinement/threepaths5120.gr") as f:
#         graph_list = read_graph_list(Graph, f)
#     color_refinement_main(graph_list[0])
#     print("Total time: ", time.time() - start)
