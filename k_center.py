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
        return final_result


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    graph_raw = ['network1.txt', 'network2.txt']
    k = 5
    pre_calculated_optimal_centers = [[3, 11, 13, 20, 26], [1, 11, 15, 22, 30]]
    number_of_iteration = 10
    for i in range(len(graph_raw)):
        file_name = graph_raw[i]
        kcenter = KCenter(file_name)
        # this bruteforce is very slow.
        # I am using the same graph. so I precomputed the optimal centers
        # uncomment if you are using different graph than network1, network2
        # optimal_centers = kmeans.optimal_centers(k=k)

        optimal_centers = pre_calculated_optimal_centers[i]
        print(f"Optimized K means: K = {k}, Graph = {file_name}")
        print("Iteration  |  Avg distance  |  Pi  |                  Poptimal")
        print("-" * 75)
        avg_avg_distance = 0
        for j in range(number_of_iteration):
            centers = kcenter.k_centers(k=k)
            # uncomment following line for visualization
            # kcenter.visualize(centers=centers, optimal_centers=optimal_centers)
            avg_distance = kcenter.avg_distance_from_optimal_center(centers=centers,
                                                                   optimal_centers=optimal_centers)
            avg_avg_distance += avg_distance
            print(f"{j:<11}|  {avg_distance:<14}|  {str(list(centers)):<20}|  {optimal_centers}")

        avg_avg_distance /= number_of_iteration
        print("Average(Avg Distance)) = ", avg_avg_distance)

        print("\n" + "-" * 75)
