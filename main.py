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
        print("Maximum distance from center to any node: ", max_distance)
        return final_result

    def visualize(self, centers=[]):
        """Visualize the graph using NetworkX and Matplotlib."""
        # Create a layout for the nodes
        layout = nx.spring_layout(self.graph, seed=42)
        node_colors = ['red' if node in centers else 'skyblue' for node in self.graph.nodes()]
        # Draw the nodes and edges
        nx.draw(self.graph, pos=layout, with_labels=True, node_size=500, node_color=node_colors, font_size=10,
                font_color='black')
        plt.title("Graph Visualization")
        plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    gh = GraphHandler("edges.txt")
    centers = gh.k_centers(k=4)
    gh.visualize(centers)
