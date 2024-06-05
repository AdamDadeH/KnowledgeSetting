import networkx as nx

from concept_store.concept_graph_store import ConceptGraph
from concept_store.concept_store import ConceptStore


class NxConceptGraph(ConceptGraph):
    """
    Internal representation content dependencies.

    The content forms a directed acyclic graph with edges
    defined by dependencies between content.

    Note : The dependencies are currently unlabelled, but is
    meaningful to define types of relationships.
    """

    def __init__(self, dependency_graph: nx.DiGraph = None, node_list=None):
        """
        Includes possibility of disconnected nodes - or where node_list is
        distinct from nodes in dependency_graph.

        :param dependency_graph:
        :param node_list:
        """
        if dependency_graph is None:
            dependency_graph = nx.DiGraph()
        self.dependency_graph = dependency_graph

        if node_list is None:
            node_list = list(dependency_graph)
        self.node_list = node_list

    def add_relation(self, source, target):
        self.dependency_graph.add_edge(target, source)

    def get_source_content(self):
        """
        Return keys to Content with no dependencies.
        :return: List of keys
        """
        return [k for (k, v) in self.dependency_graph.in_degree if v == 0]

    def usage_count(self):
        """
        Counts of usages
        :return:
        """
        return self.dependency_graph.out_degree

    def disconnected_nodes(self):
        """
        Find any disconnected nodes
        :return:
        """
        disconnected = []
        for k in self.node_list:
            if k not in self.dependency_graph:
                disconnected.append(k)
        return disconnected

    def get_minimum_requirements(self, target_nodes):
        """
        Given a list of `target_nodes` - generate all dependencies / requirements
        for those nodes.

        :param target_nodes: List of targets.
        :return:
        """
        if len(target_nodes) == 0:
            return []
        required = set(target_nodes)
        for target in target_nodes:
            required = required.union(nx.ancestors(self.dependency_graph, target))
        return required

    def subset_by_targets(self, target_nodes):
        """
        Get all dependencies for transform and rebuild DAG.
        :param target_nodes:
        :return:
        """
        if len(target_nodes) == 0:
            return self
        requirements = self.get_minimum_requirements(target_nodes)
        to_remove = set(self.node_list) - set(requirements)
        new_graph = self.dependency_graph.copy(as_view=False)
        new_graph.remove_nodes_from(to_remove)
        return NxConceptGraph(new_graph, set(requirements))

    def get_unique_ancestors_subgraph(self, sources, targets):
        # Set to store unique ancestors of targets not shared with sources
        unique_ancestors = set(targets)  # Start with targets as they should be in the subgraph
        exclude_ancestors = set()

        # Get all ancestors for each transform and source
        for target in targets:
            unique_ancestors.update(nx.ancestors(self.dependency_graph, target))
        for source in sources:
            exclude_ancestors.update(nx.ancestors(self.dependency_graph, source))

        # Remove excluded ancestors from the unique ancestors
        valid_nodes = unique_ancestors - exclude_ancestors
        print(valid_nodes)
        subgraph = nx.DiGraph()
        for node in valid_nodes:
            if node in self.dependency_graph:
                # Add the node and its attributes
                subgraph.add_node(node, **self.dependency_graph.nodes[node])
                # Add relevant edges with attributes
                for u, v, attrs in self.dependency_graph.out_edges(node, data=True):
                    if v in valid_nodes:
                        subgraph.add_edge(u, v, **attrs)

        return subgraph

    def subset_by_known_and_goals(self, known_nodes, goal_nodes):
        """
        Does not work - we lose access to notations needed for dependencies
        we cannot throw away the others - but we can hide them from view.
        :param known_nodes:
        :param goal_nodes:
        :return:
        """
        new_graph = self.subset_by_targets(goal_nodes)
        satisfied = self.get_minimum_requirements(known_nodes)
        new_graph.dependency_graph.remove_nodes_from(satisfied)
        return NxConceptGraph(new_graph.dependency_graph, new_graph.node_list)
