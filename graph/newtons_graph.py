import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Define concepts and dependencies (edges)
concepts = [
    ("Matter", "Mass"),
    ("Mass", "Inertia"),
    ("Mass", "Force"),
    ("Force", "Newton's First Law"),
    ("Force", "Newton's Second Law"),
    ("Force", "Newton's Third Law"),
    ("Force", "Acceleration"),
    ("Force", "Momentum"),
    ("Momentum", "Impulse"),
    ("Impulse", "Collision Types")
]

# Add edges to the graph
G.add_edges_from(concepts)

# Draw graph
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', edge_color='gray')
plt.title("Knowledge Graph: Newton’s Laws of Motion")
plt.show()
