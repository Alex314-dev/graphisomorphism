from graph import *
from graph_io import *


def convert_dict_to_list(alpha):
    list_of_lists = []

    sorted_keys = sorted(alpha.keys())

    for key in sorted_keys:
        list_of_lists.append(alpha[key])

    return list_of_lists


def initialization(G):
    alpha = dict()
    i = 0

    for v in G.vertices:
        v.colornum = v.degree
        if v.colornum in alpha.keys():
            alpha[v.colornum].append(v)
        else:
            alpha[v.colornum] = [v]
        # i = max(i, v.degree)

    alpha_list = convert_dict_to_list(alpha)
    return alpha_list


def has_neighbour_in_color_class_i(neighbours, color_class_i):
    for vertex in neighbours:
        if vertex.colornum == color_class_i:
            return True

    return False


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
        if len(C_i_vertices) <= len(new_color_class):
            queue.append(i)
        else:
            queue.append(l)


def update_color(new_color_class, new_color):
    updates_color_vertices_list = []

    for vertex in new_color_class:
        vertex.colornum = new_color
        updates_color_vertices_list.append(vertex)

    return updates_color_vertices_list


def add_new_color(alpha_list, new_color_class, new_color):
    alpha_list.append(update_color(new_color_class, new_color))


def update_alpha_list_and_queue(alpha_list, i, queue, new_color_classes, new_color):
    # 1 color should remain as is
    alpha_list[i] = new_color_classes[0]

    for new_color_class in new_color_classes[1:]:
        add_new_color(alpha_list, new_color_class, new_color)
        update_queue(queue, C_i_vertices=alpha_list[i], new_color_class=alpha_list[-1], i=alpha_list[i][0].colornum,
                     l=new_color)
        new_color += 1  # TODO: IS THAT CORRECT?

    return new_color - 1  # minus 1, since we add 1 one more time after updating the queue


def refine_graph(alpha_list, color_class_i, queue):
    stable = True

    max_color = alpha_list[-1][0].colornum  # the last colorclass

    for i in range(len(alpha_list)):  # TODO: dont iterate through the new added colo_classes
        C_i_vertices = alpha_list[i]

        if C_i_vertices[0].colornum == color_class_i:  # dont compare a class with itself!
            continue

        new_color = max_color + 1  # find the new l
        new_color_classes = {}
        for vertex in C_i_vertices:
            neighbors_with_color_class_i_counter = count_neighbors_with_color_class_i(vertex.neighbours, color_class_i)
            if neighbors_with_color_class_i_counter not in new_color_classes.keys():
                new_color_classes[neighbors_with_color_class_i_counter] = [vertex]
            else:
                new_color_classes[neighbors_with_color_class_i_counter].append(vertex)

        if len(new_color_classes.keys()) > 1:  # 1 if all vertices have same amount of neighbors to color_class_i
            max_color = update_alpha_list_and_queue(alpha_list, i, queue, list(new_color_classes.values()), new_color)
            stable = False  # the graph is still not stable, since a change has occured in this coloring iteration


# initialize queue to have k-1 colors (k=#of colors)
def initialize_queue(alpha_list):
    queue = []
    for i in range(len(alpha_list) - 1):
        queue.append(alpha_list[i][0].colornum)

    return queue


def color_refinement(G: "Graph"):
    alpha_list = initialization(G)
    queue = initialize_queue(alpha_list)  # put the minimum colornum in the queue

    while queue:
        color_class_i = queue[0]
        refine_graph(alpha_list, color_class_i, queue)
        queue = queue[1:]  # Dequeue


def write_graph(G, graph_name):
    if G:
        with open('Colored//{}.dot'.format(graph_name), 'w') as f:
            print("Writing to .dot document...")
            write_dot(G, f)
            print("Done!")

def get_graph_attributes(graph):
    return {'vertices_num': len(graph.vertices), 'edges_num': len(graph.edges), 'is_directed': graph.directed}


def disjoint_union_graphs(graphs_to_union):
    graphs_attributes = []
    G = graphs_to_union[0]
    graphs_attributes.append(get_graph_attributes(G))

    for i in range(1, len(graphs_to_union)):
        graph_to_add = graphs_to_union[i]
        graphs_attributes.append(get_graph_attributes(graph_to_add))
        G = G + graph_to_add

    return G, graphs_attributes


def execute(file_path, graph_name):
    with open(file_path) as f:
        L = load_graph(f, read_list=True)
        graphs = L[0]

        (G, graphs_attributes) = disjoint_union_graphs(L[0])

        color_refinement(G)
        write_graph(G, graph_name + "UNION")

        for count, G in enumerate(graphs):
            color_refinement(G)
            write_graph(G, graph_name + "-" + str(count))


def main():
    graph_name = "colorref_smallexample_4_16"
    file_path = f'sample//{graph_name}.grl'
    execute(file_path, graph_name)

    dict = {'1': [1, 2, 4], '0': [0, 5, 6], '2': [123, 123, 32]}
    print(dict)
    print(convert_dict_to_list(dict))


if __name__ == '__main__':
    main()
