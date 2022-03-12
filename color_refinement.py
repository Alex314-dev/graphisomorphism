from graph import *
from graph_io import *


def color_refinement(D: ["Vertex"], I: ["Vertex"], G: "Graph"):
    prev_i = -1
    i = 0
    alpha = dict()

    if len(D) == 0:
        for v in G.vertices:
            v.colornum = v.degree
            if v.colornum in alpha.keys():
                alpha[v.colornum].append(v)
            else:
                alpha[v.colornum] = [v]
            i = max(i, v.degree)
        i = i + 1  # the next available coloring
    else:
        for v in G.vertices:
            i = max(i, v.colornum)
        for x in range(0, len(D)):
            i = i + 1
            D[x].colornum = i
            I[x].colornum = i
        for v in G.vertices:
            if v.colornum in alpha.keys():
                alpha[v.colornum].append(v)
            else:
                alpha[v.colornum] = [v]
        i = i + 1  # the next available coloring

    while prev_i != i:
        if prev_i != -1:
            update_vertex_coloring(alpha, prev_i)
        alpha_minus_one = alpha.copy()
        prev_i = i
        for colornum, vertices in alpha_minus_one.items():
            if len(vertices) == 1:
                continue

            vertex_neighbourhood = dict()
            for v in vertices:
                vertex_neighbourhood[v] = sorted_neighbour_coloring(v)

            separated = list()
            while len(vertices) != 0:
                eq_class = list()

                if len(vertices) == 1:
                    eq_class.append(vertices[0])
                    separated.append(eq_class)
                    vertices.remove(vertices[0])
                    break

                v = vertices[0]
                eq_class.append(v)
                for j in range(1, len(vertices)):
                    if vertex_neighbourhood[v] == vertex_neighbourhood[vertices[j]]:
                        eq_class.append(vertices[j])
                separated.append(eq_class)

                for v in eq_class:
                    vertices.remove(v)

            alpha[colornum] = separated[0]
            if len(separated) > 1:
                for j in range(1, len(separated)):
                    alpha[i] = separated[j]
                    i = i + 1
    return separate_coloring(alpha, len(G.vertices) // 2)


def separate_coloring(alpha: {int: ["Vertex"]}, vertex_num: int):
    alpha1 = dict() #dictionary to store colornums and their respective vertices for first graph
    alpha2 = dict() #dictionary to store colornums and their respective vertices for second graph

    for key, val in alpha.items(): #iterating through the union graph
        alpha1[key] = list() #every colornum present in the union is assigned as key
        alpha2[key] = list()
        for v in val: #iterate through the vertices
            if v.label // vertex_num == 0: # if the vertix label devided by the number of vertices is 0
                alpha1[key].append(v)  # then vertix is in first graph
            else:
                alpha2[key].append(v)  # otherwise, vertix is in second graph

    return [alpha1, alpha2]


def sorted_neighbour_coloring(v: "Vertex") -> [int]:
    neighbour_coloring = list()
    for n in v.neighbours:
        neighbour_coloring.append(n.colornum)
    return sorted(neighbour_coloring)


def update_vertex_coloring(alpha: {int: ["Vertex"]}, i: int):
    for j in list(filter(lambda x: x >= i, list(alpha.keys()))):
        for v in alpha[j]:
            v.colornum = j


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
#     color_refinement(G)
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
if __name__ == '__main__':
    G = Graph(False, 8)
    H = Graph(False, 8)
    Gv = sorted(list(G.vertices), key=lambda v: v.label)
    Hv = sorted(list(H.vertices), key=lambda v: v.label)
    G.add_edge(Edge(Gv[0], Gv[1]))
    G.add_edge(Edge(Gv[0], Gv[5]))
    G.add_edge(Edge(Gv[0], Gv[2]))
    G.add_edge(Edge(Gv[1], Gv[4]))
    G.add_edge(Edge(Gv[1], Gv[7]))
    G.add_edge(Edge(Gv[2], Gv[3]))
    G.add_edge(Edge(Gv[2], Gv[5]))
    G.add_edge(Edge(Gv[3], Gv[4]))
    G.add_edge(Edge(Gv[3], Gv[6]))
    G.add_edge(Edge(Gv[4], Gv[7]))
    G.add_edge(Edge(Gv[5], Gv[6]))
    G.add_edge(Edge(Gv[6], Gv[7]))
    H.add_edge(Edge(Hv[0], Hv[1]))
    H.add_edge(Edge(Hv[0], Hv[6]))
    H.add_edge(Edge(Hv[0], Hv[7]))
    H.add_edge(Edge(Hv[1], Hv[2]))
    H.add_edge(Edge(Hv[1], Hv[3]))
    H.add_edge(Edge(Hv[2], Hv[3]))
    H.add_edge(Edge(Hv[2], Hv[4]))
    H.add_edge(Edge(Hv[3], Hv[5]))
    H.add_edge(Edge(Hv[4], Hv[5]))
    H.add_edge(Edge(Hv[4], Hv[6]))
    H.add_edge(Edge(Hv[5], Hv[7]))
    H.add_edge(Edge(Hv[6], Hv[7]))
    U = G + H
    print(color_refinement([], [], U))
    Uv = sorted(list(U.vertices), key=lambda v: v.label)
    alpha = color_refinement([Uv[0], Uv[5]], [Uv[8], Uv[15]], U)
    print(alpha)
