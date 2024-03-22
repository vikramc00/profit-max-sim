import networkx as nx
from parse import read_input_file, write_output_file
from utils import is_valid_solution, calculate_score
import sys
from os.path import basename, normpath
import glob
from itertools import islice

def k_shortest_paths(G, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

def isIncluded(paths, op, isEdge):
    if (isEdge):
        for path in paths:
            for n in range(len(path) - 1):
                if path[n] == op[0] and path[n+1] == op[1]:
                    return True

    else:
        for path in paths:
            if op in path:
                return True

    return False



def solve(G):
    """
    Args:
        G: networkx.Graph
    Returns:
        c: list of cities to remove
        k: list of edges to remove
    """
    c, k = 0, 0
    s = 0
    e = len(G.nodes) - 1
    if (len(G.nodes) > 50):
        k = 100
        c = 5
    elif (len(G.nodes) > 30):
        k = 50
        c = 3
    else:
        k = 15
        c = 1

    remove_nodes = []
    remove_weighted_edges = []
    remove_edges = []

    r_n, r_e = c, k
    while r_n > 0 or r_e > 0:
        paths = k_shortest_paths(G, s, e, 8, weight="weight")
        p = nx.shortest_path(G, source=s, target=e)
        edges = []
        nodes = []

        for i in range(len(p) - 1):
            weight = G[p[i]][p[i+1]]["weight"]
            edge = [p[i], p[i+1], weight]
            node = p[i+1]


            if (i != len(p) - 2):
                nodes.append(node)
            edges.append(edge)

        isEdge = -1
        min_Op = -1
        min_Val = float("inf")
        add_Back_Edges = []
        best_heuristic = 0

        for edge in edges:
            heuristic = 0
            for m in range(len(paths)):
                if isIncluded(paths, edge, True):
                    heuristic += (10-m)*50

            if (r_e == 0):
                break
            G.remove_edge(edge[0], edge[1])
            if (not nx.has_path(G, s, e)):
                G.add_edge(edge[0], edge[1], weight = edge[2])
                continue
            if (nx.dijkstra_path_length(G, source=s, target=e) < min_Val or heuristic > best_heuristic):
                if (isEdge == -1):
                    blank = 0
                elif (isEdge):
                    G.add_edge(min_Op[0], min_Op[1], weight = min_Op[2])
                else:
                    G.add_node(min_Op)
                    G.add_weighted_edges_from(add_Back_Edges)
                    add_Back_Edges = []
                isEdge = True
                min_Op = edge
                min_Val = nx.dijkstra_path_length(G, source=s, target=e)
                best_heuristic = heuristic
            else:
                G.add_edge(edge[0], edge[1], weight = edge[2])

        for node in nodes:
            heuristic = 0
            for m in range(len(paths)):
                if isIncluded(paths, node, False):
                    heuristic += (10-m)*50

            if (r_n == 0):
                break
            n_edges = list(G.edges(node))
            for j in range(len(n_edges)):
                n_edge = list(n_edges[j])
                n_edge.append(G[n_edge[0]][n_edge[1]]["weight"])
                n_edges[j] = n_edge

            G.remove_node(node)
            if (not nx.has_path(G, s, e) or not nx.is_connected(G)):
                 G.add_node(node)
                 G.add_weighted_edges_from(n_edges)
                 continue
            if (nx.dijkstra_path_length(G, source=s, target=e) < min_Val or heuristic > best_heuristic):
                if (isEdge == -1):
                    blank = 0
                elif (isEdge):
                    G.add_edge(min_Op[0], min_Op[1], weight = min_Op[2])
                else:
                    G.add_node(min_Op)
                    G.add_weighted_edges_from(add_Back_Edges)
                    add_Back_Edges = []
                isEdge = False
                min_Op = node
                add_Back_Edges.extend(n_edges)
                min_Val = nx.dijkstra_path_length(G, source=s, target=e)
                best_heuristic = heuristic
            else:
                G.add_node(node)
                G.add_weighted_edges_from(n_edges)

        if (isEdge == -1):
            break
        if (isEdge):
            r_e -= 1
            remove_edges.append([min_Op[0], min_Op[1]])
            remove_weighted_edges.append(min_Op)
        else:
            r_n -= 1
            remove_nodes.append(min_Op)
            remove_weighted_edges.extend(add_Back_Edges)

    G.add_nodes_from(remove_nodes)
    G.add_weighted_edges_from(remove_weighted_edges)

    return remove_nodes, remove_edges


# Here's an example of how to run your solver.

# Usage: python3 solver.py test.in

# if __name__ == '__main__':
#     assert len(sys.argv) == 2
#     path = sys.argv[1]
#     G = read_input_file(path)
#     c, k = solve(G)
#     assert is_valid_solution(G, c, k)
#     print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
#     write_output_file(G, c, k, 'outputs/small-1.out')


# For testing a folder of inputs to create a folder of outputs, you can use glob (need to import it)
if __name__ == '__main__':
    inputs = glob.glob('inputs/small/*')
    inputs.extend(glob.glob('inputs/medium/*'))
    inputs.extend(glob.glob('inputs/large/*'))
    # inputs = []
    # inputs.append("inputs/large/large-1.in")
    total = 0
    i = 0
    for input_path in inputs:
        output_path = 'outputs/' + input_path.split("/")[1] + "/" + basename(normpath(input_path))[:-3] + '.out'
        G = read_input_file(input_path)
        c, k = solve(G)
        total += calculate_score(G, c, k)
        i+=1
        print(i)
        print("Shortest Path Difference: {}".format(calculate_score(G, c, k)))
        assert is_valid_solution(G, c, k)
        distance = calculate_score(G, c, k)
        write_output_file(G, c, k, output_path)
    print(total)
