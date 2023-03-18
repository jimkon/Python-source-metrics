import unittest

import pystruct.utils.graph_structures as gs


class TestGraphs(unittest.TestCase):
    def test_init(self):
        test_edges = [[1, 2], [1, 3], [2, 4]]
        test_graph = gs.Graph(test_edges)

        self.assertEqual(test_graph.nodes, {1, 2, 3, 4})
        self.assertEqual(test_graph.edges, test_edges)

    def test__filter_edges_for_subset_of_nodes(self):
        test_edges = [[1, 2], [1, 3], [2, 4], [5, 6]]
        test_graph = gs.Graph(test_edges)

        result = test_graph._filter_edges_for_subset_of_nodes([1, 5])
        self.assertEqual(result, [[1, 2], [1, 3], [5, 6]])

    def test_subgraphs(self):
        test_edges = [[1, 2], [1, 3], [2, 4], [5, 6]]
        test_graph = gs.Graph(test_edges)

        subgraphs = test_graph.subgraphs()
        self.assertEqual(len(subgraphs), 2)
        self.assertEqual(subgraphs[0].nodes, {1, 2, 3, 4})
        self.assertEqual(subgraphs[0].edges, [[1, 2], [1, 3], [2, 4]])

        self.assertEqual(subgraphs[1].nodes, {5, 6})
        self.assertEqual(subgraphs[1].edges, [[5, 6]])


if __name__ == '__main__':
    unittest.main()
