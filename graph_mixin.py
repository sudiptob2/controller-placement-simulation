import itertools

import matplotlib.pyplot as plt
import networkx as nx

INF = 10 ** 9


class GraphMixin:
    def __init__(self, edge_file):
        self.graph = self.load_graph(edge_file)

    def load_graph(self, edge_file) -> nx.Graph:
        graph = nx.Graph()
        try:
            with open(edge_file, 'r') as file:
                for line in file:
                    node1, node2 = map(int, line.strip().split())
                    graph.add_edge(node1, node2)
        except FileNotFoundError:
            print(f"File '{edge_file}' not found.")
        return graph

    def maximum_distance_from_centers(self, centers):
        """
        Calculate the maximum distance from any node to its nearest center.

        Args:
            centers (list): List of center nodes.

        Returns:
            int: Maximum distance from any node to its nearest center.
        """
        max_distance = 0

        for node in self.graph.nodes:
            min_distance_to_centers = INF

            # Calculate the minimum distance from the current node to any of the centers
            for center in centers:
                distance_to_center = nx.shortest_path_length(self.graph, source=node, target=center)
                min_distance_to_centers = min(min_distance_to_centers, distance_to_center)

            # Update the maximum distance if the current node's distance is greater
            max_distance = max(max_distance, min_distance_to_centers)

        return max_distance

    def optimal_centers(self, k):
        """
        Find optimal K centers in the graph through brute force.

        Args:
            k (int): The number of centers to find.

        Returns:
            list: A list of K optimal center nodes.
        """
        nodes = list(self.graph.nodes())
        min_total_distance = float('inf')
        optimal_centers = []

        # Generate all possible combinations of k nodes as centers
        center_combinations = itertools.combinations(nodes, k)

        for centers in center_combinations:
            total_distance = 0

            # Calculate total distance from each node to its nearest center
            for node in nodes:
                min_distance = min(
                    nx.shortest_path_length(self.graph, source=center, target=node) for center in centers)
                total_distance += min_distance

            # Update optimal centers if the total distance is minimized
            if total_distance < min_total_distance:
                min_total_distance = total_distance
                optimal_centers = list(centers)

        print("Optimal Centers:", *optimal_centers)
        print("Maximum distance from any node to its nearest center:",
              self.maximum_distance_from_centers(optimal_centers))
        return optimal_centers

    def avg_distance_from_optimal_center(self, centers, optimal_centers):
        avg_distance = 0
        for center in centers:
            lowest_dist = INF
            for op_center in optimal_centers:
                lowest_dist = min(lowest_dist, nx.shortest_path_length(self.graph, source=center, target=op_center))

            avg_distance += lowest_dist

        return avg_distance / len(centers)

    def visualize(self, centers=None, optimal_centers=None, seed=22):
        """Visualize the graph using NetworkX and Matplotlib."""
        # Create a layout for the nodes
        layout = nx.spring_layout(self.graph, seed=seed)
        node_colors = []
        for node in self.graph.nodes():
            if centers and optimal_centers and node in centers and node in optimal_centers:
                node_colors.append('yellow')
            elif centers and node in centers:
                node_colors.append('red')
            elif optimal_centers and node in optimal_centers:
                node_colors.append('green')
            else:
                node_colors.append('skyblue')

        # Draw the nodes and edges
        nx.draw(self.graph, pos=layout, with_labels=True, node_size=500, node_color=node_colors, font_size=10,
                font_color='black')
        plt.title("Graph Visualization")
        plt.show()
