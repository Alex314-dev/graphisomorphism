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
            v.colornum = 0
        for x in range(0, len(D)):
            vertexD = D[x]
            vertexI = I[x]
            vertexD.colornum = x + 1
            vertexI.colornum = x + 1
        i = len(D) + 1  # the next available coloring

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
    alpha1 = dict()
    alpha2 = dict()

    for key, val in alpha.items():
        alpha1[key] = list()
        alpha2[key] = list()
        for v in val:
            if v.label // vertex_num == 0:
                alpha1[key].append(v)
            else:
                alpha2[key].append(v)

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
# if __name__ == '__main__':
#     with open("./SignOffColRefBackup/SignOffColRefBackup1.grl") as f:
#         graph_list = read_graph_list(Graph, f)
#     color_refinement_main(graph_list[0])
