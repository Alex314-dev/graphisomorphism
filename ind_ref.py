from fast_partition_refinement import *
from ahu_trees import *
from basicpermutationgroup import *
import collections


global y_to_its_orbits
global X
y_to_its_orbits = dict()
X = list()


def generating_set_x(U):
    global X
    global y_to_its_orbits
    for l in range(len(U.vertices) // 2, len(U.vertices)):
        y_to_its_orbits[l] = set()

    generate_automorphism([], [], U)
    result = order_computation(X)
    X = list()
    return result


def order_computation(permutation: "permutation"):
    nontrivial_found = False
    for p in permutation:
        if not p.istrivial():
            nontrivial_found = True
            break
    if not nontrivial_found:
        return 1
    a = FindNonTrivialOrbit(permutation)
    orb_a = Orbit(permutation, a, False)
    stab_a = Stabilizer(permutation, a)             # I should not just take the length of stab_a
    return order_computation(stab_a) * len(orb_a)   # Orbit-Stabilizer Theorem


# TODO
def membership_test(f: "permutation", generator: ["permutation"]):
    if len(generator) == 0:
        return False
    else:
        a = FindNonTrivialOrbit(generator)
        a = 0 if a is None else a
        orb_transversal = Orbit(generator, a, True)
        orb_a = orb_transversal[0]
        transversal = orb_transversal[1]
        b = f[a]
        if b not in orb_a:
            return False
        else:
            # sifting
            return False


def generate_automorphism(D, I, U):
    global X
    alpha = fast_refinement(D, I, U)

    if not is_balanced(alpha):
        return 0
    if is_bijection(alpha):
        f = create_permutation_f_and_update_orbits(alpha, len(U.vertices) // 2)
        if not membership_test(f, X):
            X.append(f)
        return 1

    color_class = get_color_class(alpha[0])
    x = alpha[0][color_class][0]

    branch_color = alpha[1][color_class]
    # in the below for loop I try to make sure x is mapped to x first
    for v in branch_color:
        if v.label == x.label + len(U.vertices) // 2:
            branch_color.remove(v)
            branch_color = [v] + branch_color
            break
    for y in branch_color:
        D_ = D + [x]
        I_ = I + [y]
        if generate_automorphism(D_, I_, U) == 1:
            # check whether D and I are the same (not D_ and I_ -- this is important).
            # if they are, this is a trivial node and simply continue the for loop
            # if not then return 1 up the chain
            if not D_and_I_are_the_same(D, I, len(U.vertices) // 2):
                return 1
    # should I return 1 here?


def D_and_I_are_the_same(D: ["Vertex"], I: ["Vertex"], mod: int):
    for i in range(len(D)):
        if D[i].label + mod != I[i].label:
            return False
    return True


def create_permutation_f_and_update_orbits(alpha: [{int: ["Vertex"]}], mod: int):
    global y_to_its_orbits
    mapping = [i for i in range(mod)]
    for c in alpha[0].keys():
        mapping[alpha[0][c][0].label] = alpha[1][c][0].label - mod
        y_to_its_orbits[alpha[0][c][0].label + mod].add(alpha[1][c][0].label)
    return permutation(mod, mapping=mapping)


def ind_ref_with_orbit_pruning(D, I, U):
    global y_to_its_orbits
    alpha = fast_refinement(D, I, U)

    if not is_balanced(alpha):
        return 0
    if is_bijection(alpha):
        return 1

    color_class = get_color_class(alpha[0])     # TODO: improve
    x = alpha[0][color_class][0]                # TODO: improve

    y_to_flag = dict()
    for i in range(len(U.vertices) // 2, len(U.vertices)):
        y_to_flag[i] = False
    for y in alpha[1][color_class]:
        if y_to_flag[y.label]:
            continue
        D_ = D + [x]
        I_ = I + [y]
        if ind_ref_with_orbit_pruning(D_, I_, U) == 1:
            # go up the recursion tree and terminate
            return 1
        else:
            for orbit_of_y in y_to_its_orbits[y.label]:
                y_to_flag[orbit_of_y] = True
    return 0


def union(G, H):
    return G + H


def get_color_class(dict_colornum_vertices):
    for colornum, vertex_list in dict_colornum_vertices.items():
        if len(vertex_list) >= 2:
            color_class = colornum

    return color_class  # it is mathematical certainty that `color_class` will be assigned a value


# Branching algorithm with twin pruning.
# The general idea is the same with what was presented in the lecture.
# But we misunderstood something and built a very cool thing. We are not counting twins and comparing them;
# we are storing the twins of all the vertices and if for one of the twins we have computed the automorphism count
# we use that solution for the other twin as well. As the coarsest stable coloring should satisfy the neighbours
# and twins have the same neighbourhood they have to share the automorphism count.
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


def ind_ref_without_twin_pruning(D, I, U):
    alpha = fast_refinement(D, I, U)

    if not is_balanced(alpha):
        return 0
    if is_bijection(alpha):
        return 1

    color_class = get_color_class(alpha[0])     # TODO: improve
    x = alpha[0][color_class][0]                # TODO: improve

    num = 0
    for y in alpha[1][color_class]:              # vertices in the second graph with color `color_class`
        D_ = D + [x]
        I_ = I + [y]
        num = num + ind_ref_without_twin_pruning(D_, I_, U)
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


def deep_graph_copy(G):
    G_ = Graph(False)

    vertex_dict = {}
    for v in G.vertices:
        v_ = Vertex(G_)
        G_.add_vertex(v_)
        vertex_dict[v] = v_
    for e in G.edges:
        head_of_e_ = vertex_dict[e.head]
        tail_of_e_ = vertex_dict[e.tail]
        e_ = Edge(tail_of_e_, head_of_e_)
        G_.add_edge(e_)

    return G_


def find_isomorphic_graphs(graphs, tree_ids):
    isomorphic_graphs_groups = []
    group = []  # list of isomorphic graphs

    # the graphs that were already added to the groups, should not be compared again to other graphs
    selected = [False] * len(graphs)

    for index_graph1 in range(0, len(graphs) - 1):
        if selected[index_graph1] or index_graph1 in tree_ids:
            continue

        group_count_automorphism = generating_set_x(union(graphs[index_graph1], deep_graph_copy(graphs[index_graph1])))

        for index_graph2 in range(index_graph1 + 1, len(graphs)):
            if index_graph2 not in tree_ids and index_graph1 != index_graph2:
                U = union(graphs[index_graph2], graphs[index_graph1])
                iso_test = ind_ref_with_orbit_pruning([], [], U)

                if iso_test:  # if the graphs are isomorphic
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

        isomorphic_graphs_groups, graphs_no_trees = exec_ahu_trees_graphs(graphs)

        if len(graphs_no_trees) > 0:
            print(f"Tree graphs: {graphs_no_trees}\n")

        isomorphic_graphs_groups = isomorphic_graphs_groups + find_isomorphic_graphs(graphs, graphs_no_trees)
        iso_print(isomorphic_graphs_groups)


if __name__ == '__main__':
    start = time.time()

    graph_name = "torus144"
    file_path = f'SampleGraphSetBranching//{graph_name}.grl'
    execute(file_path)

    print(time.time() - start)
