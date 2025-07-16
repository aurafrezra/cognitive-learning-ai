import json
import os
import datetime
import math
import networkx as nx
import matplotlib.pyplot as plt

USER_DATA_PATH = 'user_data'

def load_user_responses(username):
    file_path = os.path.join(USER_DATA_PATH, f"{username}_responses.json")
    if not os.path.exists(file_path):
        print("❌ No data found.")
        return []
    with open(file_path, 'r') as f:
        return json.load(f)

def calculate_strength(response):
    base = response['correct'] * response['confidence']
    time_then = datetime.datetime.strptime(response['timestamp'], "%Y-%m-%d %H:%M:%S")
    time_now = datetime.datetime.now()
    days_passed = (time_now - time_then).days + 1
    decay = math.exp(-0.1 * days_passed)
    return round(base * decay, 2)

def build_strength_map(responses):
    concept_strength = {}
    for r in responses:
        concept = r['concept']
        score = calculate_strength(r)
        if concept not in concept_strength:
            concept_strength[concept] = []
        concept_strength[concept].append(score)
    return {
        concept: round(sum(scores)/len(scores), 2)
        for concept, scores in concept_strength.items()
    }

def draw_graph(strength_map):
    G = nx.DiGraph()

    for concept, strength in strength_map.items():
        G.add_node(concept, strength=strength)

    # Dummy edges to show concept links (customize as needed)
    links = {
        "Newton's First Law": ["Inertia"],
        "Newton's Second Law": ["Force", "Mass", "Acceleration"],
        "Newton's Third Law": ["Force"],
        "Force": ["Acceleration", "Mass"],
        "Impulse": ["Force", "Momentum", "Time"],
        "Momentum": ["Mass", "Velocity"],
        "Collision Types": ["Momentum", "Mass"],
    }

    for parent, children in links.items():
        for child in children:
            if parent in G and child in G:
                G.add_edge(parent, child)

    # Color and size logic
    colors = []
    sizes = []
    for node in G.nodes:
        strength = G.nodes[node]['strength']
        if strength >= 4:
            colors.append('green')
        elif strength >= 2.5:
            colors.append('yellow')
        else:
            colors.append('red')
        sizes.append(1200)

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5, seed=42)
    nx.draw(G, pos, with_labels=True, node_color=colors, node_size=sizes,
            font_size=10, font_weight='bold', edge_color='gray', arrows=True)
    plt.title("🧠 Knowledge Graph — Concept Strengths", fontsize=14)
    plt.show()

if __name__ == "__main__":
    username = input("Enter your name: ").strip()
    responses = load_user_responses(username)
    if responses:
        strength_map = build_strength_map(responses)
        draw_graph(strength_map)
