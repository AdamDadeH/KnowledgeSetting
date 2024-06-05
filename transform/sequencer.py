import networkx as nx
import numpy as np
from collections import deque

from transform.transform import BaseRenderer


class Sequencer(BaseRenderer):

    def __init__(self, keep_disconnected=True):
        self.keep_disconnected = keep_disconnected

    def execute(self, content_dag):
        topological_ordered = list(nx.topological_sort(content_dag))
        if self.keep_disconnected:
            print("Keeping disconnected")
            return topological_ordered
            # + content_dag.disconnected_nodes()
        else:
            print("Discard disconnected")
            return topological_ordered

class SpectralSortSequencer(BaseRenderer):
    def execute(self, content_dag):

        spectral_order = self.spectral_sequence(content_dag)
        final_order = self.adjust_for_dependencies(spectral_order, content_dag)
        return final_order

    def spectral_sequence(self, graph):
        # Convert to undirected for spectral purposes
        undirected_graph = graph.to_undirected()
        laplacian = nx.laplacian_matrix(undirected_graph).toarray()
        eigenvalues, eigenvectors = np.linalg.eigh(laplacian)
        # Using the Fiedler vector
        fiedler_vector = eigenvectors[:, 1]
        nodes = list(graph.nodes())
        spectral_order = sorted(nodes, key=lambda n: fiedler_vector[nodes.index(n)])
        return spectral_order


    def adjust_for_dependencies(self, spectral_order, graph):
        adjusted_order = []
        queue = deque(spectral_order)  # Start with the spectral order in a queue
        placed = set()  # Set to track placed nodes

        while queue:
            node = queue.popleft()
            # Check if all predecessors have been placed
            if all(pred in placed for pred in graph.predecessors(node)):
                adjusted_order.append(node)
                placed.add(node)
            else:
                queue.append(node)  # Requeue the node to try again later

        return adjusted_order

    def handle_disconnected(self, ordered, content_dag):
        if self.keep_disconnected:
            disconnected_nodes = [node for node in nx.isolates(content_dag)]
            print("Keeping disconnected")
            return ordered + disconnected_nodes
        else:
            print("Discard disconnected")
            return ordered