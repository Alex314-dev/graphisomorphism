from graph import *
from graph_io import *


# def convert_dict_to_list(alpha):
#     list_of_lists = []
#     sorted_keys = sorted(alpha.keys())
#
#     for key in sorted_keys:
#         list_of_lists.append(alpha[key])
#
#     return list_of_lists


def initialization(D, I, G):
    alpha = dict()

    if not len(D):
        for v in G.vertices:
            v.colornum = v.degree
            if v.colornum in alpha.keys():
                alpha[v.colornum].append(v)
            else:
                alpha[v.colornum] = [v]
    else:
        for v in G.vertices:
            v.colornum = 0
        for x in range(0, len(D)):
            D[x].colornum = x + 1
            I[x].colornum = x + 1
        for v in G.vertices:
            if v.colornum in alpha.keys():
                alpha[v.colornum].append(v)
            else:
                alpha[v.colornum] = [v]

    return alpha


# initialize queue to have k-1 colors (k=#of colors), the longest C_i should not be included in the queue!
def initialize_queue(alpha):
    queue = []
    largest_color_class = max(alpha.items(), key=lambda tup: len(tup[1]))[0]

    for color_class in alpha.keys():
        if color_class != largest_color_class:
            queue.append(color_class)

    return queue


def count_neighbors_with_color_class_i(neighbours, color_class_i):
    counter = 0
    for vertex in neighbours:
        if vertex.colornum == color_class_i:
            counter += 1
    return counter


def update_queue(queue, C_i_vertices, new_color_class, i, l):
    if i in queue:
        queue.append(l)
    else:
        if len(C_i_vertices) < len(new_color_class):
            queue.append(i)
        else:
            queue.append(l)


def update_color(new_color_class, new_color):
    for vertex in new_color_class:
        vertex.colornum = new_color


def update_alpha_list_and_queue(alpha, C_i, queue, new_color_classes, new_color):
    # 1 color should remain as is
    alpha[C_i] = new_color_classes[0]

    for new_color_class in new_color_classes[1:]:
        alpha[new_color] = new_color_class
        update_color(new_color_class, new_color)
        update_queue(queue, alpha[C_i], new_color_class, C_i, new_color)
        new_color += 1

    return new_color - 1  # minus 1, since we add 1 one more time after updating the queue


def refine_graph(alpha: {int: ["Vertex"]}, color_class_i: int, queue: [int]):
    max_color = max(list(alpha.keys())) + 1
    keys = list()
    for key in alpha.keys():
        keys.append(key)
    for C_i in keys:  # don't iterate through the newly added color_classes
        if C_i == color_class_i or len(alpha[C_i]) == 1:
            continue

        C_i_vertices = alpha[C_i]
        new_color_classes = dict()
        for vertex in C_i_vertices:
            neighbors_with_color_class_i_counter = count_neighbors_with_color_class_i(vertex.neighbours, color_class_i)
            if neighbors_with_color_class_i_counter not in new_color_classes.keys():
                new_color_classes[neighbors_with_color_class_i_counter] = [vertex]
            else:
                new_color_classes[neighbors_with_color_class_i_counter].append(vertex)

        if len(new_color_classes.keys()) > 1:  # 1 if all vertices have same amount of neighbors to color_class_i
            max_color = update_alpha_list_and_queue(alpha, C_i, queue, list(new_color_classes.values()), max_color)


def color_refinement(D: ["Vertex"], I: ["Vertex"], U: "Graph"):
    alpha = initialization(D, I, U)
    queue = initialize_queue(alpha)

    while queue:
        color_class_i = queue[0]
        refine_graph(alpha, color_class_i, queue)
        queue = queue[1:]  # Dequeue

    return separate_coloring(alpha, len(U.vertices) // 2)


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


# def write_graph(G, graph_name):
#     if G:
#         with open('Colored//{}.dot'.format(graph_name), 'w') as f:
#             print("Writing to .dot document...")
#             write_dot(G, f)
#             print("Done!")
#
#
# def get_graph_attributes(graph):
#     return {'vertices_num': len(graph.vertices), 'edges_num': len(graph.edges), 'is_directed': graph.directed}
#
#
# def disjoint_union_graphs(graphs_to_union):
#     graphs_attributes = []
#     G = graphs_to_union[0]
#     graphs_attributes.append(get_graph_attributes(G))
#
#     for i in range(1, len(graphs_to_union)):
#         graph_to_add = graphs_to_union[i]
#         graphs_attributes.append(get_graph_attributes(graph_to_add))
#         G = G + graph_to_add
#
#     return G, graphs_attributes
#
#
# def execute(file_path, graph_name):
#     with open(file_path) as f:
#         L = load_graph(f, read_list=True)
#         G = L[0][0]
#
#         color_refinement(G)
#         write_graph(G, graph_name)
#
#
# def execute_2(file_path, graph_name):
#     with open(file_path) as f:
#         L = load_graph(f, read_list=True)
#         graphs = L[0]
#
#         (G, graphs_attributes) = disjoint_union_graphs(L[0])
#
#         start = time.time()
#         color_refinement(G)
#         end = time.time()
#         print(f"Time elapsed: {end - start}")
#         write_graph(G, graph_name + "UNION")
#
#         for count, G in enumerate(graphs):
#             color_refinement(G)
#             write_graph(G, graph_name + "-" + str(count))
#
#
# def main():
#     # start = time.time()
#     # graph_name = "threepaths5.gr"
#     # file_path = f'SampleGraphsFastColorRefinement//{graph_name}'
#     # execute(file_path, graph_name)
#     # print(time.time() - start)
#
#     start = time.time()
#     graph_name = "colorref_largeexample_4_1026"
#     file_path = f'sample//{graph_name}.grl'
#     execute_2(file_path, graph_name)
#
#
#
# if __name__ == '__main__':
#     main()
