import random
from collections import defaultdict

import networkx as nx

from graph_mixin import GraphMixin

INF = 10 ** 9


class KMeans(GraphMixin):

    def k_means_partion_helper(self, d, centers, k):
        cluster = defaultdict(lambda: [])
        for v in self.graph.nodes():
            min_center, min_center_dist = INF, INF
            for i in range(k):
                if d[v][centers[i]] < min_center_dist:
                    min_center, min_center_dist = centers[i], d[v][centers[i]]
            cluster[min_center].append(v)

        return cluster

    def k_means_optimized(self, k):
        n = self.graph.number_of_nodes()
        d = [[0] * n for _ in range(n)]
        all_pair_shortest_path = dict(nx.all_pairs_shortest_path_length(self.graph))
        for u, paths in all_pair_shortest_path.items():
            for v, distance in paths.items():
                d[u][v] = distance

        random_node = random.choice(list(self.graph.nodes()))
        centers = [random_node]  # initial 1 center
        cluster = None
        for ki in range(1, k+1):
            cluster = self.k_means_partion_helper(d, centers, ki)
            centers = list(cluster.keys())
            g_target, g_target_distance = -1, 0
            for center_p in centers:
                neighbors = cluster[center_p]
                for v in neighbors:
                    if d[center_p][v] >= g_target_distance:
                        g_target_distance = d[center_p][v]
                        g_target = v

            centers.append(g_target)

        return cluster


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    graph_raw = ['network1.txt', 'network2.txt']
    k = 5
    pre_calculated_optimal_centers = [[3, 11, 13, 20, 26], [1, 11, 15, 22, 30]]
    number_of_iteration = 10
    for i in range(len(graph_raw)):
        file_name = graph_raw[i]
        kmeans = KMeans(file_name)
        # this bruteforce is very slow.
        # I am using the same graph. so I precomputed the optimal centers
        # uncomment if you are using different graph than network1, network2
        # optimal_centers = kmeans.optimal_centers(k=k)

        optimal_centers = pre_calculated_optimal_centers[i]
        print(f"Optimized K means: K = {k}, Graph = {file_name}")
        print("Iteration  |  Avg distance  |  Pi  |                  Poptimal")
        print("-" * 75)
        for j in range(number_of_iteration):
            cluster = kmeans.k_means_optimized(k=k)
            # uncomment following line for visualization
            # kmeans.visualize(centers=cluster.keys(), optimal_centers=optimal_centers)
            avg_distance = kmeans.avg_distance_from_optimal_center(centers=cluster.keys(), optimal_centers=optimal_centers)
            print(f"{j:<11}|  {avg_distance:<14}|  {str(list(cluster.keys())):<20}|  {optimal_centers}")

        print("\n" + "-" * 75)
