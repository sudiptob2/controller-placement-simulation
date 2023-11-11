import itertools
import random
from collections import defaultdict

import networkx as nx

from graph_mixin import GraphMixin

INF = 10 ** 9


class KMeans(GraphMixin):

    def partition(self, d, centers, k):
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
        all_pair_shortest_path = dict(nx.all_pairs_shortest_path_length(km.graph))
        for u, paths in all_pair_shortest_path.items():
            for v, distance in paths.items():
                d[u][v] = distance

        random_node = random.choice(list(self.graph.nodes()))
        centers = [random_node]  # initial 1 center
        current_k = 0
        cluster = None
        while current_k < k:
            current_k += 1
            cluster = self.partition(d, centers, current_k)
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
    km = KMeans("edges.txt")
    cluster = km.k_means_optimized(4)
    # centers = kc.k_centers(k=4)
    # optimal_centers = kc.optimal_centers(k=4)
    km.visualize(centers=cluster.keys())
