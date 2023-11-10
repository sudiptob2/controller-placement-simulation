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

    def visualize(self, centers=None, optimal_centers=None):
        """Visualize the graph using NetworkX and Matplotlib."""
        # Create a layout for the nodes
        layout = nx.spring_layout(self.graph, seed=22)
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
