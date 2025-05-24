from typing import List, Tuple
import networkx as nx
import random
import logging
import matplotlib.pyplot as plt
from networkx.classes import neighbors

from db import query_for_algorithm

logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')


def generate_random_graph(n):
    """
    Generates a directed graph where each node has an out-degree of 3.

    Parameters:
    n (int): The number of nodes in the graph.

    Returns:
    G (networkx.DiGraph): A directed graph with each node having an out-degree of 3.
    """
    # Create a directed graph
    G = nx.DiGraph()
    G.add_nodes_from(range(n))
    print("1")
    for node in G.nodes():
        # Choose 3 nodes as neighbors
        neighbors = random.sample(list(G.nodes()), 3)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    return G

def generate_from_db():
    """
    Generates a directed graph where each node has an out-degree of 3.

    Parameters:
    n (int): The number of nodes in the graph.

    Returns:
    G (networkx.DiGraph): A directed graph with each node having an out-degree of 3.
    """
    # Create a directed graph
    G = nx.DiGraph()
    neighbor_list = query_for_algorithm.get_student_neighbors()
    G.add_nodes_from(range(1, len(neighbor_list)+1))
    for node in G.nodes():
        # Choose 3 nodes as neighbors
        neighbors = neighbor_list[node-1]
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    return G


def break_into_disjoint_cycles(G):
    """
    Breaks a directed graph into disjoint cycles, ensuring no node appears in more than one cycle.

    Parameters:
    G (networkx.DiGraph): A directed graph.

    Returns:
    list of lists: A list where each sublist is a cycle in the graph.
    """
    print("2")
    # Get all simple cycles in the graph
    logging.debug('Getting all cycles')
    all_cycles = list(nx.simple_cycles(G))

    logging.debug('Sorting cycles')
    # Sort cycles by length (smallest first)
    all_cycles.sort(key=len)

    # To keep track of covered nodes
    covered_nodes = set()
    disjoint_cycles = []
    logging.debug('Breaking into small cycles')
    for cycle in all_cycles:
        # Check if this cycle introduces only new nodes
        if not covered_nodes.intersection(cycle):
            disjoint_cycles.append(cycle)
            covered_nodes.update(cycle)

        # If all nodes are covered, we can stop early
        if covered_nodes == set(G.nodes()):
            break

    return disjoint_cycles


def find_cycle_containing_node(node, cycles):
    """
    Finds the cycle containing the specified node.

    Parameters:
    node: The node to search for.
    cycles (list of lists): A list of cycles, where each cycle is a list of nodes.

    Returns:
    list or None: The cycle containing the node, or None if the node is not in any cycle.
    """
    for cycle in cycles:
        if node in cycle:
            return cycle
    return None


def break_into_subgraphs_with_outdegree(G):
    """
    Breaks a directed graph into subgraphs where each node has an out-degree > 0.

    Parameters:
    G (networkx.DiGraph): A directed graph.

    Returns:
    list of lists: A list where each sublist is a subgraph in the graph.
    """
    visited = set()
    subgraphs = []

    def form_subgraph(start_node):
        subgraph_nodes = set()
        stack = [start_node]

        while stack:
            node = stack.pop()
            if node in visited:
                continue
            visited.add(node)
            subgraph_nodes.add(node)

            # Add neighbors if they have out-degree > 0
            for neighbor in G.successors(node):
                if G.out_degree(neighbor) > 0 and neighbor not in visited:
                    stack.append(neighbor)

        return subgraph_nodes

    for node in G.nodes():
        if node not in visited and G.out_degree(node) > 0:
            subgraph = form_subgraph(node)
            if subgraph:
                subgraphs.append(subgraph)

    return subgraphs


def break_into_cycles(G):
    """
    Breaks a directed graph into cycles, ensuring all nodes are part of a cycle.

    Parameters:
    G (networkx.DiGraph): A directed graph.

    Returns:
    list of lists: A list where each sublist is a cycle in the graph.
    """
    cycles = []
    visited = set()

    def visit(node, path):
        if node in visited:
            return

        path.append(node)
        visited.add(node)

        for neighbor in G.successors(node):
            if neighbor in path:
                # Cycle detected
                cycle_start_index = path.index(neighbor)
                cycles.append(path[cycle_start_index:])
                return
            visit(neighbor, path.copy())

    for node in G.nodes():
        if node not in visited:
            visit(node, [])

    # Ensure all nodes are in some cycle
    covered_nodes = set(node for cycle in cycles for node in cycle)
    if covered_nodes != set(G.nodes()):
        not_in_cycles = set(G.nodes()) - covered_nodes
        for node in not_in_cycles:
            # Append to any existing cycle
            # Just append to the first cycle for simplicity
            cycles[0].append(node)

    return cycles


def is_valid_component(subgraph, remove_invalid=False):
    """ Make sure each node in the subgraph has degOut > 0 """
    for node in subgraph:
        if subgraph.out_degree(node) == 0:
            if remove_invalid:
                subgraph.remove_node(node)

            return False
    return True


def has_cycle(graph):
    try:
        nx.find_cycle(graph)
        return True
    except nx.NetworkXNoCycle:
        return False


def get_components_and_orphands(graph) -> Tuple[List[nx.DiGraph], list]:
    components = []
    remainder_graph = graph.copy()

    while remainder_graph:
        component = None
        logging.debug(f'Nodes: {remainder_graph.nodes()}')
        reachable = {list(remainder_graph.nodes())[0]}
        # Get all the nodes reachable from the reachable nodes
        while True:
            discovered = set()
            for node in reachable:
                neighbors = set(remainder_graph.neighbors(node))
                discovered.update(neighbors)

            reachable.update(discovered)
            subgraph = remainder_graph.subgraph(reachable)
            # Check if there are cycles
            if has_cycle(subgraph):
                # Create subgraph of remainder_graph from reachable
                component = subgraph.copy()
                while not is_valid_component(component, remove_invalid=True):
                    pass
                # Remove the nodes in the new component from the remainder_graph
                remainder_graph.remove_nodes_from(component.nodes())
                components.append(component)
                break

            if not (discovered - reachable):
                # Try to start from a different point
                other_nodes = set(remainder_graph.nodes()) - reachable
                if other_nodes:
                    reachable.update({list(other_nodes)[0]})
                else:
                    # In the case that we were left with a tree in the remainder_graph
                    break
            reachable.update(discovered)
        
        # If we didn't manage to create a component (i.e. left with a tree), we can exit
        if component is None:
            break
    orphands = remainder_graph.nodes()
    return components, list(orphands)

        
def force_not_set(graph, component):
    if isinstance(component, set):
        return graph.subgraph(component).copy()
    return component

def break_into_components(graph):
    # cycles = break_into_cycles(graph)
    components, orphands = get_components_and_orphands(graph)

    logging.debug("Components in the graph:")
    for component in components:
        logging.debug(f'{len(component)}: {component}')

    # subgraphs = break_into_subgraphs_with_outdegree(random_graph)
    # logging.debug("Subgraphs in the graph:")
    # for subgraph in subgraphs:
    #     logging.debug(subgraph)

    # logging.debug("Subgraphs in the graph with orphaned nodes:")
    # for subgraph in subgraphs:
    #     logging.debug(subgraph)

    # Break large cycles apart
    # logging.debug('breaking big components')
    # components = []
    # for cycle in components:
    #     if len(cycle) > 20:
    #         parts = len(cycle) // 10
    #         for i in range(parts):
    #             components.append(cycle[i*10:(i+1)*10])
    #         if len(cycle) - (i+1)*10 > 1:
    #             components.append(cycle[(i+1)*10:])
    #     else:
    #         components.append(cycle)

    logging.debug('Adding orphaned nodes')
    logging.debug(f'Orphands: {orphands}')

    for node in orphands:
        # Components with a neighbor
        neighbor_components = [
            component for neighbor in graph.neighbors(node)
            if (component := next((comp for comp in components if neighbor in comp), None))
        ]

        # Sort components by size (smallest first)
        neighbor_components.sort(key=len)

        if neighbor_components:
            # Add to the smallest component that shares a neighbor
            smallest_component = neighbor_components[0]
            logging.debug(
                f'Smallest component: {smallest_component} ({type(smallest_component)})')
            
            if isinstance(smallest_component, set):
                smallest_component.add(node)
            else:
                smallest_component.add_node(node)
            # smallest_component.add_edge(node, smallest_component.nodes()[0])
        else:
            # If no neighbor components are found, create a new component
            components.append({node})

    # return components
    # Return a List[List[node_value]]
    groups = [list(component) for component in components]
    print(f'{groups=}')
    return groups



def verify_components(components):
    """
    Verifies that a list of components has no nodes that appear in two components.

    Parameters:
    components (list of sets): A list of components, where each component is a set of nodes.

    Returns:
    bool: True if no nodes appear in more than one component, False otherwise.
    """
    all_nodes = set()
    for component in components:
        if (intersection := all_nodes.intersection(component)):
            logging.error(f'{intersection} appears in more than one component')
            return False
        all_nodes.update(component)
    return True


def plot_components(G, components):
    """
    Plots a list of components in a directed graph.

    Parameters:
    G (networkx.DiGraph): The original graph.
    components (list of sets): A list of components, where each component is a set of nodes.
    """
    pos = nx.spring_layout(G)
    for component in components:
        nx.draw_networkx_nodes(G, pos, nodelist=component, node_size=500)
    nx.draw_networkx_edges(G, pos, arrowsize=20)
    nx.draw_networkx_labels(G, pos)
    plt.show()


def count_friends_in_classes(lst_classes, graph):
    """
    For each class, count how many students have at least one friend (edge i -> j)
    within the same class.

    Parameters:
    - lst_classes: List[List[int]], list of final classes with student indices.
    - graph: networkx.DiGraph, where an edge i -> j means j is a friend of i.
    """
    lst = []
    for idx, class_group in enumerate(lst_classes):

        class_set = set(class_group)
        count = 0
        for i in class_group:
            if any(j in class_set for j in graph.successors(i)):
                count += 1
        print(f"Class {idx + 1}: {count} / {len(lst_classes[idx])} student(s) have at least one friend in class")
        lst.append(count/len(lst_classes[idx]))
    return lst


def run_algorithm(num_classes):
    N =100
    left_behind = []
    random_graph = generate_from_db()
    lst_classes = []
    components = break_into_components(random_graph)
    logging.debug("Components in the graph with orphaned nodes added:")
    components.sort(key=len)
    for component in components:
        logging.debug(f'{len(component)}: {component}')

    if not verify_components(components):
        logging.error('Failed to verify components')
    else:
        logging.info('Components verified')
    # plot_components(components)
    for i in range(len(components) - 1, -1, -1):
        comp = components[i]
        if len(comp) > N // num_classes:
            lst_classes.append(comp[:N // num_classes])
            left_behind.extend(comp[N // num_classes:])
        else:
            left_behind.extend(comp)

    # Group leftover elements into valid class sizes
    while len(left_behind) >= N // num_classes:
        lst_classes.append(left_behind[:N // num_classes])
        left_behind = left_behind[N // num_classes:]

    # If any are left (and not enough for a full group), just append them as one last group
    if left_behind:
        for i in range(len(left_behind)):
            lst_classes[i%num_classes].append(left_behind[i])

    print(lst_classes)
    lst_present = count_friends_in_classes(lst_classes, random_graph)
    return lst_classes, lst_present
    # Generate a random graph
    random_graph = generate_from_db()

    cycles = break_into_cycles(random_graph)
    # cycles = break_into_disjoint_cycles(random_graph)
    logging.debug("Cycles in the graph:")
    for cycle in cycles:
        logging.debug(cycle)

    # subgraphs = break_into_subgraphs_with_outdegree(random_graph)
    # logging.debug("Subgraphs in the graph:")
    # for subgraph in subgraphs:
    #     logging.debug(subgraph)

    # logging.debug("Subgraphs in the graph with orphaned nodes:")
    # for subgraph in subgraphs:
    #     logging.debug(subgraph)

    # Break large cycles apart
    logging.debug('breaking cycles')
    components = []
    for cycle in cycles:
        if len(cycle) > 20:
            parts = len(cycle) // 10
            for i in range(parts):
                components.append(cycle[i*10:(i+1)*10])
            if len(cycle) - (i+1)*10 > 1:
                components.append(cycle[(i+1)*10:])
        else:
            components.append(cycle)

    logging.debug('Adding orphaned nodes')
    not_in_components = set(random_graph.nodes()) - \
        set(node for component in components for node in component)

    for node in not_in_components:
        # Components with a neighbor
        neighbor_components = [
            component for neighbor in random_graph.neighbors(node)
            if (component := next((comp for comp in components if neighbor in comp), None))
        ]

        # Sort components by size (smallest first)
        neighbor_components.sort(key=len)

        if neighbor_components:
            # Add to the smallest component that shares a neighbor
            smallest_component = neighbor_components[0]
            smallest_component.add(node)
        else:
            # If no neighbor components are found, create a new component
            components.append({node})

    logging.debug("Components in the graph with orphaned nodes added:")
    components.sort(key=len)
    for component in components:
        logging.debug(f'{len(component)}: {component}')


