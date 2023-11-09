import itertools
import random

import networkx as nx
import matplotlib.pyplot as plt

INF = 10 ** 9


class GraphHandler:
    def __init__(self, edge_file):
        self.graph = self.load_graph(edge_file)

    def load_graph(self, edge_file) -> nx.Graph:
        G = nx.Graph()
        try:
            with open(edge_file, 'r') as file:
                for line in file:
                    node1, node2 = map(int, line.strip().split())
                    G.add_edge(node1, node2)
        except FileNotFoundError:
            print(f"File '{edge_file}' not found.")
        return G

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
        print("Maximum distance from any node to its nearest center:", self.maximum_distance_from_centers(optimal_centers))
        return optimal_centers

    def visualize(self, centers=[], optimal_centers=[]):
        """Visualize the graph using NetworkX and Matplotlib."""
        # Create a layout for the nodes
        layout = nx.spring_layout(self.graph, seed=42)
        node_colors = []
        for node in self.graph.nodes():
            if node in centers and node in optimal_centers:
                node_colors.append('yellow')
            elif node in centers:
                node_colors.append('red')
            elif node in optimal_centers:
                node_colors.append('green')
            else:
                node_colors.append('skyblue')


        # Draw the nodes and edges
        nx.draw(self.graph, pos=layout, with_labels=True, node_size=500, node_color=node_colors, font_size=10,
                font_color='black')
        plt.title("Graph Visualization")
        plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gh = GraphHandler("edges.txt")
    centers = gh.k_centers(k=4)
    optimal_centers = gh.optimal_centers(k=4)
    gh.visualize(centers, optimal_centers)
