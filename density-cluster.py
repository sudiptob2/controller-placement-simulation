from collections import defaultdict
from queue import PriorityQueue

import networkx as nx

from graph_mixin import GraphMixin

INF = 10 ** 9


class DensityCluster(GraphMixin):

    def __init__(self, edge_file):
        self.delta = None
        self.p = None
        self.delta_avg = None
        super().__init__(edge_file)

    def number_of_nodes_within_distance(self, s, dc):
        """the number of switches whose distances to switch s are less than dc"""
        nodes = list(self.graph.nodes())
        p = 0
        for node in nodes:
            if node == s:
                continue
            distance = nx.shortest_path_length(self.graph, source=node, target=s)
            if distance - dc < 0:
                p += 1
        return p

    def minimum_distance_to_higher_density_node(self, s, p):
        """δi measured by computing the minimum distance between switch si and any other switch with higher density"""
        nodes = list(self.graph.nodes())
        delta_s = max(p)
        for node in nodes:
            if p[node] > p[s]:
                # mens density(node) > density(s)
                distance = nx.shortest_path_length(self.graph, source=node, target=s)
                delta_s = min(distance, delta_s)
        return delta_s

    def recommended_controller(self, dc):
        k = 0
        S = sorted(list(self.graph.nodes()))
        n = len(S)
        p = [0] * n
        delta = [0] * n

        for s in S:
            p[s] = self.number_of_nodes_within_distance(s, dc)
        delta_avg = 0
        for s in S:
            delta_avg += self.minimum_distance_to_higher_density_node(s, p)
        delta_avg /= n

        for s in S:
            delta[s] = self.minimum_distance_to_higher_density_node(s, p)

            if delta[s] > delta_avg:
                k += 1

        self.delta = delta
        self.p = p
        self.delta_avg = delta_avg
        return k

    def find_nodes_as_cluster_center(self, k):
        S = self.graph.nodes()
        centers = []
        center_count = 0
        for s in S:
            if self.delta[s] > self.delta_avg:
                centers.append(s)
                center_count += 1

            if center_count == k:
                break

        if center_count < k:
            # we need more centers
            # node with higher value of p will get priority
            priority_queue = PriorityQueue()
            for s in S:
                if s not in centers:
                    priority_queue.put([self.p[s] * -1, s])  # <priority, node>

            while center_count < k:
                _, s = priority_queue.get()
                centers.append(s)
                center_count += 1
        return centers

    def make_cluster(self, k):
        S = self.graph.nodes
        cluster = defaultdict(lambda: [])
        max_k_s = self.find_nodes_as_cluster_center(k)
        for s in S:
            if s not in max_k_s:
                # s belongs to the cluster of nearest higher density node
                # find the distance to all cluster centers in max_k_s from s
                # choose the center with the lowest center
                minimum_dist, mini_node = INF, -1
                for node in max_k_s:
                    distance = nx.shortest_path_length(self.graph, source=s, target=node)
                    if distance < minimum_dist:
                        minimum_dist = distance
                        mini_node = node
                cluster[mini_node].append(s)

        return cluster


if __name__ == '__main__':
    graph_raw = ['network1.txt', 'network2.txt']
    pre_calculated_optimal_centers = [[6], [1, 11, 15, 22, 30]]
    number_of_iteration = 1

    for i in range(len(graph_raw)):
        file_name = graph_raw[i]
        density_cluster = DensityCluster(file_name)

        diameter = nx.diameter(density_cluster.graph)
        dc = 0.3 * diameter
        k = density_cluster.recommended_controller(dc)

        # this bruteforce is very slow.
        # I am using the same graph. so I precomputed the optimal centers
        optimal_centers = pre_calculated_optimal_centers[i]
        # uncomment if you are using different graph than network1, network2
        # optimal_centers = density_cluster.optimal_centers(k=k)

        print(f"Density based clustering: Recommended K = {k}, Graph = {file_name}")
        print("-" * 25)
        nodes = sorted(density_cluster.graph.nodes)
        print("{:<8} {:<8} {:<8}".format("Node", "nd", "δ"))
        print("-" * 25)
        for v in nodes:
            print("{:<8} {:<8} {:<8}".format(v, density_cluster.p[v], density_cluster.delta[v]))

        print("\n" + "-" * 75)

        print("Iteration  |  Avg distance  |  Pi                   |  Poptimal")
        print("-" * 75)
        cluster = density_cluster.make_cluster(k=k)
        # uncomment following line for visualization
        density_cluster.visualize(centers=cluster.keys(), optimal_centers=optimal_centers,
                                  figure_title=f"Netowrk:{file_name} Algorithm: Density based clustering")
        avg_distance = density_cluster.avg_distance_from_optimal_center(centers=cluster.keys(),
                                                                        optimal_centers=optimal_centers)
        print(f"{i + 1:<11}|  {avg_distance:<14}|  {str(list(cluster.keys())):<20}|  {optimal_centers}")

        print("\n" + "-" * 75)
