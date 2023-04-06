from itertools import chain

import networkx as nx


class Graph:
    def __init__(self, edges):
        self._edges = edges
        self._nodes = set(chain.from_iterable(self._edges))
        self._ngraph = nx.DiGraph()

        self._ngraph.add_nodes_from(self._nodes)

        for a, b in self._edges:
            self._ngraph.add_edge(a, b)

    @property
    def nodes(self):
        return set(self._nodes)

    @property
    def edges(self):
        return self._edges

    def _filter_edges_for_subset_of_nodes(self, subset_of_nodes):
        subset_of_nodes = set(subset_of_nodes)
        filtered_edges = [edge for edge in self.edges if len(subset_of_nodes.intersection(edge))>0]
        return filtered_edges

    def subgraphs(self):
        und_graph = self._ngraph.to_undirected()
        subgraphs_sets = [list(und_graph.subgraph(c).nodes) for c in nx.connected_components(und_graph)]

        res_graph_objs = [Graph(self._filter_edges_for_subset_of_nodes(subgraph_nodes)) for subgraph_nodes in subgraphs_sets]
        res_graph_objs.sort(key=lambda g: len(g.nodes), reverse=True)
        return res_graph_objs

