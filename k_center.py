import itertools
import random

import networkx as nx

from graph_mixin import GraphMixin

INF = 10 ** 9


class KCenter(GraphMixin):

    def k_centers(self, k):
        """
        Find approximate K centers in the graph.

        Args:
            k (int): The number of centers to find.

        Returns:
            list: A list of K center nodes.
        """
        final_result = set()
        max_distance = 1

        while True:
            center_nodes = set()
            remaining_nodes = list(self.graph.nodes())
            while len(remaining_nodes) > 0:
                pick = random.choice(remaining_nodes)  # we pick a randon node
                center_nodes.add(pick)
                for node in remaining_nodes:
                    if nx.shortest_path_length(self.graph, source=pick, target=node) <= max_distance:
                        remaining_nodes.remove(node)

            if len(center_nodes) <= k:
                final_result = center_nodes
                break
            else:
                # could not find k center which cover all nodes under the max_distance
                max_distance += 1
        print("Centers: ", *list(center_nodes))
        print("Maximum distance from center to any node: ", self.maximum_distance_from_centers(list(center_nodes)))
        return final_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    kc = KCenter("network1.txt")
    centers = kc.k_centers(k=4)
    optimal_centers = kc.optimal_centers(k=4)
    kc.visualize(centers=centers, optimal_centers=optimal_centers)
